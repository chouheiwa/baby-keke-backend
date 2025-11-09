"""
数据访问层 (DAO)
使用SQLAlchemy 2.0的Session进行数据库操作
"""
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from wxcloudrun.model import Counters

logger = logging.getLogger(__name__)


def query_counterbyid(db: Session, counter_id: int) -> Counters:
    """
    根据ID查询Counter实体
    :param db: 数据库会话
    :param counter_id: Counter的ID
    :return: Counter实体或None
    """
    try:
        return db.query(Counters).filter(Counters.id == counter_id).first()
    except SQLAlchemyError as e:
        logger.error(f"query_counterbyid error: {e}")
        return None


def delete_counterbyid(db: Session, counter_id: int) -> bool:
    """
    根据ID删除Counter实体
    :param db: 数据库会话
    :param counter_id: Counter的ID
    :return: 是否删除成功
    """
    try:
        counter = query_counterbyid(db, counter_id)
        if counter is None:
            return False
        db.delete(counter)
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"delete_counterbyid error: {e}")
        db.rollback()
        return False


def insert_counter(db: Session, counter: Counters) -> Counters:
    """
    插入一个Counter实体
    :param db: 数据库会话
    :param counter: Counters实体
    :return: 插入后的实体
    """
    try:
        db.add(counter)
        db.commit()
        db.refresh(counter)
        return counter
    except SQLAlchemyError as e:
        logger.error(f"insert_counter error: {e}")
        db.rollback()
        return None


def update_counterbyid(db: Session, counter_id: int, count: int) -> Counters:
    """
    根据ID更新counter的值
    :param db: 数据库会话
    :param counter_id: Counter的ID
    :param count: 新的计数值
    :return: 更新后的实体
    """
    try:
        counter = query_counterbyid(db, counter_id)
        if counter is None:
            return None
        counter.count = count
        db.commit()
        db.refresh(counter)
        return counter
    except SQLAlchemyError as e:
        logger.error(f"update_counterbyid error: {e}")
        db.rollback()
        return None
