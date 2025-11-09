"""
喂养记录模型
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Enum, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class FeedingRecord(Base):
    """喂养记录表"""
    __tablename__ = 'feeding_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete='CASCADE'), nullable=False, index=True, comment='宝宝ID')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='记录人ID')

    # 喂养类型
    feeding_type = Column(
        Enum('breast', 'formula', 'solid', name='feeding_type_enum'),
        nullable=False,
        comment='喂养类型(breast母乳/formula奶粉/solid辅食)'
    )

    # 母乳喂养字段
    breast_side = Column(Enum('left', 'right', 'both', name='breast_side_enum'), comment='哺乳侧(left左/right右/both双侧)')
    duration_left = Column(Integer, comment='左侧时长(分钟)')
    duration_right = Column(Integer, comment='右侧时长(分钟)')

    # 奶粉喂养字段
    amount = Column(Integer, comment='奶量(ml)或食量(g)')

    # 辅食字段
    food_name = Column(String(100), comment='食物名称')

    # 通用字段
    start_time = Column(TIMESTAMP, nullable=False, comment='开始时间')
    end_time = Column(TIMESTAMP, comment='结束时间')
    notes = Column(Text, comment='备注')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    baby = relationship("Baby", back_populates="feeding_records")

    # 索引
    __table_args__ = (
        Index('idx_baby_time', 'baby_id', 'start_time'),
    )
