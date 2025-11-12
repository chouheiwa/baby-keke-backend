from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,      # 连接池预检查，确保连接可用
    pool_recycle=3600,       # 连接回收时间（1小时）
    pool_size=5,             # 连接池大小
    max_overflow=10,         # 最大溢出连接数
    pool_timeout=60,         # 获取连接的超时时间（秒）
    echo=settings.debug,     # 开发环境打印SQL
    connect_args={
        "connect_timeout": 60,   # MySQL 连接超时（秒）
        "read_timeout": 60,      # 读取超时（秒）
        "write_timeout": 60,     # 写入超时（秒）
    }
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    用于FastAPI的依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库，创建所有表
    """
    Base.metadata.create_all(bind=engine)
