from fastapi import Depends, Header, HTTPException, Request, status

from app.core.security import decode_access_token


class Principal:
    def __init__(self, email: str, tenant_id: str, role: str):
        self.email = email
        self.tenant_id = tenant_id
        self.role = role


def get_tenant_header(request: Request, x_tenant_id: str = Header(default="")) -> str:
    path = request.url.path
    if path.endswith("/health") or "/auth/" in path:
        return x_tenant_id

    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header is required")
    return x_tenant_id


def get_current_principal(
    request: Request,
    tenant_header: str = Depends(get_tenant_header),
    authorization: str = Header(default=""),
) -> Principal:
    path = request.url.path
    if path.endswith("/health") or "/auth/" in path:
        return Principal(email="anonymous", tenant_id=tenant_header or "", role="anonymous")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    if tenant_header and payload.get("tenant_id") != tenant_header:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant mismatch")

    return Principal(email=payload["sub"], tenant_id=payload["tenant_id"], role=payload["role"])


def require_roles(*roles: str):
    def _dep(principal: Principal = Depends(get_current_principal)) -> Principal:
        if principal.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return principal

    return _dep
