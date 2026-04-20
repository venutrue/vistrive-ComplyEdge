from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ComplianceTask, Establishment, Filing, Notice, Tenant
from app.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    today = date.today()
    total_tenants = db.query(Tenant).count()
    total_establishments = db.query(Establishment).count()
    total_tasks = db.query(ComplianceTask).count()
    overdue_tasks = db.query(ComplianceTask).filter(ComplianceTask.due_date < today).count()
    open_notices = db.query(Notice).filter(Notice.status == "open").count()
    draft_filings = db.query(Filing).filter(Filing.status == "draft").count()

    return DashboardSummary(
        total_tenants=total_tenants,
        total_establishments=total_establishments,
        total_tasks=total_tasks,
        overdue_tasks=overdue_tasks,
        open_notices=open_notices,
        draft_filings=draft_filings,
    )
