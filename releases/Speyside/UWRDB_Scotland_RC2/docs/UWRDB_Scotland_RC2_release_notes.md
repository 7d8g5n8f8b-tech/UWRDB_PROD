# UWRDB Scotland RC2 — SWA Baseline Reconciliation

Generated: 2026-07-02

## Summary

This release reconciles UWRDB Scotland RC1 against the official Scotch Whisky Association April 2026 list of current operating Scotch Whisky distilleries.

## Result

- SWA April 2026 operating baseline: 154 distilleries
- RC2 operating canonical records: 154
- Matched from RC1: 114
- Added in RC2: 40
- Non-baseline RC1 records flagged for review: 7
- Evidence records: 164
- QA blockers: 0

## Important clarification: Clydebank

There is no current SWA operating-list item named "Clydebank Distillery." RC2 handles this in two ways:

1. **Clydeside Distillery** is present on the SWA list and has been added/verified.
2. **Auchentoshan Distillery** is physically in Clydebank and has a Clydebank address note/source.

## Added examples requested by user

- 8 Doors Distillery
- Rosebank Distillery
- Clydeside Distillery

## Caveat

RC2 achieves operating-list completeness against the SWA April 2026 baseline. It does not yet make every technical field Gold. Rows added from the SWA list have operating-status evidence; owner, address, coordinates and production fields remain open where not yet verified.
