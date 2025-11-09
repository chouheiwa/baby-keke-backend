"""
宝宝相关的 CRUD 操作
"""
from typing import Optional
from sqlalchemy.orm import Session
from wxcloudrun.models.baby import Baby, BabyFamily
from wxcloudrun.schemas.baby import BabyCreate, BabyUpdate, BabyFamilyCreate


# ==================== Baby CRUD ====================

def get_baby(db: Session, baby_id: int) -> Optional[Baby]:
    """根据ID获取宝宝信息"""
    return db.query(Baby).filter(Baby.id == baby_id).first()


def get_babies_by_user(db: Session, user_id: int) -> list[Baby]:
    """获取用户关联的所有宝宝"""
    return (
        db.query(Baby)
        .join(BabyFamily)
        .filter(BabyFamily.user_id == user_id)
        .all()
    )


def get_babies(db: Session, skip: int = 0, limit: int = 100) -> list[Baby]:
    """获取宝宝列表"""
    return db.query(Baby).offset(skip).limit(limit).all()


def create_baby(db: Session, baby: BabyCreate, creator_id: int) -> Baby:
    """创建宝宝"""
    db_baby = Baby(**baby.model_dump(), created_by=creator_id)
    db.add(db_baby)
    db.commit()
    db.refresh(db_baby)

    # 自动添加创建者为家庭成员
    db_family = BabyFamily(
        baby_id=db_baby.id,
        user_id=creator_id,
        is_admin=1  # 创建者默认为管理员
    )
    db.add(db_family)
    db.commit()

    return db_baby


def update_baby(db: Session, baby_id: int, baby: BabyUpdate) -> Optional[Baby]:
    """更新宝宝信息"""
    db_baby = get_baby(db, baby_id)
    if not db_baby:
        return None

    update_data = baby.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_baby, field, value)

    db.commit()
    db.refresh(db_baby)
    return db_baby


def delete_baby(db: Session, baby_id: int) -> bool:
    """删除宝宝（会级联删除相关记录）"""
    db_baby = get_baby(db, baby_id)
    if not db_baby:
        return False

    db.delete(db_baby)
    db.commit()
    return True


# ==================== BabyFamily CRUD ====================

def get_family_members(db: Session, baby_id: int) -> list[BabyFamily]:
    """获取宝宝的所有家庭成员"""
    return db.query(BabyFamily).filter(BabyFamily.baby_id == baby_id).all()


def add_family_member(db: Session, family: BabyFamilyCreate) -> BabyFamily:
    """添加家庭成员"""
    db_family = BabyFamily(**family.model_dump())
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family


def remove_family_member(db: Session, baby_id: int, user_id: int) -> bool:
    """移除家庭成员"""
    db_family = (
        db.query(BabyFamily)
        .filter(BabyFamily.baby_id == baby_id, BabyFamily.user_id == user_id)
        .first()
    )
    if not db_family:
        return False

    db.delete(db_family)
    db.commit()
    return True


def is_family_member(db: Session, baby_id: int, user_id: int) -> bool:
    """检查用户是否是宝宝的家庭成员"""
    return (
        db.query(BabyFamily)
        .filter(BabyFamily.baby_id == baby_id, BabyFamily.user_id == user_id)
        .first()
        is not None
    )


def is_admin(db: Session, baby_id: int, user_id: int) -> bool:
    """检查用户是否是宝宝的管理员"""
    family = (
        db.query(BabyFamily)
        .filter(BabyFamily.baby_id == baby_id, BabyFamily.user_id == user_id)
        .first()
    )
    return family is not None and family.is_admin == 1
