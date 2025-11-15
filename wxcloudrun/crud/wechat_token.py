from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from wxcloudrun.models.wechat_token import WeChatAccessToken


def get_token(db: Session, appid: str) -> Optional[WeChatAccessToken]:
    return db.query(WeChatAccessToken).filter(WeChatAccessToken.appid == appid).first()


def upsert_token(db: Session, appid: str, token: str, expires_at: datetime) -> WeChatAccessToken:
    rec = get_token(db, appid)
    if rec:
        rec.token = token
        rec.expires_at = expires_at
    else:
        rec = WeChatAccessToken(appid=appid, token=token, expires_at=expires_at)
        db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec