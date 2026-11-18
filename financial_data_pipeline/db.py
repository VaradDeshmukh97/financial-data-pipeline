import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS observations (
 company_id TEXT NOT NULL, company_name TEXT NOT NULL, metric TEXT NOT NULL,
 period_end TEXT NOT NULL, available_date TEXT NOT NULL, value REAL NOT NULL,
 currency TEXT NOT NULL, unit TEXT NOT NULL, source TEXT NOT NULL, source_url TEXT NOT NULL,
 ingested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(company_id, metric, period_end, available_date)
);
CREATE INDEX IF NOT EXISTS idx_observation_cutoff ON observations(available_date, company_id, metric);
"""

def connect(path: str) -> sqlite3.Connection:
    target=Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    db=sqlite3.connect(target); db.row_factory=sqlite3.Row; db.executescript(SCHEMA); return db
