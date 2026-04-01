# 01 — FIRST STEPS (Do these in order, no skipping)

## Step 1 (Do this first): Create your Google account workspace
1. On your Android tablet, open **Chrome**.
2. Go to https://drive.google.com.
3. Sign in.
4. Tap **+ New** → **New folder**.
5. Create one folder named exactly:
   - `CASE_HQ_3_25_cv_00253`

## Step 2: Build your folder structure inside CASE_HQ_3_25_cv_00253
Inside that folder, create these folders exactly:

- `00_INBOX`
- `01_DOCKET`
- `02_ORDERS`
- `03_PLEADINGS_FILED`
- `04_PLEADINGS_OPPOSITION`
- `05_EVIDENCE_RAW`
- `06_EVIDENCE_OCR_TEXT`
- `07_RESEARCH_AUTHORITIES`
- `08_DEADLINES`
- `09_CONTRADICTION_TRACKER`
- `10_DRAFTS`
- `11_FINAL_PDFS_FOR_FILING`
- `12_SERVICE_LOGS`

## Step 3: Use naming rules (this prevents chaos)
Every file name must begin with date in this format:
`YYYY-MM-DD`

Examples:
- `2026-04-01_motion_to_compel_draft_v1.docx`
- `2026-04-01_order_on_discovery.pdf`
- `2026-04-01_exhibit_A_bodycam_request.pdf`

## Step 4: Add this GitHub repository files to Codespaces
1. Open GitHub in Chrome.
2. Open your repo.
3. Open **Code** → **Codespaces** → create/open codespace.
4. Confirm these files exist in the repo:
   - `docs/`
   - `scripts/`
   - `README.md`

## Step 5: Set up your OCR station (Google Colab + Tesseract)
1. Open https://colab.research.google.com.
2. Create new notebook.
3. Copy all code from `scripts/colab_tesseract_ocr.py` into a Colab code cell.
4. Run first cell that installs dependencies.
5. Upload PDFs/images when prompted.
6. Download OCR text output.
7. Put source files in `05_EVIDENCE_RAW` and OCR output in `06_EVIDENCE_OCR_TEXT`.

## Step 6: Create your contradiction tracker
1. Open `docs/templates/contradiction_tracker.csv`.
2. Import into Google Sheets.
3. Keep one row per contradiction.
4. Never argue without citation: docket number, exhibit, page/line.

## Step 7: Initialize your master deadlines sheet
1. Open Google Sheets.
2. Create columns:
   - `Task`
   - `Source (Order/Rule)`
   - `Due Date`
   - `Days Left`
   - `Status`
   - `Filed?`
3. In `Days Left`, use formula:
   `=D2-TODAY()`

## Step 8: Start AI team prompts
1. Open `docs/prompts/AGENT_PROMPTS.md`.
2. Copy each prompt into your AI app one at a time.
3. Use role tags when asking:
   - `[Docket Clerk]`
   - `[Rules Auditor]`
   - `[Evidence Mapper]`
   - `[Contradiction Analyst]`
   - `[Draft Builder]`

## Step 9: Daily routine (15–25 minutes)
- Check new docket entries.
- Save each new filing/order to correct folder.
- Update deadlines sheet.
- Update contradiction sheet.
- Make tomorrow's top 3 tasks.

## Step 10: Pre-filing checklist (always)
Before filing any document:
1. Rule compliance check complete.
2. Every factual statement has citation.
3. Relief requested is clear and specific.
4. Signature block complete.
5. Certificate of service included.
6. File name includes date + clear title.

If any item is missing, do not file yet.
