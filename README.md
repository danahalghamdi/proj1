# proj1
# CSV Profiler

A simple Python tool to analyze CSV files and generate basic profiling reports.

## Features
- Reads CSV files
- Infers column types (text / number)
- Calculates missing values and basic statistics
- Generates JSON and Markdown reports

## Project Structure
- `csv_profiler/io.py` – Read CSV files
- `csv_profiler/profile.py` – Profile columns and compute statistics
- `csv_profiler/models.py` – Data models (ColumnProfile)
- `csv_profiler/render.py` – Render Markdown and JSON reports
- `main.py` – Run the profiler

## How to Run
From the project root:

```bash
PYTHONPATH=src python main.py
```

## Data Parameter
- **CSV file path**: Path to the CSV file to be analyzed.
  - Example: `data/sample.csv`
