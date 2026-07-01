from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
RELEASES = ROOT / "releases"
OUT = RELEASES / "RELEASE_INDEX.md"

def main():
    rows = []
    for region_dir in sorted([p for p in RELEASES.iterdir() if p.is_dir() and p.name != "Scotland"]):
        for release_dir in sorted([p for p in region_dir.iterdir() if p.is_dir()]):
            rows.append((region_dir.name, release_dir.name, release_dir.relative_to(ROOT)))

    lines = [
        "# Release Index",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "| Region | Release | Path |",
        "|---|---|---|",
    ]
    for region, rel, path in rows:
        lines.append(f"| {region} | {rel} | `{path}` |")

    OUT.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
    print(OUT)

if __name__ == "__main__":
    main()
