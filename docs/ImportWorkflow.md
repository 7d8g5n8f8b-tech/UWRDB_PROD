# Import Workflow

1. Place raw operating register rows in `data/raw/swa/operating_distilleries.csv`.
2. Run `python scripts/import_swa_register.py`.
3. Review `data/staging/distillery_import_review.csv`.
4. Run `python scripts/build.py`.
5. Enrich values using `scripts/add_evidence.py`.
