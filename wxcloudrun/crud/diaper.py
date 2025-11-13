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
    if not record:
        return

    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        record.created_by = None
        return

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

    relation_map = {
        'mom': '妈妈',
        'dad': '爸爸',
        'grandpa_p': '爷爷',
        'grandma_p': '奶奶',
        'grandpa_m': '外公',
        'grandma_m': '外婆',
        'other': '其他'
    }
    relation_display = relation_display or relation_map.get(relation, relation)

    record.created_by = CreatorInfo(
        user_id=user.id,
        nickname=user.nickname,
        relation=relation,
        relation_display=relation_display
    )


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
