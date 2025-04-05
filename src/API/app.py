from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .routers import prepare_routers


class ChatbotFastAPIApp:
    def start():
        _app = FastAPI(title=settings.PROJECT_NAME)

        _app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Add routers to the application
        routers = prepare_routers()  # Get routers from the preparation function
        for router in routers:
            _app.include_router(router)

        return _app
