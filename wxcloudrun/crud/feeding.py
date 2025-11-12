"""
喂养记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime
import json
from sqlalchemy.orm import Session
from wxcloudrun.models.feeding import FeedingRecord
from wxcloudrun.models.user import User
from wxcloudrun.models.baby import BabyFamily
from wxcloudrun.schemas.feeding import (
    FeedingRecordCreate,
    FeedingRecordUpdate,
    FeedingSequenceItem,
)
from wxcloudrun.schemas.user import CreatorInfo


def _deserialize_feeding_sequence(record: FeedingRecord) -> None:
    """反序列化喂养序列（从JSON字符串转为对象列表）"""
    if record.feeding_sequence:
        try:
            sequence_data = json.loads(record.feeding_sequence)
            record.feeding_sequence = [
                FeedingSequenceItem(**item) for item in sequence_data
            ]
        except (json.JSONDecodeError, TypeError, ValueError):
            record.feeding_sequence = None


def _serialize_feeding_sequence(data: dict) -> dict:
    """序列化喂养序列（从对象列表转为JSON字符串）"""
    if 'feeding_sequence' in data and data['feeding_sequence'] is not None:
        sequence_list = data['feeding_sequence']
        if isinstance(sequence_list, list) and len(sequence_list) > 0:
            # 转换为字典列表，然后序列化为JSON
            serialized_items = []
            for item in sequence_list:
                if hasattr(item, 'model_dump'):
                    # 使用 mode='json' 来确保 datetime 被转换为字符串
                    item_dict = item.model_dump(mode='json')
                else:
                    item_dict = item
                serialized_items.append(item_dict)

            data['feeding_sequence'] = json.dumps(
                serialized_items,
                ensure_ascii=False,
                default=str,
            )
    return data


def _attach_creator_info(db: Session, record: FeedingRecord) -> None:
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


def get_feeding_record(db: Session, record_id: int) -> Optional[FeedingRecord]:
    """根据ID获取喂养记录"""
    record = (
        db.query(FeedingRecord)
        .filter(FeedingRecord.id == record_id)
        .first()
    )
    if record:
        _deserialize_feeding_sequence(record)
        _attach_creator_info(db, record)
    return record


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

    records = (
        query.order_by(FeedingRecord.start_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # 为每条记录反序列化和附加创建者信息
    for record in records:
        _deserialize_feeding_sequence(record)
        _attach_creator_info(db, record)

    return records


def create_feeding_record(db: Session, record: FeedingRecordCreate, user_id: int) -> FeedingRecord:
    """创建喂养记录"""
    record_data = record.model_dump()
    record_data = _serialize_feeding_sequence(record_data)
    db_record = FeedingRecord(**record_data, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    _deserialize_feeding_sequence(db_record)
    return db_record


def update_feeding_record(
    db: Session, record_id: int, record: FeedingRecordUpdate
) -> Optional[FeedingRecord]:
    """更新喂养记录"""
    db_record = get_feeding_record(db, record_id)
    if not db_record:
        return None

    update_data = record.model_dump(exclude_unset=True)
    update_data = _serialize_feeding_sequence(update_data)

    for field, value in update_data.items():
        setattr(db_record, field, value)

    db.commit()
    db.refresh(db_record)
    _deserialize_feeding_sequence(db_record)
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
    record = (
        db.query(FeedingRecord)
        .filter(FeedingRecord.baby_id == baby_id)
        .order_by(FeedingRecord.start_time.desc())
        .first()
    )
    if record:
        _deserialize_feeding_sequence(record)
        _attach_creator_info(db, record)
    return record
