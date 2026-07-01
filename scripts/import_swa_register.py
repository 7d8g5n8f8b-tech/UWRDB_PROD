from pathlib import Path
import csv, re

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data/raw/swa/operating_distilleries.csv"
STAGING=ROOT/"data/staging/distillery_import_review.csv"

HEAD=["distillery_id","official_name","preferred_name","region_id","type","status","founded_year","owner_id","parent_company_id","website","address","postcode","latitude","longitude","notes","source_note","review_status"]
REG={"speyside":"AVR-SPEYSIDE","highlands":"AVR-HIGHLANDS","highland":"AVR-HIGHLANDS","islay":"AVR-ISLAY","islands":"AVR-ISLANDS","lowlands":"AVR-LOWLANDS","lowland":"AVR-LOWLANDS","campbeltown":"AVR-CAMPBELTOWN","grain":"AVR-GRAIN"}

def rid(n):
    return "AVD-"+re.sub(r"[^A-Z0-9]+","-",n.upper()).strip("-").replace("THE-","")

def read(path):
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, headers, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(rows)

def main():
    rows=[]
    for r in read(RAW):
        name=(r.get("official_name") or "").strip()
        if not name: continue
        rows.append({
            "distillery_id":rid(name),
            "official_name":name,
            "preferred_name":name,
            "region_id":REG.get((r.get("region") or "").lower(),"AVR-UNKNOWN"),
            "type":r.get("type") or "Unknown",
            "status":r.get("status") or "Operating",
            "founded_year":"",
            "owner_id":"AVO-UNKNOWN",
            "parent_company_id":"AVP-UNKNOWN",
            "website":"",
            "address":"",
            "postcode":"",
            "latitude":"",
            "longitude":"",
            "notes":"Imported from raw operating register; enrichment pending verification.",
            "source_note":r.get("source_note",""),
            "review_status":"pending"
        })
    seen=set(); out=[]
    for row in rows:
        if row["distillery_id"] in seen:
            continue
        seen.add(row["distillery_id"]); out.append(row)
    write_csv(STAGING,HEAD,out)
    print(f"Wrote {len(out)} staged records to {STAGING}")

if __name__=="__main__":
    main()
