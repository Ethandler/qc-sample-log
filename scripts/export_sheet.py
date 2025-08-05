# scripts/export_sheet.py
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Sample  # 'app' is resolvable when run as a module

# Resolve DB at repo root regardless of working dir
REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "qc_log.db"
OUTPUT_PDF = REPO_ROOT / "daily_sample_log.pdf"

def fetch_samples():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Session = sessionmaker(bind=engine)
    with Session() as session:
        return session.query(Sample).order_by(Sample.id).all()

def draw_table(c, rows, x_start=50, y_start=750, row_h=20, col_w=(40, 160, 160)):
    headers = ["#", "Sample ID", "Material"]
    c.setFont("Helvetica-Bold", 10)
    for i, h in enumerate(headers):
        c.drawString(x_start + sum(col_w[:i]), y_start, h)

    y = y_start - row_h
    c.setFont("Helvetica", 10)
    for idx, r in enumerate(rows, start=1):
        c.drawString(x_start + 0, y, str(idx))
        c.drawString(x_start + col_w[0], y, r.sample_id)
        c.drawString(x_start + col_w[0] + col_w[1], y, r.material)
        y -= row_h
        if y < 50:
            c.showPage()
            y = y_start
            c.setFont("Helvetica-Bold", 10)
            for i, h in enumerate(headers):
                c.drawString(x_start + sum(col_w[:i]), y, h)
            c.setFont("Helvetica", 10)
            y -= row_h

def generate_pdf():
    rows = fetch_samples()
    c = canvas.Canvas(str(OUTPUT_PDF), pagesize=letter)
    c.setTitle("Daily Sample Log")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, "Daily Sample Log")
    draw_table(c, rows)
    c.save()
    print(f"PDF generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_pdf()
