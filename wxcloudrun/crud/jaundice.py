from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
from wxcloudrun.models.jaundice import JaundiceRecord
from wxcloudrun.schemas.jaundice import JaundiceRecordCreate, JaundiceRecordUpdate

def create_jaundice_record(db: Session, record: JaundiceRecordCreate, user_id: int) -> JaundiceRecord:
    """创建黄疸记录"""
    db_record = JaundiceRecord(
        baby_id=record.baby_id,
        user_id=user_id,
        record_date=record.record_date,
        value=record.value,
        photo_url=record.photo_url,
        notes=record.notes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_jaundice_record(db: Session, record_id: int) -> Optional[JaundiceRecord]:
    """获取单条黄疸记录"""
    return db.query(JaundiceRecord).filter(JaundiceRecord.id == record_id).first()

def get_jaundice_records_by_baby(
    db: Session, 
    baby_id: int, 
    skip: int = 0, 
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[JaundiceRecord]:
    """获取宝宝的黄疸记录列表"""
    query = db.query(JaundiceRecord).filter(JaundiceRecord.baby_id == baby_id)
    
    if start_date:
        query = query.filter(JaundiceRecord.record_date >= start_date)
    if end_date:
        query = query.filter(JaundiceRecord.record_date <= end_date)
        
    return query.order_by(desc(JaundiceRecord.record_date))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_latest_jaundice(db: Session, baby_id: int) -> Optional[JaundiceRecord]:
    """获取最新的黄疸记录"""
    return db.query(JaundiceRecord)\
        .filter(JaundiceRecord.baby_id == baby_id)\
        .order_by(desc(JaundiceRecord.record_date))\
        .first()

def update_jaundice_record(
    db: Session, 
    record_id: int, 
    record: JaundiceRecordUpdate
) -> Optional[JaundiceRecord]:
    """更新黄疸记录"""
    db_record = get_jaundice_record(db, record_id)
    if not db_record:
        return None
    
    update_data = record.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_jaundice_record(db: Session, record_id: int) -> bool:
    """删除黄疸记录"""
    db_record = get_jaundice_record(db, record_id)
    if not db_record:
        return False
    
    db.delete(db_record)
    db.commit()
    return True
