"""
吸奶记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from wxcloudrun.models.pumping import PumpingRecord
from wxcloudrun.models.user import User
from wxcloudrun.models.baby import BabyFamily
from wxcloudrun.schemas.pumping import PumpingRecordCreate, PumpingRecordUpdate
from wxcloudrun.schemas.user import CreatorInfo


def _attach_creator_info(db: Session, record: PumpingRecord) -> None:
    """为吸奶记录附加创建者信息"""
    if not record:
        return

    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        record.created_by = None
        return

    # 查找家庭关系
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

    # 关系映射
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


def get_pumping_record(db: Session, record_id: int) -> Optional[PumpingRecord]:
    """根据ID获取吸奶记录"""
    record = db.query(PumpingRecord).filter(PumpingRecord.id == record_id).first()
    if record:
        _attach_creator_info(db, record)
    return record


def get_pumping_records_by_baby(
    db: Session,
    baby_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> list[PumpingRecord]:
    """获取宝宝的吸奶记录"""
    query = db.query(PumpingRecord).filter(PumpingRecord.baby_id == baby_id)

    if start_date:
        query = query.filter(PumpingRecord.record_time >= start_date)
    if end_date:
        query = query.filter(PumpingRecord.record_time <= end_date)

    records = query.order_by(PumpingRecord.record_time.desc()).offset(skip).limit(limit).all()

    # 为每条记录附加创建者信息
    for record in records:
        _attach_creator_info(db, record)

    return records


def create_pumping_record(db: Session, record: PumpingRecordCreate, user_id: int) -> PumpingRecord:
    """创建吸奶记录"""
    db_record = PumpingRecord(**record.model_dump(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    _attach_creator_info(db, db_record)
    return db_record


def update_pumping_record(
    db: Session, record_id: int, record: PumpingRecordUpdate
) -> Optional[PumpingRecord]:
    """更新吸奶记录"""
    db_record = get_pumping_record(db, record_id)
    if not db_record:
        return None

    update_data = record.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)

    db.commit()
    db.refresh(db_record)
    _attach_creator_info(db, db_record)
    return db_record


def delete_pumping_record(db: Session, record_id: int) -> bool:
    """删除吸奶记录"""
    db_record = db.query(PumpingRecord).filter(PumpingRecord.id == record_id).first()
    if not db_record:
        return False

    db.delete(db_record)
    db.commit()
    return True


def get_pumping_stats_by_date(
    db: Session, baby_id: int, start_date: datetime, end_date: datetime
) -> dict:
    """统计指定日期范围内的吸奶量"""
    records = get_pumping_records_by_baby(
        db, baby_id, start_date=start_date, end_date=end_date, limit=1000
    )

    total_amount = sum(record.total_amount for record in records)
    left_total = sum(record.left_amount or 0 for record in records)
    right_total = sum(record.right_amount or 0 for record in records)

    return {
        'count': len(records),
        'total_amount': total_amount,
        'left_total': left_total,
        'right_total': right_total,
        'average_amount': total_amount / len(records) if len(records) > 0 else 0
    }
