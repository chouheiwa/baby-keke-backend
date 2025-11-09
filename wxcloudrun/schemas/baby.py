"""
宝宝相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class BabyBase(BaseModel):
    """宝宝基础字段"""
    name: str = Field(..., max_length=50, description="宝宝姓名")
    gender: Literal['male', 'female', 'unknown'] = Field(default='unknown', description="性别")
    birthday: datetime = Field(..., description="出生日期")
    avatar_url: Optional[str] = Field(None, max_length=500, description="宝宝头像")
    notes: Optional[str] = Field(None, description="备注")


class BabyCreate(BabyBase):
    """创建宝宝的请求数据"""
    pass


class BabyUpdate(BaseModel):
    """更新宝宝的请求数据"""
    name: Optional[str] = Field(None, max_length=50, description="宝宝姓名")
    gender: Optional[Literal['male', 'female', 'unknown']] = Field(None, description="性别")
    birthday: Optional[datetime] = Field(None, description="出生日期")
    avatar_url: Optional[str] = Field(None, max_length=500, description="宝宝头像")
    notes: Optional[str] = Field(None, description="备注")


class BabyResponse(BabyBase):
    """宝宝响应数据"""
    id: int = Field(..., description="宝宝ID")
    created_by: int = Field(..., description="创建人ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)


# ==================== 家庭成员关系 ====================

class BabyFamilyBase(BaseModel):
    """家庭成员关系基础字段"""
    relation: Optional[str] = Field(None, max_length=20, description="关系(爸爸/妈妈/爷爷/奶奶等)")
    is_admin: int = Field(default=0, description="是否为管理员(0否1是)")


class BabyFamilyCreate(BabyFamilyBase):
    """添加家庭成员的请求数据"""
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="用户ID")


class BabyFamilyResponse(BabyFamilyBase):
    """家庭成员关系响应数据"""
    id: int = Field(..., description="关系ID")
    baby_id: int = Field(..., description="宝宝ID")
    user_id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")

    model_config = ConfigDict(from_attributes=True)
