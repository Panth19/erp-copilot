from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    role: str


class InvoiceOut(BaseModel):
    invoice_id: str
    vendor_id: str
    vendor_name: str
    amount: float
    date: str
    status: str


class ApprovalOut(BaseModel):
    approval_id: str
    invoice_id: str
    approver_role: str
    status: str
    threshold: float
    invoice_amount: Optional[float] = None
    vendor_name: Optional[str] = None
