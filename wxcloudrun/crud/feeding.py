"""
喂养记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from wxcloudrun.models.feeding import FeedingRecord
from wxcloudrun.schemas.feeding import FeedingRecordCreate, FeedingRecordUpdate


def get_feeding_record(db: Session, record_id: int) -> Optional[FeedingRecord]:
    """根据ID获取喂养记录"""
    return db.query(FeedingRecord).filter(FeedingRecord.id == record_id).first()


def get_feeding_records_by_baby(
    db: Session,
    baby_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> list[FeedingRecord]:
    """获取宝宝的喂养记录"""
    query = db.query(FeedingRecord).filter(FeedingRecord.baby_id == baby_id)

    if start_date:
        query = query.filter(FeedingRecord.start_time >= start_date)
    if end_date:
        query = query.filter(FeedingRecord.start_time <= end_date)

    return query.order_by(FeedingRecord.start_time.desc()).offset(skip).limit(limit).all()


def create_feeding_record(db: Session, record: FeedingRecordCreate, user_id: int) -> FeedingRecord:
    """创建喂养记录"""
    db_record = FeedingRecord(**record.model_dump(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_feeding_record(
    db: Session, record_id: int, record: FeedingRecordUpdate
) -> Optional[FeedingRecord]:
    """更新喂养记录"""
    db_record = get_feeding_record(db, record_id)
    if not db_record:
        return None

    update_data = record.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)

    db.commit()
    db.refresh(db_record)
    return db_record


def delete_feeding_record(db: Session, record_id: int) -> bool:
    """删除喂养记录"""
    db_record = get_feeding_record(db, record_id)
    if not db_record:
        return False

    db.delete(db_record)
    db.commit()
    return True


def get_latest_feeding(db: Session, baby_id: int) -> Optional[FeedingRecord]:
    """获取最近一次喂养记录"""
    return (
        db.query(FeedingRecord)
        .filter(FeedingRecord.baby_id == baby_id)
        .order_by(FeedingRecord.start_time.desc())
        .first()
    )
