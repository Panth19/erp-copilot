# Enterprise AI Copilot for ERP

A natural-language copilot layered on top of mock SAP S/4HANA-style ERP data
(invoices, vendors, approvals) combining retrieval-augmented generation over
policy documents with live structured-data lookups and role-based access
control. See `docs/Project1_ERP_Copilot_Plan.pdf` for the full build plan.

## Status

- [x] **Stage 0** — scope, synthetic data, policy docs (this commit)
- [ ] Stage 1 — FastAPI + mock ERP + auth
- [ ] Stage 2 — RAG copilot backend
- [ ] Stage 3 — React chat UI
- [ ] Stage 4 — Docker, docs, recorded demo

## Repo layout

```
data/        synthetic vendors/invoices/approvals CSVs
policies/    policy documents the RAG layer will index
docs/        design docs and the original build plan
scripts/     helper/validation scripts
```

## Stage 0 — verifying it's good

```
python3 scripts/validate_stage0.py
```

This checks: required files exist, CSV referential integrity (every invoice
points to a real vendor, every approval points to a real invoice), invoice
statuses are valid, approval-row counts match the approval-threshold policy
(0 rows under €1,000, 1 row €1,000–€10,000, 2 rows above €10,000), and the
policy docs actually mention the €1,000 / €10,000 thresholds. It exits
non-zero if anything is broken.

## Next step

Stage 1: implement `GET /invoices`, `GET /approvals/pending`, and
`POST /auth/login` in FastAPI against this dataset.
