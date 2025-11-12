"""
睡眠记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from wxcloudrun.models.sleep import SleepRecord
from wxcloudrun.models.user import User
from wxcloudrun.models.baby import BabyFamily
from wxcloudrun.schemas.sleep import SleepRecordCreate, SleepRecordUpdate
from wxcloudrun.schemas.user import CreatorInfo


def _attach_creator_info(db: Session, record: SleepRecord) -> None:
    """给记录附加创建者信息"""
    if not record:
        return

    # 查询创建者信息和关系
    creator_query = (
        db.query(User, BabyFamily.relation)
        .outerjoin(BabyFamily, and_(
            BabyFamily.user_id == User.id,
            BabyFamily.baby_id == record.baby_id
        ))
        .filter(User.id == record.user_id)
        .first()
    )

    if creator_query:
        user, relation = creator_query
        record.created_by = CreatorInfo(
            user_id=user.id,
            nickname=user.nickname,
            relation=relation,
            relation_display=relation
        )
    else:
        record.created_by = None


def get_sleep_record(db: Session, record_id: int) -> Optional[SleepRecord]:
    """根据ID获取睡眠记录"""
    record = db.query(SleepRecord).filter(SleepRecord.id == record_id).first()
    if record:
        _attach_creator_info(db, record)
    return record


def get_sleep_records_by_baby(
    db: Session,
    baby_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> list[SleepRecord]:
    """获取宝宝的睡眠记录"""
    query = db.query(SleepRecord).filter(SleepRecord.baby_id == baby_id)

    if start_date:
        query = query.filter(SleepRecord.start_time >= start_date)
    if end_date:
        query = query.filter(SleepRecord.start_time <= end_date)

    records = query.order_by(SleepRecord.start_time.desc()).offset(skip).limit(limit).all()

    # 为每条记录附加创建者信息
    for record in records:
        _attach_creator_info(db, record)

    return records


def create_sleep_record(db: Session, record: SleepRecordCreate, user_id: int) -> SleepRecord:
    """创建睡眠记录"""
    db_record = SleepRecord(**record.model_dump(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_sleep_record(
    db: Session, record_id: int, record: SleepRecordUpdate
) -> Optional[SleepRecord]:
    """更新睡眠记录"""
    db_record = get_sleep_record(db, record_id)
    if not db_record:
        return None

    update_data = record.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)

    db.commit()
    db.refresh(db_record)
    return db_record


def delete_sleep_record(db: Session, record_id: int) -> bool:
    """删除睡眠记录"""
    db_record = get_sleep_record(db, record_id)
    if not db_record:
        return False

    db.delete(db_record)
    db.commit()
    return True


def get_sleep_stats_by_date(db: Session, baby_id: int, start_date: datetime, end_date: datetime) -> dict:
    """统计指定日期范围内的睡眠数据"""
    records = get_sleep_records_by_baby(db, baby_id, start_date=start_date, end_date=end_date, limit=1000)

    total_duration = 0
    total_wake_count = 0
    night_sleep_count = 0
    nap_count = 0

    for record in records:
        if record.duration:
            total_duration += record.duration
        total_wake_count += record.wake_count or 0

        if record.sleep_type == 'night':
            night_sleep_count += 1
        else:
            nap_count += 1

    return {
        'total_records': len(records),
        'total_duration_minutes': total_duration,
        'total_duration_hours': round(total_duration / 60, 2) if total_duration > 0 else 0,
        'average_duration_minutes': round(total_duration / len(records), 2) if records else 0,
        'total_wake_count': total_wake_count,
        'night_sleep_count': night_sleep_count,
        'nap_count': nap_count,
    }
