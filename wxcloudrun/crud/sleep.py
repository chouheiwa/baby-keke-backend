"""
睡眠记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime, timedelta
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
    payload = record.model_dump()
    if payload.get('end_time'):
        start = payload['start_time']
        end = payload['end_time']
        dur = int((end - start).total_seconds() // 60)
        payload['duration'] = dur if dur >= 0 else None
        payload['sleep_type'] = compute_sleep_type(start, end)
        payload['status'] = 'completed'
    else:
        payload.setdefault('sleep_type', 'nap')
        payload['status'] = 'in_progress'
    db_record = SleepRecord(**payload, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_sleep_record(
    db: Session, record_id: int, record: SleepRecordUpdate
) -> Optional[SleepRecord]:
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
    records = get_sleep_records_by_baby(db, baby_id, start_date=start_date, end_date=end_date, limit=1000)

    total_duration = 0
    total_wake_count = 0
    night_sleep_count = 0
    nap_count = 0

    for record in records:
        if getattr(record, 'status', 'completed') != 'completed':
            continue
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
        'average_duration_minutes': round(total_duration / max(1, total_records_completed(records)), 2),
        'total_wake_count': total_wake_count,
        'night_sleep_count': night_sleep_count,
        'nap_count': nap_count,
    }

def total_records_completed(records: list[SleepRecord]) -> int:
    return sum(1 for r in records if getattr(r, 'status', 'completed') == 'completed')

def compute_sleep_type(start: datetime, end: datetime) -> str:
    night_start_hour = 21
    night_end_hour = 6
    def is_night(dt: datetime) -> bool:
        h = dt.hour
        return h >= night_start_hour or h < night_end_hour
    total_minutes = int((end - start).total_seconds() // 60)
    if total_minutes <= 0:
        return 'nap'
    night_minutes = 0
    cursor = start
    step = timedelta(minutes=1)
    while cursor < end:
        if is_night(cursor):
            night_minutes += 1
        cursor += step
    if night_minutes >= 90 or (start.date() != end.date() and total_minutes >= 120):
        return 'night'
    return 'nap'

def create_sleep_start(db: Session, baby_id: int, start_time: datetime, user_id: int, source: str = 'manual') -> SleepRecord:
    db_record = SleepRecord(
        baby_id=baby_id,
        user_id=user_id,
        sleep_type='nap',
        status='in_progress',
        start_time=start_time,
        source=source,
        wake_count=0
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def stop_sleep_record(db: Session, record_id: int, end_time: datetime) -> Optional[SleepRecord]:
    db_record = get_sleep_record(db, record_id)
    if not db_record:
        return None
    if db_record.end_time:
        return db_record
    db_record.end_time = end_time
    dur = int((end_time - db_record.start_time).total_seconds() // 60)
    db_record.duration = dur if dur >= 0 else None
    db_record.sleep_type = compute_sleep_type(db_record.start_time, end_time)
    db_record.status = 'completed'
    db.commit()
    db.refresh(db_record)
    return db_record

def auto_close_sleep_record(db: Session, record_id: int, auto_closed_at: datetime) -> Optional[SleepRecord]:
    db_record = get_sleep_record(db, record_id)
    if not db_record:
        return None
    if db_record.end_time:
        return db_record
    db_record.auto_closed_at = auto_closed_at
    db_record.status = 'auto_closed'
    db.commit()
    db.refresh(db_record)
    return db_record

def get_active_sleep_records_by_baby(db: Session, baby_id: int) -> list[SleepRecord]:
    query = db.query(SleepRecord).filter(SleepRecord.baby_id == baby_id)
    records = query.filter(SleepRecord.status.in_(['in_progress', 'auto_closed'])).order_by(SleepRecord.start_time.desc()).all()
    for record in records:
        _attach_creator_info(db, record)
    return records
