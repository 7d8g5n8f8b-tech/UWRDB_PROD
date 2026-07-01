from pathlib import Path
import argparse, csv

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"data/curated/evidence.csv"
HEAD=["evidence_id","entity_type","entity_id","field_name","field_value","source_id","evidence_strength","verification_status","verified_date","notes"]

def read_rows():
    if not EVIDENCE.exists(): return []
    with EVIDENCE.open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))

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
    a=ap.parse_args()
    rows=read_rows()
    rows.append({
        "evidence_id":next_id(rows),"entity_type":a.entity_type,"entity_id":a.entity_id,
        "field_name":a.field_name,"field_value":a.field_value,"source_id":a.source_id,
        "evidence_strength":str(a.strength),"verification_status":a.status,
        "verified_date":a.date,"notes":a.notes
    })
    with EVIDENCE.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=HEAD); w.writeheader(); w.writerows(rows)
    print(f"Added evidence {rows[-1]['evidence_id']}")

if __name__=="__main__":
    main()
