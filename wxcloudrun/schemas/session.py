"""
会话相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class LoginRequest(BaseModel):
    """登录请求数据"""
    code: str = Field(..., min_length=1, description="微信登录凭证 code")


class LoginResponse(BaseModel):
    """登录响应数据"""
    user_id: int = Field(..., description="用户ID")
    openid: str = Field(..., description="微信OpenID")
    nickname: Optional[str] = Field(None, description="用户昵称")
    phone: Optional[str] = Field(None, description="手机号")
    unionid: Optional[str] = Field(None, description="微信UnionID")
    session_expires_at: datetime = Field(..., description="会话过期时间")
    is_new_user: bool = Field(..., description="是否为新用户")


class CheckSessionRequest(BaseModel):
    """检验登录态请求数据"""
    openid: str = Field(..., description="微信OpenID")


class CheckSessionResponse(BaseModel):
    """检验登录态响应数据"""
    valid: bool = Field(..., description="会话是否有效")
    expires_at: Optional[datetime] = Field(None, description="过期时间")


class ResetSessionRequest(BaseModel):
    """重置登录态请求数据"""
    openid: str = Field(..., description="微信OpenID")


class ResetSessionResponse(BaseModel):
    """重置登录态响应数据"""
    openid: str = Field(..., description="微信OpenID")
    expires_at: datetime = Field(..., description="新的过期时间")


class SessionInfo(BaseModel):
    """会话信息"""
    id: int = Field(..., description="会话ID")
    user_id: int = Field(..., description="用户ID")
    openid: str = Field(..., description="微信OpenID")
    unionid: Optional[str] = Field(None, description="微信UnionID")
    expires_at: datetime = Field(..., description="过期时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    model_config = ConfigDict(from_attributes=True)

