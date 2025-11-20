"""
首页聚合数据相关的 API 路由
"""
from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access
from wxcloudrun.crud import feeding as feeding_crud
from wxcloudrun.crud import diaper as diaper_crud
from wxcloudrun.crud import sleep as sleep_crud
from wxcloudrun.crud import growth as growth_crud
from wxcloudrun.schemas.feeding import FeedingRecordResponse
from wxcloudrun.schemas.diaper import DiaperRecordResponse
from wxcloudrun.schemas.sleep import SleepRecordResponse
from wxcloudrun.schemas.growth import GrowthRecordResponse

router = APIRouter(
    prefix="/api/home",
    tags=["首页"]
)


@router.get("/baby/{baby_id}", response_model=dict)
def get_home_aggregated_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=500, description="返回记录数"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
):
    verify_baby_access(baby_id, user_id, db)

    feeding_records = feeding_crud.get_feeding_records_by_baby(
        db=db,
        baby_id=baby_id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        feeding_type=None,
        sort_by="start_time",
        order="desc",
    )

    diaper_records = diaper_crud.get_diaper_records_by_baby(
        db, baby_id, skip, limit, start_date, end_date
    )

    sleep_records = sleep_crud.get_sleep_records_by_baby(
        db, baby_id, skip, limit, start_date, end_date
    )

    growth_records = growth_crud.get_growth_records_by_baby(
        db, baby_id, skip, limit, start_date, end_date
    )

    return {
        "feeding": [
            FeedingRecordResponse.model_validate(r, from_attributes=True)
            for r in feeding_records
        ],
        "diaper": [
            DiaperRecordResponse.model_validate(r, from_attributes=True)
            for r in diaper_records
        ],
        "sleep": [
            SleepRecordResponse.model_validate(r, from_attributes=True)
            for r in sleep_records
        ],
        "growth": [
            GrowthRecordResponse.model_validate(r, from_attributes=True)
            for r in growth_records
        ],
    }