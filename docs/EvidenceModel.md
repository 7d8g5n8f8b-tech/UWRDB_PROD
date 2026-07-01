# Evidence Model

UWRDB treats evidence as first-class data.

A fact is not simply stored as a value. It should be supportable by an evidence record:

| Column | Meaning |
|---|---|
| evidence_id | Permanent identifier for one evidence claim |
| entity_type | distillery, brand, owner, source, etc. |
| entity_id | ID of the entity being supported |
| field_name | Field being evidenced |
| field_value | Value asserted |
| source_id | Source supporting the value |
| evidence_strength | 1–5 strength of evidence |
| verification_status | captured, verified, reviewed, gold |
| verified_date | Date checked |

## Evidence strength

| Score | Meaning |
|---:|---|
| 5 | Official source plus corroboration |
| 4 | Official source |
| 3 | Reliable secondary source |
| 2 | Limited or conflicting evidence |
| 1 | Historical or uncertain |

## Gold rule

A field is only Gold when:
- evidence exists,
- source exists,
- evidence strength is high enough for the field type,
- verification status is `gold`.
