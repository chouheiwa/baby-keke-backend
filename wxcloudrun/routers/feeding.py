"""
喂养记录相关的 API 路由
"""
from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.feeding import FeedingRecordCreate, FeedingRecordUpdate, FeedingRecordResponse
from wxcloudrun.crud import feeding as feeding_crud
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access

router = APIRouter(
    prefix="/api/feeding",
    tags=["喂养记录"]
)


@router.post("/", response_model=FeedingRecordResponse, status_code=status.HTTP_201_CREATED)
def create_feeding_record(
    record: FeedingRecordCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """创建喂养记录"""
    verify_baby_access(record.baby_id, user_id, db)
    created = feeding_crud.create_feeding_record(db, record, user_id)
    return FeedingRecordResponse.model_validate(created, from_attributes=True)


@router.get("/baby/{baby_id}", response_model=list[FeedingRecordResponse])
def get_feeding_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    feeding_type: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("start_time"),
    order: Optional[str] = Query("desc")
):
    verify_baby_access(baby_id, user_id, db)
    records = feeding_crud.get_feeding_records_by_baby(
        db=db,
        baby_id=baby_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        feeding_type=feeding_type,
        sort_by=sort_by,
        order=order,
    )
    return [FeedingRecordResponse.model_validate(r, from_attributes=True) for r in records]


@router.get("/{record_id}", response_model=FeedingRecordResponse)
def get_feeding_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取单条喂养记录"""
    db_record = feeding_crud.get_feeding_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)
    return FeedingRecordResponse.model_validate(db_record, from_attributes=True)


@router.patch("/{record_id}", response_model=FeedingRecordResponse)
def update_feeding_record(
    record_id: int,
    record: FeedingRecordUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新喂养记录"""
    db_record = feeding_crud.get_feeding_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    updated_record = feeding_crud.update_feeding_record(db, record_id, record)
    if not updated_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
    return FeedingRecordResponse.model_validate(updated_record, from_attributes=True)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feeding_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除喂养记录"""
    db_record = feeding_crud.get_feeding_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    success = feeding_crud.delete_feeding_record(db, record_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="删除失败")
    return None


@router.get("/baby/{baby_id}/latest", response_model=FeedingRecordResponse)
def get_latest_feeding(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取最近一次喂养记录"""
    verify_baby_access(baby_id, user_id, db)

    latest = feeding_crud.get_latest_feeding(db, baby_id)
    if not latest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="暂无喂养记录")
    return FeedingRecordResponse.model_validate(latest, from_attributes=True)
    return FeedingRecordResponse.model_validate(latest, from_attributes=True)


@router.get("/stats/daily", response_model=dict)
def get_daily_stats(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    date: Optional[datetime] = Query(None)
):
    """获取每日喂养统计"""
    verify_baby_access(baby_id, user_id, db)
    
    query_date = date or datetime.now()
    stats = feeding_crud.get_daily_feeding_stats(db, baby_id, query_date)
    return stats
