from fastapi import FastAPI

from app.api.routes import health, tenants
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    description="ComplyEdge multi-tenant compliance platform API (FastAPI scaffold).",
)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(tenants.router, prefix=settings.api_prefix)
