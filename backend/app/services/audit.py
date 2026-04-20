import json

from sqlalchemy.orm import Session

from app.models import AuditEvent


def log_event(db: Session, actor: str, entity_type: str, entity_id: str, action: str, details: dict) -> None:
    event = AuditEvent(
        actor=actor,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        details=json.dumps(details, default=str),
    )
    db.add(event)
    db.commit()
