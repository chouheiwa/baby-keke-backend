"""
用户会话模型
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class UserSession(Base):
    """用户会话表 - 存储微信登录会话信息"""
    __tablename__ = 'user_sessions'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='会话ID')
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='用户ID')
    openid = Column(String(64), unique=True, nullable=False, index=True, comment='微信OpenID')
    session_key = Column(String(128), nullable=False, comment='微信会话密钥')
    unionid = Column(String(64), comment='微信UnionID')
    expires_at = Column(TIMESTAMP, nullable=False, comment='过期时间')
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')

    # 关系
    user = relationship("User", backref="sessions")

