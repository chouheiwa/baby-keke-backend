from sqlalchemy import Column, Integer, String, Text, DateTime, func
from wxcloudrun.models import Base

class AlbumRecord(Base):
    __tablename__ = 'album_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    baby_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    file_id = Column(String(255), nullable=False)
    media_type = Column(String(20), nullable=False, default='image')
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
