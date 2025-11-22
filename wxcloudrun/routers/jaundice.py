from typing import Annotated, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.jaundice import JaundiceRecordCreate, JaundiceRecordUpdate, JaundiceRecordResponse
from wxcloudrun.crud import jaundice as jaundice_crud
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access

router = APIRouter(
    prefix="/api/jaundice",
    tags=["黄疸记录"]
)

@router.post("/", response_model=JaundiceRecordResponse, status_code=status.HTTP_201_CREATED)
def create_jaundice_record(
    record: JaundiceRecordCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """创建黄疸记录"""
    verify_baby_access(record.baby_id, user_id, db)
    created = jaundice_crud.create_jaundice_record(db, record)
    return JaundiceRecordResponse.model_validate(created, from_attributes=True)

@router.get("/baby/{baby_id}", response_model=List[JaundiceRecordResponse])
def get_jaundice_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """获取宝宝的黄疸记录列表"""
    verify_baby_access(baby_id, user_id, db)
    records = jaundice_crud.get_jaundice_records_by_baby(db, baby_id, skip, limit)
    return [JaundiceRecordResponse.model_validate(r, from_attributes=True) for r in records]

@router.get("/baby/{baby_id}/latest", response_model=Optional[JaundiceRecordResponse])
def get_latest_jaundice(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取最新的黄疸记录"""
    verify_baby_access(baby_id, user_id, db)
    latest = jaundice_crud.get_latest_jaundice(db, baby_id)
    if not latest:
        return None
    return JaundiceRecordResponse.model_validate(latest, from_attributes=True)

@router.get("/{record_id}", response_model=JaundiceRecordResponse)
def get_jaundice_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取单条黄疸记录"""
    db_record = jaundice_crud.get_jaundice_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    
    verify_baby_access(db_record.baby_id, user_id, db)
    return JaundiceRecordResponse.model_validate(db_record, from_attributes=True)

@router.patch("/{record_id}", response_model=JaundiceRecordResponse)
def update_jaundice_record(
    record_id: int,
    record: JaundiceRecordUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新黄疸记录"""
    db_record = jaundice_crud.get_jaundice_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    
    verify_baby_access(db_record.baby_id, user_id, db)
    
    updated = jaundice_crud.update_jaundice_record(db, record_id, record)
    return JaundiceRecordResponse.model_validate(updated, from_attributes=True)

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jaundice_record(
    record_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除黄疸记录"""
    db_record = jaundice_crud.get_jaundice_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    
    verify_baby_access(db_record.baby_id, user_id, db)
    
    jaundice_crud.delete_jaundice_record(db, record_id)
    return None
