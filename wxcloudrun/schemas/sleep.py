"""
睡眠记录相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from .user import CreatorInfo


class SleepRecordBase(BaseModel):
    start_time: datetime = Field(..., description="入睡时间")
    end_time: Optional[datetime] = Field(None, description="醒来时间")
    duration: Optional[int] = Field(None, ge=0, description="睡眠时长(分钟)")
    quality: Optional[Literal['good', 'normal', 'poor']] = Field(None, description="睡眠质量")
    position: Optional[Literal['left', 'middle', 'right']] = Field(None, description="睡眠姿势(左/中/右)")
    wake_count: int = Field(default=0, ge=0, description="夜醒次数")
    notes: Optional[str] = Field(None, description="备注")


class SleepRecordCreate(SleepRecordBase):
    baby_id: int = Field(..., description="宝宝ID")
    source: Optional[Literal['manual', 'auto']] = Field('manual', description="记录来源")
    status: Optional[Literal['in_progress', 'completed', 'auto_closed', 'cancelled']] = Field('completed', description="记录状态")


class SleepRecordUpdate(BaseModel):
    start_time: Optional[datetime] = Field(None, description="入睡时间")
    end_time: Optional[datetime] = Field(None, description="醒来时间")
    duration: Optional[int] = Field(None, ge=0, description="睡眠时长(分钟)")
    quality: Optional[Literal['good', 'normal', 'poor']] = Field(None, description="睡眠质量")
    position: Optional[Literal['left', 'middle', 'right']] = Field(None, description="睡眠姿势(左/中/右)")
    wake_count: Optional[int] = Field(None, ge=0, description="夜醒次数")
    notes: Optional[str] = Field(None, description="备注")
    status: Optional[Literal['in_progress', 'completed', 'auto_closed', 'cancelled']] = Field(None, description="记录状态")
    auto_closed_at: Optional[datetime] = Field(None, description="自动关闭时间")
    source: Optional[Literal['manual', 'auto']] = Field(None, description="记录来源")

class SleepStartCreate(BaseModel):
    baby_id: int = Field(..., description="宝宝ID")
    start_time: datetime = Field(..., description="入睡时间")
    source: Optional[Literal['manual', 'auto']] = Field('manual', description="记录来源")
    position: Optional[Literal['left', 'middle', 'right']] = Field(None, description="睡眠姿势(左/中/右)")

class SleepStopUpdate(BaseModel):
    end_time: datetime = Field(..., description="醒来时间")

class SleepAutoCloseUpdate(BaseModel):
    auto_closed_at: datetime = Field(..., description="自动关闭时间")


class SleepRecordResponse(SleepRecordBase):
    id: int = Field(..., description="记录ID")
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="记录人ID")
    status: Literal['in_progress', 'completed', 'auto_closed', 'cancelled'] = Field(..., description="记录状态")
    auto_closed_at: Optional[datetime] = Field(None, description="自动关闭时间")
    source: Literal['manual', 'auto'] = Field(..., description="记录来源")
    created_by: Optional[CreatorInfo] = Field(None, description="创建者信息")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)
