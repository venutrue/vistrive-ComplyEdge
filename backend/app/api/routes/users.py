from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import Principal, get_current_principal, require_roles
from app.db.session import get_db
from app.models import Role, Tenant, User
from app.schemas.users import RoleCreateRequest, RoleResponse, UserCreateRequest, UserResponse
from app.services.audit import log_event

router = APIRouter(prefix="/users", tags=["users-rbac"])


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreateRequest,
    _: Principal = Depends(require_roles("Compliance Admin", "Super Admin")),
    db: Session = Depends(get_db),
) -> RoleResponse:
def create_role(payload: RoleCreateRequest, db: Session = Depends(get_db)) -> RoleResponse:
    role = Role(name=payload.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return RoleResponse.model_validate(role)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreateRequest,
    principal: Principal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> UserResponse:
    if payload.tenant_id != principal.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot create user for another tenant")

def create_user(payload: UserCreateRequest, db: Session = Depends(get_db)) -> UserResponse:
    tenant = db.query(Tenant).filter(Tenant.id == payload.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    role = db.query(Role).filter(Role.id == payload.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user = User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    log_event(db, "system", "user", user.id, "created", payload.model_dump())
    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
def list_users(
    principal: Principal = Depends(get_current_principal),
    db: Session = Depends(get_db),
) -> list[UserResponse]:
    users = db.query(User).filter(User.tenant_id == principal.tenant_id).all()
    return [UserResponse.model_validate(u) for u in users]
