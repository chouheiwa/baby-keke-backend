"""
用户模型
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


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
