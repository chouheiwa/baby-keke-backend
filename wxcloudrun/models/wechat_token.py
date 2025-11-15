from sqlalchemy import Column, Integer, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from wxcloudrun.core.database import Base


class WeChatAccessToken(Base):
    __tablename__ = 'wechat_access_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    appid = Column(String(64), nullable=False)
    token = Column(String(512), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('appid', name='uk_wechat_appid'),
    )