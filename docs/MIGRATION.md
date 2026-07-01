# Migration Guide

## Existing repository

Keep your existing folders:

- `releases/`
- `docs/`
- `data/`
- `schema/`
- `scripts/`

Then copy this UWRDB 2.0 package over the repo root.

## Do not delete

Do not delete:

```text
releases/Campbeltown/Gold_v0.1/
```

That is your first public release.

## Migration workflow

1. Copy UWRDB 2.0 files into repo root.
2. Commit.
3. Run `python scripts/build_all.py`.
4. Confirm `exports/UWRDB_master.sqlite`.
5. Confirm `exports/UWRDB_master.xlsx`.
6. Confirm `exports/qa_report.md`.
