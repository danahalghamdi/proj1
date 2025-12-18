# proj1
# CSV Profiler

A simple Python tool to analyze CSV files and generate basic profiling reports.

## --------------------
## Features
## --------------------
- Reads CSV files
- Infers column types (text / number)
- Calculates missing values and basic statistics
- Generates JSON and Markdown reports

## --------------------
## Project Structure
## --------------------
- `csv_profiler/io.py`      ## Read CSV files
- `csv_profiler/profile.py` ## Profile columns and compute statistics
- `csv_profiler/models.py`  ## Data models (ColumnProfile)
- `csv_profiler/render.py`  ## Render Markdown and JSON reports
- `csv_profiler/cli.py`     ## Command-line interface using Typer
- `main.py`                 ## Run the profiler (core logic)
- `app.py`                  ## Streamlit web application 


## --------------------
## Requirements
## --------------------
This project requires the following Python packages:

- typer (for the CLI interface)
- streamlit (for the web application)

Install using uv:
```bash
uv pip install typer streamlit

```

## --------------------
## Part 1: Generate Reports (JSON & Markdown)
## --------------------
## Run the core profiler from the project root:
```bash
PYTHONPATH=. uv run python3 main.py
```
## --------------------

## Data Parameter
- **CSV file path**: Path to the CSV file to be analyzed.
  - Example: `data/sample.csv`

  - **CLI (Typer)**
Run the profiler with parameters:
```bash
PYTHONPATH=. uv run python3 csv_profiler/cli.py data/sample.csv --out-dir outputs
```
## View CLI options
To display all available CLI parameters:
```bash
PYTHONPATH=. uv run python3 csv_profiler/cli.py --help
```
**CLI Parameters:**
- `csv_path` : Path to the input CSV file (required)
- `--out-dir` : Output directory for generated reports (default: outputs/)
## --------------------
## Output
```text
outputs/report.json
outputs/report.md
```
## --------------------
## Part 2: Streamlit Web App
## --------------------
## This part extends the profiler with a simple web interface.

## Run the Streamlit application from the project root:
```bash
PYTHONPATH=. uv run python3 -m streamlit run app.py
```
## Open in browser
```text
http://localhost:8501
```
Steps:
1. Upload a CSV file
2. (Optional) Preview the first rows
3. Click "Generate report"
4. View the profiling results
5. Download:
   - report.json
   - report.md
   