from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Rule
from app.schemas.ai import CopilotQueryRequest, CopilotResponse

router = APIRouter(prefix="/copilot", tags=["ai-copilot"])


@router.post("/query", response_model=CopilotResponse)
def copilot_query(payload: CopilotQueryRequest, db: Session = Depends(get_db)) -> CopilotResponse:
    top_rule = db.query(Rule).order_by(Rule.effective_from.desc()).first()
    if top_rule:
        answer = (
            f"Applicable guidance: '{top_rule.name}'. This answer is generated from configured rule catalog and "
            "must be reviewed by compliance/legal owner before filing."
        )
        citations = [top_rule.source_reference]
        confidence = 0.72
    else:
        answer = "No rule data is configured yet for your tenant context."
        citations = []
        confidence = 0.3

    return CopilotResponse(
        answer=answer,
        confidence=confidence,
        citations=citations,
        requires_human_review=True,
    )
