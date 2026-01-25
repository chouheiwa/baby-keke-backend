"""
喂养记录相关的 CRUD 操作
"""
from typing import Optional
from datetime import datetime
import json
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
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
    feeding_type: Optional[str] = None,
    sort_by: Optional[str] = "start_time",
    order: Optional[str] = "desc",
) -> list[FeedingRecord]:
    query = db.query(FeedingRecord).filter(FeedingRecord.baby_id == baby_id)
    if feeding_type:
        query = query.filter(FeedingRecord.feeding_type == feeding_type)
    if start_date:
        query = query.filter(FeedingRecord.start_time >= start_date)
    if end_date:
        query = query.filter(FeedingRecord.start_time <= end_date)
    sort_col = FeedingRecord.start_time
    if sort_by == "end_time":
        sort_col = FeedingRecord.end_time
    elif sort_by == "created_at":
        sort_col = FeedingRecord.created_at
    elif sort_by == "updated_at":
        sort_col = FeedingRecord.updated_at
    if order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())
    records = query.offset(skip).limit(limit).all()
    for record in records:
        _deserialize_feeding_sequence(record)
        _attach_creator_info(db, record)
    return records


def _calculate_durations(data: dict) -> dict:
    """从 feeding_sequence 计算 duration_left 和 duration_right"""
    if 'feeding_sequence' in data and data['feeding_sequence']:
        sequence = data['feeding_sequence']
        if isinstance(sequence, list):
            left_duration = 0
            right_duration = 0
            for item in sequence:
                # item 可能是 dict 或 object
                side = getattr(item, 'side', None) or item.get('side')
                duration = getattr(item, 'duration_seconds', 0) or item.get('duration_seconds', 0)
                
                if side == 'left':
                    left_duration += duration
                elif side == 'right':
                    right_duration += duration
            
            # 如果没有手动指定时长，则使用计算值
            if 'duration_left' not in data or data['duration_left'] is None:
                data['duration_left'] = left_duration
            if 'duration_right' not in data or data['duration_right'] is None:
                data['duration_right'] = right_duration
    return data


def create_feeding_record(db: Session, record: FeedingRecordCreate, user_id: int) -> FeedingRecord:
    """创建喂养记录"""
    record_data = record.model_dump()
    record_data = _calculate_durations(record_data)
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
    update_data = _calculate_durations(update_data)
    update_data = _serialize_feeding_sequence(update_data)
    if 'start_time' not in update_data:
        update_data['start_time'] = db_record.start_time
        # 强制写回 start_time，避免数据库自动更新时间覆盖
        flag_modified(db_record, 'start_time')

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


def get_daily_feeding_stats(db: Session, baby_id: int, date: datetime) -> dict:
    """获取指定日期的喂养统计（左右侧总时长、最近一次喂养侧）"""
    # 1. 获取当天的所有记录
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    records = (
        db.query(FeedingRecord)
        .filter(
            FeedingRecord.baby_id == baby_id,
            FeedingRecord.feeding_type == 'breast',
            FeedingRecord.start_time >= start_of_day,
            FeedingRecord.start_time <= end_of_day
        )
        .order_by(FeedingRecord.start_time.asc())
        .all()
    )
    
    total_left = 0
    total_right = 0
    
    for r in records:
        total_left += (r.duration_left or 0)
        total_right += (r.duration_right or 0)
        
    # 2. 获取最近一次喂养记录（不限当天，只要是最近的）
    last_record = get_latest_feeding(db, baby_id)
    last_side = None
    last_time = None
    
    if last_record:
        # 尝试从 feeding_sequence 判断最后一次的具体侧
        # 如果没有 sequence，则尝试用 duration 判断
        # 简单起见，我们看 duration_left 和 duration_right
        # 如果都有，说明是双侧，或者最后一次是某一侧？
        # 这里我们简单逻辑：如果 sequence 存在，取最后一个 item 的 side
        # 否则，如果 duration_right > 0 则 right，否则 left (假设)
        
        if last_record.feeding_sequence and isinstance(last_record.feeding_sequence, list) and len(last_record.feeding_sequence) > 0:
             last_item = last_record.feeding_sequence[-1]
             last_side = getattr(last_item, 'side', None) or last_item.get('side')
        else:
             # Fallback
             if (last_record.duration_right or 0) > 0:
                 last_side = 'right'
             elif (last_record.duration_left or 0) > 0:
                 last_side = 'left'
                 
        last_time = last_record.end_time or last_record.start_time

    return {
        "total_left": total_left,
        "total_right": total_right,
        "last_side": last_side,
        "last_time": last_time
    }
