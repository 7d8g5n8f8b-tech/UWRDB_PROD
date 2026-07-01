from pathlib import Path
import csv, re
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data/raw/swa/operating_distilleries.csv"
CURATED=ROOT/"data/curated/distillery.csv"
STAGING=ROOT/"data/staging/distillery_import_review.csv"
HEAD=["distillery_id","official_name","preferred_name","region_id","type","status","founded_year","owner_id","parent_company_id","website","address","postcode","latitude","longitude","notes"]
REG={"speyside":"AVR-SPEYSIDE","highlands":"AVR-HIGHLANDS","highland":"AVR-HIGHLANDS","islay":"AVR-ISLAY","islands":"AVR-ISLANDS","lowlands":"AVR-LOWLANDS","lowland":"AVR-LOWLANDS","campbeltown":"AVR-CAMPBELTOWN","grain":"AVR-GRAIN"}
def rid(n): return "AVD-"+re.sub(r"[^A-Z0-9]+","-",n.upper()).strip("-").replace("THE-","")
def read(p):
    with p.open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def write(p,h,rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=h); w.writeheader(); w.writerows(rows)
rows=[]; review=[]
for r in read(RAW):
    name=(r.get("official_name") or "").strip()
    if not name: continue
    out={"distillery_id":rid(name),"official_name":name,"preferred_name":name,"region_id":REG.get((r.get("region") or "").lower(),"AVR-UNKNOWN"),"type":r.get("type") or "Unknown","status":r.get("status") or "Operating","founded_year":"","owner_id":"AVO-UNKNOWN","parent_company_id":"AVP-UNKNOWN","website":"","address":"","postcode":"","latitude":"","longitude":"","notes":"Imported from raw operating register; enrichment pending verification."}
    rows.append(out); review.append({**out,"source_note":r.get("source_note","")})
seen=set(); unique=[]
for r in rows:
    if r["distillery_id"] not in seen:
        seen.add(r["distillery_id"]); unique.append(r)
write(CURATED,HEAD,unique)
write(STAGING,HEAD+["source_note"],review)
print(f"Imported {len(unique)} records")
