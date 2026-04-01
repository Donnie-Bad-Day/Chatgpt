"""Google Colab OCR pipeline (Tesseract) for pro se case document processing.

This script is valid Python (no notebook `!` shell magics), so it should not show
IDE red-line syntax errors in GitHub/Codespaces.

Quick use in Google Colab:
1) Open https://colab.research.google.com
2) New notebook
3) Upload this file and run: `!python colab_tesseract_ocr.py`
4) Upload PDFs/images when prompted
5) Download generated zip files
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Dict


def in_colab() -> bool:
    """Return True if running inside Google Colab."""
    return "google.colab" in sys.modules


def run_command(cmd: list[str]) -> None:
    """Run a shell command with clear logging."""
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def install_dependencies_if_colab() -> None:
    """Install system/python dependencies in Colab only."""
    if not in_colab():
        print(
            "Not running in Google Colab. Skipping auto-install.\n"
            "Install these manually if needed:\n"
            "  - apt: tesseract-ocr poppler-utils\n"
            "  - pip: pytesseract pdf2image pillow pandas"
        )
        return

    run_command(["apt-get", "update", "-y"])
    run_command(["apt-get", "install", "-y", "tesseract-ocr", "poppler-utils"])
    run_command([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "pytesseract",
        "pdf2image",
        "pillow",
        "pandas",
    ])


def clean_filename(name: str) -> str:
    base = os.path.splitext(name)[0]
    return re.sub(r"[^A-Za-z0-9._-]+", "_", base)


def ensure_dirs() -> None:
    Path("input").mkdir(exist_ok=True)
    Path("output_text").mkdir(exist_ok=True)
    Path("output_csv").mkdir(exist_ok=True)


def upload_files() -> Dict[str, bytes]:
    """Use Colab uploader to collect input files."""
    if not in_colab():
        raise RuntimeError(
            "File upload requires Google Colab. Run this in Colab, "
            "or copy files into ./input manually before running."
        )

    from google.colab import files  # type: ignore

    print("Upload PDFs/images now (png/jpg/jpeg/tif/tiff/pdf).")
    uploaded = files.upload()

    for name, data in uploaded.items():
        Path("input", name).write_bytes(data)

    print(f"Uploaded {len(uploaded)} file(s).")
    return uploaded


def process_files() -> None:
    import pandas as pd
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image

    def ocr_image(img: Image.Image) -> str:
        return pytesseract.image_to_string(img)

    def process_pdf(path: Path, out_base: str) -> None:
        pages = convert_from_path(str(path), dpi=300)
        page_records = []
        full_text = []

        for i, page in enumerate(pages, start=1):
            text = ocr_image(page)
            full_text.append(f"\n\n===== PAGE {i} =====\n{text}")
            page_records.append({"file": out_base, "page": i, "text": text})

        Path(f"output_text/{out_base}.txt").write_text("".join(full_text), encoding="utf-8")
        pd.DataFrame(page_records).to_csv(f"output_csv/{out_base}_pages.csv", index=False)

    def process_image(path: Path, out_base: str) -> None:
        img = Image.open(path)
        text = ocr_image(img)

        Path(f"output_text/{out_base}.txt").write_text(text, encoding="utf-8")
        pd.DataFrame([{"file": out_base, "page": 1, "text": text}]).to_csv(
            f"output_csv/{out_base}_pages.csv", index=False
        )

    supported_images = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}

    for path in Path("input").iterdir():
        if not path.is_file():
            continue

        ext = path.suffix.lower()
        out_base = clean_filename(path.name)

        try:
            if ext == ".pdf":
                print(f"Processing PDF: {path.name}")
                process_pdf(path, out_base)
            elif ext in supported_images:
                print(f"Processing image: {path.name}")
                process_image(path, out_base)
            else:
                print(f"Skipping unsupported file: {path.name}")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR processing {path.name}: {exc}")


def zip_folder(src_dir: str, zip_name: str) -> None:
    with zipfile.ZipFile(zip_name, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in Path(src_dir).rglob("*"):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(src_dir))


def maybe_download_outputs() -> None:
    if not in_colab():
        print("Done. Output files are in ./output_text, ./output_csv, and zip files in cwd.")
        return

    from google.colab import files  # type: ignore

    print("Done. Downloading zip outputs...")
    files.download("ocr_output_text.zip")
    files.download("ocr_output_csv.zip")


def main() -> None:
    install_dependencies_if_colab()
    ensure_dirs()

    if in_colab():
        upload_files()
    else:
        print("Running outside Colab: place files into ./input before execution.")

    process_files()
    zip_folder("output_text", "ocr_output_text.zip")
    zip_folder("output_csv", "ocr_output_csv.zip")
    maybe_download_outputs()


if __name__ == "__main__":
    main()
