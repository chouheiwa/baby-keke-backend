"""
数据库模型定义
MySQL 5.7 兼容版本
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, Enum, Numeric, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


# ==================== 用户相关模型 ====================

class User(Base):
    """用户表 - 微信用户"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='用户ID')
    openid = Column(String(64), unique=True, nullable=False, index=True, comment='微信OpenID')
    nickname = Column(String(100), comment='用户昵称')
    avatar_url = Column(String(500), comment='头像URL')
    phone = Column(String(20), comment='手机号')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    babies = relationship("BabyFamily", back_populates="user")


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
    family_members = relationship("BabyFamily", back_populates="baby")
    feeding_records = relationship("FeedingRecord", back_populates="baby")
    diaper_records = relationship("DiaperRecord", back_populates="baby")
    sleep_records = relationship("SleepRecord", back_populates="baby")
    growth_records = relationship("GrowthRecord", back_populates="baby")


class BabyFamily(Base):
    """宝宝-家庭成员关系表"""
    __tablename__ = 'baby_family'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    baby_id = Column(Integer, ForeignKey('babies.id'), nullable=False, comment='宝宝ID')
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


# ==================== 记录相关模型 ====================

class FeedingRecord(Base):
    """喂养记录表"""
    __tablename__ = 'feeding_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id'), nullable=False, index=True, comment='宝宝ID')
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


class DiaperRecord(Base):
    """排便记录表(尿不湿记录)"""
    __tablename__ = 'diaper_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id'), nullable=False, index=True, comment='宝宝ID')
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


class SleepRecord(Base):
    """睡眠记录表"""
    __tablename__ = 'sleep_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id'), nullable=False, index=True, comment='宝宝ID')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='记录人ID')

    sleep_type = Column(
        Enum('night', 'nap', name='sleep_type_enum'),
        nullable=False,
        comment='睡眠类型(night夜间/nap小睡)'
    )
    start_time = Column(TIMESTAMP, nullable=False, comment='入睡时间')
    end_time = Column(TIMESTAMP, comment='醒来时间')
    duration = Column(Integer, comment='睡眠时长(分钟)')
    quality = Column(
        Enum('good', 'normal', 'poor', name='sleep_quality_enum'),
        comment='睡眠质量'
    )
    wake_count = Column(Integer, default=0, comment='夜醒次数')
    notes = Column(Text, comment='备注')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    baby = relationship("Baby", back_populates="sleep_records")

    # 索引
    __table_args__ = (
        Index('idx_baby_start_time', 'baby_id', 'start_time'),
    )


class GrowthRecord(Base):
    """生长发育记录表"""
    __tablename__ = 'growth_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='记录ID')
    baby_id = Column(Integer, ForeignKey('babies.id'), nullable=False, index=True, comment='宝宝ID')
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


# ==================== 示例计数表(保留用于测试) ====================

class Counters(Base):
    """计数器模型(示例)"""
    __tablename__ = 'counters'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    count = Column(Integer, default=1, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
