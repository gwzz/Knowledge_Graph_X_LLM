from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DiagnosisStandard(Base):
    __tablename__ = "diagnosis_standards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    describes = Column(Text, nullable=True)  # 描述
    symptom = Column(Text, nullable=True)  # 症状
    seek_medical_attention_immediately = Column(Integer, nullable=True)  # 是否立即就医
    follow_up = Column(Integer, nullable=True)  # 是否需要随访
    follow_up_describe = Column(Text, nullable=True)  # 随访描述
    type_ab = Column(String(50), nullable=True)  # AB类型
    is_emergency = Column(Integer, nullable=True)  # 是否急诊
    urgency_level = Column(Integer, nullable=True)  # 紧急程度级别

    def __repr__(self):
        return f"<DiagnosisStandard(id={self.id}, name='{self.name}')>"