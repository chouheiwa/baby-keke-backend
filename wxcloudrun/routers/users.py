"""
用户相关的 API 路由
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from wxcloudrun.crud import user as user_crud
from wxcloudrun.utils.deps import get_current_user_id

router = APIRouter(
    prefix="/api/users",
    tags=["用户管理"]
)


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login(
    user_data: UserLogin,
    db: Annotated[Session, Depends(get_db)]
):
    """
    小程序快捷登录接口
    - 如果用户已存在，直接返回用户信息
    - 如果用户不存在，自动创建新用户
    """
    # 检查用户是否已存在
    db_user = user_crud.get_user_by_openid(db, user_data.openid)

    if db_user:
        # 用户已存在，直接返回
        return db_user

    # 用户不存在，自动创建新用户
    new_user = UserCreate(
        openid=user_data.openid,
        nickname=user_data.nickname,
        avatar_url=user_data.avatar_url
    )

    return user_crud.create_user(db, new_user)


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
