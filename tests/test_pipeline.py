import csv, tempfile, unittest
from pathlib import Path
from financial_data_pipeline.pipeline import ingest_csv, snapshot

class TestPipeline(unittest.TestCase):
 def test_point_in_time(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(__file__).parents[1]; db=str(Path(d)/"x.db"); out=str(Path(d)/"out.csv")
   r=ingest_csv(str(root/"data/sample_financials.csv"),db); self.assertEqual(r["accepted"],7)
   n=snapshot(db,"2025-04-01",out); self.assertEqual(n,6)
   rows=list(csv.DictReader(open(out,encoding="utf-8")))
   self.assertTrue(all(x["available_date"]<="2025-04-01" for x in rows))
   rev=next(x for x in rows if x["company_id"]=="SYN001" and x["metric"]=="revenue")
   self.assertEqual(rev["period_end"],"2024-12-31")
if __name__=="__main__": unittest.main()
