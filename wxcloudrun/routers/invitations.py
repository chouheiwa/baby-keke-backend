from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.utils.deps import get_current_user_id
from wxcloudrun.crud import invitation as invitation_crud, baby as baby_crud

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