import argparse
from .pipeline import ingest_csv, snapshot

def main():
    p=argparse.ArgumentParser(description="Point-in-time financial data pipeline")
    sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("ingest"); a.add_argument("input"); a.add_argument("--db",required=True)
    b=sub.add_parser("snapshot"); b.add_argument("--db",required=True); b.add_argument("--as-of-date",required=True); b.add_argument("--output",required=True)
    x=p.parse_args()
    if x.cmd=="ingest":
        r=ingest_csv(x.input,x.db); print(f"Accepted {r['accepted']} | rejected {r['rejected']}")
        for err in r["errors"]: print("ERROR:",err)
    else: print(f"Wrote {snapshot(x.db,x.as_of_date,x.output)} observations to {x.output}")
if __name__=="__main__": main()
