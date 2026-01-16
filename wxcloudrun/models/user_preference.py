"""用户偏好设置模型"""
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.sql import func
from wxcloudrun.core.database import Base


class UserPreference(Base):
    """用户偏好设置表"""
    __tablename__ = "user_preferences"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    preference_key = Column(
        String(100),
        nullable=False,
        comment="偏好设置键"
    )
    preference_value = Column(
        JSON,
        nullable=False,
        comment="偏好设置值"
    )
    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        comment="创建时间"
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'preference_key', name='unique_user_preference'),
    )

    def __repr__(self):
        return f"<UserPreference(id={self.id}, user_id={self.user_id}, key={self.preference_key})>"
