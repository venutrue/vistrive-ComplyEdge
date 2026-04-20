from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Establishment
from app.schemas.payroll import PayrollValidationRequest, PayrollValidationResponse

router = APIRouter(prefix="/payroll", tags=["payroll"])


@router.post("/validate", response_model=PayrollValidationResponse)
def validate_payroll(payload: PayrollValidationRequest, db: Session = Depends(get_db)) -> PayrollValidationResponse:
    establishment = db.query(Establishment).filter(Establishment.id == payload.establishment_id).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    issues: list[str] = []
    if payload.paid_wage < payload.min_wage:
        issues.append("Paid wage is below configured minimum wage")
    if payload.overtime_hours > 120:
        issues.append("Overtime hours exceed policy threshold")

    return PayrollValidationResponse(compliant=len(issues) == 0, issues=issues)
