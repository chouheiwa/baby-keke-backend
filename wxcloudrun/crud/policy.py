from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from wxcloudrun.models.policy import Policy


def create_policy(db: Session, policy_type: str, data) -> Policy:
    existing = db.query(Policy).filter(
        and_(
            Policy.type == policy_type,
            Policy.version == data.version,
            Policy.locale == (data.locale or "zh-CN"),
        )
    ).first()
    if existing:
        return existing

    policy = Policy(
        type=policy_type,
        version=data.version,
        title=data.title,
        content=data.content,
        format=data.format or "markdown",
        locale=data.locale or "zh-CN",
        status='draft'
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def update_policy(db: Session, policy_type: str, version: str, locale: Optional[str], data) -> Optional[Policy]:
    locale_val = locale or "zh-CN"
    policy = db.query(Policy).filter(
        and_(Policy.type == policy_type, Policy.version == version, Policy.locale == locale_val)
    ).first()
    if not policy:
        return None

    if data.title is not None:
        policy.title = data.title
    if data.content is not None:
        policy.content = data.content
    if data.format is not None:
        policy.format = data.format

    db.commit()
    db.refresh(policy)
    return policy


def publish_policy(db: Session, policy_type: str, version: str, locale: Optional[str], effective_at: Optional[datetime]) -> Optional[Policy]:
    locale_val = locale or "zh-CN"
    policy = db.query(Policy).filter(
        and_(Policy.type == policy_type, Policy.version == version, Policy.locale == locale_val)
    ).first()
    if not policy:
        return None

    policy.status = 'published'
    policy.effective_at = effective_at or datetime.now()
    db.commit()
    db.refresh(policy)
    return policy


def get_policy_by_version(db: Session, policy_type: str, version: str, locale: Optional[str]) -> Optional[Policy]:
    locale_val = locale or "zh-CN"
    return db.query(Policy).filter(
        and_(Policy.type == policy_type, Policy.version == version, Policy.locale == locale_val)
    ).first()


def get_current_policy(db: Session, policy_type: str, locale: Optional[str]) -> Optional[Policy]:
    locale_val = locale or "zh-CN"
    q = db.query(Policy).filter(
        and_(Policy.type == policy_type, Policy.locale == locale_val, Policy.status == 'published')
    )
    policy = q.order_by(desc(Policy.effective_at), desc(Policy.created_at)).first()
    return policy


def list_policies(
    db: Session,
    policy_type: str,
    locale: Optional[str],
    status: Optional[str],
    skip: int = 0,
    limit: int = 20
) -> Tuple[List[Policy], int]:
    locale_val = locale or "zh-CN"
    q = db.query(Policy).filter(and_(Policy.type == policy_type, Policy.locale == locale_val))
    if status:
        q = q.filter(Policy.status == status)
    total = q.count()
    items = q.order_by(desc(Policy.created_at)).offset(skip).limit(limit).all()
    return items, total