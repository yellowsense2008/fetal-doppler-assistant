# Changelog

All notable changes to Fetal Doppler Assistant. Newest first.

## Unreleased

### Fixed
- The app now pre-fills only values whose formula check passed; every other value is marked "needs manual entry" (REQ-03, RISK-01).

### Added
- YellowSense-themed app: upload with progress and per-vessel read results, guideline result with severity banner and rule tags, saved anonymised demo cases.
- Table-based PDF report with logo header, Doppler table with limits, management table with rules, and signature lines (REQ-21).
- RapidOCR fallback (`reader/ocr_backend.py`): same OCR models via ONNX, used when PaddleOCR is not installed.

### Added
- Project records: README, contributing guide, code owners, pull request checklist, proprietary notice.
- Quality records in `quality/`: requirements, risk register, decision log.

### Changed
- `.gitignore` now also blocks DICOM files, more image and video types, archives and spreadsheets.

## 0.1.0 — 2026-10-05

### Added
- Integrated prototype: scan reader, RCOG Green-top Guideline 31 rules engine, Streamlit app and PDF report.
- Engine test suite (`tests/test_engine.py`) and clinical test cases.

## 2026-09-30

### Added
- Scan reader (`reader/read_scan.py`): OCR plus optional local vision model, formula cross-checks, shared JSON output.
- Starter structure, shared schemas and test cases.
