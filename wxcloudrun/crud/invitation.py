from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from wxcloudrun.models.invitation import Invitation


def get_active_invitation_by_baby(db: Session, baby_id: int) -> Optional[Invitation]:
    return (
        db.query(Invitation)
        .filter(
            Invitation.baby_id == baby_id,
            Invitation.status == 'active',
            Invitation.expire_at > datetime.utcnow(),
        )
        .order_by(Invitation.id.desc())
        .first()
    )


def create_invitation_for_baby(db: Session, baby_id: int, creator_id: int, ttl_days: int = 3650) -> Invitation:
    existing = get_active_invitation_by_baby(db, baby_id)
    if existing:
        return existing

    def gen_code() -> str:
        import random
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(chars) for _ in range(8))

    code = gen_code()
    while db.query(Invitation).filter(Invitation.invite_code == code).first() is not None:
        code = gen_code()

    # 使用不带微秒的时间，避免某些 MySQL TIMESTAMP 不接受微秒
    # 同时将默认有效期设置为 10 年（TIMESTAMP 通常支持到 2038 年）
    expire_at = datetime.utcnow().replace(microsecond=0) + timedelta(days=ttl_days)
    inv = Invitation(
        baby_id=baby_id,
        invite_code=code,
        created_by=creator_id,
        expire_at=expire_at,
        status='active',
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv


def get_invitation_by_code(db: Session, code: str) -> Optional[Invitation]:
    return (
        db.query(Invitation)
        .filter(Invitation.invite_code == code)
        .first()
    )
