"""
用户会话的 CRUD 操作
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from wxcloudrun.models.session import UserSession


def create_or_update_session(
    db: Session,
    user_id: int,
    openid: str,
    session_key: str,
    unionid: Optional[str] = None,
    expires_days: int = 30
) -> UserSession:
    """
    创建或更新用户会话
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        openid: 微信OpenID
        session_key: 会话密钥
        unionid: 微信UnionID（可选）
        expires_days: 过期天数，默认30天
        
    Returns:
        UserSession: 用户会话对象
    """
    # 计算过期时间
    expires_at = datetime.now() + timedelta(days=expires_days)
    
    # 检查是否已存在
    db_session = db.query(UserSession).filter(UserSession.openid == openid).first()
    
    if db_session:
        # 更新现有会话
        db_session.user_id = user_id
        db_session.session_key = session_key
        db_session.unionid = unionid
        db_session.expires_at = expires_at
    else:
        # 创建新会话
        db_session = UserSession(
            user_id=user_id,
            openid=openid,
            session_key=session_key,
            unionid=unionid,
            expires_at=expires_at
        )
        db.add(db_session)
    
    db.commit()
    db.refresh(db_session)
    return db_session


def get_session_by_openid(db: Session, openid: str) -> Optional[UserSession]:
    """
    根据 OpenID 获取会话
    
    Args:
        db: 数据库会话
        openid: 微信OpenID
        
    Returns:
        UserSession: 用户会话对象，不存在则返回 None
    """
    return db.query(UserSession).filter(UserSession.openid == openid).first()


def get_session_by_user_id(db: Session, user_id: int) -> Optional[UserSession]:
    """
    根据用户ID获取会话
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        UserSession: 用户会话对象，不存在则返回 None
    """
    return db.query(UserSession).filter(UserSession.user_id == user_id).first()


def is_session_valid(db: Session, openid: str) -> bool:
    """
    检查会话是否有效（未过期）
    
    Args:
        db: 数据库会话
        openid: 微信OpenID
        
    Returns:
        bool: 有效返回 True，无效或不存在返回 False
    """
    db_session = get_session_by_openid(db, openid)
    
    if not db_session:
        return False
    
    # 检查是否过期
    return db_session.expires_at > datetime.now()


def delete_expired_sessions(db: Session) -> int:
    """
    删除所有过期的会话
    
    Args:
        db: 数据库会话
        
    Returns:
        int: 删除的记录数
    """
    count = db.query(UserSession).filter(
        UserSession.expires_at <= datetime.now()
    ).delete()
    
    db.commit()
    return count


def delete_session_by_openid(db: Session, openid: str) -> bool:
    """
    删除指定 OpenID 的会话
    
    Args:
        db: 数据库会话
        openid: 微信OpenID
        
    Returns:
        bool: 删除成功返回 True，会话不存在返回 False
    """
    db_session = get_session_by_openid(db, openid)
    
    if not db_session:
        return False
    
    db.delete(db_session)
    db.commit()
    return True


def update_session_key(
    db: Session,
    openid: str,
    new_session_key: str,
    expires_days: int = 30
) -> Optional[UserSession]:
    """
    更新会话密钥并延长过期时间
    
    Args:
        db: 数据库会话
        openid: 微信OpenID
        new_session_key: 新的会话密钥
        expires_days: 过期天数，默认30天
        
    Returns:
        UserSession: 更新后的会话对象，不存在则返回 None
    """
    db_session = get_session_by_openid(db, openid)
    
    if not db_session:
        return None
    
    # 更新会话密钥和过期时间
    db_session.session_key = new_session_key
    db_session.expires_at = datetime.now() + timedelta(days=expires_days)
    
    db.commit()
    db.refresh(db_session)
    return db_session

