#!/usr/bin/env python3
from pathlib import Path
import argparse, csv
ROOT=Path(__file__).resolve().parents[1]
STAGING=ROOT/"data/staging/distillery_import_review.csv"
CURATED=ROOT/"data/curated/distillery.csv"
HEAD=["distillery_id","official_name","preferred_name","region_id","type","status","founded_year","owner_id","parent_company_id","website","address","postcode","latitude","longitude","notes"]
def read(path):
    if not path.exists(): return []
    with path.open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def write(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=HEAD); w.writeheader(); w.writerows(rows)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["append-new","replace"], default="append-new")
    args=ap.parse_args()
    staged=[{k:r.get(k,"") for k in HEAD} for r in read(STAGING) if (r.get("review_status") or "").lower()=="approved"]
    current=read(CURATED)
    if args.mode=="replace":
        out=staged
    else:
        seen={r["distillery_id"] for r in current}
        out=current+[r for r in staged if r["distillery_id"] not in seen]
    write(CURATED,out)
    print(f"Promoted {len(out)} curated distillery records using mode={args.mode}")
if __name__=="__main__": main()
