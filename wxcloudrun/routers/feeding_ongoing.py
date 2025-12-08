"""
正在进行的喂养记录相关的 API 路由
"""
from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.models.feeding_ongoing import FeedingOngoing
from wxcloudrun.models.feeding import FeedingRecord
from wxcloudrun.schemas.feeding_ongoing import FeedingOngoingCreate, FeedingOngoingResponse
from wxcloudrun.schemas.feeding import FeedingRecordResponse
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access
from wxcloudrun.crud import feeding as feeding_crud

router = APIRouter(
    prefix="/api/feeding/ongoing",
    tags=["喂养计时同步"]
)

@router.get("/{baby_id}", response_model=Optional[FeedingOngoingResponse])
def get_ongoing_feeding(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取正在进行的喂养状态"""
    verify_baby_access(baby_id, user_id, db)
    
    ongoing = db.query(FeedingOngoing).filter(FeedingOngoing.baby_id == baby_id).first()
    if not ongoing:
        return None
        
    return FeedingOngoingResponse.model_validate(ongoing, from_attributes=True)

@router.post("/action", response_model=FeedingOngoingResponse)
def update_ongoing_action(
    action_data: FeedingOngoingCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新喂养状态（开始/暂停）"""
    verify_baby_access(action_data.baby_id, user_id, db)
    
    now = datetime.now()
    ongoing = db.query(FeedingOngoing).filter(FeedingOngoing.baby_id == action_data.baby_id).first()
    
    if not ongoing:
        # 如果不存在，且操作是开始，则创建
        if action_data.action == 'pause':
            raise HTTPException(status_code=400, detail="没有正在进行的喂养，无法暂停")
            
        ongoing = FeedingOngoing(
            baby_id=action_data.baby_id,
            start_time=now,
            last_action_time=now,
            current_side='left' if action_data.action == 'start_left' else 'right',
            accumulated_left=0,
            accumulated_right=0
        )
        db.add(ongoing)
    else:
        # 计算上一个阶段的时长并累加
        if ongoing.current_side != 'paused':
            duration = (now - ongoing.last_action_time).total_seconds()
            if ongoing.current_side == 'left':
                ongoing.accumulated_left += int(duration)
            else:
                ongoing.accumulated_right += int(duration)
        
        # 更新状态
        if action_data.action == 'start_left':
            ongoing.current_side = 'left'
        elif action_data.action == 'start_right':
            ongoing.current_side = 'right'
        elif action_data.action == 'pause':
            ongoing.current_side = 'paused'
            
        ongoing.last_action_time = now
    
    db.commit()
    db.refresh(ongoing)
    return FeedingOngoingResponse.model_validate(ongoing, from_attributes=True)

@router.post("/resume/{record_id}", response_model=FeedingOngoingResponse)
def resume_feeding_from_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """从已有记录恢复ongoing session（仅支持1小时内的记录）"""
    # 获取原记录
    original_record = db.query(FeedingRecord).filter(FeedingRecord.id == record_id).first()
    if not original_record:
        raise HTTPException(status_code=404, detail="记录不存在")

    verify_baby_access(original_record.baby_id, user_id, db)

    # 检查记录是否在1小时内
    now = datetime.now()
    time_diff = (now - original_record.start_time).total_seconds() / 60
    if time_diff > 60:
        raise HTTPException(status_code=400, detail="只能恢复1小时内的记录")

    # 检查是否已有ongoing session
    existing_ongoing = db.query(FeedingOngoing).filter(
        FeedingOngoing.baby_id == original_record.baby_id
    ).first()
    if existing_ongoing:
        raise HTTPException(status_code=400, detail="已有正在进行的喂养，请先完成")

    # 创建新的ongoing session，使用原记录的时长作为初始累计值
    ongoing = FeedingOngoing(
        baby_id=original_record.baby_id,
        start_time=original_record.start_time,  # 保持原开始时间
        last_action_time=now,  # 当前时间作为最后操作时间
        current_side='paused',  # 初始为暂停状态
        accumulated_left=original_record.duration_left or 0,
        accumulated_right=original_record.duration_right or 0
    )

    db.add(ongoing)

    # 删除原记录
    db.delete(original_record)

    db.commit()
    db.refresh(ongoing)

    return FeedingOngoingResponse.model_validate(ongoing, from_attributes=True)

@router.post("/finish/{baby_id}", response_model=FeedingRecordResponse)
def finish_ongoing_feeding(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """结束喂养并保存记录"""
    verify_baby_access(baby_id, user_id, db)
    
    ongoing = db.query(FeedingOngoing).filter(FeedingOngoing.baby_id == baby_id).first()
    if not ongoing:
        raise HTTPException(status_code=404, detail="没有正在进行的喂养")
    
    # 计算最后一段时长
    now = datetime.now()
    if ongoing.current_side != 'paused':
        duration = (now - ongoing.last_action_time).total_seconds()
        if ongoing.current_side == 'left':
            ongoing.accumulated_left += int(duration)
        else:
            ongoing.accumulated_right += int(duration)
            
    # 创建正式记录
    # 构造 feeding_sequence (简化版，因为我们只存了总时长，如果需要详细片段，需要更复杂的表结构)
    # 这里为了兼容，我们构造两个大的片段
    sequence = []
    if ongoing.accumulated_left > 0:
        sequence.append({
            "side": "left",
            "duration_seconds": ongoing.accumulated_left,
            "start_time": ongoing.start_time # 近似值
        })
    if ongoing.accumulated_right > 0:
        sequence.append({
            "side": "right",
            "duration_seconds": ongoing.accumulated_right,
            "start_time": ongoing.start_time # 近似值
        })
        
    # 序列化 sequence
    import json
    sequence_json = json.dumps(sequence, default=str)
    
    new_record = FeedingRecord(
        baby_id=baby_id,
        user_id=user_id,
        feeding_type='breast',
        start_time=ongoing.start_time,
        end_time=now,
        duration_left=ongoing.accumulated_left,
        duration_right=ongoing.accumulated_right,
        feeding_sequence=sequence_json,
        notes="" 
    )
    
    db.add(new_record)
    db.delete(ongoing) # 删除临时状态
    db.commit()
    db.refresh(new_record)
    
    # 触发反序列化以便返回
    feeding_crud._deserialize_feeding_sequence(new_record)
    feeding_crud._attach_creator_info(db, new_record)
    
    return FeedingRecordResponse.model_validate(new_record, from_attributes=True)
