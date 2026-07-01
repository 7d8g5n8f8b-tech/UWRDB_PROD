# UWRDB – Universal Whisky Reference Database

Project: **Aqua Vitae – Magnum Opus**

UWRDB is an evidence-backed whisky reference database. Excel files are release artifacts, not the source of truth.

## Repository layout

- `data/` – source-of-truth CSV data used by the build pipeline.
- `schema/` – SQL schema.
- `scripts/` – import, promotion, validation and release scripts.
- `qa/` – validation rules and generated reports.
- `exports/` – generated build outputs.
- `releases/` – preserved human-facing regional and Scotland-wide releases.
- `docs/` – methodology, curation and release documentation.

## Current showable release

- `releases/Campbeltown/Gold_v0.1/`

## Recommended workflow

```bash
python scripts/import_swa_register.py
python scripts/promote_register.py
python scripts/build.py
python scripts/build_release_index.py
```
