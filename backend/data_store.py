"""
Loads the Stage 0 CSVs into memory once at import time and exposes simple
filter functions. No database needed for this scale of demo data.
"""
import csv
import os
from datetime import datetime
from config import settings


def _load_csv(filename):
    path = os.path.join(settings.DATA_DIR, filename)
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


_vendors_raw = _load_csv("vendors.csv")
_invoices_raw = _load_csv("invoices.csv")
_approvals_raw = _load_csv("approvals.csv")

# Build a vendor lookup so invoice responses can include the vendor name
_vendor_by_id = {v["vendor_id"]: v for v in _vendors_raw}


def _parse_invoice(row):
    return {
        "invoice_id": row["invoice_id"],
        "vendor_id": row["vendor_id"],
        "vendor_name": _vendor_by_id.get(row["vendor_id"], {}).get("name", "Unknown vendor"),
        "amount": float(row["amount"]),
        "date": row["date"],
        "status": row["status"],
    }


def _parse_approval(row):
    return {
        "approval_id": row["approval_id"],
        "invoice_id": row["invoice_id"],
        "approver_role": row["approver_role"],
        "status": row["status"],
        "threshold": float(row["threshold"]),
    }


VENDORS = _vendors_raw
INVOICES = [_parse_invoice(r) for r in _invoices_raw]
APPROVALS = [_parse_approval(r) for r in _approvals_raw]

# Fast lookup for joining approvals -> invoice info
_invoice_by_id = {inv["invoice_id"]: inv for inv in INVOICES}


def get_invoices(vendor: str = None, start_date: str = None, end_date: str = None, status: str = None):
    """Filter invoices by vendor name (partial, case-insensitive), date range, and status."""
    results = INVOICES

    if vendor:
        v = vendor.lower()
        results = [i for i in results if v in i["vendor_name"].lower() or v == i["vendor_id"].lower()]

    if start_date:
        start = datetime.fromisoformat(start_date)
        results = [i for i in results if datetime.fromisoformat(i["date"]) >= start]

    if end_date:
        end = datetime.fromisoformat(end_date)
        results = [i for i in results if datetime.fromisoformat(i["date"]) <= end]

    if status:
        results = [i for i in results if i["status"].lower() == status.lower()]

    return results


def get_pending_approvals_for_role(role: str):
    """Approvals with status 'pending' that this role is responsible for,
    enriched with the parent invoice's info."""
    pending = [a for a in APPROVALS if a["status"] == "pending" and a["approver_role"] == role]
    enriched = []
    for a in pending:
        inv = _invoice_by_id.get(a["invoice_id"], {})
        enriched.append({**a, "invoice_amount": inv.get("amount"), "vendor_name": inv.get("vendor_name")})
    return enriched
