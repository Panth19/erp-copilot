from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Response, Request, status as http_status
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError

import auth
import data_store as ds
from config import settings
from models import LoginRequest, LoginResponse, InvoiceOut, ApprovalOut

app = FastAPI(title="ERP Copilot API -- Stage 1 (mock ERP + auth, no LLM yet)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Auth dependency (Step 7) ----------
def get_current_user(request: Request) -> dict:
    """Reads the JWT from the HttpOnly cookie, validates it, and returns
    {'user_id': ..., 'role': ...}. Raises 401 if missing/invalid/expired."""
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = auth.decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return {"user_id": payload["sub"], "role": payload["role"]}


def require_role(required_role: str):
    """Dependency factory: only allow through if current user has this role."""
    def dependency(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] != required_role:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail=f"This action requires the '{required_role}' role",
            )
        return user
    return dependency


# ---------- Auth endpoint (Step 6) ----------
@app.post("/auth/login", response_model=LoginResponse)
def login(body: LoginRequest, response: Response):
    user = auth.authenticate_user(body.username, body.password)
    if not user:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = auth.create_access_token(user_id=user["user_id"], role=user["role"])
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
    )
    return LoginResponse(message="Login successful", role=user["role"])


@app.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(settings.COOKIE_NAME)
    return {"message": "Logged out"}


# ---------- Invoices endpoint (Step 8) ----------
@app.get("/invoices", response_model=list[InvoiceOut])
def list_invoices(
    vendor: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    user: dict = Depends(get_current_user),
):
    try:
        return ds.get_invoices(vendor=vendor, start_date=start_date, end_date=end_date, status=status)
    except ValueError:
        raise HTTPException(
            status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="start_date and end_date must be in YYYY-MM-DD format",
        )


# ---------- Approvals endpoint (Step 9, manager-only) ----------
@app.get("/approvals/pending", response_model=list[ApprovalOut])
def pending_approvals(user: dict = Depends(require_role("manager"))):
    return ds.get_pending_approvals_for_role("manager")


@app.get("/health")
def health():
    return {"status": "ok"}
