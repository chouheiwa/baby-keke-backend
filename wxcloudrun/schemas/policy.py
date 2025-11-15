from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PolicyCreate(BaseModel):
    version: str = Field(..., max_length=32, description="版本号")
    title: Optional[str] = Field(None, max_length=200, description="标题")
    content: str = Field(..., description="政策内容")
    format: Optional[str] = Field("markdown", description="内容格式: markdown/html/text")
    locale: Optional[str] = Field("zh-CN", max_length=16, description="语言/地区")


class PolicyUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200, description="标题")
    content: Optional[str] = Field(None, description="政策内容")
    format: Optional[str] = Field(None, description="内容格式: markdown/html/text")


class PolicyPublishRequest(BaseModel):
    effective_at: Optional[datetime] = Field(None, description="生效时间，不传则为当前时间")


class PolicyResponse(BaseModel):
    id: int
    type: str
    version: str
    title: Optional[str]
    content: str
    format: str
    locale: str
    status: str
    effective_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    content_html: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)