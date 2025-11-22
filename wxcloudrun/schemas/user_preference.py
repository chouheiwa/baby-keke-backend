"""用户偏好设置的 Pydantic 模型"""
from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime


class UserPreferenceBase(BaseModel):
    """用户偏好设置基础模型"""
    preference_key: str = Field(..., max_length=100, description="偏好设置键")
    preference_value: Any = Field(..., description="偏好设置值")


class UserPreferenceCreate(UserPreferenceBase):
    """创建用户偏好设置"""
    pass


class UserPreferenceUpdate(BaseModel):
    """更新用户偏好设置"""
    preference_value: Any = Field(..., description="偏好设置值")


class UserPreferenceResponse(UserPreferenceBase):
    """用户偏好设置响应模型"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPreferencesResponse(BaseModel):
    """用户所有偏好设置响应"""
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="偏好设置字典，key为preference_key，value为preference_value"
    )
