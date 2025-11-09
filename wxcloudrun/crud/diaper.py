"""
排便/排尿记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from wxcloudrun.models.diaper import DiaperRecord
from wxcloudrun.schemas.diaper import DiaperRecordCreate, DiaperRecordUpdate


def get_diaper_record(db: Session, record_id: int) -> Optional[DiaperRecord]:
    """根据ID获取排便/排尿记录"""
    return db.query(DiaperRecord).filter(DiaperRecord.id == record_id).first()


def get_diaper_records_by_baby(
    db: Session,
    baby_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> list[DiaperRecord]:
    """获取宝宝的排便/排尿记录"""
    query = db.query(DiaperRecord).filter(DiaperRecord.baby_id == baby_id)

    if start_date:
        query = query.filter(DiaperRecord.record_time >= start_date)
    if end_date:
        query = query.filter(DiaperRecord.record_time <= end_date)

    return query.order_by(DiaperRecord.record_time.desc()).offset(skip).limit(limit).all()


def create_diaper_record(db: Session, record: DiaperRecordCreate, user_id: int) -> DiaperRecord:
    """创建排便/排尿记录"""
    db_record = DiaperRecord(**record.model_dump(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_diaper_record(
    db: Session, record_id: int, record: DiaperRecordUpdate
) -> Optional[DiaperRecord]:
    """更新排便/排尿记录"""
    db_record = get_diaper_record(db, record_id)
    if not db_record:
        return None

    update_data = record.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)

    db.commit()
    db.refresh(db_record)
    return db_record


def delete_diaper_record(db: Session, record_id: int) -> bool:
    """删除排便/排尿记录"""
    db_record = get_diaper_record(db, record_id)
    if not db_record:
        return False

    db.delete(db_record)
    db.commit()
    return True


def get_diaper_count_by_date(db: Session, baby_id: int, start_date: datetime, end_date: datetime) -> dict:
    """统计指定日期范围内的排便/排尿次数"""
    records = get_diaper_records_by_baby(db, baby_id, start_date=start_date, end_date=end_date, limit=1000)

    count = {
        'pee': 0,
        'poop': 0,
        'both': 0,
        'total': len(records)
    }

    for record in records:
        count[record.diaper_type] += 1

    return count
