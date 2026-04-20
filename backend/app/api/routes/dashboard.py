from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import Principal, get_current_principal
from app.db.session import get_db
from app.models import ComplianceTask, Establishment, Filing, LegalEntity, Notice, Tenant
from app.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    principal: Principal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> DashboardSummary:
    today = date.today()

    legal_entity_ids = [e.id for e in db.query(LegalEntity).filter(LegalEntity.tenant_id == principal.tenant_id).all()]
    establishment_ids = [
        e.id for e in db.query(Establishment).filter(Establishment.legal_entity_id.in_(legal_entity_ids)).all()
    ] if legal_entity_ids else []

    total_tenants = db.query(Tenant).filter(Tenant.id == principal.tenant_id).count()
    total_establishments = len(establishment_ids)
    total_tasks = db.query(ComplianceTask).filter(ComplianceTask.establishment_id.in_(establishment_ids)).count() if establishment_ids else 0
    overdue_tasks = (
        db.query(ComplianceTask)
        .filter(ComplianceTask.establishment_id.in_(establishment_ids), ComplianceTask.due_date < today)
        .count()
        if establishment_ids
        else 0
    )
    open_notices = db.query(Notice).filter(Notice.establishment_id.in_(establishment_ids), Notice.status == "open").count() if establishment_ids else 0
    draft_filings = db.query(Filing).filter(Filing.establishment_id.in_(establishment_ids), Filing.status == "draft").count() if establishment_ids else 0

    return DashboardSummary(
        total_tenants=total_tenants,
        total_establishments=total_establishments,
        total_tasks=total_tasks,
        overdue_tasks=overdue_tasks,
        open_notices=open_notices,
        draft_filings=draft_filings,
    )
