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
    """给记录附加创建者信息。

    优先获取在该宝宝下非空的关系，找不到则回退。
    同时生成中文显示名称（relation_display）。
    """
    if not record:
        return

    # 查询用户信息
    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        record.created_by = None
        return

    # 优先获取非空 relation 的家庭成员记录
    family_with_relation = (
        db.query(BabyFamily)
        .filter(
            BabyFamily.user_id == user.id,
            BabyFamily.baby_id == record.baby_id,
            BabyFamily.relation.isnot(None)
        )
        .order_by(BabyFamily.id.desc())
        .first()
    )

    relation = None
    relation_display = None
    if family_with_relation:
        relation = family_with_relation.relation
        relation_display = family_with_relation.relation_display
    else:
        # 回退：任意一条家庭成员记录（可能 relation 为 NULL）
        family_any = (
            db.query(BabyFamily)
            .filter(
                BabyFamily.user_id == user.id,
                BabyFamily.baby_id == record.baby_id
            )
            .order_by(BabyFamily.id.desc())
            .first()
        )
        if family_any:
            relation = family_any.relation
            relation_display = family_any.relation_display
        else:
            relation = None
            relation_display = None

    # 关系显示映射（同时支持枚举代码和中文原值）
    relation_map = {
        'mom': '妈妈',
        'dad': '爸爸',
        'grandpa_p': '爷爷',
        'grandma_p': '奶奶',
        'grandpa_m': '外公',
        'grandma_m': '外婆',
        'other': '其他'
    }
    # 如果数据库中没有显示名称，则根据枚举映射生成中文显示
    relation_display = relation_display or relation_map.get(relation, relation)

    record.created_by = CreatorInfo(
        user_id=user.id,
        nickname=user.nickname,
        relation=relation,
        relation_display=relation_display
    )


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
    limit: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by: str = "start_time",
    order: str = "desc"
) -> list[SleepRecord]:
    """获取宝宝的睡眠记录"""
    query = db.query(SleepRecord).filter(SleepRecord.baby_id == baby_id)

    if start_date:
        query = query.filter(SleepRecord.start_time >= start_date)
    if end_date:
        query = query.filter(SleepRecord.start_time <= end_date)

    # 动态排序
    sort_column = getattr(SleepRecord, sort_by, SleepRecord.start_time)
    query = query.order_by(sort_column.desc() if order == "desc" else sort_column.asc())

    query = query.offset(skip)
    if limit:
        query = query.limit(limit)

    records = query.all()

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
        payload['status'] = 'completed'
    else:
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

    for record in records:
        if getattr(record, 'status', 'completed') != 'completed':
            continue
        if record.duration:
            total_duration += record.duration
        total_wake_count += record.wake_count or 0

    return {
        'total_records': len(records),
        'total_duration_minutes': total_duration,
        'total_duration_hours': round(total_duration / 60, 2) if total_duration > 0 else 0,
        'average_duration_minutes': round(total_duration / max(1, total_records_completed(records)), 2),
        'total_wake_count': total_wake_count,
    }

def total_records_completed(records: list[SleepRecord]) -> int:
    return sum(1 for r in records if getattr(r, 'status', 'completed') == 'completed')


def create_sleep_start(db: Session, baby_id: int, start_time: datetime, user_id: int, source: str = 'manual', position: Optional[str] = None) -> SleepRecord:
    db_record = SleepRecord(
        baby_id=baby_id,
        user_id=user_id,
        status='in_progress',
        start_time=start_time,
        source=source,
        position=position,
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

def get_active_sleep_records_by_baby(db: Session, baby_id: int) -> Optional[SleepRecord]:
    record = db.query(SleepRecord).filter(
        SleepRecord.baby_id == baby_id,
        SleepRecord.status == 'in_progress'
    ).order_by(SleepRecord.start_time.desc()).first()
    if record:
        _attach_creator_info(db, record)
    return record
