# Fetal Doppler Assistant

**YellowSense Technologies Pvt. Ltd.** · Research prototype (TRL 4) · Not for clinical use

Fetal Doppler Assistant reads photos of fetal Doppler ultrasound screens, checks every value with the Doppler formulas, and applies RCOG Green-top Guideline No. 31 (the guideline used by our clinical partner) to give the obstetrician the findings, the surveillance and delivery plan, and the guideline rule behind each line. The doctor always decides.

## Status

| Area | State |
|---|---|
| Reader (photo → values) | Working on real scans from one clinic and one machine model; multi-machine support in progress |
| Guideline engine | RCOG GTG-31 Appendix III implemented; reference chart is a **placeholder** until replaced with a published chart |
| App + PDF report | Working prototype (Streamlit) |
| Clinical validation | Planned: evaluation on past anonymised cases, then a shadow-mode pilot after ethics approval |

Plan and milestones: see the October 2026 project plan (shared document) and the **October 2026** milestone on GitHub.

## Repository layout

| Folder | What | Owner |
|---|---|---|
| `reader/` | Scan photo → vessel values (OCR, optional local vision model, formula checks) | Varshini S N |
| `engine/` | RCOG rules (`rules.py`) and reference limits (`reference_charts.py`) | Sharanya A |
| `app/` | Streamlit UI (`app.py`) and PDF report (`report.py`) | Sharanya A / Talha Nagina |
| `schemas/` | Shared JSON formats between reader, engine and app | Talha Nagina |
| `tests/` | `pytest` suite and clinical test cases every change must pass | All |
| `docs/` | Guideline rules table and test-case notes | All |
| `quality/` | Requirements, risk register, decision log (medical-software records) | Talha Nagina |

## Run

```bash
pip install -r requirements.txt          # app + engine (light)
pip install -r requirements-reader.txt   # scan reader (RapidOCR; PaddleOCR is used instead if installed)
python -m pytest -q                      # must pass before any demo or merge
streamlit run app/app.py
```

Optional local vision model: install Ollama, run `ollama pull qwen2.5vl:3b` and `ollama serve`, then switch it on in the app.

## Ground rules

1. **No patient data in git, ever.** No scan images, report PDFs, names, IDs or answer-key sheets. Images are anonymised at the clinic and kept in the restricted project drive. `.gitignore` blocks common image and document types; it is a safety net, not a permission.
2. **The tool never detects, stores or displays fetal sex** (PCPNDT Act).
3. **No secrets in git.** API keys and passwords live in `.env` or `.streamlit/secrets.toml`, both ignored.
4. **All changes reach `main` through a pull request** reviewed by the code owner. See [CONTRIBUTING.md](CONTRIBUTING.md).
5. **Any change to a clinical rule** needs Dr Jini Gupta's approval and an entry in `quality/decision-log.md`.

## Team

Prakhar Goyal (sponsor) · Dr Jini Gupta, MS (Obs & Gyn), Jeevisha Clinic, Udaipur (clinical lead) · Talha Nagina (project lead, backend) · Varshini S N (reader) · Sharanya A (guideline engine)

## Ownership

Proprietary software of YellowSense Technologies Pvt. Ltd. See [NOTICE](NOTICE).
