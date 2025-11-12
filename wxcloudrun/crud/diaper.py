"""
排便/排尿记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from wxcloudrun.models.diaper import DiaperRecord
from wxcloudrun.models.user import User
from wxcloudrun.models.baby import BabyFamily
from wxcloudrun.schemas.diaper import DiaperRecordCreate, DiaperRecordUpdate
from wxcloudrun.schemas.user import CreatorInfo


def _attach_creator_info(db: Session, record: DiaperRecord) -> None:
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


def get_diaper_record(db: Session, record_id: int) -> Optional[DiaperRecord]:
    """根据ID获取排便/排尿记录"""
    record = db.query(DiaperRecord).filter(DiaperRecord.id == record_id).first()
    if record:
        _attach_creator_info(db, record)
    return record


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

    records = query.order_by(DiaperRecord.record_time.desc()).offset(skip).limit(limit).all()

    # 为每条记录附加创建者信息
    for record in records:
        _attach_creator_info(db, record)

    return records


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
