from sqlalchemy.orm import Session
from . import knowledge_models as models
from . import knowledge_schemas as schemas
from sqlalchemy import MetaData, Table, inspect, text, and_
from databases import engine
from sqlalchemy.sql import select
import json
from typing import Dict, Any, List, Optional
from urllib.parse import unquote

def get_diagnosis_standard(db: Session, diagnosis_id: int):
    return db.query(models.DiagnosisStandard).filter(models.DiagnosisStandard.id == diagnosis_id).first()

def get_diagnosis_standards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DiagnosisStandard).offset(skip).limit(limit).all()

def get_diagnosis_standards_for_vector(db: Session):
    return db.query(models.DiagnosisStandard.name, models.DiagnosisStandard.describes, models.DiagnosisStandard.type_ab, models.DiagnosisStandard.is_emergency, models.DiagnosisStandard.urgency_level).filter(models.DiagnosisStandard.seek_medical_attention_immediately == 1).all()

def create_diagnosis_standard(db: Session, diagnosis: schemas.DiagnosisStandardCreate):
    db_diagnosis = models.DiagnosisStandard(**diagnosis.dict())
    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)
    return db_diagnosis

def update_diagnosis_standard(db: Session, diagnosis_id: int, diagnosis: schemas.DiagnosisStandardBase):
    db_diagnosis = db.query(models.DiagnosisStandard).filter(models.DiagnosisStandard.id == diagnosis_id).first()
    if db_diagnosis:
        for key, value in diagnosis.dict().items():
            setattr(db_diagnosis, key, value)
        db.commit()
        db.refresh(db_diagnosis)
    return db_diagnosis

def delete_diagnosis_standard(db: Session, diagnosis_id: int):
    db_diagnosis = db.query(models.DiagnosisStandard).filter(models.DiagnosisStandard.id == diagnosis_id).first()
    if db_diagnosis:
        db.delete(db_diagnosis)
        db.commit()
    return db_diagnosis


def get_database_tables(db: Session):
    """Return a list of all table names in the connected database."""
    tables = []

    for mapper in models.Base.registry.mappers:
        m_cls = mapper.class_
        m_tname = m_cls.__tablename__
        m_name = m_cls.__name__
        m_count = db.query(m_cls).count()
        tables.append(print(m_name,m_tname,m_count))
        table_data = {
            "name": m_tname,
            "displayName": m_name,
            "recordCount": m_count
        }
        tables.append(table_data)
        tables = list(filter(None, tables))
    return tables

def get_table_schema(table_name:str,db: Session):
    """Return table schema infos."""

    metadata = MetaData()
    
    # 反射表结构
    table = Table(table_name, metadata, autoload_with=engine)
    
    result = {
        "name": table_name,
        "columns": []
    }
    
    # 获取主键列名
    primary_key_columns = [column.name for column in table.primary_key.columns]
    
    for column in table.columns:
        column_info = {
            "name": column.name,
            "type": str(column.type).split('(')[0].lower(),
            "nullable": column.nullable,
            "primaryKey": column.name in primary_key_columns
        }
        result['columns'].append(column_info)
    
    return result


def get_table_data(table_name: str, db:Session, page: int = 1,page_size: int = 50,filters: Optional[str] = None,sort: Optional[str] = None) -> Dict[str, Any]:
    """
    获取分页表数据，支持过滤和排序
    
    Args:
        connection_string: 数据库连接字符串
        table_name: 表名
        page: 页码，默认1
        page_size: 每页记录数，默认50
        filters: JSON字符串，过滤条件
        sort: JSON字符串，排序条件
    
    Returns:
        Dict: 包含数据、分页信息和表结构的字典
    """
    
    try:
        # 反射表结构
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)
        
        query = select(table)
        
        if filters:
            filter_conditions = parse_filters(filters, table)
            if filter_conditions:
                query = query.where(and_(*filter_conditions))
        
        total_records = get_total_count(db, query, table)
        
        if sort:
            sort_conditions = parse_sort(sort, table)
            if sort_conditions:
                query = query.order_by(*sort_conditions)
        
        # 应用分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # 执行查询
        result = db.execute(query)
        rows = result.fetchall()
        
        # 转换为字典列表
        data = [dict(row._mapping) for row in rows]
        
        # 获取表结构信息
        schema = get_table_schema(table_name,db)
        
        # 计算总页数
        total_pages = (total_records + page_size - 1) // page_size
        
        return {
            "data": data,
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "totalRecords": total_records,
                "totalPages": total_pages
            },
            "schema": schema
        }
    finally:
        db.close()
        

def parse_filters(filters_json: str, table: Table) -> List:
    """
    解析过滤条件
    
    Args:
        filters_json: JSON格式的过滤条件字符串
        table: SQLAlchemy Table对象
    
    Returns:
        List: 过滤条件列表
    """
    try:
        filters = json.loads(unquote(filters_json))
        conditions = []
        
        for filter_condition in filters:
            column_name = filter_condition.get('column')
            operator = filter_condition.get('operator', '=')
            value = filter_condition.get('value')
            
            if not column_name or value is None:
                continue
            
            column = table.columns.get(column_name)
            if not column:
                continue
            
            # 根据操作符构建条件
            if operator == '=':
                conditions.append(column == value)
            elif operator == '!=':
                conditions.append(column != value)
            elif operator == '>':
                conditions.append(column > value)
            elif operator == '>=':
                conditions.append(column >= value)
            elif operator == '<':
                conditions.append(column < value)
            elif operator == '<=':
                conditions.append(column <= value)
            elif operator == 'like':
                conditions.append(column.like(f'%{value}%'))
            elif operator == 'in':
                if isinstance(value, list):
                    conditions.append(column.in_(value))
            elif operator == 'not_in':
                if isinstance(value, list):
                    conditions.append(~column.in_(value))
            elif operator == 'is_null':
                conditions.append(column.is_(None))
            elif operator == 'is_not_null':
                conditions.append(column.isnot(None))
        
        return conditions
        
    except json.JSONDecodeError:
        return []

def parse_sort(sort_json: str, table: Table) -> List:
    """
    解析排序条件
    
    Args:
        sort_json: JSON格式的排序条件字符串
        table: SQLAlchemy Table对象
    
    Returns:
        List: 排序条件列表
    """
    try:
        sort_conditions = json.loads(unquote(sort_json))
        orders = []
        
        for sort_condition in sort_conditions:
            column_name = sort_condition.get('column')
            direction = sort_condition.get('direction', 'asc').lower()
            
            if not column_name:
                continue
            
            column = table.columns.get(column_name)
            if not column:
                continue
            
            if direction == 'asc':
                orders.append(column.asc())
            elif direction == 'desc':
                orders.append(column.desc())
        
        return orders
        
    except json.JSONDecodeError:
        return []

def get_total_count(session, query, table: Table) -> int:
    """
    获取总记录数
    
    Args:
        session: SQLAlchemy session
        query: 当前查询
        table: SQLAlchemy Table对象
    
    Returns:
        int: 总记录数
    """
    # 移除排序和分页，计算总数
    count_query = query.with_only_columns(table).order_by(None).offset(None).limit(None)
    count_query = count_query.with_only_columns(text('COUNT(1)'))
    
    result = session.execute(count_query)
    return result.scalar()


