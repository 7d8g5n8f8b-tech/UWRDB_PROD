# UWRDB 2.0 Architecture

## Principle

The database is the product. Excel is an export.

## Core tables

- `region`
- `parent_company`
- `owner`
- `distillery`
- `brand`
- `source`
- `evidence`
- `release`

## Folders

```text
data/core/      canonical CSV source tables
schema/         SQL schema
uwrdb/          Python package
scripts/        command entrypoints
exports/        generated outputs
data/releases/  generated release metadata
```

## Migration from v1 foundation

Existing release artifacts stay in `releases/`. Canonical data should be progressively migrated into `data/core/`.
