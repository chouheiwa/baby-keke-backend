"""
用户相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    """用户基础字段"""
    nickname: Optional[str] = Field(None, max_length=100, description="用户昵称")
    avatar_url: Optional[str] = Field(None, max_length=500, description="头像URL")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserCreate(BaseModel):
    """创建用户的请求数据"""
    openid: str = Field(..., max_length=64, description="微信OpenID")
    nickname: Optional[str] = Field(None, max_length=100, description="用户昵称")
    avatar_url: Optional[str] = Field(None, max_length=500, description="头像URL")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserUpdate(BaseModel):
    """更新用户的请求数据"""
    nickname: Optional[str] = Field(None, max_length=100, description="用户昵称")
    avatar_url: Optional[str] = Field(None, max_length=500, description="头像URL")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserLogin(BaseModel):
    """用户登录请求数据"""
    openid: str = Field(..., max_length=64, description="微信OpenID")
    nickname: Optional[str] = Field(None, max_length=100, description="用户昵称（首次登录时可选）")
    avatar_url: Optional[str] = Field(None, max_length=500, description="头像URL（首次登录时可选）")


class UserResponse(UserBase):
    """用户响应数据"""
    id: int = Field(..., description="用户ID")
    openid: str = Field(..., description="微信OpenID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    model_config = ConfigDict(from_attributes=True)
