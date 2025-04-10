from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..modules.utils import ModuleInitializer
from .core import logging, middleware
from .core.exceptions.errors import APIError
from .core.exceptions.handlers import global_exception_handler
from .core.utils.import_helpers import get_settings
from .core.utils.routing import collect_routers


class APIFactory:
    def __init__(self):
        self.app: Optional[FastAPI] = None
        self.settings = get_settings()

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        """Async context manager for application lifespan events"""
        # Startup logic
        logging.configure_logging()
        yield
        # Shutdown logic (none needed in this simplified version)

    def create_app(self) -> FastAPI:
        """Factory method for creating and configuring the FastAPI application"""
        self.app = FastAPI(
            title=self.settings.PROJECT_NAME,
            version=self.settings.API_VERSION,
            description=self.settings.API_DESCRIPTION,
            lifespan=self._lifespan,
            docs_url=self.settings.DOCS_URL if self.settings.ENABLE_DOCS else None,
            redoc_url=self.settings.REDOC_URL if self.settings.ENABLE_DOCS else None,
            contact=self.settings.CONTACT_INFO,
            license_info=self.settings.LICENSE_INFO,
            openapi_url=self.settings.OPENAPI_URL if self.settings.ENABLE_DOCS else None,
        )

        self._init_modules()
        self._configure_middleware()
        self._register_exception_handlers()
        self._register_routers()

        return self.app

    def run(self, **uvicorn_kwargs):
        """
        Run the FastAPI application using Uvicorn with settings integration

        Args:
            **uvicorn_kwargs: Additional arguments to pass to uvicorn.run()
        """
        if not self.app:
            self.create_app()

        uvicorn.run(
            app=self.app,
            host=self.settings.HOST,
            port=self.settings.PORT,
            reload=self.settings.DEBUG,
            workers=self.settings.WORKERS if not self.settings.DEBUG else 1,
            log_level="debug" if self.settings.DEBUG else "info",
            **uvicorn_kwargs,
        )

    def _configure_middleware(self):
        """Configure essential middleware"""
        self.app.add_middleware(middleware.SecurityHeadersMiddleware)

        if self.settings.CORS_ENABLED:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=self.settings.CORS_ORIGINS,
                allow_credentials=self.settings.CORS_ALLOW_CREDENTIALS,
                allow_methods=self.settings.CORS_ALLOW_METHODS,
                allow_headers=self.settings.CORS_ALLOW_HEADERS,
            )

    def _register_routers(self):
        """Register all API routers"""
        routers = collect_routers()
        for router in routers:
            self.app.include_router(
                router, prefix=f"/api/{self.settings.API_VERSION}", tags=[router.tags[0]] if router.tags else None
            )

    def _register_exception_handlers(self):
        """Register exception handlers"""
        for error in APIError.__subclasses__():
            self.app.add_exception_handler(error, global_exception_handler)
        self.app.add_exception_handler(Exception, global_exception_handler)

    def _init_modules(self):
        """Initialize all modules"""
        ModuleInitializer.initialize()


app = APIFactory().create_app()
