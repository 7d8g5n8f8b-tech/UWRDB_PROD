# Canonical Distillery Register

The canonical register is the trunk of UWRDB.

## Rule

One physical production site = one `distillery_id`.

Brands, expressions, historic aliases, owners, technical details, and evidence are linked separately.

## Workflow

1. Put raw operating list rows in `data/raw/swa/operating_distilleries.csv`.
2. Run `scripts/import_swa_register.py`.
3. Review `data/staging/distillery_import_review.csv`.
4. Run `scripts/promote_register.py`.
5. Run `scripts/build.py`.
6. Review `qa/reports/qa_report.md`.
7. Review `qa/reports/gold_readiness.md`.
