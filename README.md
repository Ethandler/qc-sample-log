# QC Sample Log

A digital replacement for paper logbooks (concrete/asphalt/soil/masonry) with collision-proof ID allocation and audit-ready traceability.

## Quickstart

```bash
git clone https://github.com/Ethandler/qc-sample-log.git
cd qc-sample-log
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run_cli.py allocate concrete 2
uvicorn run_api:app --reload
pytest

---

## ✅ RUN INSTRUCTIONS

```bash
# Set up once
python -m venv .venv && .venv\Scripts\activate  # (Win) or source .venv/bin/activate
pip install -r requirements.txt

# Allocate via CLI
python run_cli.py allocate concrete 2

# Run FastAPI server
uvicorn run_api:app --reload  # Access at http://127.0.0.1:8000/docs

# Run tests
pytest
