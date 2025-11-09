"""
API路由定义
使用FastAPI进行路由和依赖注入
"""
from datetime import datetime
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from wxcloudrun import app
from database import get_db
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.schemas import ResponseModel, CounterRequest


@app.get("/")
async def index():
    """
    健康检查接口
    :return: 欢迎信息
    """
    return ResponseModel(
        code=0,
        data={
            "message": "欢迎使用可可宝宝记API",
            "version": "1.0.0",
            "docs": "/docs"
        }
    )


@app.post("/api/count", response_model=ResponseModel)
async def count(
    request: CounterRequest,
    db: Session = Depends(get_db)
):
    """
    计数器操作接口
    :param request: 操作请求（inc增加或clear清除）
    :param db: 数据库会话（依赖注入）
    :return: 操作结果
    """
    action = request.action

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(db, 1)
        if counter is None:
            # 创建新的计数器
            counter = Counters(id=1, count=1)
            counter = insert_counter(db, counter)
        else:
            # 更新计数器
            counter = update_counterbyid(db, 1, counter.count + 1)

        if counter:
            return ResponseModel(code=0, data=counter.count)
        else:
            raise HTTPException(status_code=500, detail="计数器操作失败")

    # 执行清0操作
    elif action == 'clear':
        result = delete_counterbyid(db, 1)
        if result:
            return ResponseModel(code=0, data={})
        else:
            raise HTTPException(status_code=500, detail="清除计数器失败")

    # action参数错误
    else:
        return ResponseModel(code=-1, error_msg='action参数错误，只支持inc或clear')


@app.get("/api/count", response_model=ResponseModel)
async def get_count(db: Session = Depends(get_db)):
    """
    获取当前计数
    :param db: 数据库会话（依赖注入）
    :return: 计数值
    """
    counter = query_counterbyid(db, 1)
    count = 0 if counter is None else counter.count
    return ResponseModel(code=0, data=count)
