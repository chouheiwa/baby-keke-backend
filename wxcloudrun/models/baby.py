"""
宝宝相关模型
"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Text,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class Baby(Base):
    """宝宝信息表"""
    __tablename__ = 'babies'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        comment='宝宝ID',
    )
    name = Column(String(50), nullable=False, comment='宝宝姓名')
    nickname = Column(String(100), comment='宝宝昵称')
    gender = Column(
        Enum('male', 'female', 'unknown', name='gender_enum'),
        default='unknown',
        comment='性别',
    )
    birthday = Column(TIMESTAMP, nullable=False, comment='出生日期')
    birth_weight = Column(Integer, comment='出生体重(g)')
    birth_height = Column(Integer, comment='出生身长(cm)')
    notes = Column(Text, comment='备注')
    created_by = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        comment='创建人ID',
    )
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        comment='创建时间',
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间',
    )

    # 关系
    family_members = relationship(
        "BabyFamily", back_populates="baby", cascade="all, delete-orphan"
    )
    feeding_records = relationship(
        "FeedingRecord", back_populates="baby", cascade="all, delete-orphan"
    )
    diaper_records = relationship(
        "DiaperRecord", back_populates="baby", cascade="all, delete-orphan"
    )
    sleep_records = relationship(
        "SleepRecord", back_populates="baby", cascade="all, delete-orphan"
    )
    growth_records = relationship(
        "GrowthRecord", back_populates="baby", cascade="all, delete-orphan"
    )
    pumping_records = relationship(
        "PumpingRecord", back_populates="baby", cascade="all, delete-orphan"
    )


class BabyFamily(Base):
    """宝宝-家庭成员关系表"""
    __tablename__ = 'baby_family'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    baby_id = Column(
        Integer,
        ForeignKey('babies.id', ondelete='CASCADE'),
        nullable=False,
        comment='宝宝ID',
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        comment='用户ID',
    )
    relation = Column(String(20), comment='关系(爸爸/妈妈/爷爷/奶奶等)')
    relation_display = Column(
        String(50), comment='角色显示名称（用于自定义角色或特殊称呼）'
    )
    is_admin = Column(Integer, default=0, comment='是否为管理员(0否1是)')
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        comment='创建时间',
    )

    # 关系
    baby = relationship("Baby", back_populates="family_members")
    user = relationship("User", back_populates="babies")

    # 联合索引
    __table_args__ = (
        Index('idx_baby_user', 'baby_id', 'user_id'),
    )
