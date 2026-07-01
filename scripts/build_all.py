from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from uwrdb.core.database import build_sqlite
from uwrdb.exporters.excel import export_excel
from uwrdb.exporters.csv_export import export_csvs
from uwrdb.exporters.release import package_release
from uwrdb.qa.validate import validate
from uwrdb.core.config import EXPORTS

def main():
    issues=validate()
    qa_path=EXPORTS/'qa_report.md'
    qa_path.parent.mkdir(parents=True,exist_ok=True)
    blockers=[i for i in issues if i[0]=='BLOCKER']
    lines=['# UWRDB QA Report','',f'Blockers: {len(blockers)}',f'Total issues: {len(issues)}','','## Issues']
    lines.extend([f'- {sev} {table}:{line} `{field}` — {msg}' for sev,table,line,field,msg in issues] or ['No issues found.'])
    qa_path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if blockers:
        raise SystemExit('Build failed: QA blockers found.')
    print('Build complete')
    print(build_sqlite())
    print(export_excel())
    print(export_csvs())
    print(package_release())
    print(qa_path)
if __name__ == '__main__': main()
