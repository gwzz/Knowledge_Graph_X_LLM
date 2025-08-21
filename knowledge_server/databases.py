from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

local_db_username = os.getenv("LOCAL_MYSQL_USER_NAME")
local_db_password = os.getenv("LOCAL_MYSQL_PASSWD")
local_db_host = os.getenv("LOCAL_MYSQL_HOST")
local_db_name = os.getenv("LOCAL_MYSQL_DATABASE")
# MySQL 连接格式: mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{local_db_username}:{local_db_password}@{local_db_host}:3306/{local_db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 自动检测连接是否有效
    pool_recycle=3600,   # 避免 MySQL 自动断开连接
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# import os
# import pymysql
# from configs import *
# from utils import get_logging


# logger = get_logging(__file__)

# host = MYSQL_HOST
# user = MYSQL_USER_NAME
# password = MYSQL_PASSWD
# database = MYSQL_DATABASE
# connection = None

# class MysqlInterface:
#     def __init__(self):
#         pass

#     def _db_connect(self):
#         self.get_connection = pymysql.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=database,
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#         )
    
#     def _db_close(self):
#         self.get_connection.close()

# class Database(MysqlInterface):
#     def __init__(self):
#         pass

#     def insert_disease_data(self, disease, disease_main):
#         try:
#             self._db_connect()
#             cursor = self.get_connection.cursor()
#             sql_insert = f"INSERT INTO common_disease (disease_main, disease_subclass) VALUES ( '{disease}','{disease_main}')"
#             # params_insert = ('user3@example.com', 'secret456')
#             logger.info(sql_insert)
#             cursor.execute(sql_insert)
#             self.get_connection.commit()
#         except Exception as e:
#             logger.info("db error")
#         finally:
#             self._db_close()
    
#     def query_disease_data(self, disease):
#         try:
#             self._db_connect()
#             cursor = self.get_connection.cursor()
#             sql = f"select disease_main from common_disease where disease_subclass = '{disease}'"
#             # params_insert = ('user3@example.com', 'secret456')
#             logger.info(sql)
#             cursor.execute(sql)
#             result = cursor.fetchone()
#         except Exception as e:
#             logger.info("db error")
#         finally:
#             self._db_close()
#         return result
    
#     def query_department(self, disease):
#         try:
#             self._db_connect()
#             cursor = self.get_connection.cursor()
#             sql = f"select department, department_id from common_disease_to_department where common_disease = '{disease}'"
#             # params_insert = ('user3@example.com', 'secret456')
#             logger.info(sql)
#             cursor.execute(sql)
#             result = cursor.fetchone()
#         except Exception as e:
#             logger.info("db error")
#         finally:
#             self._db_close()
#         return result
    
#     def query_doctor(self, doctor_name, department=None):
#         try:
#             self._db_connect()
#             cursor = self.get_connection.cursor()
#             if department:
#                 sql = f"select name, department, position, title, good, intorduce, date, photo from changzhou_one_hosp_doctors where name = '{doctor_name}' and department like '%{department}%'"
#             else:
#                 sql = f"select name, department, position, title, good, intorduce, date, photo from changzhou_one_hosp_doctors where name = '{doctor_name}'"
#             # params_insert = ('user3@example.com', 'secret456')
#             logger.info(sql)
#             cursor.execute(sql)
#             result = cursor.fetchone()
#         except Exception as e:
#             logger.info("db error")
#         finally:
#             self._db_close()
#         return result
    
#     def insert_check_data(self, check, similarity_gold_check, score):
#         try:
#             self._db_connect()
#             cursor = self.get_connection.cursor()
#             sql_insert = f"INSERT INTO gold_check_for_graph_check (graph_check, similarity_gold_check, score) VALUES ( '{check}','{similarity_gold_check}','{str(score)}')"
#             logger.info(sql_insert)
#             # params_insert = ('user3@example.com', 'secret456')
#             logger.info(sql_insert)
#             cursor.execute(sql_insert)
#             self.get_connection.commit()
#         except Exception as e:
#             logger.info("db error")
#         finally:
#             self._db_close()

#     def query_check_data(self, check_name):
#         try:
#             self._db_connect()
#             cursor = self.get_connection.cursor()
#             sql = f"select similarity_gold_check from gold_check_for_graph_check where graph_check = '{check_name}' and score <> ''"
#             # params_insert = ('user3@example.com', 'secret456')
#             logger.info(sql)
#             cursor.execute(sql)
#             result = cursor.fetchone()
#         except Exception as e:
#             logger.info("db error")
#         finally:
#             self._db_close()
#         return result
    

#     def query_diagnosis_data(self):
#         try:
#             self._db_connect()
#             cursor = self.get_connection.cursor()
#             sql = f"select id,name,describes from diagnostic_trigger where  seek_medical_attention_immediately = 1"
#             # params_insert = ('user3@example.com', 'secret456')
#             logger.info(sql)
#             cursor.execute(sql)
#             result = cursor.fetchall()
#         except Exception as e:
#             logger.info("db error")
#         finally:
#             self._db_close()
#         return result
    
#     def insert_disease_diagnosis_criteria_data(self, disease, criteria, seek=1, type_ab = None):
#         try:
#             self._db_connect()
#             cursor = self.get_connection.cursor()
#             sql_insert = f"INSERT INTO diagnostic_trigger (name, describes, seek_medical_attention_immediately, type_ab) VALUES ( '{disease}','{criteria}', '{seek}', '{type_ab}')"
#             # params_insert = ('user3@example.com', 'secret456')
#             logger.info(sql_insert)
#             cursor.execute(sql_insert)
#             self.get_connection.commit()
#         except Exception as e:
#             logger.info("db error")
#         finally:
#             self._db_close()