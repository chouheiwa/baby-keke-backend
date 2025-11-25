"""
API 路由模块
"""
from .auth import router as auth_router
from .users import router as users_router
from .babies import router as babies_router
from .feeding import router as feeding_router
from .diaper import router as diaper_router
from .sleep import router as sleep_router
from .growth import router as growth_router
from .invitations import router as invitations_router
from .policies import router as policies_router
from .home import router as home_router

from .feeding_ongoing import router as feeding_ongoing_router

from .jaundice import router as jaundice_router

from .user_preference import router as user_preference_router
from .notifications import router as notifications_router
from .vaccines import router as vaccines_router

__all__ = [
    "auth_router",
    "users_router",
    "babies_router",
    "feeding_router",
    "feeding_ongoing_router",
    "diaper_router",
    "sleep_router",
    "growth_router",
    "jaundice_router",
    "invitations_router",
    "policies_router",
    "home_router",
    "user_preference_router",
    "notifications_router",
    "vaccines_router",
]
