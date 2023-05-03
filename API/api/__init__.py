from fastapi import APIRouter
from .user_api import router as user_router
from .check_api import router as check_router

router = APIRouter(prefix="/api",)
router.include_router(user_router)
router.include_router(check_router)
