from __future__ import annotations

from pathlib import Path
import typer

from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown

app = typer.Typer()

@app.command()
def run(
    csv_path: Path = typer.Argument(..., help="Path to the input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output directory"),
) -> None:
    rows = read_csv_rows(csv_path)
    report = basic_profile(rows)

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(report, out_dir / "report.json")
    write_markdown(report, out_dir / "report.md")

    typer.echo(f"Wrote {out_dir/'report.json'} and {out_dir/'report.md'}")

if __name__ == "__main__":
    app()
