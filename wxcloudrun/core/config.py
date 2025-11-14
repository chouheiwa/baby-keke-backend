import os
from typing import Literal
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    # 环境配置
    env: Literal["development", "test", "production"] = "development"

    # 应用配置
    app_name: str = "可可宝宝记"
    debug: bool = True

    # 数据库配置
    mysql_username: str = "root"
    mysql_password: str = "root"
    mysql_address: str = "127.0.0.1:3306"
    mysql_database: str = "baby_record"

    # 微信小程序配置
    wx_appid: str = ""
    wx_appsecret: str = ""
    
    # JWT配置（未来用于认证）
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    http_verify: bool = True
    ca_bundle_path: str | None = None

    class Config:
        # 根据环境变量 ENV 加载对应的配置文件
        # 优先级: .env.{ENV} > .env
        case_sensitive = False

    @property
    def database_url(self) -> str:
        """构建数据库连接URL"""
        return f"mysql+pymysql://{self.mysql_username}:{self.mysql_password}@{self.mysql_address}/{self.mysql_database}"

    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return self.env == "production"

    @property
    def is_test(self) -> bool:
        """是否为测试环境"""
        return self.env == "test"

    @property
    def is_development(self) -> bool:
        """是否为开发环境"""
        return self.env == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置单例
    根据 ENV 环境变量加载对应的配置文件
    """
    env = os.getenv("ENV", "development")

    # 根据环境加载不同的配置文件
    env_file_map = {
        "development": ".env",
        "test": ".env.test",
        "production": ".env.production"
    }

    env_file = env_file_map.get(env, ".env")

    # 如果指定的环境配置文件不存在，回退到 .env
    if not os.path.exists(env_file) and env != "development":
        print(f"⚠️  警告: 环境配置文件 {env_file} 不存在，使用默认配置 .env")
        env_file = ".env"

    # 创建Settings时指定env_file
    return Settings(_env_file=env_file if os.path.exists(env_file) else None)
