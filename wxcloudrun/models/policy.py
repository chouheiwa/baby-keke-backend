from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Enum, UniqueConstraint
from sqlalchemy.sql import func
from wxcloudrun.core.database import Base


class Policy(Base):
    __tablename__ = 'policies'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Enum('terms', 'privacy', name='policy_type_enum'), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    format = Column(Enum('markdown', 'html', 'text', name='policy_format_enum'), nullable=False, default='markdown')
    locale = Column(String(16), nullable=False, default='zh-CN', index=True)
    status = Column(Enum('draft', 'published', 'archived', name='policy_status_enum'), nullable=False, default='draft', index=True)
    effective_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('type', 'version', 'locale', name='uq_policy_type_version_locale'),
    )