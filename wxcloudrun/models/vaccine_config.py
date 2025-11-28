from datetime import datetime
from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey
from wxcloudrun.core.database import Base

class VaccineConfig(Base):
    """疫苗配置表"""
    __tablename__ = 'vaccine_config'

    baby_id = Column(Integer, primary_key=True, comment='宝宝ID')
    config = Column(JSON, default={}, comment='配置内容')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
