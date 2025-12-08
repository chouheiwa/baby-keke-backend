from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from wxcloudrun.models.album import AlbumRecord
from wxcloudrun.schemas.album import AlbumRecordCreate

def create_album_record(db: Session, record: AlbumRecordCreate, user_id: int) -> AlbumRecord:
    """创建相册记录"""
    db_record = AlbumRecord(
        baby_id=record.baby_id,
        user_id=user_id,
        file_id=record.file_id,
        media_type=record.media_type,
        description=record.description
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_album_records_by_baby(
    db: Session, 
    baby_id: int, 
    skip: int = 0, 
    limit: int = 20
) -> List[AlbumRecord]:
    """获取宝宝的相册记录列表"""
    return db.query(AlbumRecord)\
        .filter(AlbumRecord.baby_id == baby_id)\
        .order_by(desc(AlbumRecord.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_album_record(db: Session, record_id: int) -> Optional[AlbumRecord]:
    """获取单条相册记录"""
    return db.query(AlbumRecord).filter(AlbumRecord.id == record_id).first()

def delete_album_record(db: Session, record_id: int) -> bool:
    """删除相册记录"""
    db_record = db.query(AlbumRecord).filter(AlbumRecord.id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    return False
