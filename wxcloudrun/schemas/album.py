from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlbumRecordBase(BaseModel):
    file_id: str
    media_type: str = 'image'
    description: Optional[str] = None

class AlbumRecordCreate(AlbumRecordBase):
    baby_id: int

class AlbumRecordResponse(AlbumRecordBase):
    id: int
    baby_id: int
    user_id: int
    url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
