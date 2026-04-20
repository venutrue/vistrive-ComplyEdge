from app.schemas.common import APIModel


class RoleCreateRequest(APIModel):
    name: str


class RoleResponse(APIModel):
    id: str
    name: str


class UserCreateRequest(APIModel):
    tenant_id: str
    email: str
    full_name: str
    role_id: str


class UserResponse(APIModel):
    id: str
    tenant_id: str
    email: str
    full_name: str
    role_id: str
    is_active: bool
