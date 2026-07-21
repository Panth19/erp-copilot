# Invoice Status Definitions

company_code: ALL
doc_type: reference

Every invoice in the system carries one of four statuses:

- **paid** — the invoice has been fully settled and no further action is needed.
- **unpaid** — the invoice has passed approval (or did not need it) but has not
  yet been paid. It is within its normal payment terms.
- **overdue** — the invoice is unpaid and has passed its due date. Overdue
  invoices should be surfaced to the AP Clerk as a priority.
- **pending_approval** — the invoice is currently waiting on one or more Manager
  approvals as defined in the Invoice Approval Thresholds policy, and cannot be
  paid until those approvals are completed.

A vendor is considered to have "unpaid invoices" if any of their invoices carry
a status of unpaid, overdue, or pending_approval.
