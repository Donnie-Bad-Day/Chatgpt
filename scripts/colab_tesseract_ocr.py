"""
Google Colab OCR pipeline (Tesseract) for pro se case document processing.

How to use in Colab:
1) Open colab.research.google.com
2) New notebook
3) Paste this entire file into a code cell
4) Run all
5) Upload files when prompted
"""

# STEP A: install dependencies
!apt-get update -y
!apt-get install -y tesseract-ocr poppler-utils
!pip -q install pytesseract pdf2image pillow pandas

# STEP B: imports
import os
import re
import pytesseract
import pandas as pd
from PIL import Image
from pdf2image import convert_from_path
from google.colab import files

# STEP C: create working folders
os.makedirs("input", exist_ok=True)
os.makedirs("output_text", exist_ok=True)
os.makedirs("output_csv", exist_ok=True)

print("Upload PDFs or image files now (png/jpg/jpeg/tif/tiff/pdf).")
uploaded = files.upload()

for name, data in uploaded.items():
    with open(os.path.join("input", name), "wb") as f:
        f.write(data)

print(f"Uploaded {len(uploaded)} file(s).")

# STEP D: helper functions
def clean_filename(name: str) -> str:
    base = os.path.splitext(name)[0]
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", base)
    return base

def ocr_image(img: Image.Image) -> str:
    return pytesseract.image_to_string(img)

def process_pdf(path: str, out_base: str):
    pages = convert_from_path(path, dpi=300)
    page_records = []
    full_text = []

    for i, page in enumerate(pages, start=1):
        text = ocr_image(page)
        full_text.append(f"\n\n===== PAGE {i} =====\n{text}")
        page_records.append({"file": out_base, "page": i, "text": text})

    with open(f"output_text/{out_base}.txt", "w", encoding="utf-8") as f:
        f.write("".join(full_text))

    df = pd.DataFrame(page_records)
    df.to_csv(f"output_csv/{out_base}_pages.csv", index=False)

def process_image(path: str, out_base: str):
    img = Image.open(path)
    text = ocr_image(img)

    with open(f"output_text/{out_base}.txt", "w", encoding="utf-8") as f:
        f.write(text)

    df = pd.DataFrame([{"file": out_base, "page": 1, "text": text}])
    df.to_csv(f"output_csv/{out_base}_pages.csv", index=False)

# STEP E: run OCR
supported_images = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}

for fname in os.listdir("input"):
    path = os.path.join("input", fname)
    ext = os.path.splitext(fname)[1].lower()
    out_base = clean_filename(fname)

    try:
        if ext == ".pdf":
            print(f"Processing PDF: {fname}")
            process_pdf(path, out_base)
        elif ext in supported_images:
            print(f"Processing image: {fname}")
            process_image(path, out_base)
        else:
            print(f"Skipping unsupported file: {fname}")
    except Exception as e:
        print(f"ERROR processing {fname}: {e}")

# STEP F: package outputs
!zip -r ocr_output_text.zip output_text >/dev/null
!zip -r ocr_output_csv.zip output_csv >/dev/null

print("Done. Download zipped outputs now.")
files.download("ocr_output_text.zip")
files.download("ocr_output_csv.zip")
