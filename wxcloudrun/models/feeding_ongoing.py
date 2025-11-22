"""
正在进行的喂养记录模型
"""
from sqlalchemy import Column, Integer, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from wxcloudrun.core.database import Base

class FeedingOngoing(Base):
    """正在进行的喂养记录表"""
    __tablename__ = 'feeding_ongoing'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete='CASCADE'), nullable=False, unique=True, comment='宝宝ID')
    
    start_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='本次喂养开始时间')
    current_side = Column(
        Enum('left', 'right', 'paused', name='ongoing_side_enum'),
        nullable=False,
        default='paused',
        comment='当前状态'
    )
    last_action_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='最后一次操作时间')
    
    accumulated_left = Column(Integer, nullable=False, default=0, comment='左侧累计时长(秒)')
    accumulated_right = Column(Integer, nullable=False, default=0, comment='右侧累计时长(秒)')
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')
