from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from wxcloudrun.core.config import get_settings
from wxcloudrun.core.database import Base, engine

settings = get_settings()

# 初始化FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="宝宝成长记录应用API",
    version="1.0.0",
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    # 初始化数据库表
    Base.metadata.create_all(bind=engine)

    # 打印启动信息
    print("=" * 60)
    print(f"🚀 {settings.app_name} 启动成功！")
    print(f"📌 运行环境: {settings.env.upper()}")
    print(f"🗄️  数据库地址: {settings.mysql_address}")
    print(f"📊 数据库名称: {settings.mysql_database}")
    print(f"🔧 调试模式: {'开启' if settings.debug else '关闭'}")
    print(f"📖 API文档: http://localhost/docs (或对应的访问地址)")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print(f"{settings.app_name} 已关闭")


# 健康检查接口
@app.get("/", tags=["健康检查"])
async def root():
    """根路径健康检查"""
    return {
        "message": f"欢迎使用{settings.app_name}",
        "environment": settings.env,
        "status": "running"
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "service": settings.app_name}


# 注册所有路由
from wxcloudrun.routers import (
    users_router,
    babies_router,
    feeding_router,
    diaper_router,
    sleep_router,
    growth_router
)

app.include_router(users_router)
app.include_router(babies_router)
app.include_router(feeding_router)
app.include_router(diaper_router)
app.include_router(sleep_router)
app.include_router(growth_router)
