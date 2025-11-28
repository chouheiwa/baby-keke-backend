from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base

class Vaccine(Base):
    """
    疫苗基础信息表
    """
    __tablename__ = 'vaccines'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment='疫苗名称')
    code = Column(String(20), nullable=False, comment='疫苗代码')
    dose_seq = Column(Integer, nullable=False, comment='剂次')
    type = Column(String(20), nullable=False, comment='类型：FREE(免费)/PAID(自费)')
    target_age_month = Column(Integer, nullable=False, comment='接种月龄(0为出生)')
    description = Column(Text, comment='说明')
    side_effects = Column(Text, comment='常见副作用')
    precautions = Column(Text, comment='注意事项')
    contraindications = Column(Text, comment='禁忌症')
    interval_info = Column(Text, comment='接种间隔说明')
    administration_route = Column(String(20), default='INJECTION', comment='接种途径：INJECTION(注射)/ORAL(口服)')
    is_active = Column(Boolean, default=True, comment='是否启用')

class VaccinationRecord(Base):
    """
    接种记录表
    """
    __tablename__ = 'vaccination_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    baby_id = Column(Integer, nullable=False, comment='宝宝ID')
    vaccine_id = Column(Integer, ForeignKey('vaccines.id'), nullable=False, comment='疫苗ID')
    status = Column(String(20), default='PENDING', comment='状态：PENDING(待接种)/COMPLETED(已接种)/SKIPPED(跳过)')
    vaccination_date = Column(DateTime, nullable=True, comment='实际接种时间')
    location = Column(String(100), nullable=True, comment='接种地点')
    batch_number = Column(String(50), nullable=True, comment='疫苗批号')
    notes = Column(Text, nullable=True, comment='备注')
    photos = Column(Text, nullable=True, comment='照片URL列表(JSON)')
    
    # 关联
    vaccine = relationship("Vaccine")
