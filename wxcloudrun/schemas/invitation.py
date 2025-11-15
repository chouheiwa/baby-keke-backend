from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class InviteCodeResponse(BaseModel):
    code: str = Field(...)
    baby_id: int = Field(...)
    expire_at: datetime = Field(...)
    status: str = Field(...)

    model_config = ConfigDict(from_attributes=True)