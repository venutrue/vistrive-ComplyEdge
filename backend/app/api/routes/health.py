from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    settings = get_settings()
    database = "down"
    try:
        db.execute(text("SELECT 1"))
        database = "up"
    except Exception:
        database = "down"

    return HealthResponse(status="ok", service=settings.app_name, environment=settings.app_env, database=database)
def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", service=settings.app_name, environment=settings.app_env)
