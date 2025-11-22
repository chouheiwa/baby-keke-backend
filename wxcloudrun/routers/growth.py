"""
生长发育记录相关的 API 路由
"""
from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.growth import GrowthRecordCreate, GrowthRecordUpdate, GrowthRecordResponse
from wxcloudrun.crud import growth as growth_crud
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access

router = APIRouter(
    prefix="/api/growth",
    tags=["生长发育记录"]
)


@router.post("/", response_model=GrowthRecordResponse, status_code=status.HTTP_201_CREATED)
def create_growth_record(
    record: GrowthRecordCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """创建生长发育记录"""
    verify_baby_access(record.baby_id, user_id, db)
    created = growth_crud.create_growth_record(db, record, user_id)
    return GrowthRecordResponse.model_validate(created, from_attributes=True)


@router.get("/baby/{baby_id}", response_model=list[GrowthRecordResponse])
def get_growth_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=500, description="返回记录数"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期")
):
    """获取宝宝的生长发育记录列表"""
    verify_baby_access(baby_id, user_id, db)
    records = growth_crud.get_growth_records_by_baby(
        db, baby_id, skip, limit, start_date, end_date
    )
    return [GrowthRecordResponse.model_validate(r, from_attributes=True) for r in records]


@router.get("/{record_id}", response_model=GrowthRecordResponse)
def get_growth_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取单条生长发育记录"""
    db_record = growth_crud.get_growth_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)
    return GrowthRecordResponse.model_validate(db_record, from_attributes=True)


@router.patch("/{record_id}", response_model=GrowthRecordResponse)
def update_growth_record(
    record_id: int,
    record: GrowthRecordUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新生长发育记录"""
    db_record = growth_crud.get_growth_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    updated_record = growth_crud.update_growth_record(db, record_id, record)
    if not updated_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="更新失败")
    return GrowthRecordResponse.model_validate(updated_record, from_attributes=True)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_growth_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除生长发育记录"""
    db_record = growth_crud.get_growth_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    verify_baby_access(db_record.baby_id, user_id, db)

    success = growth_crud.delete_growth_record(db, record_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="删除失败")
    return None


@router.get("/baby/{baby_id}/latest", response_model=Optional[GrowthRecordResponse])
def get_latest_growth(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取最新的生长发育记录"""
    verify_baby_access(baby_id, user_id, db)

    latest = growth_crud.get_latest_growth(db, baby_id)
    if not latest:
        return None
    return GrowthRecordResponse.model_validate(latest, from_attributes=True)


@router.get("/baby/{baby_id}/curve", response_model=list[dict])
def get_growth_curve(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取生长曲线数据"""
    verify_baby_access(baby_id, user_id, db)
    return growth_crud.get_growth_curve_data(db, baby_id)
