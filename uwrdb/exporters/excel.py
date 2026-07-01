from openpyxl import Workbook
from uwrdb.core.config import DATA_CORE, EXPORTS
from uwrdb.core.io import read_csv

def export_excel(output=None):
    output = output or EXPORTS / "UWRDB_master.xlsx"
    output.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook(); wb.remove(wb.active)
    for path in sorted(DATA_CORE.glob("*.csv")):
        rows = read_csv(path); ws=wb.create_sheet(path.stem[:31])
        if rows:
            headers=list(rows[0].keys()); ws.append(headers)
            for row in rows: ws.append([row.get(h,"") for h in headers])
            ws.freeze_panes="A2"
    wb.save(output); return output
