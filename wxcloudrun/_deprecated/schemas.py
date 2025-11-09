"""
Pydantic数据模型定义
用于API请求和响应的数据验证和序列化
"""
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


# 通用响应模型
class ResponseModel(BaseModel):
    """统一响应格式"""
    code: int = 0
    data: Optional[Any] = None
    error_msg: Optional[str] = None


# 计数器相关模型
class CounterRequest(BaseModel):
    """计数器操作请求"""
    action: str  # inc 或 clear


class CounterResponse(BaseModel):
    """计数器响应"""
    id: int
    count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2语法，允许从ORM对象创建
