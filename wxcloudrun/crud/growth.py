"""
生长发育记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from wxcloudrun.models.growth import GrowthRecord
from wxcloudrun.models.user import User
from wxcloudrun.models.baby import BabyFamily
from wxcloudrun.schemas.growth import GrowthRecordCreate, GrowthRecordUpdate
from wxcloudrun.schemas.user import CreatorInfo


def _attach_creator_info(db: Session, record: GrowthRecord) -> None:
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


def get_growth_record(db: Session, record_id: int) -> Optional[GrowthRecord]:
    """根据ID获取生长发育记录"""
    record = db.query(GrowthRecord).filter(GrowthRecord.id == record_id).first()
    if record:
        _attach_creator_info(db, record)
    return record


def get_growth_records_by_baby(
    db: Session,
    baby_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> list[GrowthRecord]:
    """获取宝宝的生长发育记录"""
    query = db.query(GrowthRecord).filter(GrowthRecord.baby_id == baby_id)

    if start_date:
        query = query.filter(GrowthRecord.record_date >= start_date)
    if end_date:
        query = query.filter(GrowthRecord.record_date <= end_date)

    records = query.order_by(GrowthRecord.record_date.desc()).offset(skip).limit(limit).all()

    # 为每条记录附加创建者信息
    for record in records:
        _attach_creator_info(db, record)

    return records


def create_growth_record(db: Session, record: GrowthRecordCreate, user_id: int) -> GrowthRecord:
    """创建生长发育记录"""
    db_record = GrowthRecord(**record.model_dump(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_growth_record(
    db: Session, record_id: int, record: GrowthRecordUpdate
) -> Optional[GrowthRecord]:
    """更新生长发育记录"""
    db_record = get_growth_record(db, record_id)
    if not db_record:
        return None

    update_data = record.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)

    db.commit()
    db.refresh(db_record)
    return db_record


def delete_growth_record(db: Session, record_id: int) -> bool:
    """删除生长发育记录"""
    db_record = get_growth_record(db, record_id)
    if not db_record:
        return False

    db.delete(db_record)
    db.commit()
    return True


def get_latest_growth(db: Session, baby_id: int) -> Optional[GrowthRecord]:
    """获取最新的生长发育记录"""
    record = (
        db.query(GrowthRecord)
        .filter(GrowthRecord.baby_id == baby_id)
        .order_by(GrowthRecord.record_date.desc())
        .first()
    )
    if record:
        _attach_creator_info(db, record)
    return record


def get_growth_curve_data(db: Session, baby_id: int) -> list[dict]:
    """获取生长曲线数据（按时间排序）"""
    records = (
        db.query(GrowthRecord)
        .filter(GrowthRecord.baby_id == baby_id)
        .order_by(GrowthRecord.record_date.asc())
        .all()
    )

    return [
        {
            'date': record.record_date,
            'weight': float(record.weight) if record.weight else None,
            'height': float(record.height) if record.height else None,
            'head_circumference': float(record.head_circumference) if record.head_circumference else None,
        }
        for record in records
    ]
