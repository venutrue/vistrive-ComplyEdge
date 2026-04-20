from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    auth,
    copilot,
    dashboard,
    establishments,
    filings,
    health,
    incidents,
    inspections,
    legal_entities,
    notices,
    notifications,
    payroll,
    rules,
    tasks,
    tenants,
    users,
)
from app.core.config import get_settings
from app.db.session import engine
from app.models import Base
from app.api.routes import health, tenants
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.5.0",
    version="0.4.0",
    debug=settings.debug,
    description="ComplyEdge multi-tenant compliance platform API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(tenants.router, prefix=settings.api_prefix)
app.include_router(legal_entities.router, prefix=settings.api_prefix)
app.include_router(establishments.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(rules.router, prefix=settings.api_prefix)
app.include_router(tasks.router, prefix=settings.api_prefix)
app.include_router(filings.router, prefix=settings.api_prefix)
app.include_router(notices.router, prefix=settings.api_prefix)
app.include_router(incidents.router, prefix=settings.api_prefix)
app.include_router(notifications.router, prefix=settings.api_prefix)
app.include_router(dashboard.router, prefix=settings.api_prefix)
app.include_router(inspections.router, prefix=settings.api_prefix)
app.include_router(payroll.router, prefix=settings.api_prefix)
app.include_router(copilot.router, prefix=settings.api_prefix)
    version="0.1.0",
    debug=settings.debug,
    description="ComplyEdge multi-tenant compliance platform API (FastAPI scaffold).",
)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(tenants.router, prefix=settings.api_prefix)
