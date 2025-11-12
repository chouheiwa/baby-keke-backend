"""
用户相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    """用户基础字段"""
    nickname: Optional[str] = Field(None, max_length=100, description="用户昵称")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserCreate(BaseModel):
    """创建用户的请求数据"""
    openid: str = Field(..., max_length=64, description="微信OpenID")
    nickname: Optional[str] = Field(None, max_length=100, description="用户昵称")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserUpdate(BaseModel):
    """更新用户的请求数据"""
    nickname: Optional[str] = Field(None, max_length=100, description="用户昵称")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserResponse(UserBase):
    """用户响应数据"""
    id: int = Field(..., description="用户ID")
    openid: str = Field(..., description="微信OpenID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)


class CreatorInfo(BaseModel):
    """创建者信息（用于记录列表）"""
    user_id: int = Field(..., description="用户ID")
    nickname: Optional[str] = Field(None, description="用户昵称")
    relation: Optional[str] = Field(None, description="与宝宝的关系")
    relation_display: Optional[str] = Field(None, description="关系显示名称")

    model_config = ConfigDict(from_attributes=True)
