from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class InviteCodeResponse(BaseModel):
    code: str = Field(...)
    baby_id: int = Field(...)
    expire_at: datetime = Field(...)
    status: str = Field(...)

    model_config = ConfigDict(from_attributes=True)


class AcceptInvitationRequest(BaseModel):
    code: str = Field(..., description="邀请码")
    relation: str | None = Field(None, max_length=20, description="关系代码或中文，如 mom/爸爸")
    relation_display: str | None = Field(None, max_length=50, description="角色显示名称，如 妈妈/爸爸")