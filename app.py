import csv
import json
from io import StringIO

import streamlit as st

from csv_profiler.profile import basic_profile

st.set_page_config(page_title="CSV Profiler", layout="wide")

st.title("CSV Profiler")
st.caption("Upload a CSV → Generate report → Display + Markdown preview + Downloads")

uploaded = st.file_uploader("Upload a CSV", type=["csv"])
show_preview = st.checkbox("Show preview", value=True)

if uploaded is None:
    st.info("Upload a CSV to begin.")
    st.stop()

# Read CSV
text = uploaded.getvalue().decode("utf-8-sig")
rows = list(csv.DictReader(StringIO(text)))

st.write("Filename:", uploaded.name)

if show_preview:
    with st.expander("Preview (first 5 rows)", expanded=False):
        st.write(rows[:5])

if st.button("Generate report"):
    st.session_state["report"] = basic_profile(rows)

report = st.session_state.get("report")

def build_markdown(report: dict) -> str:
    summary = report.get("summary", {})
    columns = report.get("columns", [])
    rows_count = summary.get("rows", 0)

    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{rows_count}**")
    lines.append(f"- Columns: **{len(columns)}**\n")

    lines.append("## Missing values\n")
    lines.append("| Column | Missing |")
    lines.append("|--------|---------|")

    for c in columns:
        col = c.get("name", "")
        stats = c.get("stats", {})
        missing = stats.get("missing", 0)
        lines.append(f"| {col} | {missing} |")

    return "\n".join(lines) + "\n"

if report is not None:
    summary = report.get("summary", {})
    c1, c2 = st.columns(2)
    c1.metric("Rows", summary.get("rows", 0))
    c2.metric("Columns", summary.get("columns", 0))

    st.subheader("Column profiles")
    st.write(report.get("columns", []))

    # Markdown preview
    md = build_markdown(report)
    with st.expander("Markdown preview", expanded=False):
        st.markdown(md)
        st.code(md, language="markdown")

    # Downloads (JSON + Markdown)
    st.subheader("Downloads")
    json_text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"

    st.download_button(
        "Download report.json",
        data=json_text.encode("utf-8"),
        file_name="report.json",
        mime="application/json",
    )
    st.download_button(
        "Download report.md",
        data=md.encode("utf-8"),
        file_name="report.md",
        mime="text/markdown",
    )

    with st.expander("Raw JSON (debug)", expanded=False):
        st.json(report)
else:
    st.info("Click **Generate report** to display results.")
