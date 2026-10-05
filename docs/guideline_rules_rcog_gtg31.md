# RCOG Green-top Guideline No. 31 (SGA fetus, 2013, rev. 2014) - rules v2
Source of truth: Appendix III algorithm (page 31) + executive summary (pages 3-5).
Scope: singleton pregnancies without fetal abnormality. Not for twins or known anomalies.

## Step 1 - Is the baby SGA? (entry gate)
| Condition | Result |
|---|---|
| EFW or AC < 10th centile (customised chart preferred) | SGA |
| EFW or AC < 3rd centile | Severe SGA |
| Serial scans (>= 3 weeks apart) show slowing growth | Treat as SGA / FGR |
| EFW and AC both >= 10th, growth normal | Not SGA -> outside this pathway |
| EFW and AC both missing | Cannot decide SGA -> show Doppler findings, ask for EFW/AC |

## Step 2 - Umbilical artery (UA) Doppler decides the branch (only if SGA)
| Branch | UA finding | Surveillance | Delivery |
|---|---|---|---|
| A | Normal | Growth (AC & EFW) + UA Doppler every 2 weeks; add MCA Doppler after 32 weeks | OFFER delivery by 37 w (senior clinician). RECOMMEND by 37 w if MCA PI < 5th centile. Consider delivery > 34 w if growth static over 3 weeks |
| B | PI or RI > +2 SD, end-diastolic flow present | Growth weekly; UA Doppler twice weekly | RECOMMEND delivery by 37 w. Consider delivery > 34 w if growth static over 3 weeks |
| C | Absent or reversed end-diastolic flow (AREDV) | REFER to fetal medicine specialist. Growth weekly; UA Doppler daily; ductus venosus (DV) Doppler; computerised CTG if DV unavailable | Recommend delivery BEFORE 32 w (after steroids) if DV abnormal and/or cCTG STV < 3 ms, provided >= 24 w and EFW > 500 g. Otherwise recommend delivery BY 32 w after steroids; consider at 30-32 w even if DV normal. Caesarean section recommended |

## Step 3 - Modifiers
| # | Rule |
|---|---|
| M1 | Steroids: SGA 24+0 to 35+6 weeks where delivery is being considered -> single course. Beyond that: steroids if delivery is by caesarean section (per RCOG guidance) |
| M2 | MCA Doppler: preterm -> do NOT use to time delivery. SGA with normal UA after 32 w -> MCA PI < 5th centile means recommend delivery by 37 w |
| M3 | Mode of birth: AREDV -> caesarean. UA normal, or high PI with flow present -> induction can be offered, continuous heart-rate monitoring in labour |
| M4 | Amniotic fluid: use single deepest pocket; never the only surveillance test. Report it, it does not change the branch |
| M5 | Uterine artery Doppler: main use is at 20-24 w screening; limited value in 3rd trimester -> report only |
| M6 | CTG: never the only surveillance; use computerised CTG short-term variation |
| M7 | Past the "deliver by" week already (e.g. branch B at 37+ w) -> say delivery is due now |

## Wording rules for the engine
- Delivery words exactly as RCOG: "offer" (branch A) vs "recommend" (B, C, MCA < 5th).
- If SGA is not confirmed, every delivery line starts with "If SGA is confirmed:".
- Always state which branch and rule fired.
- "Abnormal" UA = PI or RI above +2 SD for gestational age. The chart used must be named.
