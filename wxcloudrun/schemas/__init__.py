"""
Pydantic 数据模式模块
用于 API 请求和响应的数据验证
"""
from .user import UserCreate, UserUpdate, UserResponse, CreatorInfo
from .session import (
    LoginRequest,
    LoginResponse,
    CheckSessionRequest,
    CheckSessionResponse,
    ResetSessionRequest,
    ResetSessionResponse,
    SessionInfo
)
from .baby import BabyCreate, BabyUpdate, BabyResponse, BabyFamilyCreate, BabyFamilyResponse
from .feeding import FeedingRecordCreate, FeedingRecordUpdate, FeedingRecordResponse
from .diaper import DiaperRecordCreate, DiaperRecordUpdate, DiaperRecordResponse
from .sleep import SleepRecordCreate, SleepRecordUpdate, SleepRecordResponse
from .growth import GrowthRecordCreate, GrowthRecordUpdate, GrowthRecordResponse

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "CreatorInfo",
    # Session schemas
    "LoginRequest",
    "LoginResponse",
    "CheckSessionRequest",
    "CheckSessionResponse",
    "ResetSessionRequest",
    "ResetSessionResponse",
    "SessionInfo",
    # Baby schemas
    "BabyCreate",
    "BabyUpdate",
    "BabyResponse",
    "BabyFamilyCreate",
    "BabyFamilyResponse",
    # Feeding schemas
    "FeedingRecordCreate",
    "FeedingRecordUpdate",
    "FeedingRecordResponse",
    # Diaper schemas
    "DiaperRecordCreate",
    "DiaperRecordUpdate",
    "DiaperRecordResponse",
    # Sleep schemas
    "SleepRecordCreate",
    "SleepRecordUpdate",
    "SleepRecordResponse",
    # Growth schemas
    "GrowthRecordCreate",
    "GrowthRecordUpdate",
    "GrowthRecordResponse",
]
