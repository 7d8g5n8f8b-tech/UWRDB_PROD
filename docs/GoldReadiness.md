# Gold Readiness

Gold readiness is measured, not guessed.

## Core identity fields

- official_name
- region_id
- type
- status
- owner_id
- parent_company_id

## Gold evidence

A Gold field requires an evidence record with:

- matching `entity_id`
- matching `field_name`
- `verification_status = gold`
- `evidence_strength >= 4`
