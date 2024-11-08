from fastapi import APIRouter

from .auth import router as AuthApiRouter
from .users import router as UserApiRouter

router = APIRouter()
router.include_router(AuthApiRouter)
router.include_router(UserApiRouter)
