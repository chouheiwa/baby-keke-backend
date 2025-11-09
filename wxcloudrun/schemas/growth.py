"""
生长发育记录相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class GrowthRecordBase(BaseModel):
    """生长发育记录基础字段"""
    record_date: datetime = Field(..., description="记录日期")
    weight: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="体重(kg)")
    height: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="身高/身长(cm)")
    head_circumference: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="头围(cm)")
    notes: Optional[str] = Field(None, description="备注")


class GrowthRecordCreate(GrowthRecordBase):
    """创建生长发育记录的请求数据"""
    baby_id: int = Field(..., description="宝宝ID")


class GrowthRecordUpdate(BaseModel):
    """更新生长发育记录的请求数据"""
    record_date: Optional[datetime] = Field(None, description="记录日期")
    weight: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="体重(kg)")
    height: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="身高/身长(cm)")
    head_circumference: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description="头围(cm)")
    notes: Optional[str] = Field(None, description="备注")


class GrowthRecordResponse(GrowthRecordBase):
    """生长发育记录响应数据"""
    id: int = Field(..., description="记录ID")
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="记录人ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)
