"""
吸奶记录模型
"""
from sqlalchemy import Column, Integer, TIMESTAMP, Text, ForeignKey, Index, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class PumpingRecord(Base):
    """吸奶记录表"""
    __tablename__ = 'pumping_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete='CASCADE'), nullable=False, index=True, comment='宝宝ID')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='记录人ID')

    # 吸奶量字段
    left_amount = Column(Integer, comment='左侧吸奶量(ml)')
    right_amount = Column(Integer, comment='右侧吸奶量(ml)')
    total_amount = Column(Integer, nullable=False, comment='总吸奶量(ml)')

    # 时间和备注
    record_time = Column(TIMESTAMP, nullable=False, comment='记录时间')
    notes = Column(Text, comment='备注')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')

    # 关系
    baby = relationship("Baby", back_populates="pumping_records")

    # 索引
    __table_args__ = (
        Index('idx_baby_record_time', 'baby_id', 'record_time'),
    )
