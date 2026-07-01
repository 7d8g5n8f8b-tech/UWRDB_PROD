#!/usr/bin/env python3
"""
Add one evidence record to data/curated/evidence.csv.

Example:
python scripts/add_evidence.py \
  --entity-type distillery \
  --entity-id AVD-ARDBEG \
  --field-name official_name \
  --field-value "Ardbeg" \
  --source-id AVS-OFFICIAL-DISTILLERY-WEBSITE \
  --strength 4 \
  --status verified \
  --date 2026-07-01
"""
from pathlib import Path
import argparse, csv

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"data/curated/evidence.csv"
HEAD=["evidence_id","entity_type","entity_id","field_name","field_value","source_id","evidence_strength","verification_status","verified_date","notes"]

def read_rows():
    if not EVIDENCE.exists():
        return []
    with EVIDENCE.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def next_id(rows):
    nums=[]
    for r in rows:
        eid=r.get("evidence_id","")
        if eid.startswith("AVE-"):
            try: nums.append(int(eid.split("-")[1]))
            except Exception: pass
    return f"AVE-{(max(nums) if nums else 0)+1:06d}"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--entity-type",required=True)
    ap.add_argument("--entity-id",required=True)
    ap.add_argument("--field-name",required=True)
    ap.add_argument("--field-value",required=True)
    ap.add_argument("--source-id",required=True)
    ap.add_argument("--strength",required=True,type=int)
    ap.add_argument("--status",required=True,choices=["unknown","captured","verified","reviewed","gold"])
    ap.add_argument("--date",required=True)
    ap.add_argument("--notes",default="")
    args=ap.parse_args()

    rows=read_rows()
    rows.append({
        "evidence_id":next_id(rows),
        "entity_type":args.entity_type,
        "entity_id":args.entity_id,
        "field_name":args.field_name,
        "field_value":args.field_value,
        "source_id":args.source_id,
        "evidence_strength":str(args.strength),
        "verification_status":args.status,
        "verified_date":args.date,
        "notes":args.notes,
    })
    with EVIDENCE.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=HEAD); w.writeheader(); w.writerows(rows)
    print(f"Added evidence {rows[-1]['evidence_id']}")

if __name__=="__main__":
    main()
