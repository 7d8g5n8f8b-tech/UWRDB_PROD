import sqlite3
from .config import DATA_CORE, SCHEMA, EXPORTS
from .io import read_csv
TABLES = ["region","parent_company","owner","distillery","brand","source","evidence","release"]
def build_sqlite(output=None):
    output = output or EXPORTS / "UWRDB_master.sqlite"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists(): output.unlink()
    conn = sqlite3.connect(output)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    for table in TABLES:
        rows = read_csv(DATA_CORE / f"{table}.csv")
        if not rows: continue
        cols = list(rows[0].keys())
        placeholders = ",".join(["?"] * len(cols))
        conn.executemany(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})", [[row.get(c) or None for c in cols] for row in rows])
    conn.commit(); conn.close(); return output
