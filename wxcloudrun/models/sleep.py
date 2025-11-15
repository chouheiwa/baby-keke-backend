"""
睡眠记录模型
"""
from sqlalchemy import Column, Integer, TIMESTAMP, Text, Enum, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class SleepRecord(Base):
    """睡眠记录表"""
    __tablename__ = 'sleep_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete='CASCADE'), nullable=False, index=True, comment='宝宝ID')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='记录人ID')

    sleep_type = Column(
        Enum('night', 'nap', name='sleep_type_enum'),
        nullable=False,
        comment='睡眠类型(night夜间/nap小睡)'
    )
    status = Column(
        Enum('in_progress', 'completed', 'auto_closed', 'cancelled', name='sleep_status_enum'),
        nullable=False,
        server_default='completed',
        comment='记录状态'
    )
    start_time = Column(TIMESTAMP, nullable=False, comment='入睡时间')
    end_time = Column(TIMESTAMP, comment='醒来时间')
    duration = Column(Integer, comment='睡眠时长(分钟)')
    quality = Column(
        Enum('good', 'normal', 'poor', name='sleep_quality_enum'),
        comment='睡眠质量'
    )
    position = Column(
        Enum('left', 'middle', 'right', name='sleep_position_enum'),
        comment='睡眠姿势(左/中/右)'
    )
    wake_count = Column(Integer, default=0, comment='夜醒次数')
    notes = Column(Text, comment='备注')
    auto_closed_at = Column(TIMESTAMP, comment='自动关闭时间')
    source = Column(
        Enum('manual', 'auto', name='sleep_source_enum'),
        nullable=False,
        server_default='manual',
        comment='记录来源'
    )
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    baby = relationship("Baby", back_populates="sleep_records")

    # 索引
    __table_args__ = (
        Index('idx_baby_start_time', 'baby_id', 'start_time'),
    )
