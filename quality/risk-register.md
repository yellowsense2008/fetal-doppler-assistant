# Risk register

What could go wrong for a patient or their data, and what prevents it. Severity: **High** (could change a delivery decision or harm a patient), **Medium** (delay or extra work for the doctor), **Low** (inconvenience). Likelihood is our current estimate and is revisited as evidence comes in. Reviewed every Monday.

| ID | Hazard | Cause | Possible harm | Severity | Likelihood | Controls | Status |
|---|---|---|---|---|---|---|---|
| RISK-01 | A wrong value is shown as confirmed | OCR misread, wrong screen layout | Wrong management advice | High | Low | Formula cross-check; only checked values pre-filled; doctor confirms every value (REQ-02, 03, 20) | **Partly controlled**: app in this branch pre-fills unchecked values (REQ-03); fix to be merged, then verify on locked test set |
| RISK-02 | Vision model invents a value | Model error on a hard image | Wrong management advice | High | Low | Vision-only values used only if they pass the cross-check (REQ-04) | Controlled |
| RISK-03 | Reference limits are wrong | Placeholder chart in use | Abnormal flow missed or normal flow flagged | High | Medium | Replace with a published chart (REQ-14); placeholder labelled in code and README | **Open** |
| RISK-04 | Guideline rule implemented wrongly | Coding error, misread flowchart | Wrong surveillance or delivery advice | High | Medium | Test cases; rules table from Appendix III; clinical lead sign-off of every rule; rule versioning (REQ-10, 15, 16) | Partly controlled |
| RISK-05 | Wrong gestational age entered | Typing error, dating by period vs scan | Wrong thresholds applied | High | Medium | Range validation; warning when dates by period and by scan differ (REQ-13) | Controlled |
| RISK-06 | Advice given as if the baby is SGA when it is not confirmed | Missing EFW/AC centile | Over-monitoring or early delivery | Medium | Medium | "If SGA is confirmed" prefix; missing data listed (REQ-12) | Controlled |
| RISK-07 | Tool used outside the guideline's scope | Twins, very early gestation, other conditions | Inappropriate advice | High | Low | Range validation | **Open**: add explicit exclusions (e.g. multiple pregnancy) and show them on screen |
| RISK-08 | Doctor over-trusts the tool | Automation bias | Missed clinical judgement | High | Medium | Rule shown for every line; "decision support, doctor decides" on screen and report; shadow-mode pilot before any live use | Partly controlled |
| RISK-09 | Report attached to the wrong patient | Mixed-up uploads or cases | Wrong patient managed on wrong data | High | Low | Patient ID on report; values confirmed before result | Partly controlled; platform to add case IDs and audit log (REQ-33) |
| RISK-10 | Image cannot be read | Blur, glare, tilt | Delay; manual entry needed | Low | High | Image flagged for manual entry, never silently skipped | Controlled |
| RISK-11 | Patient identity exposed | Images with names leave the clinic or enter git | Privacy breach, DPDP Act violation | High | Medium | Anonymise at clinic (REQ-31); `.gitignore`; no data in repo; encrypted India-hosted storage (REQ-34) | Partly controlled |
| RISK-12 | Fetal sex disclosed | A screen shows sex and it is read or stored | PCPNDT Act violation | High | Low | No sex field anywhere; sex blanked during anonymisation (REQ-30, 31) | Controlled; verify in anonymisation step |
| RISK-13 | Unauthorised change to clinical logic | Direct edits, shared login | Untraceable wrong advice | High | Low | Pull requests with code-owner review; individual accounts; decision log for rule changes | Partly controlled; branch protection pending |
