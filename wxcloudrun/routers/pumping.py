"""
吸奶记录相关的 API 路由
"""
from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.pumping import PumpingRecordCreate, PumpingRecordUpdate, PumpingRecordResponse
from wxcloudrun.crud import pumping as pumping_crud
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access

router = APIRouter(
    prefix="/api/pumping",
    tags=["吸奶记录"]
)


@router.post("/", response_model=PumpingRecordResponse, status_code=status.HTTP_201_CREATED)
def create_pumping_record(
    record: PumpingRecordCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """创建吸奶记录"""
    verify_baby_access(record.baby_id, user_id, db)
    created = pumping_crud.create_pumping_record(db, record, user_id)
    return PumpingRecordResponse.model_validate(created, from_attributes=True)


@router.get("/baby/{baby_id}", response_model=list[PumpingRecordResponse])
def get_pumping_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=500, description="返回记录数"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期")
):
    """获取宝宝的吸奶记录列表"""
    verify_baby_access(baby_id, user_id, db)
    records = pumping_crud.get_pumping_records_by_baby(
        db, baby_id, skip, limit, start_date, end_date
    )
    return [PumpingRecordResponse.model_validate(r, from_attributes=True) for r in records]


@router.get("/{record_id}", response_model=PumpingRecordResponse)
def get_pumping_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取单条吸奶记录"""
    db_record = pumping_crud.get_pumping_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)
    return PumpingRecordResponse.model_validate(db_record, from_attributes=True)


@router.patch("/{record_id}", response_model=PumpingRecordResponse)
def update_pumping_record(
    record_id: int,
    record: PumpingRecordUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新吸奶记录"""
    db_record = pumping_crud.get_pumping_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    updated_record = pumping_crud.update_pumping_record(db, record_id, record)
    if not updated_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
    return PumpingRecordResponse.model_validate(updated_record, from_attributes=True)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pumping_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除吸奶记录"""
    db_record = pumping_crud.get_pumping_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    success = pumping_crud.delete_pumping_record(db, record_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="删除失败")
    return None


@router.get("/baby/{baby_id}/stats")
def get_pumping_stats(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    start_date: datetime = Query(..., description="开始日期"),
    end_date: datetime = Query(..., description="结束日期")
):
    """获取吸奶统计数据"""
    verify_baby_access(baby_id, user_id, db)
    stats = pumping_crud.get_pumping_stats_by_date(db, baby_id, start_date, end_date)
    return stats
