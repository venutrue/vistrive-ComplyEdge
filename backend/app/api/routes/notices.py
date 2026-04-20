from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Establishment, Notice
from app.services.audit import log_event

router = APIRouter(prefix="/notices", tags=["notices"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_notice(payload: dict, db: Session = Depends(get_db)) -> dict:
    establishment_id = payload.get("establishment_id")
    title = payload.get("title")
    if not establishment_id or not title:
        raise HTTPException(status_code=422, detail="establishment_id and title are required")

    establishment = db.query(Establishment).filter(Establishment.id == establishment_id).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Establishment not found")

    notice = Notice(establishment_id=establishment_id, title=title, status=payload.get("status", "open"))
    db.add(notice)
    db.commit()
    db.refresh(notice)

    log_event(db, "system", "notice", notice.id, "created", payload)
    return {"id": notice.id, "status": notice.status, "title": notice.title}
