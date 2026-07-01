from pathlib import Path
import csv, sqlite3, shutil, sys
from datetime import datetime, timezone
from openpyxl import Workbook
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"; EXPORTS=ROOT/"exports"
FILES={
"region":DATA/"lookup/region.csv",
"parent_company":DATA/"lookup/parent_company.csv",
"owner":DATA/"lookup/owner.csv",
"field_definition":DATA/"lookup/field_definition.csv",
"source":DATA/"lookup/source.csv",
"distillery":DATA/"curated/distillery.csv",
"brand":DATA/"curated/brand.csv",
"evidence":DATA/"curated/evidence.csv",
}
REQ={
"region":["region_id"],
"parent_company":["parent_company_id"],
"owner":["owner_id"],
"field_definition":["field_name"],
"source":["source_id"],
"distillery":["distillery_id","official_name","region_id","type","status"],
"brand":["brand_id","distillery_id","brand_name"],
"evidence":["evidence_id","entity_type","entity_id","field_name","source_id","evidence_strength","verification_status","verified_date"],
}
def read(p):
    with p.open(newline="",encoding="utf-8") as f: return list(csv.DictReader(f))
data={t:read(p) for t,p in FILES.items()}; issues=[]
def issue(sev,t,line,field,msg): issues.append([sev,t,line,field,msg])
for t,rs in data.items():
    key=REQ[t][0]; seen=set()
    for i,r in enumerate(rs,2):
        for f in REQ[t]:
            if not (r.get(f) or "").strip(): issue("BLOCKER",t,i,f,"missing required field")
        if r.get(key) in seen: issue("BLOCKER",t,i,key,"duplicate key")
        seen.add(r.get(key))
regions={r["region_id"] for r in data["region"]}; owners={r["owner_id"] for r in data["owner"]}; parents={r["parent_company_id"] for r in data["parent_company"]}; dist={r["distillery_id"] for r in data["distillery"]}; sources={r["source_id"] for r in data["source"]}; fields={r["field_name"] for r in data["field_definition"]}
for i,r in enumerate(data["distillery"],2):
    if r.get("region_id") not in regions: issue("BLOCKER","distillery",i,"region_id","invalid region")
    if r.get("owner_id") and r.get("owner_id") not in owners: issue("BLOCKER","distillery",i,"owner_id","invalid owner")
    if r.get("parent_company_id") and r.get("parent_company_id") not in parents: issue("BLOCKER","distillery",i,"parent_company_id","invalid parent")
    if r.get("owner_id")=="AVO-UNKNOWN": issue("WARNING","distillery",i,"owner_id","owner pending curation")
for i,r in enumerate(data["brand"],2):
    if r.get("distillery_id") not in dist: issue("BLOCKER","brand",i,"distillery_id","invalid distillery")
for i,r in enumerate(data["evidence"],2):
    if r.get("source_id") not in sources: issue("BLOCKER","evidence",i,"source_id","invalid source")
    if r.get("field_name") not in fields: issue("BLOCKER","evidence",i,"field_name","field not defined")
    try:
        s=int(r.get("evidence_strength",""))
        if s<1 or s>5: issue("BLOCKER","evidence",i,"evidence_strength","outside 1-5")
    except Exception: issue("BLOCKER","evidence",i,"evidence_strength","not integer")
QA=ROOT/"qa/reports"; QA.mkdir(parents=True,exist_ok=True)
with (QA/"qa_issues.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["severity","table","line","field","message"]); w.writerows(issues)
blockers=[x for x in issues if x[0]=="BLOCKER"]; warnings=[x for x in issues if x[0]=="WARNING"]
gold_required=[r["field_name"] for r in data["field_definition"] if r.get("gold_required")=="1"]
gold_evidence={(r["entity_id"],r["field_name"]) for r in data["evidence"] if r.get("verification_status")=="gold"}
gold_gaps=0
for d in data["distillery"]:
    for f in gold_required:
        if (d["distillery_id"],f) not in gold_evidence:
            gold_gaps += 1
(QA/"qa_report.md").write_text(
    "# UWRDB QA Report\n\n"
    f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n"
    "## Counts\n" + "\n".join(f"- {t}: {len(rs)}" for t,rs in data.items()) +
    f"\n\n## Issues\n- Blockers: {len(blockers)}\n- Warnings: {len(warnings)}\n- Gold evidence gaps: {gold_gaps}\n\nSee `qa_issues.csv` for line-level details.\n",
    encoding="utf-8"
)
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
    ws=wb.create_sheet(t[:31])
    if rs:
        h=list(rs[0].keys()); ws.append(h)
        for r in rs: ws.append([r.get(c,"") for c in h])
wb.save(xlsx)
(ROOT/"data/releases/release_manifest.txt").write_text(f"Generated {datetime.now(timezone.utc).isoformat()}\nDistilleries: {len(data['distillery'])}\nEvidence records: {len(data['evidence'])}\nWarnings: {len(warnings)}\nGold evidence gaps: {gold_gaps}\n",encoding="utf-8")
print("Build complete")
