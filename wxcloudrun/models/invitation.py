from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wxcloudrun.core.database import Base


class Invitation(Base):
    __tablename__ = 'invitations'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    baby_id = Column(Integer, ForeignKey('babies.id', ondelete='CASCADE'), nullable=False)
    invite_code = Column(String(64), nullable=False, unique=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    expire_at = Column(TIMESTAMP, nullable=False)
    status = Column(Enum('active', 'expired', 'used', name='invitation_status_enum'), nullable=False, default='active')
    used_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    used_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    baby = relationship('Baby')