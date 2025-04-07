from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import exceptions, logging, middleware
from .routers import prepare_routers
from .utils.import_helpers import get_settings


class APIFactory:
    def __init__(self):
        self._app = None
        self.settings = get_settings()

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        # Startup logic
        logging.configure_logging()
        yield
        # Shutdown logic (none needed in this simplified version)

    def create_app(self) -> FastAPI:
        """Factory method for creating and configuring the FastAPI application"""
        app = FastAPI(
            title=self.settings.PROJECT_NAME,
            version=self.settings.API_VERSION,
            description=self.settings.API_DESCRIPTION,
            lifespan=self._lifespan,
            docs_url=self.settings.DOCS_URL,
            redoc_url=self.settings.REDOC_URL,
            contact=self.settings.CONTACT_INFO,
            license_info=self.settings.LICENSE_INFO,
            openapi_url=self.settings.OPENAPI_URL,
        )

        # Configure middleware
        self._configure_middleware(app)

        # Register exception handlers
        exceptions.register_exception_handlers(app)

        # Add API routes
        self._register_routers(app)

        return app

    def _configure_middleware(self, app: FastAPI):
        """Configure essential middleware"""
        # Security headers middleware
        app.add_middleware(middleware.SecurityHeadersMiddleware)

        # CORS configuration
        if self.settings.CORS_ENABLED:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=self.settings.CORS_ORIGINS,
                allow_credentials=self.settings.CORS_ALLOW_CREDENTIALS,
                allow_methods=self.settings.CORS_ALLOW_METHODS,
                allow_headers=self.settings.CORS_ALLOW_HEADERS,
            )

    def _register_routers(self, app: FastAPI):
        """Register all API routers"""
        routers = prepare_routers()
        for router in routers:
            app.include_router(
                router, prefix=f"/api/{self.settings.API_VERSION}", tags=[router.tags[0]] if router.tags else None
            )
