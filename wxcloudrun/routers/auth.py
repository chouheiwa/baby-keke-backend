"""
认证和会话管理相关的 API 路由
"""
from typing import Annotated
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.session import (
    CheckSessionRequest,
    CheckSessionResponse,
    ResetSessionRequest,
    ResetSessionResponse
)
from wxcloudrun.crud import session as session_crud
from wxcloudrun.utils.wechat import get_wechat_api, WeChatAPIError

router = APIRouter(
    prefix="/api/auth",
    tags=["认证管理"]
)

logger = logging.getLogger(__name__)


@router.post("/check-session", response_model=CheckSessionResponse, status_code=status.HTTP_200_OK)
async def check_session(
    request_data: CheckSessionRequest,
    db: Annotated[Session, Depends(get_db)]
):
    """
    检验登录态
    
    检查用户的会话是否有效（未过期）
    """
    try:
        logger.info(f"/api/auth/check-session: openid={request_data.openid}")
        # 获取会话记录
        db_session = session_crud.get_session_by_openid(db, request_data.openid)
        
        if not db_session:
            logger.info("/api/auth/check-session: session not found")
            return CheckSessionResponse(
                valid=False,
                expires_at=None
            )
        
        # 检查是否过期
        is_valid = session_crud.is_session_valid(db, request_data.openid)
        logger.info(f"/api/auth/check-session: valid={is_valid} expires_at={db_session.expires_at}")
        
        return CheckSessionResponse(
            valid=is_valid,
            expires_at=db_session.expires_at if is_valid else None
        )
        
    except Exception as e:
        logger.exception("/api/auth/check-session: unexpected error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"检验登录态失败: {str(e)}"
        )


@router.post("/reset-session", response_model=ResetSessionResponse, status_code=status.HTTP_200_OK)
async def reset_session(
    request_data: ResetSessionRequest,
    db: Annotated[Session, Depends(get_db)]
):
    """
    重置登录态
    
    调用微信接口重置 session_key，并更新数据库记录
    
    注意：根据微信文档，重置登录态需要当前的 session_key 进行签名验证
    实际使用时，建议让用户重新登录以获得新的 session_key
    """
    try:
        logger.info(f"/api/auth/reset-session: openid={request_data.openid}")
        # 获取当前会话
        db_session = session_crud.get_session_by_openid(db, request_data.openid)
        
        if not db_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="会话不存在"
            )
        
        # 调用微信 API 重置 session_key
        wechat_api = get_wechat_api()
        logger.info("/api/auth/reset-session: calling reset_session_key")
        wx_result = await wechat_api.reset_session_key(
            openid=request_data.openid,
            session_key=db_session.session_key
        )
        
        new_session_key = wx_result.get("session_key")
        
        if not new_session_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="重置登录态失败"
            )
        
        # 更新数据库中的 session_key
        updated_session = session_crud.update_session_key(
            db=db,
            openid=request_data.openid,
            new_session_key=new_session_key,
            expires_days=30
        )
        
        if not updated_session:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="更新会话失败"
            )
        
        logger.info(f"/api/auth/reset-session: success openid={updated_session.openid} expires_at={updated_session.expires_at}")
        return ResetSessionResponse(
            openid=updated_session.openid,
            expires_at=updated_session.expires_at
        )
        
    except WeChatAPIError as e:
        logger.error(f"/api/auth/reset-session: WeChatAPIError errcode={e.errcode} errmsg={e.errmsg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"微信API错误: {e.errmsg}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("/api/auth/reset-session: unexpected error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"重置登录态失败: {str(e)}"
        )
