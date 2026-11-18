import csv
from pathlib import Path
from .db import connect
from .validation import normalize_metric, validate

def ingest_csv(source: str, db_path: str) -> dict:
    accepted=rejected=0; errors=[]
    with open(source, newline="", encoding="utf-8-sig") as f, connect(db_path) as db:
        reader=csv.DictReader(f)
        if not reader.fieldnames: raise ValueError("CSV must contain a header")
        for line,row in enumerate(reader, start=2):
            problems=validate(row, line)
            if problems: rejected+=1; errors.extend(problems); continue
            record={**row, "metric":normalize_metric(row["metric"]), "period_end":row["period_end"].strip(), "available_date":row["available_date"].strip(), "value":float(row["value"]), "currency":row["currency"].strip().upper(), "unit":row["unit"].strip()}
            db.execute("""INSERT INTO observations(company_id,company_name,metric,period_end,available_date,value,currency,unit,source,source_url)
            VALUES(:company_id,:company_name,:metric,:period_end,:available_date,:value,:currency,:unit,:source,:source_url)
            ON CONFLICT(company_id,metric,period_end,available_date) DO UPDATE SET company_name=excluded.company_name,value=excluded.value,currency=excluded.currency,unit=excluded.unit,source=excluded.source,source_url=excluded.source_url""", record)
            accepted+=1
    return {"accepted":accepted,"rejected":rejected,"errors":errors}

def snapshot(db_path: str, as_of_date: str, output: str) -> int:
    from datetime import date
    cutoff=date.fromisoformat(as_of_date).isoformat()
    with connect(db_path) as db:
        rows=db.execute("SELECT company_id,company_name,metric,period_end,available_date,value,currency,unit,source,source_url FROM observations WHERE available_date<=? ORDER BY company_id,metric,period_end DESC,available_date DESC", (cutoff,)).fetchall()
    latest={}
    for row in rows: latest.setdefault((row["company_id"],row["metric"]), dict(row))
    dest=Path(output); dest.parent.mkdir(parents=True,exist_ok=True)
    fields=["company_id","company_name","metric","period_end","available_date","value","currency","unit","source","source_url"]
    with dest.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(latest.values())
    return len(latest)
