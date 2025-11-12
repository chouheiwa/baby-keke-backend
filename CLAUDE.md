# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

可可宝宝记 (Baby Record) is a baby growth tracking application built with FastAPI + MySQL. It provides WeChat Mini Program backend services for recording feeding, diaper changes, sleep, and growth data.

**Tech Stack:**
- Python 3.13+
- FastAPI 0.115.6
- SQLAlchemy 2.0.36 (ORM)
- MySQL via PyMySQL
- Uvicorn server
- Pydantic Settings for configuration
- WeChat Mini Program authentication

## Development Commands

### Setup and Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Application

```bash
# Development mode with hot reload (default port 8000)
python run.py 0.0.0.0 8000

# Or using uvicorn directly
uvicorn wxcloudrun:app --host 0.0.0.0 --port 8000 --reload

# Production mode (no reload, multiple workers)
uvicorn wxcloudrun:app --host 0.0.0.0 --port 80 --workers 4
```

### Database Management

```bash
# Initialize database with all tables
mysql -u root -p < sql/init_all_tables.sql

# Or execute from MySQL shell
mysql -u root -p
source /path/to/sql/init_all_tables.sql

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### Docker Commands

```bash
# Build image
docker build -t baby-record-backend .

# Run container (development)
docker run -d -p 80:80 \
  -e ENV=development \
  -e MYSQL_USERNAME=root \
  -e MYSQL_PASSWORD=your_password \
  -e MYSQL_ADDRESS=db_host:3306 \
  -e MYSQL_DATABASE=baby_record \
  -e WX_APPID=your_appid \
  -e WX_APPSECRET=your_secret \
  --name baby-record \
  baby-record-backend
```

## Architecture

### Multi-Environment Configuration

The application supports three environments (development, test, production) controlled by the `ENV` environment variable:

- **ENV=development** → loads `.env` (default)
- **ENV=test** → loads `.env.test`
- **ENV=production** → loads `.env.production`

Configuration is managed through `wxcloudrun/core/config.py` using Pydantic Settings with `@lru_cache()` for singleton pattern.

### Project Structure

```
wxcloudrun/
├── core/
│   ├── config.py          # Environment-aware settings (Pydantic BaseSettings)
│   └── database.py        # SQLAlchemy engine, session factory, Base
├── models/                # SQLAlchemy ORM models
│   ├── user.py
│   ├── baby.py
│   ├── session.py
│   └── [feeding|diaper|sleep|growth].py
├── schemas/               # Pydantic request/response models
├── crud/                  # Database operations (CRUD functions)
├── routers/               # FastAPI route handlers
│   ├── __init__.py        # Exports all routers
│   ├── auth.py
│   ├── users.py
│   └── [babies|feeding|diaper|sleep|growth].py
├── utils/
│   ├── deps.py            # Dependency injection (get_current_user_id, verify_baby_access)
│   └── wechat.py          # WeChat API client (code2session, session management)
└── __init__.py            # FastAPI app initialization, CORS, router registration
```

### Database Architecture

**Table Dependencies (must follow this order for creation/deletion):**
1. `users` (base table)
2. `user_sessions` (FK: user_id)
3. `babies` (FK: created_by → users)
4. `baby_family` (FK: baby_id, user_id) - many-to-many relationship
5. `invitations` (FK: baby_id, inviter_id)
6. Record tables (FK: baby_id, user_id):
   - `feeding_records`
   - `diaper_records`
   - `sleep_records`
   - `growth_records`

All record tables use **cascade deletion**: deleting a baby automatically deletes all related records.

### Key Architectural Patterns

**1. Dependency Injection for Authentication**

The application uses FastAPI's dependency injection for authentication via `wxcloudrun/utils/deps.py`:

- `get_current_user_id()`: Extracts user ID from `X-Wx-Openid` header (WeChat cloud hosting auto-injects this)
- `verify_baby_access()`: Checks if user is a family member
- `verify_baby_admin()`: Checks if user has admin rights

**2. WeChat Mini Program Authentication Flow**

Implemented in `wxcloudrun/utils/wechat.py` and `wxcloudrun/routers/auth.py`:

1. User calls `wx.login()` on mini program → gets `code`
2. Frontend sends `code` to backend
3. Backend calls `WeChatAPI.code2session(code)` → gets `openid` + `session_key`
4. Backend creates/updates user and session records
5. Session expires after 30 days (configurable)

**3. CRUD Pattern**

All database operations follow the CRUD pattern:
- **models/** - SQLAlchemy ORM definitions
- **schemas/** - Pydantic models for API validation
- **crud/** - Business logic functions that take `db: Session` and return models
- **routers/** - HTTP handlers that use CRUD functions via dependency injection

**4. Router Registration**

All routers are imported in `wxcloudrun/routers/__init__.py` and registered in `wxcloudrun/__init__.py`:

```python
from wxcloudrun.routers import (
    auth_router,
    users_router,
    babies_router,
    # ...
)

app.include_router(auth_router)
app.include_router(users_router)
# ...
```

When adding new routers, update both files.

### Database Session Management

The application uses dependency injection for database sessions:

```python
from wxcloudrun.core.database import get_db

@router.get("/endpoint")
def endpoint(db: Annotated[Session, Depends(get_db)]):
    # db session is automatically created and closed
    pass
```

The `get_db()` generator ensures sessions are properly closed even if errors occur.

### WeChat API Integration

The `WeChatAPI` class (`wxcloudrun/utils/wechat.py`) handles all WeChat Mini Program API calls:

- `code2session(code)`: Validate login credentials
- `check_session_key()`: Verify session validity
- `reset_session_key()`: Reset session (requires signature - recommend using re-login instead)
- `_get_access_token()`: Get API access token (should be cached in production - 7200s lifetime)

**Important**: `WX_APPID` and `WX_APPSECRET` must be configured in environment variables. See `WECHAT_CONFIG.md` for setup instructions.

## Important Development Notes

### Adding New API Endpoints

1. Define Pydantic models in `wxcloudrun/schemas/<module>.py`
2. Define SQLAlchemy models in `wxcloudrun/models/<module>.py`
3. Implement CRUD functions in `wxcloudrun/crud/<module>.py`
4. Create router in `wxcloudrun/routers/<module>.py`
5. Export router in `wxcloudrun/routers/__init__.py`
6. Register router in `wxcloudrun/__init__.py` via `app.include_router()`

### Database Schema Changes

When modifying database schema:
1. Update SQLAlchemy model in `wxcloudrun/models/`
2. Create SQL migration in `sql/tables/` following numbering convention
3. Update `sql/init_all_tables.sql` to include new table
4. If using Alembic: `alembic revision --autogenerate -m "description"`
5. Respect foreign key dependencies when creating/dropping tables

### Environment Variables

Required environment variables (configured in `.env`, `.env.test`, or `.env.production`):

```bash
# Environment
ENV=development|test|production

# Database
MYSQL_USERNAME=root
MYSQL_PASSWORD=your_password
MYSQL_ADDRESS=127.0.0.1:3306
MYSQL_DATABASE=baby_record

# WeChat Mini Program (REQUIRED)
WX_APPID=wx1234567890abcdef
WX_APPSECRET=your_wechat_appsecret

# JWT (production requires strong SECRET_KEY)
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=可可宝宝记
DEBUG=true
```

### Authentication Flow for New Endpoints

For endpoints requiring authentication:

```python
from typing import Annotated
from fastapi import Depends
from wxcloudrun.utils.deps import get_current_user_id, verify_baby_access

@router.get("/babies/{baby_id}/records")
def get_records(
    baby_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[None, Depends(verify_baby_access)]  # Verifies access
):
    # user_id is authenticated
    # verify_baby_access already checked permissions
    pass
```

### API Documentation

FastAPI auto-generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Always test new endpoints using these interfaces during development.

### CORS Configuration

CORS is configured in `wxcloudrun/__init__.py` to allow all origins (`allow_origins=["*"]`). In production, update this to specific domains for security.

### Deployment

The application is designed for WeChat Cloud Hosting but can be deployed anywhere:

1. **WeChat Cloud Hosting**: Use provided `Dockerfile` and `container.config.json`
2. **Manual deployment**: Set environment variables and run uvicorn with production settings
3. **Docker**: Build image with `docker build` and configure environment variables at runtime
