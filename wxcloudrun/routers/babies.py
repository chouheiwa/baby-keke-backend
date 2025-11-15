"""
宝宝管理相关的 API 路由
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.baby import (
    BabyCreate, BabyUpdate, BabyResponse,
    BabyFamilyCreate, BabyFamilyResponse
)
from wxcloudrun.schemas.invitation import InviteCodeResponse
from wxcloudrun.crud import invitation as invitation_crud
from wxcloudrun.utils.wechat import get_wechat_api, WeChatAPIError
import base64
import logging

logger = logging.getLogger(__name__)
from wxcloudrun.crud import baby as baby_crud
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access, verify_baby_admin

router = APIRouter(
    prefix="/api/babies",
    tags=["宝宝管理"]
)


# ==================== 宝宝 CRUD ====================

@router.post("/", response_model=BabyResponse, status_code=status.HTTP_201_CREATED)
def create_baby(
    baby: BabyCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """创建宝宝信息"""
    return baby_crud.create_baby(db, baby, user_id)


@router.get("/my", response_model=list[BabyResponse])
def get_my_babies(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取我管理的所有宝宝"""
    return baby_crud.get_babies_by_user(db, user_id)


@router.get("/{baby_id}", response_model=BabyResponse)
def get_baby(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取宝宝详细信息"""
    verify_baby_access(baby_id, user_id, db)

    db_baby = baby_crud.get_baby(db, baby_id)
    if not db_baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宝宝不存在")
    return db_baby


@router.patch("/{baby_id}", response_model=BabyResponse)
def update_baby(
    baby_id: int,
    baby: BabyUpdate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """更新宝宝信息（需要管理员权限）"""
    verify_baby_admin(baby_id, user_id, db)

    db_baby = baby_crud.update_baby(db, baby_id, baby)
    if not db_baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宝宝不存在")
    return db_baby


@router.delete("/{baby_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_baby(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """删除宝宝（需要管理员权限，会级联删除所有相关记录）"""
    verify_baby_admin(baby_id, user_id, db)

    success = baby_crud.delete_baby(db, baby_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宝宝不存在")
    return None


# ==================== 家庭成员管理 ====================

@router.get("/{baby_id}/family", response_model=list[BabyFamilyResponse])
def get_family_members(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """获取宝宝的家庭成员列表"""
    verify_baby_access(baby_id, user_id, db)
    return baby_crud.get_family_members(db, baby_id)


@router.post("/{baby_id}/family", response_model=BabyFamilyResponse, status_code=status.HTTP_201_CREATED)
def add_family_member(
    baby_id: int,
    family: BabyFamilyCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """添加家庭成员（需要管理员权限）"""
    verify_baby_admin(baby_id, user_id, db)

    # 确保添加的是当前宝宝的家庭成员
    if family.baby_id != baby_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="宝宝ID不匹配")

    return baby_crud.add_family_member(db, family)


@router.delete("/{baby_id}/family/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_family_member(
    baby_id: int,
    target_user_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """移除家庭成员（需要管理员权限）"""
    verify_baby_admin(baby_id, user_id, db)

    success = baby_crud.remove_family_member(db, baby_id, target_user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="家庭成员不存在")
    return None


# ==================== 邀请码 ====================

@router.get("/{baby_id}/invite-code", response_model=InviteCodeResponse)
def get_invite_code(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    verify_baby_access(baby_id, user_id, db)
    inv = invitation_crud.get_active_invitation_by_baby(db, baby_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="邀请码不存在")
    return {
        "code": inv.invite_code,
        "baby_id": inv.baby_id,
        "expire_at": inv.expire_at,
        "status": inv.status,
    }


@router.post("/{baby_id}/invite-code", response_model=InviteCodeResponse, status_code=status.HTTP_201_CREATED)
def create_invite_code(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    verify_baby_admin(baby_id, user_id, db)
    inv = invitation_crud.create_invitation_for_baby(db, baby_id, user_id)
    return {
        "code": inv.invite_code,
        "baby_id": inv.baby_id,
        "expire_at": inv.expire_at,
        "status": inv.status,
    }


@router.get("/{baby_id}/invite-code/qrcode")
def get_invite_qrcode(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    """生成并返回小程序码（Base64 PNG）"""
    verify_baby_access(baby_id, user_id, db)
    inv = invitation_crud.get_active_invitation_by_baby(db, baby_id)
    if not inv:
        # 允许非管理员用户时，仅在无码的情况下返回404，不创建
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="邀请码不存在")

    wechat = get_wechat_api()
    scene = f"code={inv.invite_code}"
    page = "pages/family/join"
    try:
        logger.info(f"qrcode.begin baby_id={baby_id} code={inv.invite_code}")
        png_bytes = wechat.get_wxacode_unlimit.__wrapped__(wechat, scene=scene, page=page) if hasattr(wechat.get_wxacode_unlimit, "__wrapped__") else None
        if png_bytes is None:
            # 正常调用异步接口（FastAPI路由是同步函数，使用简单方式）
            import anyio
            png_bytes = anyio.run(wechat.get_wxacode_unlimit, scene, page)
    except WeChatAPIError as e:
        logger.error(f"qrcode.error baby_id={baby_id} err={e.errmsg}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"微信接口错误: {e.errmsg}")

    image_base64 = base64.b64encode(png_bytes).decode("ascii")
    logger.info(f"qrcode.success baby_id={baby_id} size={len(image_base64)}")
    return {
        "code": inv.invite_code,
        "image_base64": image_base64
    }
