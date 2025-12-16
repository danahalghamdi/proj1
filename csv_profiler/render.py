from __future__ import annotations

import json
from pathlib import Path


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    summary = report.get("summary", {})
    columns = report.get("columns", [])

    rows = summary.get("rows", 0)

    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{rows}**")
    lines.append(f"- Columns: **{len(columns)}**\n")

    lines.append("## Missing values\n")
    lines.append("| Column | Missing |")
    lines.append("|--------|---------|")

    for c in columns:
        col = c["name"]
        stats = c.get("stats", {})
        missing = stats.get("missing", 0)
        lines.append(f"| {col} | {missing} |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
