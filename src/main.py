from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.utils.helpers import import_members_from_package


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import all routers from the specified package
    routers = import_members_from_package("src.api.v1.endpoints", member_type=APIRouter)

    for router in routers:
        _app.include_router(router)

    return _app


app = get_application()
