"""
用户相关的 API 路由
"""
from typing import Annotated
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.user import UserCreate, UserUpdate, UserResponse
from wxcloudrun.schemas.session import LoginRequest, LoginResponse
from wxcloudrun.crud import user as user_crud
from wxcloudrun.crud import session as session_crud
from wxcloudrun.utils.deps import get_current_user_id
from wxcloudrun.utils.wechat import get_wechat_api, WeChatAPIError

router = APIRouter(
    prefix="/api/users",
    tags=["用户管理"]
)

logger = logging.getLogger(__name__)


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest,
    db: Annotated[Session, Depends(get_db)]
):
    """
    小程序登录接口
    
    流程：
    1. 接收小程序的 code
    2. 调用微信 code2Session 接口获取 openid 和 session_key
    3. 查询或创建用户
    4. 创建或更新会话记录
    5. 返回用户信息和会话信息
    """
    try:
        logger.info("/api/users/login: received code")
        # 1. 调用微信 API 获取 openid 和 session_key
        wechat_api = get_wechat_api()
        logger.info("/api/users/login: calling code2session")
        wx_result = await wechat_api.code2session(login_data.code)
        logger.info("/api/users/login: code2session returned")
        
        openid = wx_result.get("openid")
        session_key = wx_result.get("session_key")
        unionid = wx_result.get("unionid")
        
        logger.info(f"/api/users/login: openid={openid}, unionid={unionid}, session_key_received={'yes' if session_key else 'no'}")
        if not openid or not session_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="获取微信用户信息失败"
            )
        
        # 2. 查询或创建用户
        db_user = user_crud.get_user_by_openid(db, openid)
        is_new_user = False
        
        if not db_user:
            # 用户不存在，创建新用户
            new_user = UserCreate(
                openid=openid,
                nickname=None  # 昵称由用户后续填写
            )
            db_user = user_crud.create_user(db, new_user)
            is_new_user = True
            logger.info(f"/api/users/login: created new user id={db_user.id} openid={openid}")
        else:
            logger.info(f"/api/users/login: existing user id={db_user.id} openid={openid}")
        
        # 3. 创建或更新会话记录
        db_session = session_crud.create_or_update_session(
            db=db,
            user_id=db_user.id,
            openid=openid,
            session_key=session_key,
            unionid=unionid,
            expires_days=30
        )
        logger.info(f"/api/users/login: session updated openid={openid} expires_at={db_session.expires_at}")
        
        # 4. 返回登录响应
        response = LoginResponse(
            user_id=db_user.id,
            openid=db_user.openid,
            nickname=db_user.nickname,
            phone=db_user.phone,
            unionid=unionid,
            session_expires_at=db_session.expires_at,
            is_new_user=is_new_user
        )
        logger.info(f"/api/users/login: success user_id={db_user.id} openid={openid} is_new_user={is_new_user}")
        return response
        
    except WeChatAPIError as e:
        logger.error(f"/api/users/login: WeChatAPIError errcode={e.errcode} errmsg={e.errmsg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"微信登录失败: {e.errmsg}"
        )
    except Exception as e:
        logger.exception("/api/users/login: unexpected error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}"
        )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)]
):
    """创建新用户（微信登录）"""
    # 检查用户是否已存在
    db_user = user_crud.get_user_by_openid(db, user.openid)
    if db_user:
        return db_user

    return user_crud.create_user(db, user)


@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取当前登录用户信息"""
    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    """根据ID获取用户信息"""
    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return db_user


@router.patch("/me", response_model=UserResponse)
def update_current_user(
    user: UserUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新当前用户信息"""
    db_user = user_crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return db_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除当前用户"""
    success = user_crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return None
