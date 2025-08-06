# scripts/ocr_ingest.py
import pytesseract
from pathlib import Path
from PIL import Image
import csv
import re

# Directories
REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "ingest" / "raw_photos"
OUTPUT_CSV = REPO_ROOT / "ingest" / "parsed_samples.csv"

# Simple ID extractor
ID_PATTERN = re.compile(r"\bL?25[-:]?C[-:]?\d{4}\b", re.IGNORECASE)

def extract_ids_from_image(img_path: Path) -> list[dict]:
    print(f"📷 Processing: {img_path.name}")
    image = Image.open(img_path)
    raw_text = pytesseract.image_to_string(image)

    rows = []
    seen = set()

    for line in raw_text.splitlines():
        ids = ID_PATTERN.findall(line)
        for sid in ids:
            norm = sid.upper().replace(":", "-").replace("--", "-")
            norm = re.sub(r"[^A-Z0-9-]", "", norm)
            if norm not in seen:
                seen.add(norm)
                rows.append({
                    "sample_id": norm,
                    "material": "concrete",  # default assumption
                    "notes": line.strip()
                })

    return rows

def write_csv(rows: list[dict]):
    if not rows:
        print("⚠️ No valid sample IDs detected.")
        return

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Parsed {len(rows)} entries → {OUTPUT_CSV}")

def main():
    all_rows = []
    for img in RAW_DIR.glob("*.png"):
        all_rows.extend(extract_ids_from_image(img))
    write_csv(all_rows)

if __name__ == "__main__":
    main()
