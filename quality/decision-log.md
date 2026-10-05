# Decision log

Newest first. Never edit a past decision: add a new one that supersedes it.

| ID | Date | Decision | Why | Decided by | Status |
|---|---|---|---|---|---|
| DEC-10 | 2026-10-05 | All changes reach `main` through reviewed pull requests; everyone commits from their own GitHub account | Traceability of every change, needed for medical-software records | Talha Nagina (project lead) | Active |
| DEC-09 | 2026-10-01 | Data model: every record carries a clinic ID; every visit belongs to a pregnancy; every result stores rule and chart versions; outcome fields captured after delivery | Serve many clinics without mixing data; show trends across repeat scans; keep old reports explainable; build an outcomes dataset | Project team | Active |
| DEC-08 | 2026-10-01 | Live testing on new patients only in shadow mode (doctor decides independently, tool output recorded) and only after ethics committee approval; October uses past anonymised cases and written scenarios | Patient safety and research ethics (ICMR guidelines) | Project team | Active |
| DEC-07 | 2026-10-01 | Accuracy is quoted only from a locked test set never used for fixing, always with the number of cases | Avoid overstating results | Project team | Active |
| DEC-06 | 2026-09-30 | Only values that pass the formula cross-check are pre-filled; all others go to manual entry | A silent wrong value is the most dangerous failure | Project team | Active |
| DEC-05 | 2026-09-30 | Run OCR first; call the local vision model only when OCR misses a value; vision-only values must pass the formula check | OCR is fast (seconds) and reliable on clear screens; the vision model is slow (minutes) and can invent values | Varshini S N, project team | Active |
| DEC-04 | 2026-09-30 | Reference chart in `engine/reference_charts.py` is a temporary placeholder | Needed to build and test the engine before a published chart is chosen and its licence checked | Project team | **Temporary**: to be superseded by a published chart |
| DEC-03 | 2026-09-30 | Clinical decisions come from a transparent rules engine, not a machine-learning model | Every recommendation must be explainable and traceable to the guideline; no outcome data exists yet to train a model | Project team | Active |
| DEC-02 | 2026-09 | Apply RCOG Green-top Guideline No. 31 (Appendix III algorithm), replacing the earlier FOGSI 2022 + Barcelona staging approach | It is the guideline our clinical partner uses, and its published algorithm can be implemented rule by rule | Dr Jini Gupta with the project team | Active (supersedes the earlier approach) |
| DEC-01 | 2026-09 | Product name: Fetal Doppler Assistant | Plain, descriptive name | Project team | Active |
