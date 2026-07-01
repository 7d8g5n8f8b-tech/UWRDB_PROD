# Architecture

## Core tables

- `distillery`
- `brand`
- `owner`
- `parent_company`
- `region`
- `source`
- `evidence`

## Design rule

Each physical production site appears once in `distillery`.

Brands, expressions, owners, and evidence are linked relationally.
