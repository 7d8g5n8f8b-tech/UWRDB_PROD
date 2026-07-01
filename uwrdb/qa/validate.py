from uwrdb.core.config import DATA_CORE
from uwrdb.core.io import read_csv

def validate():
    issues=[]
    data={p.stem:read_csv(p) for p in DATA_CORE.glob("*.csv")}
    required={"region":["region_id","region_name"],"parent_company":["parent_company_id","parent_company_name"],"owner":["owner_id","owner_name","parent_company_id"],"distillery":["distillery_id","official_name","region_id","type","status"],"brand":["brand_id","distillery_id","brand_name"],"source":["source_id","source_type","authority"],"evidence":["evidence_id","entity_type","entity_id","field_name","source_id","evidence_strength"],"release":["release_id","release_name"]}
    for table, fields in required.items():
        seen=set(); rows=data.get(table,[]); key=fields[0]
        for idx,row in enumerate(rows,start=2):
            for field in fields:
                if not (row.get(field) or '').strip(): issues.append(("BLOCKER",table,idx,field,"missing required field"))
            if row.get(key) in seen: issues.append(("BLOCKER",table,idx,key,"duplicate primary key"))
            seen.add(row.get(key))
    regions={r['region_id'] for r in data.get('region',[])}; owners={r['owner_id'] for r in data.get('owner',[])}; parents={r['parent_company_id'] for r in data.get('parent_company',[])}; dist={r['distillery_id'] for r in data.get('distillery',[])}; sources={r['source_id'] for r in data.get('source',[])}
    for idx,row in enumerate(data.get('owner',[]),start=2):
        if row.get('parent_company_id') not in parents: issues.append(("BLOCKER","owner",idx,"parent_company_id","invalid parent company"))
    for idx,row in enumerate(data.get('distillery',[]),start=2):
        if row.get('region_id') not in regions: issues.append(("BLOCKER","distillery",idx,"region_id","invalid region"))
        if row.get('owner_id') not in owners: issues.append(("BLOCKER","distillery",idx,"owner_id","invalid owner"))
    for idx,row in enumerate(data.get('brand',[]),start=2):
        if row.get('distillery_id') not in dist: issues.append(("BLOCKER","brand",idx,"distillery_id","invalid distillery"))
    for idx,row in enumerate(data.get('evidence',[]),start=2):
        if row.get('source_id') not in sources: issues.append(("BLOCKER","evidence",idx,"source_id","invalid source"))
        try:
            s=int(row.get('evidence_strength',''))
            if not 1 <= s <= 5: issues.append(("BLOCKER","evidence",idx,"evidence_strength","outside 1-5"))
        except Exception: issues.append(("BLOCKER","evidence",idx,"evidence_strength","not integer"))
    return issues
