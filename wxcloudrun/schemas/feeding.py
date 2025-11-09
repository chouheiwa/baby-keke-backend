"""
喂养记录相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict, model_validator


class FeedingRecordBase(BaseModel):
    """喂养记录基础字段"""
    feeding_type: Literal['breast', 'formula', 'solid'] = Field(..., description="喂养类型(breast母乳/formula奶粉/solid辅食)")

    # 母乳喂养字段
    breast_side: Optional[Literal['left', 'right', 'both']] = Field(None, description="哺乳侧")
    duration_left: Optional[int] = Field(None, ge=0, description="左侧时长(分钟)")
    duration_right: Optional[int] = Field(None, ge=0, description="右侧时长(分钟)")

    # 奶粉/辅食字段
    amount: Optional[int] = Field(None, ge=0, description="奶量(ml)或食量(g)")

    # 辅食字段
    food_name: Optional[str] = Field(None, max_length=100, description="食物名称")

    # 通用字段
    start_time: datetime = Field(..., description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    notes: Optional[str] = Field(None, description="备注")


class FeedingRecordCreate(FeedingRecordBase):
    """创建喂养记录的请求数据"""
    baby_id: int = Field(..., description="宝宝ID")

    @model_validator(mode='after')
    def validate_fields(self):
        """根据喂养类型验证必填字段"""
        if self.feeding_type == 'breast':
            if not self.breast_side:
                raise ValueError("母乳喂养必须指定哺乳侧")
        elif self.feeding_type == 'formula':
            if not self.amount:
                raise ValueError("奶粉喂养必须指定奶量")
        elif self.feeding_type == 'solid':
            if not self.food_name:
                raise ValueError("辅食必须指定食物名称")
        return self


class FeedingRecordUpdate(BaseModel):
    """更新喂养记录的请求数据"""
    feeding_type: Optional[Literal['breast', 'formula', 'solid']] = Field(None, description="喂养类型")
    breast_side: Optional[Literal['left', 'right', 'both']] = Field(None, description="哺乳侧")
    duration_left: Optional[int] = Field(None, ge=0, description="左侧时长(分钟)")
    duration_right: Optional[int] = Field(None, ge=0, description="右侧时长(分钟)")
    amount: Optional[int] = Field(None, ge=0, description="奶量(ml)或食量(g)")
    food_name: Optional[str] = Field(None, max_length=100, description="食物名称")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    notes: Optional[str] = Field(None, description="备注")


class FeedingRecordResponse(FeedingRecordBase):
    """喂养记录响应数据"""
    id: int = Field(..., description="记录ID")
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="记录人ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)
