#!/usr/bin/env python3
"""
UWRDB build script.

Validates curated CSV files and builds a SQLite database.
"""

from pathlib import Path
import csv
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SCHEMA = ROOT / "schema" / "001_core_schema.sql"
OUT = ROOT / "exports" / "sqlite" / "uwrdb.sqlite"

TABLE_FILES = {
    "region": DATA / "lookup" / "region.csv",
    "parent_company": DATA / "lookup" / "parent_company.csv",
    "owner": DATA / "lookup" / "owner.csv",
    "source": DATA / "lookup" / "source.csv",
    "distillery": DATA / "curated" / "distillery.csv",
    "brand": DATA / "curated" / "brand.csv",
    "evidence": DATA / "curated" / "evidence.csv",
}

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def insert_rows(conn, table, rows):
    if not rows:
        return
    cols = list(rows[0].keys())
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['?']*len(cols))})"
    values = [[row.get(c, "") or None for c in cols] for row in rows]
    conn.executemany(sql, values)

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()

    conn = sqlite3.connect(OUT)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))

    for table, path in TABLE_FILES.items():
        rows = read_csv(path)
        if rows:
            insert_rows(conn, table, rows)

    conn.commit()

    # basic QA
    issues = []
    for table in TABLE_FILES:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count}")

    for row in conn.execute("SELECT distillery_id, official_name FROM distillery WHERE website IS NOT NULL AND website NOT LIKE 'https://%'"):
        issues.append(f"Non-HTTPS website: {row}")

    if issues:
        print("QA issues:")
        for issue in issues:
            print("-", issue)
        return 1

    print(f"Built {OUT}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
