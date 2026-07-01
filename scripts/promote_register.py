from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parents[1]
STAGING=ROOT/"data/staging/distillery_import_review.csv"
CURATED=ROOT/"data/curated/distillery.csv"

HEAD=["distillery_id","official_name","preferred_name","region_id","type","status","founded_year","owner_id","parent_company_id","website","address","postcode","latitude","longitude","notes"]

def read(path):
    if not path.exists(): return []
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, headers, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(rows)

def main():
    staged=read(STAGING)
    existing=read(CURATED)
    by_id={r["distillery_id"]:r for r in existing if r.get("distillery_id")}
    promoted=0
    for row in staged:
        did=row["distillery_id"]
        base={h:row.get(h,"") for h in HEAD}
        if did not in by_id:
            by_id[did]=base
            promoted += 1
    rows=sorted(by_id.values(), key=lambda r: r["distillery_id"])
    write_csv(CURATED,HEAD,rows)
    print(f"Promoted {promoted} new records into curated register.")
    print(f"Curated register now has {len(rows)} records.")

if __name__=="__main__":
    main()
