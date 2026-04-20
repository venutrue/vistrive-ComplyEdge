from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ObligationTemplate, Regulation, Rule
from app.schemas.rules import (
    ObligationTemplateCreateRequest,
    ObligationTemplateResponse,
    RegulationCreateRequest,
    RegulationResponse,
    RuleCreateRequest,
    RuleResponse,
)
from app.services.audit import log_event

router = APIRouter(prefix="/rules", tags=["rules"])


@router.post("/regulations", response_model=RegulationResponse, status_code=status.HTTP_201_CREATED)
def create_regulation(payload: RegulationCreateRequest, db: Session = Depends(get_db)) -> RegulationResponse:
    regulation = Regulation(code_name=payload.code_name)
    db.add(regulation)
    db.commit()
    db.refresh(regulation)
    log_event(db, "system", "regulation", regulation.id, "created", payload.model_dump())
    return RegulationResponse.model_validate(regulation)


@router.post("", response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
def create_rule(payload: RuleCreateRequest, db: Session = Depends(get_db)) -> RuleResponse:
    regulation = db.query(Regulation).filter(Regulation.id == payload.regulation_id).first()
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")

    rule = Rule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    log_event(db, "system", "rule", rule.id, "created", payload.model_dump())
    return RuleResponse.model_validate(rule)


@router.post("/obligations", response_model=ObligationTemplateResponse, status_code=status.HTTP_201_CREATED)
def create_obligation(payload: ObligationTemplateCreateRequest, db: Session = Depends(get_db)) -> ObligationTemplateResponse:
    rule = db.query(Rule).filter(Rule.id == payload.rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    obligation = ObligationTemplate(**payload.model_dump())
    db.add(obligation)
    db.commit()
    db.refresh(obligation)
    log_event(db, "system", "obligation_template", obligation.id, "created", payload.model_dump())
    return ObligationTemplateResponse.model_validate(obligation)
