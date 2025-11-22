"""
喂养记录相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional, Literal, List
from pydantic import BaseModel, Field, ConfigDict, model_validator
from .user import CreatorInfo


class FeedingSequenceItem(BaseModel):
    """喂养序列项（用于记录母乳交替喂养）"""
    side: Literal['left', 'right'] = Field(..., description="喂养侧别")
    duration_seconds: int = Field(..., ge=0, description="持续时长（秒）")
    start_time: datetime = Field(..., description="开始时间")

    model_config = ConfigDict(from_attributes=True)


class FeedingRecordBase(BaseModel):
    """喂养记录基础字段"""
    feeding_type: Literal['breast', 'formula', 'solid'] = Field(..., description="喂养类型(breast母乳/formula奶粉/solid辅食)")

    # 母乳喂养字段（支持两种模式）
    feeding_sequence: Optional[List[FeedingSequenceItem]] = Field(None, description="喂养序列(母乳交替记录) - 详细模式")
    breast_side: Optional[Literal['left', 'right', 'both', 'unknown']] = Field(None, description="哺乳侧 - 快速模式(用于快速补记)")
    duration_left: Optional[int] = Field(None, ge=0, description="左侧时长(秒)")
    duration_right: Optional[int] = Field(None, ge=0, description="右侧时长(秒)")

    # 奶粉/辅食字段
    amount: Optional[int] = Field(None, ge=0, description="奶量(ml)或食量(g)")
    bottle_content: Optional[Literal['breast', 'formula']] = Field(None, description="奶瓶内容（breast母乳/formula奶粉）")

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
            # 母乳喂养支持两种模式：
            # 1. 详细模式：提供 feeding_sequence
            # 2. 快速模式：不提供 feeding_sequence（用于快速补记，breast_side 可选）
            has_sequence = self.feeding_sequence and len(self.feeding_sequence) > 0
            # 只要有 start_time 即可（快速模式），或者有详细的 feeding_sequence
            if not has_sequence and not self.start_time:
                raise ValueError("母乳喂养必须提供开始时间或喂养序列")
        elif self.feeding_type == 'formula':
            if not self.amount:
                raise ValueError("奶粉喂养必须指定奶量")
            if not self.bottle_content:
                raise ValueError("奶瓶喂养必须指定奶瓶内容（母乳/奶粉）")
        elif self.feeding_type == 'solid':
            if not self.food_name:
                raise ValueError("辅食必须指定食物名称")
        return self


class FeedingRecordUpdate(BaseModel):
    """更新喂养记录的请求数据"""
    feeding_type: Optional[Literal['breast', 'formula', 'solid']] = Field(None, description="喂养类型")
    feeding_sequence: Optional[List[FeedingSequenceItem]] = Field(None, description="喂养序列(母乳交替记录)")
    breast_side: Optional[Literal['left', 'right', 'both', 'unknown']] = Field(None, description="哺乳侧(快速模式)")
    duration_left: Optional[int] = Field(None, ge=0, description="左侧时长(秒)")
    duration_right: Optional[int] = Field(None, ge=0, description="右侧时长(秒)")
    amount: Optional[int] = Field(None, ge=0, description="奶量(ml)或食量(g)")
    bottle_content: Optional[Literal['breast', 'formula']] = Field(None, description="奶瓶内容（母乳/奶粉）")
    food_name: Optional[str] = Field(None, max_length=100, description="食物名称")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    notes: Optional[str] = Field(None, description="备注")


class FeedingRecordResponse(FeedingRecordBase):
    """喂养记录响应数据"""
    id: int = Field(..., description="记录ID")
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="记录人ID")
    created_by: Optional[CreatorInfo] = Field(None, description="创建者信息")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)
