# Fetal Doppler Assistant
Powered by YellowSense Technologies. Research prototype, not for clinical use.

Reads fetal Doppler screens, applies RCOG Green-top Guideline No. 31 (the guideline our clinical partner uses) and gives the obstetrician the findings, the plan and the rule behind each line. The doctor always decides.

| Folder | What | Owner |
|---|---|---|
| `reader/` | Scan photo -> vessel values (PaddleOCR + optional local vision model, formula checks) | Varshini |
| `engine/` | RCOG rules (`rules.py`) + reference limits (`reference_charts.py`) | Sharanya |
| `app/` | Streamlit UI (`app.py`) + PDF report (`report.py`) | Sharanya / Talha |
| `tests/` | `pytest` - engine checked on 11 cases + an unseen patient | all |
| `docs/` | Rules table (from the guideline's Appendix III flowchart), test cases | |

## Run
```bash
pip install -r requirements.txt          # app + engine (light)
pip install -r requirements-reader.txt   # only if this machine reads scans (heavy)
python -m pytest -q                 # must pass before any demo
streamlit run app/app.py
```
For the local vision model: install Ollama, `ollama pull qwen2.5vl:3b`, `ollama serve`, then switch it on in the app.

## Known gaps
- `engine/reference_charts.py` holds APPROXIMATE placeholder limits. Replace with a published chart before clinical use.
- MCA reversed-flow and ductus venosus waveform are not yet read from images.

## Rules
No patient images, PDFs with names, or API keys in git.
