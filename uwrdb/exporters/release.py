from zipfile import ZipFile
from uwrdb.core.config import EXPORTS, ROOT

def package_release(name="UWRDB_master_release"):
    zip_path = EXPORTS / f"{name}.zip"
    with ZipFile(zip_path,"w") as z:
        for p in EXPORTS.rglob("*"):
            if p.is_file() and p != zip_path: z.write(p,p.relative_to(ROOT))
    return zip_path
