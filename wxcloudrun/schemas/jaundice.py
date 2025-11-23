from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class JaundiceRecordBase(BaseModel):
    """黄疸记录基础字段"""
    record_date: datetime = Field(..., description="记录日期")
    value: Decimal = Field(..., ge=0, decimal_places=2, description="黄疸值(mg/dL)")
    photo_url: Optional[str] = Field(None, description="照片URL")
    notes: Optional[str] = Field(None, description="备注")


class JaundiceRecordCreate(JaundiceRecordBase):
    """创建黄疸记录的请求数据"""
    baby_id: int = Field(..., description="宝宝ID")


class JaundiceRecordUpdate(BaseModel):
    """更新黄疸记录的请求数据"""
    record_date: Optional[datetime] = Field(None, description="记录日期")
    value: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="黄疸值(mg/dL)")
    photo_url: Optional[str] = Field(None, description="照片URL")
    notes: Optional[str] = Field(None, description="备注")


from wxcloudrun.schemas.user import UserResponse

class JaundiceRecordResponse(JaundiceRecordBase):
    """黄疸记录响应数据"""
    id: int = Field(..., description="记录ID")
    baby_id: int = Field(..., description="宝宝ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    created_by: Optional[UserResponse] = Field(None, description="创建人")

    model_config = ConfigDict(from_attributes=True)
