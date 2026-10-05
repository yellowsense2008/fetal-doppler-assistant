# Requirements

Status: **Done** = implemented and tested · **Partial** = implemented, not yet complete or verified · **Planned** = not started.

## Reading scans

| ID | Requirement | Status | How it is checked |
|---|---|---|---|
| REQ-01 | Extract PI, RI, S/D ratio and fetal heart rate for the umbilical artery, middle cerebral artery and left/right uterine arteries from a photo of the Doppler screen | Partial (one machine model) | Reader accuracy report on the locked test set, per value and machine |
| REQ-02 | Cross-check extracted values with the Doppler formulas and a plausible heart-rate range | Done | Reader checks in `reader/read_scan.py` |
| REQ-03 | Pre-fill only values that pass the cross-check; send everything else to manual entry | Done (app pre-fills only values whose formula check passed; others are marked "needs manual entry") | App behaviour; reader report counts silent errors |
| REQ-04 | Values seen only by the vision model are never used unless they pass the cross-check | Done | Reader merge logic |
| REQ-05 | Support at least three further machine brands | Planned | Accuracy report per machine |

## Clinical logic

| ID | Requirement | Status | How it is checked |
|---|---|---|---|
| REQ-10 | Apply RCOG Green-top Guideline No. 31, Appendix III, for small-for-gestational-age management | Done | `tests/test_engine.py`, `tests/cases/test_cases.json` |
| REQ-11 | Every finding and recommendation shows the guideline rule it comes from | Done | Engine output includes rule tags |
| REQ-12 | When SGA status is unknown, advice is marked "If SGA is confirmed" | Done | Engine tests |
| REQ-13 | Reject out-of-range inputs (gestational age 20–43 weeks, centile 0–100, PI 0.1–5) | Done | Engine validation |
| REQ-14 | Use a published reference chart for UA, MCA, CPR and uterine artery limits | Planned (placeholder in use) | Chart source and licence recorded in decision log; engine tests |
| REQ-15 | Store the rule version and chart version with every result | Planned | Platform tests |
| REQ-16 | Engine agrees with the clinical lead on written scenarios; every disagreement reviewed | Planned | Scenario agreement report |

## Doctor in control

| ID | Requirement | Status | How it is checked |
|---|---|---|---|
| REQ-20 | The doctor reviews and confirms all values before the guideline is applied | Done | App flow |
| REQ-21 | The report states it is decision support and carries signature lines for the doctor | Done | PDF report |

## Data protection and safety

| ID | Requirement | Status | How it is checked |
|---|---|---|---|
| REQ-30 | Never detect, store or display fetal sex (PCPNDT Act) | Done (no such field exists) | Code review; schema has no sex field |
| REQ-31 | Patient names are removed from images before they leave the clinic | Planned | Anonymisation step test |
| REQ-32 | Every record carries a clinic ID; data of different clinics is never mixed | Planned | Platform tests |
| REQ-33 | Every action (upload, read, correction, result, report) is written to an audit log | Planned | Platform tests |
| REQ-34 | Data is stored in India, encrypted at rest and in transit; access is logged | Planned | Deployment checklist |
| REQ-35 | Each visit belongs to a pregnancy, so repeat scans can be shown as a trend | Planned | Platform tests |
| REQ-36 | Each case records outcome fields after delivery (birth weight, gestational age at birth, NICU admission) | Planned | Platform tests |
