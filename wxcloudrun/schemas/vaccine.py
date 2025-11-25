from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VaccineBase(BaseModel):
    name: str
    code: str
    dose_seq: int
    type: str # FREE, PAID
    target_age_month: int
    description: Optional[str] = None
    is_active: bool = True

class VaccineCreate(VaccineBase):
    pass

class Vaccine(VaccineBase):
    id: int

    class Config:
        orm_mode = True

class VaccinationRecordBase(BaseModel):
    status: str # PENDING, COMPLETED, SKIPPED
    vaccination_date: Optional[datetime] = None
    location: Optional[str] = None
    batch_number: Optional[str] = None
    notes: Optional[str] = None
    photos: Optional[str] = None

class VaccinationRecordCreate(VaccinationRecordBase):
    pass

class VaccinationRecord(VaccinationRecordBase):
    id: int
    baby_id: int
    vaccine_id: int
    vaccine: Optional[Vaccine] = None

    class Config:
        orm_mode = True

class VaccineWithStatus(Vaccine):
    """
    带有接种状态的疫苗信息（用于前端展示）
    """
    status: str = 'PENDING' # PENDING, COMPLETED, SKIPPED, OVERDUE
    record: Optional[VaccinationRecord] = None
    due_date: Optional[str] = None # 预计接种日期
