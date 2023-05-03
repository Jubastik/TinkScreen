from fastapi import APIRouter
from .user_api import router as user_router

router = APIRouter(prefix="/api",)
router.include_router(user_router)
