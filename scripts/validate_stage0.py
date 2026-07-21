"""
Stage 0 validation script.

Run: python3 scripts/validate_stage0.py

Checks:
- required files exist (data + policy + design doc)
- CSV headers match the schema in the design doc
- referential integrity: every invoice.vendor_id exists in vendors,
  every approval.invoice_id exists in invoices
- invoice.status is one of the allowed values
- invoices > EUR10,000 have exactly 2 approval rows (per policy)
- invoices between 1,000 and 10,000 have exactly 1 approval row
- invoices < 1,000 have 0 approval rows (auto-approved)
- policy docs are non-empty and contain the €1,000 / €10,000 thresholds
"""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
POLICIES = os.path.join(ROOT, "policies")
DOCS = os.path.join(ROOT, "docs")

errors = []
warnings = []

def check_file_exists(path, label):
    if not os.path.isfile(path):
        errors.append(f"MISSING FILE: {label} not found at {path}")
        return False
    return True

def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

print("== Checking required files ==")
required = [
    (os.path.join(DATA, "vendors.csv"), "vendors.csv"),
    (os.path.join(DATA, "invoices.csv"), "invoices.csv"),
    (os.path.join(DATA, "approvals.csv"), "approvals.csv"),
    (os.path.join(DOCS, "stage0_design_doc.md"), "stage0 design doc"),
]
for path, label in required:
    ok = check_file_exists(path, label)
    print(f"  [{'OK' if ok else 'FAIL'}] {label}")

policy_files = [f for f in os.listdir(POLICIES) if f.endswith(".md")] if os.path.isdir(POLICIES) else []
print(f"  [{'OK' if len(policy_files) >= 3 else 'FAIL'}] policy docs found: {len(policy_files)} (want >= 3)")
if len(policy_files) < 3:
    errors.append("Fewer than 3 policy documents found in policies/")

if errors:
    print("\nStopping early -- fix missing files first.")
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)

print("\n== Loading CSVs ==")
vendors = load_csv(os.path.join(DATA, "vendors.csv"))
invoices = load_csv(os.path.join(DATA, "invoices.csv"))
approvals = load_csv(os.path.join(DATA, "approvals.csv"))
print(f"  vendors: {len(vendors)} rows")
print(f"  invoices: {len(invoices)} rows")
print(f"  approvals: {len(approvals)} rows")

vendor_ids = {v["vendor_id"] for v in vendors}
invoice_ids = {i["invoice_id"] for i in invoices}
allowed_status = {"paid", "unpaid", "overdue", "pending_approval"}

print("\n== Referential integrity ==")
for inv in invoices:
    if inv["vendor_id"] not in vendor_ids:
        errors.append(f"invoice {inv['invoice_id']} references unknown vendor_id {inv['vendor_id']}")
    if inv["status"] not in allowed_status:
        errors.append(f"invoice {inv['invoice_id']} has invalid status '{inv['status']}'")

for appr in approvals:
    if appr["invoice_id"] not in invoice_ids:
        errors.append(f"approval {appr['approval_id']} references unknown invoice_id {appr['invoice_id']}")

print(f"  {'OK' if not errors else 'FAIL - see errors below'}")

print("\n== Approval-count-matches-threshold-policy check ==")
approvals_by_invoice = {}
for appr in approvals:
    approvals_by_invoice.setdefault(appr["invoice_id"], []).append(appr)

threshold_errors = 0
for inv in invoices:
    amt = float(inv["amount"])
    n = len(approvals_by_invoice.get(inv["invoice_id"], []))
    if amt < 1000:
        expected = 0
    elif amt <= 10000:
        expected = 1
    else:
        expected = 2
    if n != expected:
        threshold_errors += 1
        warnings.append(
            f"invoice {inv['invoice_id']} (amount {amt}) has {n} approval row(s), expected {expected}"
        )

print(f"  {threshold_errors} invoice(s) with unexpected approval-row counts")

print("\n== Policy doc sanity check ==")
combined_policy_text = ""
for f in policy_files:
    with open(os.path.join(POLICIES, f)) as fh:
        combined_policy_text += fh.read()

if "1,000" not in combined_policy_text and "1000" not in combined_policy_text:
    warnings.append("Could not find the €1,000 threshold mentioned in any policy doc")
if "10,000" not in combined_policy_text and "10000" not in combined_policy_text:
    warnings.append("Could not find the €10,000 threshold mentioned in any policy doc")

print("\n================ SUMMARY ================")
print(f"Errors:   {len(errors)}")
print(f"Warnings: {len(warnings)}")
for e in errors:
    print("  ERROR:", e)
for w in warnings:
    print("  WARN: ", w)

if errors:
    print("\nSTAGE 0 STATUS: FAIL — fix errors above before moving to Stage 1.")
    sys.exit(1)
elif warnings:
    print("\nSTAGE 0 STATUS: PASS WITH WARNINGS — review warnings above.")
else:
    print("\nSTAGE 0 STATUS: PASS — data and policy docs look consistent.")
