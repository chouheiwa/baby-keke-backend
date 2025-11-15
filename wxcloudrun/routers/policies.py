from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from wxcloudrun.core.database import get_db
from wxcloudrun.schemas.policy import PolicyCreate, PolicyUpdate, PolicyPublishRequest, PolicyResponse
from wxcloudrun.utils.markdown import render_markdown
from wxcloudrun.crud import policy as policy_crud
from wxcloudrun.utils.deps import require_admin_token


router = APIRouter(
    prefix="/api/policies",
    tags=["协议与政策"]
)


@router.post("/{policy_type}", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
def create_policy(
    policy_type: str,
    payload: PolicyCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_token)
):
    created = policy_crud.create_policy(db, policy_type, payload)
    return created


@router.patch("/{policy_type}/versions/{version}", response_model=PolicyResponse)
def update_policy(
    policy_type: str,
    version: str,
    payload: PolicyUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_token),
    locale: Optional[str] = Query(None, description="语言/地区")
):
    updated = policy_crud.update_policy(db, policy_type, version, locale, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="策略不存在")
    return updated


@router.post("/{policy_type}/versions/{version}/publish", response_model=PolicyResponse)
def publish_policy(
    policy_type: str,
    version: str,
    payload: PolicyPublishRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin_token),
    locale: Optional[str] = Query(None, description="语言/地区")
):
    published = policy_crud.publish_policy(db, policy_type, version, locale, payload.effective_at)
    if not published:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="策略不存在")
    return published


@router.get("/{policy_type}/current", response_model=PolicyResponse)
def get_current_policy(
    policy_type: str,
    db: Session = Depends(get_db),
    locale: Optional[str] = Query(None, description="语言/地区")
):
    current = policy_crud.get_current_policy(db, policy_type, locale)
    if not current:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到已发布政策")
    content_html = render_markdown(current.content) if current.format == 'markdown' else None
    return PolicyResponse(
        id=current.id,
        type=current.type,
        version=current.version,
        title=current.title,
        content=current.content,
        format=current.format,
        locale=current.locale,
        status=current.status,
        effective_at=current.effective_at,
        created_at=current.created_at,
        updated_at=current.updated_at,
        content_html=content_html
    )


@router.get("/{policy_type}/versions/{version}", response_model=PolicyResponse)
def get_policy_by_version(
    policy_type: str,
    version: str,
    db: Session = Depends(get_db),
    locale: Optional[str] = Query(None, description="语言/地区")
):
    policy = policy_crud.get_policy_by_version(db, policy_type, version, locale)
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="策略不存在")
    content_html = render_markdown(policy.content) if policy.format == 'markdown' else None
    return PolicyResponse(
        id=policy.id,
        type=policy.type,
        version=policy.version,
        title=policy.title,
        content=policy.content,
        format=policy.format,
        locale=policy.locale,
        status=policy.status,
        effective_at=policy.effective_at,
        created_at=policy.created_at,
        updated_at=policy.updated_at,
        content_html=content_html
    )


@router.get("/{policy_type}/versions", response_model=list[PolicyResponse])
def list_policies(
    policy_type: str,
    db: Session = Depends(get_db),
    locale: Optional[str] = Query(None, description="语言/地区"),
    status_filter: Optional[str] = Query(None, description="状态过滤: draft/published/archived"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    items, _ = policy_crud.list_policies(db, policy_type, locale, status_filter, skip, limit)
    resp = []
    for p in items:
        content_html = render_markdown(p.content) if p.format == 'markdown' else None
        resp.append(PolicyResponse(
            id=p.id,
            type=p.type,
            version=p.version,
            title=p.title,
            content=p.content,
            format=p.format,
            locale=p.locale,
            status=p.status,
            effective_at=p.effective_at,
            created_at=p.created_at,
            updated_at=p.updated_at,
            content_html=content_html
        ))
    return resp