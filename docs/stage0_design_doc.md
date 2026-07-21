# Stage 0 — Scope, Data, and Policy Docs

## The 3 Workflows

1. **Find invoice by vendor/date** (structured lookup)
   Maps directly to `GET /invoices?vendor=&start_date=&end_date=&status=`.

2. **Summarize open approvals for a manager** (structured lookup)
   Maps directly to `GET /approvals/pending?role=manager`.

3. **Flag invoices above the approval threshold** (hybrid: policy + data)
   Needs the €10,000 threshold rule from `policies/01_invoice_approval_thresholds.md`
   combined with live invoice amounts from the invoices table.

## Data Schema

| Table       | Key fields                                                        | Row count | Purpose |
|-------------|--------------------------------------------------------------------|-----------|---------|
| `vendors`   | vendor_id, name, company_code                                      | 15        | Who invoices come from |
| `invoices`  | invoice_id, vendor_id, amount, date, status                        | 75        | The core object the copilot queries |
| `approvals` | approval_id, invoice_id, approver_role, status, threshold           | 74        | Drives approval-limit and pending-approval scenarios |

Files: `data/vendors.csv`, `data/invoices.csv`, `data/approvals.csv`.

Policy docs (`policies/*.md`, 4 files): approval thresholds, invoice status
definitions, manager escalation/overrides, duplicate/suspicious invoice checks.

## Example User Questions per Workflow

**1. Find invoice by vendor/date**
- "Show me all invoices from Rheinmetall Components AG."
- "Which invoices from Nova Electronics Distribution are still unpaid?"
- "List invoices dated in December 2025."

**2. Summarize open approvals for a manager**
- "What approvals are currently pending for me?"
- "How many invoices are stuck waiting on a second manager approval?"
- "Show overdue invoices that also need approval."

**3. Flag invoices above the approval threshold** (hybrid)
- "Is invoice INV1001 over the approval threshold?"
- "Which unpaid invoices need two manager approvals?"
- "Is this €12,500 invoice from Baltic Steel Supply within a manager's single
  sign-off limit, or does it need a second approval?"

## Stage 0 Status
- [x] 3 workflows selected
- [x] Synthetic dataset written (vendors/invoices/approvals CSVs, 164 data rows)
- [x] 4 policy documents written covering thresholds and invoice rules
- [x] This design doc committed to the repo
