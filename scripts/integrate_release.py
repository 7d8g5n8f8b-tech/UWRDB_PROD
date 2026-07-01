from pathlib import Path
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[1]

def copy_tree(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            copy_tree(item, target)
        else:
            shutil.copy2(item, target)

def main():
    parser = argparse.ArgumentParser(description="Copy a prepared release folder into releases/<Region>/<ReleaseName>.")
    parser.add_argument("--source", required=True, help="Path to release folder")
    parser.add_argument("--region", required=True, help="Region name, e.g. Campbeltown")
    parser.add_argument("--release", required=True, help="Release name, e.g. Gold_v0.1")
    args = parser.parse_args()

    src = Path(args.source).resolve()
    dst = ROOT / "releases" / args.region / args.release

    if not src.exists():
        raise SystemExit(f"Source folder not found: {src}")

    copy_tree(src, dst)
    print(f"Copied {src} -> {dst}")

if __name__ == "__main__":
    main()
