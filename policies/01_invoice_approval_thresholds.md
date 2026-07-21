# Invoice Approval Thresholds

company_code: ALL
doc_type: approval_policy

This policy defines the approval workflow required before an invoice can be paid,
based on the invoice amount (in EUR).

- **Invoices under €1,000**: auto-approved. No manager sign-off is required. These
  invoices move directly to the payment queue once received and validated.
- **Invoices between €1,000 and €10,000 (inclusive)**: require a single Manager
  approval before payment can be released.
- **Invoices above €10,000**: require **two separate Manager approvals** before
  payment can be released. A single manager approving twice does not satisfy this
  rule — two distinct approval actions are required.

An invoice is considered "over the approval threshold" if its amount is greater
than €10,000, since that is the point at which the two-approval rule applies.

If an invoice has been sitting with a status of "pending_approval" for more than
5 business days, it should be flagged in the "open approvals" summary shown to
managers.
