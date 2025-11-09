"""
睡眠记录相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class SleepRecordBase(BaseModel):
    """睡眠记录基础字段"""
    sleep_type: Literal['night', 'nap'] = Field(..., description="睡眠类型(night夜间/nap小睡)")
    start_time: datetime = Field(..., description="入睡时间")
    end_time: Optional[datetime] = Field(None, description="醒来时间")
    duration: Optional[int] = Field(None, ge=0, description="睡眠时长(分钟)")
    quality: Optional[Literal['good', 'normal', 'poor']] = Field(None, description="睡眠质量")
    wake_count: int = Field(default=0, ge=0, description="夜醒次数")
    notes: Optional[str] = Field(None, description="备注")


class SleepRecordCreate(SleepRecordBase):
    """创建睡眠记录的请求数据"""
    baby_id: int = Field(..., description="宝宝ID")


class SleepRecordUpdate(BaseModel):
    """更新睡眠记录的请求数据"""
    sleep_type: Optional[Literal['night', 'nap']] = Field(None, description="睡眠类型")
    start_time: Optional[datetime] = Field(None, description="入睡时间")
    end_time: Optional[datetime] = Field(None, description="醒来时间")
    duration: Optional[int] = Field(None, ge=0, description="睡眠时长(分钟)")
    quality: Optional[Literal['good', 'normal', 'poor']] = Field(None, description="睡眠质量")
    wake_count: Optional[int] = Field(None, ge=0, description="夜醒次数")
    notes: Optional[str] = Field(None, description="备注")


class SleepRecordResponse(SleepRecordBase):
    """睡眠记录响应数据"""
    id: int = Field(..., description="记录ID")
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="记录人ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)
