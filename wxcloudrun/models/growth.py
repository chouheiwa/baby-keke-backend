"""
生长发育记录模型
"""
from sqlalchemy import Column, Integer, TIMESTAMP, Text, Numeric, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class GrowthRecord(Base):
    """生长发育记录表"""
    __tablename__ = 'growth_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete='CASCADE'), nullable=False, index=True, comment='宝宝ID')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='记录人ID')

    record_date = Column(TIMESTAMP, nullable=False, comment='记录日期')
    weight = Column(Numeric(5, 2), comment='体重(kg)')
    height = Column(Numeric(5, 2), comment='身高/身长(cm)')
    head_circumference = Column(Numeric(5, 2), comment='头围(cm)')
    notes = Column(Text, comment='备注')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    baby = relationship("Baby", back_populates="growth_records")

    # 索引
    __table_args__ = (
        Index('idx_baby_record_date', 'baby_id', 'record_date'),
    )
