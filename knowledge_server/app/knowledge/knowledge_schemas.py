from pydantic import BaseModel
from typing import Optional

class DiagnosisStandardBase(BaseModel):
    name: str
    describes: Optional[str] = None
    symptom: Optional[str] = None
    seek_medical_attention_immediately: Optional[int] = None
    follow_up: Optional[int] = None
    follow_up_describe: Optional[str] = None
    type_ab: Optional[str] = None
    is_emergency: Optional[int] = None
    urgency_level: Optional[int] = None

class DiagnosisStandardCreate(DiagnosisStandardBase):
    pass

class DiagnosisStandard(DiagnosisStandardBase):
    id: int

    class Config:
        from_attributes = True  # 允许从 ORM 对象转换