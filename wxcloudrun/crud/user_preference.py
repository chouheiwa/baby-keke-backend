"""用户偏好设置的 CRUD 操作"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from wxcloudrun.models.user_preference import UserPreference
from wxcloudrun.schemas.user_preference import UserPreferenceCreate, UserPreferenceUpdate


def get_preference(
    db: Session,
    user_id: int,
    preference_key: str
) -> Optional[UserPreference]:
    """获取用户的特定偏好设置"""
    return db.query(UserPreference).filter(
        UserPreference.user_id == user_id,
        UserPreference.preference_key == preference_key
    ).first()


def get_all_preferences(
    db: Session,
    user_id: int
) -> List[UserPreference]:
    """获取用户的所有偏好设置"""
    return db.query(UserPreference).filter(
        UserPreference.user_id == user_id
    ).all()


def get_preferences_dict(
    db: Session,
    user_id: int
) -> Dict[str, Any]:
    """获取用户的所有偏好设置，返回字典格式"""
    preferences = get_all_preferences(db, user_id)
    return {
        pref.preference_key: pref.preference_value
        for pref in preferences
    }


def set_preference(
    db: Session,
    user_id: int,
    preference_key: str,
    preference_value: Any
) -> UserPreference:
    """设置用户的偏好设置（创建或更新）"""
    # 尝试查找现有记录
    existing = get_preference(db, user_id, preference_key)
    
    if existing:
        # 更新现有记录
        existing.preference_value = preference_value
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # 创建新记录
        new_preference = UserPreference(
            user_id=user_id,
            preference_key=preference_key,
            preference_value=preference_value
        )
        db.add(new_preference)
        db.commit()
        db.refresh(new_preference)
        return new_preference


def delete_preference(
    db: Session,
    user_id: int,
    preference_key: str
) -> bool:
    """删除用户的特定偏好设置"""
    preference = get_preference(db, user_id, preference_key)
    if preference:
        db.delete(preference)
        db.commit()
        return True
    return False


def delete_all_preferences(
    db: Session,
    user_id: int
) -> int:
    """删除用户的所有偏好设置，返回删除的数量"""
    count = db.query(UserPreference).filter(
        UserPreference.user_id == user_id
    ).delete()
    db.commit()
    return count
