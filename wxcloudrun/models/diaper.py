"""
排便/排尿记录模型
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Enum, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class DiaperRecord(Base):
    """排便/排尿记录表(尿不湿记录)"""
    __tablename__ = 'diaper_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete='CASCADE'), nullable=False, index=True, comment='宝宝ID')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='记录人ID')

    # 排便类型
    diaper_type = Column(
        Enum('pee', 'poop', 'both', name='diaper_type_enum'),
        nullable=False,
        comment='类型(pee尿/poop便/both两者都有)'
    )

    # 大便相关
    poop_amount = Column(Enum('少量', '适中', '大量', name='poop_amount_enum'), comment='大便量')
    poop_color = Column(String(20), comment='大便颜色(黄色/绿色/褐色等)')
    poop_texture = Column(Enum('稀', '正常', '干燥', name='poop_texture_enum'), comment='大便性状')

    record_time = Column(TIMESTAMP, nullable=False, comment='记录时间')
    notes = Column(Text, comment='备注')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    baby = relationship("Baby", back_populates="diaper_records")

    # 索引
    __table_args__ = (
        Index('idx_baby_record_time', 'baby_id', 'record_time'),
    )
