# 可可宝宝记 - FastAPI 后端

![Python](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-orange)

基于 FastAPI + MySQL 的宝宝成长记录应用后端服务。

## 技术栈

- **Python**: 3.13+
- **框架**: FastAPI 0.115.6
- **ORM**: SQLAlchemy 2.0.36
- **数据库**: MySQL (通过 PyMySQL)
- **服务器**: Uvicorn 0.32.1
- **配置管理**: Pydantic Settings 2.7.1
- **数据迁移**: Alembic 1.14.0

## 快速开始

### 1. 环境准备

```bash
# Python 3.13+（推荐使用Python 3.13）
python3 --version  # 应显示 Python 3.13.x

# 创建虚拟环境（推荐）
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 升级pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

项目支持多环境配置（开发、测试、生产），通过 `ENV` 环境变量切换。

#### 开发环境（默认）

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置
# ENV=development
# MYSQL_ADDRESS=127.0.0.1:3306
# MYSQL_DATABASE=baby_record
```

#### 测试环境

```bash
# 使用测试环境配置文件（已包含测试数据库地址）
# 数据库地址: sh-cynosdbmysql-grp-qwmgtz4m.sql.tencentcdb.com:28266

# 方式1: 使用 .env.test 文件
# 编辑 .env.test，填写测试数据库密码
# 然后设置环境变量
export ENV=test

# 方式2: 直接设置环境变量（推荐用于临时测试）
export ENV=test
export MYSQL_USERNAME=root
export MYSQL_PASSWORD=your_test_password
export MYSQL_ADDRESS=sh-cynosdbmysql-grp-qwmgtz4m.sql.tencentcdb.com:28266
export MYSQL_DATABASE=baby_record_test
```

#### 生产环境

```bash
# 编辑 .env.production，填写生产数据库配置
# 然后设置环境变量
export ENV=production

# 或通过微信云托管设置环境变量（推荐）
# ENV=production
# MYSQL_USERNAME=xxx
# MYSQL_PASSWORD=xxx
# MYSQL_ADDRESS=xxx
# SECRET_KEY=强密钥（必须修改）
```

#### 环境配置文件优先级

```
ENV=development → 读取 .env
ENV=test        → 读取 .env.test
ENV=production  → 读取 .env.production
```

### 3. 本地运行

#### 开发环境运行

```bash
# 方式1: 使用 run.py (开发模式，支持热重载)
python run.py 0.0.0.0 8000

# 方式2: 直接使用 uvicorn
uvicorn wxcloudrun:app --host 0.0.0.0 --port 8000 --reload
```

#### 测试环境运行

```bash
# 设置环境为测试
export ENV=test

# 启动服务
python run.py 0.0.0.0 8000
# 或
uvicorn wxcloudrun:app --host 0.0.0.0 --port 8000 --reload
```

#### 生产环境运行

```bash
# 设置环境为生产
export ENV=production

# 生产环境不使用热重载
uvicorn wxcloudrun:app --host 0.0.0.0 --port 80 --workers 4
```

### 4. 访问服务

- **API文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/

## Docker 部署

### 本地构建运行

```bash
# 构建镜像
docker build -t baby-record-backend .

# 开发环境运行
docker run -d \
  -p 80:80 \
  -e ENV=development \
  -e MYSQL_USERNAME=root \
  -e MYSQL_PASSWORD=your_password \
  -e MYSQL_ADDRESS=db_host:3306 \
  -e MYSQL_DATABASE=baby_record \
  --name baby-record \
  baby-record-backend

# 测试环境运行
docker run -d \
  -p 80:80 \
  -e ENV=test \
  -e MYSQL_USERNAME=root \
  -e MYSQL_PASSWORD=your_test_password \
  -e MYSQL_ADDRESS=sh-cynosdbmysql-grp-qwmgtz4m.sql.tencentcdb.com:28266 \
  -e MYSQL_DATABASE=baby_record_test \
  --name baby-record-test \
  baby-record-backend

# 生产环境运行
docker run -d \
  -p 80:80 \
  -e ENV=production \
  -e MYSQL_USERNAME=root \
  -e MYSQL_PASSWORD=your_production_password \
  -e MYSQL_ADDRESS=production_db_host:3306 \
  -e MYSQL_DATABASE=baby_record \
  -e SECRET_KEY=your_strong_secret_key \
  --name baby-record-prod \
  baby-record-backend
```

### 微信云托管部署

前往 [微信云托管快速开始页面](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/basic/guide.html) 进行部署。

## 本地调试
下载代码在本地调试，请参考[微信云托管本地调试指南](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/guide/debug/)

## Dockerfile最佳实践
请参考[如何提高项目构建效率](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/scene/build/speed.html)

## 目录结构说明

```
.
├── Dockerfile                  Docker构建文件
├── README.md                   项目说明文档
├── .env.example                环境变量配置示例
├── container.config.json       微信云托管配置（二开请忽略）
├── requirements.txt            Python依赖包列表
├── config.py                   应用配置（使用Pydantic Settings）
├── database.py                 数据库连接管理（SQLAlchemy）
├── run.py                      本地开发启动脚本
└── wxcloudrun/                 应用主目录
    ├── __init__.py             FastAPI应用初始化
    ├── dao.py                  数据访问层（DAO）
    ├── model.py                数据库模型（SQLAlchemy ORM）
    ├── schemas.py              API数据模型（Pydantic）
    ├── views.py                API路由定义
    └── templates/              静态模板目录（可选）
```

## 项目特性

- ✅ **FastAPI框架**: 高性能、自动生成API文档
- ✅ **SQLAlchemy 2.0**: 最新ORM，类型安全
- ✅ **Pydantic数据验证**: 自动数据验证和序列化
- ✅ **依赖注入**: 数据库会话管理
- ✅ **CORS支持**: 跨域请求配置
- ✅ **多环境配置**: 支持开发、测试、生产环境隔离
- ✅ **环境变量配置**: 灵活的配置管理
- ✅ **自动生成文档**: Swagger UI 和 ReDoc



## 服务 API 文档

> 💡 访问 http://localhost:8000/docs 可查看完整的交互式API文档

### `GET /`

健康检查接口

#### 响应示例

```json
{
  "code": 0,
  "data": {
    "message": "欢迎使用可可宝宝记API",
    "version": "1.0.0",
    "docs": "/docs"
  }
}
```

### `GET /api/count`

获取当前计数

#### 响应格式

```json
{
  "code": 0,
  "data": 42,
  "error_msg": null
}
```

#### 调用示例

```bash
curl http://localhost:8000/api/count
```

### `POST /api/count`

更新计数（自增或清零）

#### 请求体

```json
{
  "action": "inc"  // "inc" 表示加一，"clear" 表示清零
}
```

#### 响应格式

```json
{
  "code": 0,
  "data": 43,
  "error_msg": null
}
```

#### 调用示例

```bash
# 计数加一
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"action": "inc"}' \
  http://localhost:8000/api/count

# 清零
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"action": "clear"}' \
  http://localhost:8000/api/count
```

## 环境变量配置

如果不是通过微信云托管控制台部署，需要手动配置以下环境变量：

| 环境变量 | 说明 | 示例 | 必填 |
|---------|------|------|----|
| `ENV` | 运行环境 | `development` / `test` / `production` | 否 |
| `MYSQL_USERNAME` | MySQL用户名 | `root` | 是 |
| `MYSQL_PASSWORD` | MySQL密码 | `your_password` | 是 |
| `MYSQL_ADDRESS` | MySQL地址:端口 | `127.0.0.1:3306` | 是 |
| `MYSQL_DATABASE` | 数据库名称 | `baby_record` | 是 |
| `SECRET_KEY` | JWT密钥 | `your-secret-key` | 生产必填 |
| `DEBUG` | 调试模式 | `true` / `false` | 否 |

**环境说明**:
- **开发环境** (`ENV=development`): 默认环境，使用 `.env` 配置文件
- **测试环境** (`ENV=test`): 使用 `.env.test` 配置文件，测试数据库地址已配置
- **生产环境** (`ENV=production`): 使用 `.env.production` 配置文件，需配置强密钥

## 开发指南

### 添加新的API路由

1. 在 `wxcloudrun/schemas.py` 中定义请求和响应模型
2. 在 `wxcloudrun/model.py` 中定义数据库模型
3. 在 `wxcloudrun/dao.py` 中实现数据访问逻辑
4. 在 `wxcloudrun/views.py` 中添加路由处理函数

### 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
# 初始化迁移环境（首次使用）
alembic init alembic

# 生成迁移脚本
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

## 常见问题

### 1. 数据库连接失败

检查环境变量配置是否正确，确保 MySQL 服务已启动。

### 2. 端口被占用

修改启动命令中的端口号：
```bash
python run.py 0.0.0.0 8001
```

### 3. 依赖安装失败

使用国内镜像源加速：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```



## License

[MIT](./LICENSE)
