from app.schemas.common import APIModel


class PayrollValidationRequest(APIModel):
    establishment_id: str
    min_wage: float
    paid_wage: float
    overtime_hours: float = 0


class PayrollValidationResponse(APIModel):
    compliant: bool
    issues: list[str]
