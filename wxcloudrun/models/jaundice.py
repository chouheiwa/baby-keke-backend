from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Text
from datetime import datetime
from wxcloudrun.core.database import Base

class JaundiceRecord(Base):
    """黄疸记录模型"""
    __tablename__ = 'jaundice_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    baby_id = Column(Integer, nullable=False, comment='宝宝ID')
    record_date = Column(DateTime, nullable=False, comment='记录时间')
    value = Column(DECIMAL(5, 2), nullable=False, comment='黄疸值(mg/dL)')
    photo_url = Column(String(255), nullable=True, comment='照片URL')
    notes = Column(Text, nullable=True, comment='备注')
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
