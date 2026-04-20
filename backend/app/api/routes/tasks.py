from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ComplianceTask, Establishment
from app.schemas.tasks import ComplianceTaskResponse, GenerateTasksRequest
from app.services.applicability import generate_tasks_for_establishment
from app.services.audit import log_event

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/generate", response_model=list[ComplianceTaskResponse], status_code=status.HTTP_201_CREATED)
def generate_tasks(payload: GenerateTasksRequest, db: Session = Depends(get_db)) -> list[ComplianceTaskResponse]:
    establishment = db.query(Establishment).filter(Establishment.id == payload.establishment_id).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    tasks = generate_tasks_for_establishment(db, establishment)
    log_event(
        db,
        actor="system",
        entity_type="compliance_task",
        entity_id=establishment.id,
        action="generated",
        details={"count": len(tasks), "establishment_id": establishment.id},
    )
    return [ComplianceTaskResponse.model_validate(task) for task in tasks]


@router.get("/establishment/{establishment_id}", response_model=list[ComplianceTaskResponse])
def list_tasks(establishment_id: str, db: Session = Depends(get_db)) -> list[ComplianceTaskResponse]:
    tasks = db.query(ComplianceTask).filter(ComplianceTask.establishment_id == establishment_id).all()
    return [ComplianceTaskResponse.model_validate(task) for task in tasks]
