"""
正在进行的喂养记录相关的 Pydantic Schema
"""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

class FeedingOngoingBase(BaseModel):
    """基础字段"""
    current_side: Literal['left', 'right', 'paused'] = Field(..., description="当前状态")
    accumulated_left: int = Field(0, ge=0, description="左侧累计时长(秒)")
    accumulated_right: int = Field(0, ge=0, description="右侧累计时长(秒)")

class FeedingOngoingCreate(BaseModel):
    """创建/更新请求"""
    baby_id: int = Field(..., description="宝宝ID")
    action: Literal['start_left', 'start_right', 'pause'] = Field(..., description="操作类型")

class FeedingOngoingResponse(BaseModel):
    """响应数据"""
    id: int
    baby_id: int
    start_time: datetime
    current_side: Literal['left', 'right', 'paused']
    last_action_time: datetime
    accumulated_left: int
    accumulated_right: int
    updated_at: datetime
    
    # 计算属性：服务器当前时间（用于客户端校准）
    server_time: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
