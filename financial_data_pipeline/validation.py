from datetime import date
import math

REQUIRED = ("company_id", "company_name", "metric", "period_end", "available_date", "value", "currency", "unit", "source", "source_url")
ALIASES = {"total revenue":"revenue", "revenues":"revenue", "sales":"revenue", "net sales":"revenue", "adjusted ebitda":"adjusted_ebitda", "operating income":"operating_income", "net income":"net_income", "total assets":"total_assets"}
UNITS = {"USD", "USD millions", "USD thousands", "shares", "percent"}

def normalize_metric(value: str) -> str:
    key=value.strip().lower()
    return ALIASES.get(key, "_".join(key.replace("&", "and").split()))

def validate(row: dict, line: int) -> list[str]:
    errors=[]
    for field in REQUIRED:
        if not row.get(field, "").strip(): errors.append(f"line {line}: missing {field}")
    if errors: return errors
    for field in ("period_end", "available_date"):
        try: date.fromisoformat(row[field].strip())
        except ValueError: errors.append(f"line {line}: {field} must be YYYY-MM-DD")
    try:
        if not math.isfinite(float(row["value"])): errors.append(f"line {line}: value must be finite")
    except ValueError: errors.append(f"line {line}: value must be numeric")
    if row["unit"].strip() not in UNITS: errors.append(f"line {line}: unsupported unit {row['unit']!r}")
    return errors
