from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.models import User
from app.schemas.auth import LoginRequest, LoginResponse, MfaVerifyRequest, MfaVerifyResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    settings = get_settings()
    user = db.query(User).filter(User.email == payload.email, User.is_active.is_(True)).first()
    tenant_id = payload.tenant_id
    role = payload.role

    if user:
        tenant_id = user.tenant_id
        role = "Compliance Admin"

    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tenant_id is required for bootstrap login")

    ttl = settings.access_token_minutes * (24 if payload.remember_device else 1)
    token = create_access_token(subject=payload.email, tenant_id=tenant_id, role=role, minutes=ttl)
    return LoginResponse(access_token=token, mfa_required=True)


@router.post("/mfa/verify", response_model=MfaVerifyResponse)
def verify_mfa(payload: MfaVerifyRequest) -> MfaVerifyResponse:
    settings = get_settings()
    return MfaVerifyResponse(verified=payload.otp_code == settings.mfa_static_otp)
