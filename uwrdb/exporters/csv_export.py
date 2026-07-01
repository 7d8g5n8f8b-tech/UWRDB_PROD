import shutil
from uwrdb.core.config import DATA_CORE, EXPORTS

def export_csvs(output_dir=None):
    output_dir = output_dir or EXPORTS / "csv"
    output_dir.mkdir(parents=True, exist_ok=True)
    for path in DATA_CORE.glob("*.csv"): shutil.copy2(path, output_dir / path.name)
    return output_dir
