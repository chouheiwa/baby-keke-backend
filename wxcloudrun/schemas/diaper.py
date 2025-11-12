"""
排便/排尿记录相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from .user import CreatorInfo


class DiaperRecordBase(BaseModel):
    """排便/排尿记录基础字段"""
    diaper_type: Literal['pee', 'poop', 'both'] = Field(..., description="类型(pee尿/poop便/both两者都有)")

    # 大便相关字段
    poop_amount: Optional[Literal['少量', '适中', '大量']] = Field(None, description="大便量")
    poop_color: Optional[str] = Field(None, max_length=20, description="大便颜色(黄色/绿色/褐色等)")
    poop_texture: Optional[Literal['稀', '正常', '干燥']] = Field(None, description="大便性状")

    record_time: datetime = Field(..., description="记录时间")
    notes: Optional[str] = Field(None, description="备注")


class DiaperRecordCreate(DiaperRecordBase):
    """创建排便/排尿记录的请求数据"""
    baby_id: int = Field(..., description="宝宝ID")


class DiaperRecordUpdate(BaseModel):
    """更新排便/排尿记录的请求数据"""
    diaper_type: Optional[Literal['pee', 'poop', 'both']] = Field(None, description="类型")
    poop_amount: Optional[Literal['少量', '适中', '大量']] = Field(None, description="大便量")
    poop_color: Optional[str] = Field(None, max_length=20, description="大便颜色")
    poop_texture: Optional[Literal['稀', '正常', '干燥']] = Field(None, description="大便性状")
    record_time: Optional[datetime] = Field(None, description="记录时间")
    notes: Optional[str] = Field(None, description="备注")


class DiaperRecordResponse(DiaperRecordBase):
    """排便/排尿记录响应数据"""
    id: int = Field(..., description="记录ID")
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="记录人ID")
    created_by: Optional[CreatorInfo] = Field(None, description="创建者信息")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)
