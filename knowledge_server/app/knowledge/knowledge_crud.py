from sqlalchemy.orm import Session
from . import knowledge_models as models
from . import knowledge_schemas as schemas

def get_diagnosis_standard(db: Session, diagnosis_id: int):
    return db.query(models.DiagnosisStandard).filter(models.DiagnosisStandard.id == diagnosis_id).first()

def get_diagnosis_standards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DiagnosisStandard).offset(skip).limit(limit).all()

def get_diagnosis_standards_for_vector(db: Session):
    return db.query(models.DiagnosisStandard.name, models.DiagnosisStandard.describes).filter(models.DiagnosisStandard.seek_medical_attention_immediately == 1).all()

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