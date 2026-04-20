from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import Principal, get_current_principal
from app.db.session import get_db
from app.models import Notification, Tenant
from app.schemas.notifications import NotificationCreateRequest, NotificationResponse
from app.services.audit import log_event

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(
    payload: NotificationCreateRequest,
    principal: Principal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> NotificationResponse:
    if payload.tenant_id != principal.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot create notification for another tenant")

    tenant = db.query(Tenant).filter(Tenant.id == payload.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    notification = Notification(**payload.model_dump())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    log_event(db, "system", "notification", notification.id, "queued", payload.model_dump())
    return NotificationResponse.model_validate(notification)


@router.get("", response_model=list[NotificationResponse])
def list_notifications(
    principal: Principal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> list[NotificationResponse]:
    notifications = db.query(Notification).filter(Notification.tenant_id == principal.tenant_id).all()
    return [NotificationResponse.model_validate(n) for n in notifications]


@router.post("/{notification_id}/send", response_model=NotificationResponse)
def send_notification(
    notification_id: str,
    principal: Principal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> NotificationResponse:
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.tenant_id != principal.tenant_id:
        raise HTTPException(status_code=403, detail="Tenant mismatch")

    notification.status = "sent"
    db.commit()
    db.refresh(notification)
    log_event(db, "system", "notification", notification.id, "sent", {"status": "sent"})
    return NotificationResponse.model_validate(notification)
