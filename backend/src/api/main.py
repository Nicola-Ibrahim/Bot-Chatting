import os
from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from ..initializer import BackendInitializer
from .core import middleware
from .core.config import get_settings
from .core.config.dev import Settings as DevSettings
from .core.exceptions.errors import APIError
from .core.exceptions.handlers import global_exception_handler
from .routing import collect_routers


# TODO: Split the settings of api settings the modules settings, for cleaner initialization
class APIFactory:
    def __init__(self):
        self.app: Optional[FastAPI] = None

        raw_settings = DevSettings()
        settings_dict = (
            raw_settings
            if isinstance(raw_settings, dict)
            else (raw_settings.model_dump() if hasattr(raw_settings, "model_dump") else raw_settings.__dict__)
        )

        # 🔹 Split once, keep dict-only
        self.api_cfg = settings_dict.get("api", {})
        self.modules_cfg = settings_dict.get("modules", settings_dict)  # fallback to legacy flat shape

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        # 🔹 Initialize modules with separated configs
        handles = BackendInitializer.initialize(self.modules_cfg)

        # Optional: expose handles for routers/tests
        app.state.modules = handles

        try:
            yield
        finally:
            if handles:
                handles.shutdown()

    def create_app(self) -> FastAPI:
        self.app = FastAPI(
            title=self.api_cfg.get("PROJECT_NAME", "API"),
            version=self.api_cfg.get("API_VERSION", "v1"),
            description=self.api_cfg.get("API_DESCRIPTION", ""),
            lifespan=self._lifespan,  # 🔹 use lifespan (recommended)
            docs_url=self.api_cfg.get("DOCS_URL") if self.api_cfg.get("ENABLE_DOCS", True) else None,
            redoc_url=self.api_cfg.get("REDOC_URL") if self.api_cfg.get("ENABLE_DOCS", True) else None,
            contact=self.api_cfg.get("CONTACT_INFO"),
            license_info=self.api_cfg.get("LICENSE_INFO"),
            openapi_url=self.api_cfg.get("OPENAPI_URL") if self.api_cfg.get("ENABLE_DOCS", True) else None,
        )

        self._configure_middleware()
        self._register_exception_handlers()
        self._register_routers()
        self._mount_frontend()
        return self.app

    def run(self, **uvicorn_kwargs):
        if not self.app:
            self.create_app()
        uvicorn.run(
            app=self.app,
            host=self.api_cfg.get("HOST", "0.0.0.0"),
            port=self.api_cfg.get("PORT", 8000),
            reload=self.api_cfg.get("DEBUG", False),
            workers=self.api_cfg.get("WORKERS", 1) if not self.api_cfg.get("DEBUG", False) else 1,
            log_level="debug" if self.api_cfg.get("DEBUG", False) else "info",
            **uvicorn_kwargs,
        )

    def _configure_middleware(self):
        self.app.add_middleware(middleware.SecurityHeadersMiddleware)
        if self.api_cfg.get("CORS_ENABLED", True):
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=self.api_cfg.get("CORS_ORIGINS", ["*"]),
                allow_credentials=self.api_cfg.get("CORS_ALLOW_CREDENTIALS", True),
                allow_methods=self.api_cfg.get("CORS_ALLOW_METHODS", ["*"]),
                allow_headers=self.api_cfg.get("CORS_ALLOW_HEADERS", ["*"]),
            )

    def _register_routers(self):
        routers = collect_routers()
        for router in routers:
            self.app.include_router(
                router,
                prefix=f"/api/{self.api_cfg.get('API_VERSION', 'v1')}",
                tags=[router.tags[0]] if router.tags else None,
            )

    def _register_exception_handlers(self):
        for error in APIError.__subclasses__():
            self.app.add_exception_handler(error, global_exception_handler)
        self.app.add_exception_handler(Exception, global_exception_handler)

    def _mount_frontend(self) -> None:
        try:
            if self.app is None:
                return
            base_dir = os.path.dirname(os.path.abspath(__file__))
            frontend_path = os.path.join(base_dir, "..", "frontend")
            if os.path.isdir(frontend_path):
                self.app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
        except Exception:
            import logging as _logging

            _logging.getLogger(__name__).exception("An error occurred while mounting the frontend directory")


# Module-level app for ASGI servers (e.g., uvicorn expects `app`)
app = APIFactory().create_app()
