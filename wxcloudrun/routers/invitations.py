from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.orm import Session
from datetime import datetime
from wxcloudrun.core.database import get_db
from wxcloudrun.utils.deps import get_current_user_id
from wxcloudrun.crud import invitation as invitation_crud, baby as baby_crud
from wxcloudrun.schemas.baby import BabyFamilyCreate
from wxcloudrun.schemas.invitation import AcceptInvitationRequest

router = APIRouter(
    prefix="/api/invitations",
    tags=["邀请"]
)


@router.get("/resolve")
def resolve_invite_code(
    code: str,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    inv = invitation_crud.get_invitation_by_code(db, code)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="邀请码不存在")
    baby = baby_crud.get_baby(db, inv.baby_id)
    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宝宝不存在")
    return {
        "code": inv.invite_code,
        "baby_id": inv.baby_id,
        "baby_name": baby.name,
        "expire_at": inv.expire_at,
        "status": inv.status
    }


@router.post("/accept")
def accept_invitation(
    payload: AcceptInvitationRequest | None = Body(None),
    code: str | None = Query(None),
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    real_code = (payload.code if payload and payload.code else code)
    if not real_code:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="缺少邀请码")

    inv = invitation_crud.get_invitation_by_code(db, real_code)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="邀请码不存在")
    if inv.status != 'active' or inv.expire_at <= datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邀请码已失效")

    baby = baby_crud.get_baby(db, inv.baby_id)
    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="宝宝不存在")

    if baby_crud.is_family_member(db, inv.baby_id, user_id):
        return {"baby_id": inv.baby_id, "joined": False, "message": "已是家庭成员"}

    family = BabyFamilyCreate(
        baby_id=inv.baby_id,
        user_id=user_id,
        is_admin=0,
        relation=None,
        relation_display=None,
    )
    baby_crud.add_family_member(db, family)
    return {"baby_id": inv.baby_id, "joined": True}
