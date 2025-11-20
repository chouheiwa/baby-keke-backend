"""
排便/排尿记录相关的 API 路由
"""
from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.diaper import DiaperRecordCreate, DiaperRecordUpdate, DiaperRecordResponse
from wxcloudrun.crud import diaper as diaper_crud
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access

router = APIRouter(
    prefix="/api/diaper",
    tags=["排便/排尿记录"]
)


@router.post("/", response_model=DiaperRecordResponse, status_code=status.HTTP_201_CREATED)
def create_diaper_record(
    record: DiaperRecordCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """创建排便/排尿记录"""
    verify_baby_access(record.baby_id, user_id, db)
    created = diaper_crud.create_diaper_record(db, record, user_id)
    return DiaperRecordResponse.model_validate(created, from_attributes=True)


@router.get("/baby/{baby_id}", response_model=list[DiaperRecordResponse])
def get_diaper_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=500, description="返回记录数"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期")
):
    """获取宝宝的排便/排尿记录列表"""
    verify_baby_access(baby_id, user_id, db)
    records = diaper_crud.get_diaper_records_by_baby(
        db, baby_id, skip, limit, start_date, end_date
    )
    return [DiaperRecordResponse.model_validate(r, from_attributes=True) for r in records]


@router.get("/{record_id}", response_model=DiaperRecordResponse)
def get_diaper_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取单条排便/排尿记录"""
    db_record = diaper_crud.get_diaper_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)
    return DiaperRecordResponse.model_validate(db_record, from_attributes=True)


@router.patch("/{record_id}", response_model=DiaperRecordResponse)
def update_diaper_record(
    record_id: int,
    record: DiaperRecordUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新排便/排尿记录"""
    db_record = diaper_crud.get_diaper_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    updated_record = diaper_crud.update_diaper_record(db, record_id, record)
    if not updated_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
    return DiaperRecordResponse.model_validate(updated_record, from_attributes=True)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_diaper_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除排便/排尿记录"""
    db_record = diaper_crud.get_diaper_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    success = diaper_crud.delete_diaper_record(db, record_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="删除失败")
    return None


@router.get("/baby/{baby_id}/stats", response_model=dict)
def get_diaper_stats(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    start_date: datetime = Query(..., description="开始日期"),
    end_date: datetime = Query(..., description="结束日期")
):
    """获取指定日期范围的排便/排尿统计"""
    verify_baby_access(baby_id, user_id, db)
    return diaper_crud.get_diaper_count_by_date(db, baby_id, start_date, end_date)
