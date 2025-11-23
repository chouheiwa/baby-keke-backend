"""用户偏好设置的路由"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from wxcloudrun.core.database import get_db
from wxcloudrun.utils.deps import get_current_user
from wxcloudrun.models.user import User
from wxcloudrun.schemas.user_preference import (
    UserPreferenceCreate,
    UserPreferenceUpdate,
    UserPreferenceResponse,
    UserPreferencesResponse
)
from wxcloudrun.crud import user_preference as crud_preference

router = APIRouter(
    prefix="/api/users/me/preferences",
    tags=["用户偏好设置"]
)


@router.get("", response_model=UserPreferencesResponse)
async def get_all_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的所有偏好设置"""
    preferences_dict = crud_preference.get_preferences_dict(db, current_user.id)
    return UserPreferencesResponse(preferences=preferences_dict)


@router.get("/{preference_key}")
async def get_user_preference(
    preference_key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取当前用户的特定偏好设置"""
    preference = crud_preference.get_preference(db, current_user.id, preference_key)
    if not preference:
        return None
    return preference.preference_value


@router.put("/{preference_key}", response_model=UserPreferenceResponse)
async def set_user_preference(
    preference_key: str,
    preference_update: UserPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """设置当前用户的偏好设置（创建或更新）"""
    preference = crud_preference.set_preference(
        db,
        current_user.id,
        preference_key,
        preference_update.preference_value
    )
    return preference


@router.delete("/{preference_key}")
async def delete_user_preference(
    preference_key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除当前用户的特定偏好设置"""
    success = crud_preference.delete_preference(db, current_user.id, preference_key)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preference '{preference_key}' not found"
        )
    return {"message": f"Preference '{preference_key}' deleted successfully"}
