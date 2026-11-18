import csv
import tempfile
import unittest
from pathlib import Path

from financial_data_pipeline.pipeline import ingest_csv, snapshot


class TestPipeline(unittest.TestCase):
    def test_point_in_time(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(__file__).parents[1]
            db_path = str(Path(temp_dir) / "financials.db")
            output_path = str(Path(temp_dir) / "snapshot.csv")

            result = ingest_csv(str(root / "data" / "sample_financials.csv"), db_path)
            self.assertEqual(result["accepted"], 7)

            row_count = snapshot(db_path, "2025-04-01", output_path)
            self.assertEqual(row_count, 6)

            with open(output_path, encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))

            self.assertTrue(
                all(row["available_date"] <= "2025-04-01" for row in rows)
            )
            revenue = next(
                row for row in rows
                if row["company_id"] == "SYN001" and row["metric"] == "revenue"
            )
            self.assertEqual(revenue["period_end"], "2024-12-31")


if __name__ == "__main__":
    unittest.main()
