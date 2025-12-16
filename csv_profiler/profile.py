from __future__ import annotations
from csv_profiler.models import ColumnProfile #بكج المجلد***٣**

def get_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []
    return list(rows[0].keys())
##5 change output 

def basic_profile(rows: list[dict[str, str]]) -> dict:
    cols = get_columns(rows)

    report: dict = {
        "source": None,
        "summary": {
            "rows": len(rows),
            "columns": len(cols),
            "column_names": cols,
        },
        "columns": [],
    }

    for col in cols:
        values = column_values(rows, col)
        typ = infer_type(values)

        if typ == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)

        total = len(rows)
        missing = stats["missing"]
        unique = stats["unique"]

        cp = ColumnProfile(
            name=col,
            inferred_type=typ,
            total=total,
            missing=missing,
            unique=unique,
        )

        col_dict = cp.to_dict()
        col_dict["stats"] = stats
        report["columns"].append(col_dict)

    return report


MISSING = {"", "na", "n/a", "null", "none", "nan"}


def is_missing(value: str | None) -> bool:
    """Return True if the value should be considered missing."""
    if value is None:
        return True
    return value.strip().casefold() in MISSING


def try_float(value: str) -> float | None:
    """Return float(value) or None if conversion fails."""
    try:
        return float(value)
    except ValueError:
        return None


def infer_type(values: list[str]) -> str:
    """Infer column type: 'number' or 'text'."""
    # remove missing values (هنا اثنين)
    cleaned = [v for v in values if not is_missing(v)]

    # if nothing left, default to text
    if not cleaned:
        return "text"

    # if any value cannot be converted to float الي text
    for v in cleaned:
        if try_float(v) is None:
            return "text"

    return "number"

    ##2

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    return [row.get(col, "") for row in rows]

    ##3
def numeric_stats(values: list[str]) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    nums: list[float] = []
    for v in usable:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)

    count = len(nums)
    unique = len(set(nums))

    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / count,
    }

#44

def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    # sort by count 
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:top_k]

    return {
        "count": len(usable),
        "missing": missing,
        "unique": len(counts),
        "top": top,  # list of (value, count) 
    }


##