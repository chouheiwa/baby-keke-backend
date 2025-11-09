# 项目结构说明

## 目录结构

```
backend/
├── wxcloudrun/                 # 主应用目录
│   ├── __init__.py            # FastAPI应用入口
│   ├── core/                  # 核心配置模块
│   │   ├── __init__.py
│   │   ├── config.py          # 配置管理（环境变量）
│   │   └── database.py        # 数据库连接管理
│   ├── models/                # SQLAlchemy 数据库模型
│   │   ├── __init__.py
│   │   ├── user.py            # 用户模型
│   │   ├── baby.py            # 宝宝、家庭成员模型
│   │   ├── feeding.py         # 喂养记录模型
│   │   ├── diaper.py          # 排便/排尿记录模型
│   │   ├── sleep.py           # 睡眠记录模型
│   │   └── growth.py          # 生长发育记录模型
│   ├── schemas/               # Pydantic 数据验证模式
│   │   ├── __init__.py
│   │   ├── user.py            # 用户数据模式
│   │   ├── baby.py            # 宝宝数据模式
│   │   ├── feeding.py         # 喂养记录数据模式
│   │   ├── diaper.py          # 排便/排尿记录数据模式
│   │   ├── sleep.py           # 睡眠记录数据模式
│   │   └── growth.py          # 生长发育记录数据模式
│   ├── crud/                  # CRUD 数据库操作
│   │   ├── __init__.py
│   │   ├── user.py            # 用户CRUD操作
│   │   ├── baby.py            # 宝宝CRUD操作
│   │   ├── feeding.py         # 喂养记录CRUD操作
│   │   ├── diaper.py          # 排便/排尿记录CRUD操作
│   │   ├── sleep.py           # 睡眠记录CRUD操作
│   │   └── growth.py          # 生长发育记录CRUD操作
│   ├── routers/               # API 路由
│   │   ├── __init__.py
│   │   ├── users.py           # 用户管理API
│   │   ├── babies.py          # 宝宝管理API
│   │   ├── feeding.py         # 喂养记录API
│   │   ├── diaper.py          # 排便/排尿记录API
│   │   ├── sleep.py           # 睡眠记录API
│   │   └── growth.py          # 生长发育记录API
│   ├── utils/                 # 工具函数
│   │   ├── __init__.py
│   │   └── deps.py            # 依赖注入（权限验证等）
│   └── _deprecated/           # 旧代码（已废弃）
├── sql/                       # 数据库SQL脚本
│   ├── init_all_tables.sql   # 主初始化脚本
│   ├── README.md
│   └── tables/                # 各表DDL
├── .env                       # 开发环境配置
├── .env.test                  # 测试环境配置
├── .env.production            # 生产环境配置
├── .env.example               # 配置示例
├── requirements.txt           # Python依赖
├── Dockerfile                 # Docker配置
├── run.py                     # 启动脚本
└── README.md                  # 项目说明
```

## 模块说明

### 1. core/ - 核心配置

**config.py**
- 使用 Pydantic Settings 管理配置
- 支持多环境切换（development/test/production）
- 从 .env 文件读取配置

**database.py**
- SQLAlchemy 数据库引擎初始化
- 会话管理
- 数据库连接池配置

### 2. models/ - 数据库模型

使用 SQLAlchemy ORM 定义数据库表结构：

- `User`: 用户表
- `Baby`: 宝宝信息表
- `BabyFamily`: 宝宝-家庭成员关系表
- `FeedingRecord`: 喂养记录表
- `DiaperRecord`: 排便/排尿记录表
- `SleepRecord`: 睡眠记录表
- `GrowthRecord`: 生长发育记录表

### 3. schemas/ - 数据验证

使用 Pydantic 定义API请求和响应的数据格式：

每个模块包含：
- `XXXCreate`: 创建资源的请求数据
- `XXXUpdate`: 更新资源的请求数据
- `XXXResponse`: API响应数据

### 4. crud/ - 数据库操作

封装所有数据库的增删改查操作：

- 查询操作（get, get_by_xxx, list）
- 创建操作（create）
- 更新操作（update）
- 删除操作（delete）
- 统计操作（stats, count）

### 5. routers/ - API路由

定义所有 RESTful API 端点：

- 用户管理：`/api/users`
- 宝宝管理：`/api/babies`
- 喂养记录：`/api/feeding`
- 排便/排尿记录：`/api/diaper`
- 睡眠记录：`/api/sleep`
- 生长发育记录：`/api/growth`

### 6. utils/ - 工具函数

**deps.py**
- 依赖注入函数
- 用户身份验证
- 权限验证（家庭成员、管理员）

## API 文档

启动应用后，可以访问以下地址查看API文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 环境配置

### 开发环境
```bash
export ENV=development
python run.py 0.0.0.0 8000
```

### 测试环境
```bash
export ENV=test
python run.py 0.0.0.0 8000
```

### 生产环境
```bash
export ENV=production
python run.py 0.0.0.0 8000
```

## 数据库初始化

```bash
# 方式1：使用SQL脚本
mysql -u root -p < sql/init_all_tables.sql

# 方式2：启动应用时自动创建
# FastAPI应用会在启动时自动创建所有表
python run.py 0.0.0.0 8000
```

## 开发规范

### 1. 添加新功能模块

如果要添加新的功能模块（例如：疫苗接种记录），按以下顺序创建：

1. **定义数据库模型** - `models/vaccine.py`
2. **定义数据验证模式** - `schemas/vaccine.py`
3. **实现CRUD操作** - `crud/vaccine.py`
4. **创建API路由** - `routers/vaccine.py`
5. **注册路由** - 在 `wxcloudrun/__init__.py` 中注册

### 2. 代码风格

- 遵循 PEP 8 规范
- 使用类型注解
- 添加适当的注释和文档字符串
- 函数命名：使用动词开头（get_xxx, create_xxx, update_xxx）

### 3. 错误处理

- 使用 FastAPI 的 HTTPException
- 返回适当的 HTTP 状态码
- 提供清晰的错误信息

### 4. 权限控制

- 所有需要权限的API都应该使用依赖注入验证
- `verify_baby_access`: 验证用户是否是家庭成员
- `verify_baby_admin`: 验证用户是否是管理员

## 常见问题

### 1. 如何添加新的配置项？

在 `wxcloudrun/core/config.py` 的 `Settings` 类中添加新字段。

### 2. 如何修改数据库表结构？

1. 修改对应的 model 文件
2. 使用 Alembic 生成迁移脚本（或直接修改SQL文件）
3. 执行迁移

### 3. 如何测试API？

使用内置的 Swagger UI (`/docs`) 或 ReDoc (`/redoc`) 进行测试。

## 技术栈

- **Web框架**: FastAPI 0.115.6
- **ORM**: SQLAlchemy 2.0.36
- **数据验证**: Pydantic 2.10.6
- **数据库**: MySQL 5.7+
- **ASGI服务器**: Uvicorn
- **Python版本**: 3.13+

## 后续开发计划

- [ ] 实现微信小程序登录（openid转user_id）
- [ ] 添加用户认证中间件
- [ ] 实现疫苗接种记录功能
- [ ] 添加数据统计分析API
- [ ] 实现文件上传（照片、视频）
- [ ] 添加单元测试
- [ ] 添加日志系统
- [ ] 性能优化和缓存

## 贡献指南

1. 创建功能分支
2. 编写代码并测试
3. 提交代码并说明修改内容
4. 创建 Pull Request
