<<<<<<< HEAD
# medical-image-processing-
=======
# YellowSense Fetal Doppler Decision Support

Research prototype by **YellowSense Technologies Pvt. Ltd.** — not for clinical use.

Reads fetal Doppler scans, checks them against FOGSI (2022) + Barcelona staging using Indian percentile charts, and gives the obstetrician a stage, the rule that fired and a recommendation. The doctor always decides.

| Folder | What | Owner |
|---|---|---|
| `reader/` | Scan image -> vessel values (OCR + checks) | Teammate 1 |
| `engine/` | Guideline + percentile rules engine | Teammate 2 |
| `app/` | Streamlit UI + PDF report | Teammate 2 |
| `schemas/` | Shared JSON formats | Talha |
| `tests/cases/` | Test cases every change must pass | Talha |

## Rules
1. **No patient data or API keys in git.** Images live in the restricted drive, anonymised. See `.gitignore`.
2. One branch per person; merge to `main` via pull request, reviewed by Talha.
3. Keep to the shared JSON in `schemas/`. Change it only after agreeing as a team.
4. The engine must pass `tests/cases/test_cases.json` before any demo.
>>>>>>> 89361c0 (Starter structure, schemas, test cases, branding)
