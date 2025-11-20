"""
睡眠记录相关的 API 路由
"""
from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.sleep import (
    SleepRecordCreate,
    SleepRecordUpdate,
    SleepRecordResponse,
    SleepStartCreate,
    SleepStopUpdate,
    SleepAutoCloseUpdate,
)
from wxcloudrun.crud import sleep as sleep_crud
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access

router = APIRouter(
    prefix="/api/sleep",
    tags=["睡眠记录"]
)


@router.post("/", response_model=SleepRecordResponse, status_code=status.HTTP_201_CREATED)
def create_sleep_record(
    record: SleepRecordCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    verify_baby_access(record.baby_id, user_id, db)
    created = sleep_crud.create_sleep_record(db, record, user_id)
    return SleepRecordResponse.model_validate(created, from_attributes=True)


@router.get("/baby/{baby_id}", response_model=list[SleepRecordResponse])
def get_sleep_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: Optional[int] = Query(None, ge=1, le=500, description="返回记录数"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    sort_by: str = Query("start_time", description="排序字段"),
    order: str = Query("desc", regex="^(asc|desc)$", description="排序方向")
):
    """获取宝宝的睡眠记录列表"""
    verify_baby_access(baby_id, user_id, db)
    records = sleep_crud.get_sleep_records_by_baby(
        db, baby_id, skip, limit, start_date, end_date, sort_by, order
    )
    return [SleepRecordResponse.model_validate(r, from_attributes=True) for r in records]

@router.get("/baby/{baby_id}/active", response_model=SleepRecordResponse | None)
def get_active_sleep_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    verify_baby_access(baby_id, user_id, db)
    record = sleep_crud.get_active_sleep_records_by_baby(db, baby_id)
    return SleepRecordResponse.model_validate(record, from_attributes=True) if record else None


@router.get("/{record_id}", response_model=SleepRecordResponse)
def get_sleep_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取单条睡眠记录"""
    db_record = sleep_crud.get_sleep_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)
    return SleepRecordResponse.model_validate(db_record, from_attributes=True)


@router.patch("/{record_id}", response_model=SleepRecordResponse)
def update_sleep_record(
    record_id: int,
    record: SleepRecordUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新睡眠记录"""
    db_record = sleep_crud.get_sleep_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    updated_record = sleep_crud.update_sleep_record(db, record_id, record)
    if not updated_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
    return SleepRecordResponse.model_validate(updated_record, from_attributes=True)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sleep_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除睡眠记录"""
    db_record = sleep_crud.get_sleep_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    success = sleep_crud.delete_sleep_record(db, record_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="删除失败")
    return None


@router.get("/baby/{baby_id}/stats", response_model=dict)
def get_sleep_stats(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    start_date: datetime = Query(..., description="开始日期"),
    end_date: datetime = Query(..., description="结束日期")
):
    """获取指定日期范围的睡眠统计"""
    verify_baby_access(baby_id, user_id, db)
    return sleep_crud.get_sleep_stats_by_date(db, baby_id, start_date, end_date)
@router.post("/start", response_model=SleepRecordResponse, status_code=status.HTTP_201_CREATED)
def start_sleep_record(
    payload: SleepStartCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    verify_baby_access(payload.baby_id, user_id, db)
    created = sleep_crud.create_sleep_start(db, payload.baby_id, payload.start_time, user_id, payload.source or 'manual', payload.position)
    return SleepRecordResponse.model_validate(created, from_attributes=True)

@router.post("/start/", response_model=SleepRecordResponse, status_code=status.HTTP_201_CREATED)
def start_sleep_record_slash(
    payload: SleepStartCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    verify_baby_access(payload.baby_id, user_id, db)
    created = sleep_crud.create_sleep_start(db, payload.baby_id, payload.start_time, user_id, payload.source or 'manual', payload.position)
    return SleepRecordResponse.model_validate(created, from_attributes=True)

@router.patch("/{record_id}/stop", response_model=SleepRecordResponse)
def stop_sleep_record(
    record_id: int,
    payload: SleepStopUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    db_record = sleep_crud.get_sleep_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    verify_baby_access(db_record.baby_id, user_id, db)
    try:
        updated_record = sleep_crud.stop_sleep_record(db, record_id, payload.end_time)
        if not updated_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
        return SleepRecordResponse.model_validate(updated_record, from_attributes=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{record_id}/stop/", response_model=SleepRecordResponse)
def stop_sleep_record_slash(
    record_id: int,
    payload: SleepStopUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    db_record = sleep_crud.get_sleep_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    verify_baby_access(db_record.baby_id, user_id, db)
    try:
        updated_record = sleep_crud.stop_sleep_record(db, record_id, payload.end_time)
        if not updated_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
        return SleepRecordResponse.model_validate(updated_record, from_attributes=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{record_id}/auto-close", response_model=SleepRecordResponse)
def auto_close_sleep_record(
    record_id: int,
    payload: SleepAutoCloseUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    db_record = sleep_crud.get_sleep_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    verify_baby_access(db_record.baby_id, user_id, db)
    updated_record = sleep_crud.auto_close_sleep_record(db, record_id, payload.auto_closed_at)
    if not updated_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
    return SleepRecordResponse.model_validate(updated_record, from_attributes=True)

@router.patch("/{record_id}/auto-close/", response_model=SleepRecordResponse)
def auto_close_sleep_record_slash(
    record_id: int,
    payload: SleepAutoCloseUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    db_record = sleep_crud.get_sleep_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    verify_baby_access(db_record.baby_id, user_id, db)
    updated_record = sleep_crud.auto_close_sleep_record(db, record_id, payload.auto_closed_at)
    if not updated_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
    return SleepRecordResponse.model_validate(updated_record, from_attributes=True)
