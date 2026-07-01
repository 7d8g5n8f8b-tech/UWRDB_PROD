from pathlib import Path
import csv, shutil, sqlite3, sys
from datetime import datetime
from openpyxl import Workbook

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; EXPORTS=ROOT/"exports"
SCHEMA=ROOT/"schema/001_core_schema.sql"
SQLITE=EXPORTS/"sqlite/uwrdb.sqlite"; QA=ROOT/"qa/reports/qa_report.md"
FILES={
"region":DATA/"lookup/region.csv",
"parent_company":DATA/"lookup/parent_company.csv",
"owner":DATA/"lookup/owner.csv",
"source":DATA/"lookup/source.csv",
"distillery":DATA/"curated/distillery.csv",
"brand":DATA/"curated/brand.csv",
"evidence":DATA/"curated/evidence.csv",
}
REQ={
"region":["region_id","region_name","region_type"],
"parent_company":["parent_company_id","parent_company_name"],
"owner":["owner_id","owner_name"],
"source":["source_id","source_type","authority"],
"distillery":["distillery_id","official_name","region_id","type","status"],
"brand":["brand_id","distillery_id","brand_name"],
"evidence":["evidence_id","entity_type","entity_id","field_name","source_id","confidence","verified_date"],
}
def rows(p):
    with p.open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
def main():
    data={t:rows(p) for t,p in FILES.items()}
    issues=[]
    for t,rs in data.items():
        key=REQ[t][0]; seen=set()
        for i,r in enumerate(rs,2):
            for f in REQ[t]:
                if not (r.get(f) or "").strip(): issues.append(f"{t}:{i} missing {f}")
            if r.get(key) in seen: issues.append(f"{t}:{i} duplicate {key} {r.get(key)}")
            seen.add(r.get(key))
    regions={r["region_id"] for r in data["region"]}
    owners={r["owner_id"] for r in data["owner"]}
    parents={r["parent_company_id"] for r in data["parent_company"]}
    dist={r["distillery_id"] for r in data["distillery"]}
    sources={r["source_id"] for r in data["source"]}
    for i,r in enumerate(data["distillery"],2):
        if r["region_id"] not in regions: issues.append(f"distillery:{i} bad region_id")
        if r["owner_id"] and r["owner_id"] not in owners: issues.append(f"distillery:{i} bad owner_id")
        if r["parent_company_id"] and r["parent_company_id"] not in parents: issues.append(f"distillery:{i} bad parent_company_id")
    for i,r in enumerate(data["brand"],2):
        if r["distillery_id"] not in dist: issues.append(f"brand:{i} bad distillery_id")
    for i,r in enumerate(data["evidence"],2):
        if r["source_id"] not in sources: issues.append(f"evidence:{i} bad source_id")
        try:
            c=int(r["confidence"])
            if c<1 or c>5: issues.append(f"evidence:{i} confidence out of range")
        except Exception: issues.append(f"evidence:{i} confidence not integer")
    QA.parent.mkdir(parents=True,exist_ok=True)
    QA.write_text("# UWRDB QA Report\n\nGenerated: "+datetime.utcnow().isoformat()+"Z\n\n"+"## Counts\n"+"\n".join(f"- {t}: {len(rs)}" for t,rs in data.items())+"\n\n## Issues\n"+("\n".join(f"- {x}" for x in issues) if issues else "No blocking QA issues found.")+"\n",encoding="utf-8")
    if issues:
        print(f"QA failed: {len(issues)} issue(s). See {QA}")
        return 1
    SQLITE.parent.mkdir(parents=True,exist_ok=True)
    if SQLITE.exists(): SQLITE.unlink()
    con=sqlite3.connect(SQLITE); con.execute("PRAGMA foreign_keys=ON;"); con.executescript(SCHEMA.read_text(encoding="utf-8"))
    for t,rs in data.items():
        if not rs: continue
        cols=list(rs[0].keys())
        con.executemany(f"INSERT INTO {t} ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})", [[r.get(c) or None for c in cols] for r in rs])
    con.commit(); con.close()
    csv_out=EXPORTS/"csv"; csv_out.mkdir(parents=True,exist_ok=True)
    for t,p in FILES.items(): shutil.copy2(p,csv_out/f"{t}.csv")
    xlsx=EXPORTS/"xlsx/UWRDB_release.xlsx"; xlsx.parent.mkdir(parents=True,exist_ok=True)
    wb=Workbook(); wb.remove(wb.active)
    for t,rs in data.items():
        ws=wb.create_sheet(t)
        if rs:
            h=list(rs[0].keys()); ws.append(h)
            for r in rs: ws.append([r.get(c,"") for c in h])
    wb.save(xlsx)
    print("Build complete")
    print(SQLITE); print(xlsx); print(QA)
    return 0
if __name__=="__main__": sys.exit(main())
