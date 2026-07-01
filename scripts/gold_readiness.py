from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"qa/reports/gold_readiness.md"

def read(path):
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    dist=read(ROOT/"data/curated/distillery.csv")
    fields=read(ROOT/"data/lookup/field_definition.csv")
    ev=read(ROOT/"data/curated/evidence.csv")
    required=[f["field_name"] for f in fields if f.get("gold_required")=="1"]
    gold={(e["entity_id"],e["field_name"]) for e in ev if e.get("verification_status")=="gold" and int(e.get("evidence_strength","0") or 0) >= 4}
    total=len(dist)*len(required)
    covered=sum(1 for d in dist for f in required if (d["distillery_id"],f) in gold)
    pct=(covered/total*100) if total else 0
    lines=[
        "# Gold Readiness",
        "",
        f"Distilleries: {len(dist)}",
        f"Gold-required fields per distillery: {len(required)}",
        f"Gold evidence coverage: {covered}/{total} ({pct:.1f}%)",
        "",
        "## Required fields",
        *[f"- {f}" for f in required],
        "",
        "## Missing Gold evidence",
    ]
    for d in dist:
        missing=[f for f in required if (d["distillery_id"],f) not in gold]
        if missing:
            lines.append(f"- {d['distillery_id']} {d['official_name']}: {', '.join(missing)}")
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(OUT)

if __name__=="__main__":
    main()
