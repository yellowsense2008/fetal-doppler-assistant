# Test cases for the rules engine

Real cases (R) come from the doctor's scans; expected answer = her notes. Synthetic cases (S) test engine behaviour; clinical staging in S cases must be confirmed with the doctor.

| ID | LMP age | Scan age | EFW %ile | Fluid | UA PI | UA flow | MCA PI | Ut L PI | Ut R PI | Expected |
|---|---|---|---|---|---|---|---|---|---|---|
| R1-normal | 33w2d | 32w0d | 22 | normal | 1.17 | present | 3.01 | 0.49 | 0.5 | Normal. CPR 2.57, mean uterine PI 0.50. No growth restriction. |
| R2-caseA | 36w0d | 33w0d | blank | low | 1.51 | present | 1.72 | 1.85 | 0.6 | Age-gap flag (3 weeks). High cord PI. High mean uterine PI (1.23). CPR 1.14 low/borderline (chart-dependent). Low fluid. Growth-restriction stage: cannot confirm, need EFW - but Doppler findings must still be shown. |
| R3-caseB | 32w0d | 30w0d | blank | low | 1.62 | present | 1.15 | 1.06 | 1.26 | Age-gap flag (2 weeks). High cord PI. High mean uterine PI (1.16). CPR 0.71 - clearly low = brain sparing. Low fluid. Stage: need EFW, Doppler findings still shown. |
| S1-missing-ua | 34w0d | 34w0d | 40 | normal | blank | blank | 1.8 | 0.7 | 0.7 | Cannot assess cord / CPR: need umbilical artery PI. Must NOT say Normal. |
| S2-absent-flow | 32w0d | 30w0d | 2 | low | 1.9 | absent | 1.1 | 1.3 | 1.2 | Absent flow in cord -> Barcelona Stage II. Delivery timing around 34 weeks; close monitoring (every few days). Urgent-looking output. |
| S3-reversed-flow | 31w0d | 28w5d | 1 | low | 2.2 | reversed | 1.0 | 1.4 | 1.3 | Reversed flow in cord -> Barcelona Stage III. Delivery around 30 weeks / now (already past 30w); very close monitoring. Most urgent output. |
| S4-term-40w | 40w0d | 40w0d | 50 | normal | 0.8 | present | 1.5 | 0.6 | 0.6 | Normal Doppler at term. Must discuss delivery timing - must NOT say 'rescan in 2-3 weeks'. |
| S5-SGA | 36w0d | 35w0d | 7 | normal | 0.9 | present | 1.7 | 0.7 | 0.7 | Small for gestational age (SGA), not FGR: EFW 3rd-10th with normal Doppler (FOGSI). |
| S6-efw-below-3 | 36w0d | 34w3d | 2 | normal | 0.9 | present | 1.7 | 0.7 | 0.7 | FGR by EFW <3rd percentile alone (FOGSI), Barcelona Stage I; delivery around 37 weeks. |
| S7-age-gap-only | 34w0d | 31w0d | blank | normal | 0.95 | present | 1.85 | 0.62 | 0.65 | Age-gap flag (3 weeks) shown clearly; percentiles computed with LMP age; need EFW for stage. |
| S8-bad-input | 45w0d | 34w0d | 150 | normal | 15 | present | 1.8 | 0.7 | 0.7 | Reject: 45 weeks impossible, EFW percentile >100, UA PI 15 out of range. No result produced. |

## Notes on real cases

- **R1-normal**: Doctor: normal. Scan age approx (EFW 31w3d, AC 32w1d, BPD 33w3d) - confirm. FL <1st percentile on screen; MCA shows reversed flow between beats (ED -2.09) - ask doctor.
- **R2-caseA**: Doctor: IUGR, low fluid, feto-placental + utero-placental insufficiency (left and mean PI).
- **R3-caseB**: Doctor: low fluid, feto-placental + utero-placental insufficiency, brain sparing. Screen shows 31w6d, note says 32w - confirm; it decides early (<32w) vs late FGR rules.
