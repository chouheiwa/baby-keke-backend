from sqlalchemy.orm import Session
from sqlalchemy import desc
from wxcloudrun.models.vaccine import Vaccine, VaccinationRecord
from typing import List, Optional
from datetime import datetime

# === 疫苗基础信息 ===

def get_vaccines(db: Session, active_only: bool = True) -> List[Vaccine]:
    """获取所有疫苗列表"""
    query = db.query(Vaccine)
    if active_only:
        query = query.filter(Vaccine.is_active == True)
    return query.order_by(Vaccine.target_age_month, Vaccine.dose_seq).all()

def get_vaccine(db: Session, vaccine_id: int) -> Optional[Vaccine]:
    """获取单个疫苗信息"""
    return db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()

def create_vaccine(db: Session, vaccine_data: dict) -> Vaccine:
    """创建疫苗"""
    db_vaccine = Vaccine(**vaccine_data)
    db.add(db_vaccine)
    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine

def init_vaccines(db: Session, vaccines_data: List[dict]):
    """初始化疫苗数据（如果不存在则创建）"""
    for data in vaccines_data:
        existing = db.query(Vaccine).filter(
            Vaccine.code == data['code'],
            Vaccine.dose_seq == data['dose_seq']
        ).first()
        
        if not existing:
            create_vaccine(db, data)

# === 接种记录 ===

def get_baby_vaccination_records(db: Session, baby_id: int) -> List[VaccinationRecord]:
    """获取宝宝的所有接种记录"""
    return db.query(VaccinationRecord).filter(
        VaccinationRecord.baby_id == baby_id
    ).all()

def get_vaccination_record(db: Session, baby_id: int, vaccine_id: int) -> Optional[VaccinationRecord]:
    """获取单条接种记录"""
    return db.query(VaccinationRecord).filter(
        VaccinationRecord.baby_id == baby_id,
        VaccinationRecord.vaccine_id == vaccine_id
    ).first()

def create_or_update_record(db: Session, baby_id: int, vaccine_id: int, status: str, 
                          vaccination_date: Optional[datetime] = None,
                          location: Optional[str] = None,
                          batch_number: Optional[str] = None,
                          notes: Optional[str] = None,
                          photos: Optional[str] = None) -> VaccinationRecord:
    """创建或更新接种记录"""
    record = get_vaccination_record(db, baby_id, vaccine_id)
    
    if record:
        # 更新
        record.status = status
        record.vaccination_date = vaccination_date
        if location is not None: record.location = location
        if batch_number is not None: record.batch_number = batch_number
        if notes is not None: record.notes = notes
        if photos is not None: record.photos = photos
    else:
        # 创建
        record = VaccinationRecord(
            baby_id=baby_id,
            vaccine_id=vaccine_id,
            status=status,
            vaccination_date=vaccination_date,
            location=location,
            batch_number=batch_number,
            notes=notes,
            photos=photos
        )
        db.add(record)
    
    db.commit()
    db.refresh(record)
    return record

def delete_record(db: Session, baby_id: int, vaccine_id: int):
    """删除接种记录（重置为未接种）"""
    record = get_vaccination_record(db, baby_id, vaccine_id)
    if record:
        db.delete(record)
        db.commit()
