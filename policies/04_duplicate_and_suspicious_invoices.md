# Duplicate and Suspicious Invoice Detection

company_code: ALL
doc_type: control_policy

To reduce the risk of duplicate or fraudulent payment, the following checks
apply before an invoice can move to paid status:

- Two invoices from the **same vendor** with the **same amount** and a date
  within **7 days** of each other should be flagged as a potential duplicate
  and held for manual review rather than auto-approved, even if the amount is
  under €1,000.
- A vendor with more than 3 invoices marked **overdue** at the same time should
  be flagged for review, since this may indicate a payment processing issue or
  a vendor relationship problem.
- Invoices with an amount that is unusually large compared to a vendor's
  historical average (more than 5x their typical invoice size) should be
  routed for Manager review regardless of the standard threshold rules.

These checks are advisory guardrails for the copilot to reference when asked
about "suspicious" or "unusual" invoices; they are not automated blocks in
this demo system.
