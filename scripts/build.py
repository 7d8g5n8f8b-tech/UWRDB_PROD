from pathlib import Path
import csv, sqlite3, shutil, sys
from datetime import datetime, timezone
from openpyxl import Workbook
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"; EXPORTS=ROOT/"exports"
FILES={"region":DATA/"lookup/region.csv","parent_company":DATA/"lookup/parent_company.csv","owner":DATA/"lookup/owner.csv","source":DATA/"lookup/source.csv","distillery":DATA/"curated/distillery.csv","brand":DATA/"curated/brand.csv","evidence":DATA/"curated/evidence.csv"}
REQ={"region":["region_id"],"parent_company":["parent_company_id"],"owner":["owner_id"],"source":["source_id"],"distillery":["distillery_id","official_name","region_id","type","status"],"brand":["brand_id","distillery_id","brand_name"],"evidence":["evidence_id","entity_type","entity_id","field_name","source_id","confidence","verified_date"]}
def read(p):
    with p.open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
data={t:read(p) for t,p in FILES.items()}; issues=[]
for t,rs in data.items():
    key=REQ[t][0]; seen=set()
    for i,r in enumerate(rs,2):
        for f in REQ[t]:
            if not (r.get(f) or "").strip(): issues.append(["BLOCKER",t,i,f,"missing required field"])
        if r.get(key) in seen: issues.append(["BLOCKER",t,i,key,"duplicate key"])
        seen.add(r.get(key))
regions={r["region_id"] for r in data["region"]}; owners={r["owner_id"] for r in data["owner"]}; parents={r["parent_company_id"] for r in data["parent_company"]}; dist={r["distillery_id"] for r in data["distillery"]}; sources={r["source_id"] for r in data["source"]}
for i,r in enumerate(data["distillery"],2):
    if r.get("region_id") not in regions: issues.append(["BLOCKER","distillery",i,"region_id","invalid region"])
    if r.get("owner_id") and r.get("owner_id") not in owners: issues.append(["BLOCKER","distillery",i,"owner_id","invalid owner"])
    if r.get("parent_company_id") and r.get("parent_company_id") not in parents: issues.append(["BLOCKER","distillery",i,"parent_company_id","invalid parent"])
    if r.get("owner_id")=="AVO-UNKNOWN": issues.append(["WARNING","distillery",i,"owner_id","owner pending curation"])
for i,r in enumerate(data["brand"],2):
    if r.get("distillery_id") not in dist: issues.append(["BLOCKER","brand",i,"distillery_id","invalid distillery"])
for i,r in enumerate(data["evidence"],2):
    if r.get("source_id") not in sources: issues.append(["BLOCKER","evidence",i,"source_id","invalid source"])
QA=ROOT/"qa/reports"; QA.mkdir(parents=True,exist_ok=True)
with (QA/"qa_issues.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["severity","table","line","field","message"]); w.writerows(issues)
blockers=[x for x in issues if x[0]=="BLOCKER"]
(QA/"qa_report.md").write_text("# QA Report\n\nGenerated: "+datetime.now(timezone.utc).isoformat()+"\n\n"+"\\n".join(f"- {t}: {len(rs)}" for t,rs in data.items())+f"\n\nBlockers: {len(blockers)}\nWarnings: {len(issues)-len(blockers)}\n",encoding="utf-8")
if blockers:
    print("QA failed"); sys.exit(1)
sqlite=EXPORTS/"sqlite/uwrdb.sqlite"; sqlite.parent.mkdir(parents=True,exist_ok=True)
if sqlite.exists(): sqlite.unlink()
con=sqlite3.connect(sqlite); con.executescript((ROOT/"schema/001_core_schema.sql").read_text(encoding="utf-8"))
for t,rs in data.items():
    if rs:
        cols=list(rs[0].keys())
        con.executemany(f"INSERT INTO {t} ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})", [[r.get(c) or None for c in cols] for r in rs])
con.commit(); con.close()
csvout=EXPORTS/"csv"; csvout.mkdir(parents=True,exist_ok=True)
for t,p in FILES.items(): shutil.copy2(p,csvout/f"{t}.csv")
xlsx=EXPORTS/"xlsx/UWRDB_release.xlsx"; xlsx.parent.mkdir(parents=True,exist_ok=True)
wb=Workbook(); wb.remove(wb.active)
for t,rs in data.items():
    ws=wb.create_sheet(t)
    if rs:
        h=list(rs[0].keys()); ws.append(h)
        for r in rs: ws.append([r.get(c,"") for c in h])
wb.save(xlsx)
(ROOT/"data/releases/release_manifest.txt").write_text(f"Generated {datetime.now(timezone.utc).isoformat()}\\nDistilleries: {len(data['distillery'])}\\n",encoding="utf-8")
print("Build complete")
