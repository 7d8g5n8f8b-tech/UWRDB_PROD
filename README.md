# UWRDB 2.0

**Universal Whisky Reference Database**  
Project: **Aqua Vitae – Magnum Opus**

UWRDB 2.0 is database-first.

CSV files remain human-editable source tables, but the canonical build path is:

```text
data/core/*.csv
        ↓
schema/schema.sql
        ↓
SQLite
        ↓
Excel / CSV / QA / release bundles
```

## Quick start

```bash
pip install -r requirements.txt
python scripts/build_all.py
```

Outputs are written to `exports/`.

## Why 2.0?

The earlier foundation proved the workflow. This version reorganizes it into a maintainable package:

- database-first architecture
- modular Python package
- stable domain tables
- reproducible releases
- regional release builder
- migration notes for existing Campbeltown release
