"""
通知相关的 API 路由
"""
from typing import Annotated, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.utils.deps import get_current_user_id
from wxcloudrun.utils.wechat import get_wechat_api
from wxcloudrun.crud import user as users_crud
import logging

router = APIRouter(
    prefix="/api/notifications",
    tags=["通知服务"]
)

logger = logging.getLogger(__name__)

@router.post("/subscribe/send", status_code=status.HTTP_200_OK)
async def send_subscribe_message(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    payload: Dict[str, Any] = Body(...)
):
    """
    发送订阅消息
    
    Payload:
    {
        "template_id": "模板ID",
        "page": "跳转页面",
        "data": { ... } // 模板数据
    }
    """
    template_id = payload.get("template_id")
    page = payload.get("page", "pages/index/index")
    data = payload.get("data")
    
    if not template_id or not data:
        raise HTTPException(status_code=400, detail="缺少必要参数")
        
    # 获取用户 OpenID
    user = users_crud.get_user(db, user_id)
    if not user or not user.openid:
        raise HTTPException(status_code=404, detail="用户未找到或无OpenID")
        
    wx_api = get_wechat_api()
    
    # 发送消息
    success = await wx_api.send_subscribe_message(
        openid=user.openid,
        template_id=template_id,
        page=page,
        data=data,
        miniprogram_state="formal" # 正式环境使用 formal，开发测试可用 developer/trial
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="发送订阅消息失败")
        
    return {"status": "success"}
