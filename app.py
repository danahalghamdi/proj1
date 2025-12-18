import csv
import json
from io import StringIO

import streamlit as st
from csv_profiler.profile import basic_profile

# --------------------

# --------------------
st.set_page_config(page_title="CSV Profiler", layout="wide")


st.markdown(
    """
    <style>
    .stApp {
        background-color: #faf7ff;
    }
    h1, h2, h3 {
        color: #5e3ea1;
    }
    .stButton > button {
        background-color: #b39ddb;
        color: #2e1a47;
        border-radius: 6px;
        padding: 0.5em 1.2em;
        border: none;
    }
    .stButton > button:hover {
        background-color: #a58ad4;
        color: #2e1a47;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("CSV Profiler")
st.caption("Upload a CSV → Generate report → View table → Download results")

# --------------------
# Upload CSV
# --------------------
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
show_preview = st.checkbox("Show preview", value=True)

if uploaded is None:
    st.info("Upload a CSV to begin.")
    st.stop()

# --------------------
# Read CSV
# --------------------
text = uploaded.getvalue().decode("utf-8-sig")
rows = list(csv.DictReader(StringIO(text)))

st.write("**Filename:**", uploaded.name)

if show_preview:
    with st.expander("Preview (first 5 rows)", expanded=False):
        st.write(rows[:5])

# --------------------

# --------------------
if st.button("Generate report"):
    st.session_state["report"] = basic_profile(rows)

report = st.session_state.get("report")

# --------------------
# markdown
# --------------------
def build_markdown(report: dict) -> str:
    summary = report.get("summary", {})
    columns = report.get("columns", [])

    lines = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{summary.get('rows', 0)}**")
    lines.append(f"- Columns: **{len(columns)}**\n")

    lines.append("## Missing values\n")
    lines.append("| Column | Missing |")
    lines.append("|--------|---------|")

    for c in columns:
        name = c.get("name", "")
        missing = c.get("stats", {}).get("missing", 0)
        lines.append(f"| {name} | {missing} |")

    return "\n".join(lines) + "\n"

# --------------------
# Display results
# --------------------
if report:
    summary = report.get("summary", {})

    c1, c2 = st.columns(2)
    c1.metric("Rows", summary.get("rows", 0))
    c2.metric("Columns", summary.get("columns", 0))

    st.subheader("Column profiles")

    # Table view
    table_rows = []
    for c in report.get("columns", []):
        stats = c.get("stats", {})
        table_rows.append({
            "name": c.get("name", ""),
            "type": c.get("inferred_type", ""),
            "total": c.get("total", 0),
            "missing": c.get("missing", stats.get("missing", 0)),
            "unique": c.get("unique", stats.get("unique", 0)),
        })

    st.dataframe(table_rows, use_container_width=True)

    # Markdown preview 
    md = build_markdown(report)
    st.subheader("Markdown preview")
    st.markdown(md)
    st.code(md, language="markdown")

    # Downloads
    st.subheader("Downloads")
    json_text = json.dumps(report, indent=2, ensure_ascii=False)

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

    # Raw JSON (debug)
    with st.expander("Raw JSON (debug)", expanded=False):
        st.json(report)

else:
    st.info("Click **Generate report** to display results.")