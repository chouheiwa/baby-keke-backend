"""
宝宝相关模型
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Enum, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class Baby(Base):
    """宝宝信息表"""
    __tablename__ = 'babies'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='宝宝ID')
    name = Column(String(50), nullable=False, comment='宝宝姓名')
    gender = Column(Enum('male', 'female', 'unknown', name='gender_enum'), default='unknown', comment='性别')
    birthday = Column(TIMESTAMP, nullable=False, comment='出生日期')
    avatar_url = Column(String(500), comment='宝宝头像')
    notes = Column(Text, comment='备注')
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False, comment='创建人ID')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    family_members = relationship("BabyFamily", back_populates="baby", cascade="all, delete-orphan")
    feeding_records = relationship("FeedingRecord", back_populates="baby", cascade="all, delete-orphan")
    diaper_records = relationship("DiaperRecord", back_populates="baby", cascade="all, delete-orphan")
    sleep_records = relationship("SleepRecord", back_populates="baby", cascade="all, delete-orphan")
    growth_records = relationship("GrowthRecord", back_populates="baby", cascade="all, delete-orphan")


class BabyFamily(Base):
    """宝宝-家庭成员关系表"""
    __tablename__ = 'baby_family'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete='CASCADE'), nullable=False, comment='宝宝ID')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='用户ID')
    relation = Column(String(20), comment='关系(爸爸/妈妈/爷爷/奶奶等)')
    is_admin = Column(Integer, default=0, comment='是否为管理员(0否1是)')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')

    # 关系
    baby = relationship("Baby", back_populates="family_members")
    user = relationship("User", back_populates="babies")

    # 联合索引
    __table_args__ = (
        Index('idx_baby_user', 'baby_id', 'user_id'),
    )
