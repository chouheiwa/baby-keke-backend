"""
吸奶记录相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator
from .user import CreatorInfo


class PumpingRecordBase(BaseModel):
    """吸奶记录基础字段"""
    left_amount: Optional[int] = Field(None, ge=0, description="左侧吸奶量(ml)")
    right_amount: Optional[int] = Field(None, ge=0, description="右侧吸奶量(ml)")
    total_amount: int = Field(..., ge=0, description="总吸奶量(ml)")
    record_time: datetime = Field(..., description="记录时间")
    notes: Optional[str] = Field(None, description="备注")


class PumpingRecordCreate(PumpingRecordBase):
    """创建吸奶记录的请求数据"""
    baby_id: int = Field(..., description="宝宝ID")

    @model_validator(mode='after')
    def validate_amounts(self):
        """验证吸奶量逻辑"""
        # 如果提供了左右侧的量，验证总量是否等于两侧之和
        if self.left_amount is not None or self.right_amount is not None:
            left = self.left_amount or 0
            right = self.right_amount or 0
            calculated_total = left + right

            # 允许用户同时提供总量和分侧量，但必须一致
            if self.total_amount != calculated_total:
                raise ValueError(
                    f"总量({self.total_amount}ml)必须等于左右侧之和({calculated_total}ml)"
                )

        # 如果只提供总量，至少需要一个值
        if self.total_amount == 0:
            raise ValueError("吸奶量必须大于0")

        return self


class PumpingRecordUpdate(BaseModel):
    """更新吸奶记录的请求数据"""
    left_amount: Optional[int] = Field(None, ge=0, description="左侧吸奶量(ml)")
    right_amount: Optional[int] = Field(None, ge=0, description="右侧吸奶量(ml)")
    total_amount: Optional[int] = Field(None, ge=0, description="总吸奶量(ml)")
    record_time: Optional[datetime] = Field(None, description="记录时间")
    notes: Optional[str] = Field(None, description="备注")

    @model_validator(mode='after')
    def validate_amounts(self):
        """验证更新时的吸奶量逻辑"""
        # 只有在提供了相关字段时才进行验证
        if self.total_amount is not None and (self.left_amount is not None or self.right_amount is not None):
            left = self.left_amount or 0
            right = self.right_amount or 0
            calculated_total = left + right

            if self.total_amount != calculated_total:
                raise ValueError(
                    f"总量({self.total_amount}ml)必须等于左右侧之和({calculated_total}ml)"
                )

        return self


class PumpingRecordResponse(PumpingRecordBase):
    """吸奶记录响应数据"""
    id: int = Field(..., description="记录ID")
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="记录人ID")
    created_by: Optional[CreatorInfo] = Field(None, description="创建者信息")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)
