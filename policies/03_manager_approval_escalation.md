# Manager Approval Escalation and Overrides

company_code: ALL
doc_type: approval_policy

Only users with the **Manager** role are permitted to approve invoices or view
override actions. AP Clerks can view invoice and vendor data but cannot approve
invoices or see override history.

- If an invoice above €10,000 has received only one of its two required
  approvals after 3 business days, it should be escalated to a second manager
  automatically rather than waiting indefinitely.
- A Manager may reject an invoice at any point in the approval chain. A
  rejected invoice returns to the AP Clerk for correction and does not proceed
  to payment.
- Manager override of the standard threshold rules (e.g. approving a
  >€10,000 invoice with only one approval) is only permitted in documented
  emergency-payment situations, and must be recorded with a written
  justification. This project's demo dataset does not model override records;
  override questions should be answered from this policy text alone, not from
  invoice data.
