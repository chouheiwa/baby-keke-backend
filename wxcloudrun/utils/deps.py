"""
依赖注入函数
用于 FastAPI 路由的依赖项
"""
from typing import Annotated
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.core.config import get_settings
from wxcloudrun.crud import user as user_crud, baby as baby_crud
from wxcloudrun.crud import session as session_crud


def get_current_user_id(
    x_wx_openid: Annotated[str, Header()] = None,
    db: Annotated[Session, Depends(get_db)] = None
) -> int:
    """
    从请求头获取当前用户ID
    微信小程序云托管会自动在请求头中注入 X-Wx-Openid
    """
    if not x_wx_openid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未找到用户身份信息"
        )

    # 根据 openid 查询用户
    user = user_crud.get_user_by_openid(db, x_wx_openid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在，请先登录"
        )

    # 校验登录态是否有效（未登录或过期统一返回 401）
    if not session_crud.is_session_valid(db, x_wx_openid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录态已过期或未登录，请重新登录"
        )

    return user.id


def verify_baby_access(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
) -> None:
    """
    验证用户是否有权限访问该宝宝的数据
    """
    if not baby_crud.is_family_member(db, baby_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有权限访问此宝宝的信息"
        )


def verify_baby_admin(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
) -> None:
    """
    验证用户是否是该宝宝的管理员
    """
    if not baby_crud.is_admin(db, baby_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有管理员权限"
        )


def require_admin_token(x_admin_token: Annotated[str | None, Header(alias="X-Admin-Token")] = None) -> None:
    settings = get_settings()
    if not settings.admin_token or not x_admin_token or x_admin_token != settings.admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="管理员认证失败"
        )
