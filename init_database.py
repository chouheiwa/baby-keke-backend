#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建所有数据库表
"""
import sys
from database import engine, Base, init_db
from config import get_settings
from wxcloudrun.model import (
    User, Baby, BabyFamily,
    FeedingRecord, DiaperRecord, SleepRecord, GrowthRecord,
    Counters
)

def main():
    """初始化数据库"""
    settings = get_settings()

    print("=" * 60)
    print("🗄️  开始初始化数据库...")
    print("=" * 60)
    print(f"📌 环境: {settings.env.upper()}")
    print(f"🔗 数据库地址: {settings.mysql_address}")
    print(f"📊 数据库名称: {settings.mysql_database}")
    print("=" * 60)

    try:
        # 测试数据库连接
        print("\n✓ 正在测试数据库连接...")
        connection = engine.connect()
        connection.close()
        print("✅ 数据库连接成功！")

        # 创建所有表
        print("\n✓ 正在创建数据库表...")
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功！")

        # 显示已创建的表
        print("\n📋 已创建的表:")
        tables = [
            ("users", "用户表"),
            ("babies", "宝宝信息表"),
            ("baby_family", "宝宝-家庭成员关系表"),
            ("feeding_records", "喂养记录表"),
            ("diaper_records", "排便记录表"),
            ("sleep_records", "睡眠记录表"),
            ("growth_records", "生长发育记录表"),
            ("counters", "计数器表(示例)"),
        ]

        for table_name, description in tables:
            print(f"   - {table_name:25s} {description}")

        print("\n" + "=" * 60)
        print("🎉 数据库初始化完成！")
        print("=" * 60)

        return 0

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ 数据库初始化失败: {str(e)}")
        print("=" * 60)
        print("\n请检查：")
        print("1. 数据库服务是否已启动")
        print("2. 数据库连接配置是否正确 (.env 文件)")
        print("3. 数据库用户是否有足够的权限")
        print("4. 数据库名称是否已存在")
        return 1


if __name__ == "__main__":
    sys.exit(main())
