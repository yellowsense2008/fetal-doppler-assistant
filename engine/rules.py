"""RCOG Green-top Guideline No. 31 (SGA fetus) as plain, testable rules.

Structure follows the guideline's own algorithm (Appendix III, p.31):
  Step 1  is the baby SGA?          (EFW or AC < 10th centile)
  Step 2  umbilical artery branch   A normal | B PI high, flow present | C absent/reversed flow
  Step 3  modifiers                 steroids, MCA, mode of birth, fluid, uterine
Every output line records the rule that produced it. No ML, no free text copied
from test files.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from engine import reference_charts as charts

GUIDELINE = "RCOG Green-top Guideline No. 31 (2013, rev. 2014)"


# ---------------------------------------------------------------- helpers
def parse_ga(text) -> float | None:
    """'33w2d' -> 33.2857, '36w' -> 36.0, '34' -> 34.0. None if empty/invalid."""
    if text is None:
        return None
    s = str(text).strip().lower().replace(" ", "")
    if not s:
        return None
    m = re.fullmatch(r"(\d{1,2})(?:w(\d)?d?)?", s) or re.fullmatch(r"(\d{1,2})w(\d)d", s)
    if not m:
        return None
    weeks = int(m.group(1))
    days = int(m.group(2)) if m.lastindex and m.lastindex >= 2 and m.group(2) else 0
    if days > 6:
        return None
    return weeks + days / 7


def fmt_ga(ga: float) -> str:
    w = int(ga)
    d = round((ga - w) * 7)
    if d == 7:
        w, d = w + 1, 0
    return f"{w}w{d}d"


def _num(v):
    if v in (None, ""):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


@dataclass
class Result:
    status: str = "ok"                 # ok | invalid_input
    severity: str = "normal"           # normal | watch | urgent | critical | info
    headline: str = ""
    ga_used: str | None = None
    sga: str = "unknown"               # sga | severe_sga | not_sga | unknown
    branch: str | None = None          # A | B | C | None
    findings: list = field(default_factory=list)       # [(text, rule)]
    surveillance: list = field(default_factory=list)   # [(text, rule)]
    delivery: list = field(default_factory=list)       # [(text, rule)]
    other_actions: list = field(default_factory=list)  # [(text, rule)]
    warnings: list = field(default_factory=list)       # [(text, rule)]
    missing: list = field(default_factory=list)
    values: dict = field(default_factory=dict)
    chart: str = charts.CHART_NAME
    chart_placeholder: bool = charts.CHART_IS_PLACEHOLDER
    guideline: str = GUIDELINE

    @property
    def rules_fired(self):
        seen = []
        for group in (self.findings, self.surveillance, self.delivery, self.other_actions, self.warnings):
            for _, rule in group:
                if rule and rule not in seen:
                    seen.append(rule)
        return seen

    def to_dict(self):
        d = {k: getattr(self, k) for k in self.__dataclass_fields__}
        d["rules_fired"] = self.rules_fired
        return d


# ---------------------------------------------------------------- validation
def _validate(visit: dict) -> list[str]:
    errs = []
    for key, label in (("weeks_by_lmp", "LMP age"), ("weeks_by_scan", "Scan age")):
        raw = visit.get(key)
        if raw not in (None, ""):
            ga = parse_ga(raw)
            if ga is None:
                errs.append(f"{label} '{raw}' is not in the form 34w2d")
            elif not 20 <= ga <= 43:
                errs.append(f"{label} {raw} is outside 20-43 weeks")
    if parse_ga(visit.get("weeks_by_lmp")) is None and parse_ga(visit.get("weeks_by_scan")) is None and not errs:
        errs.append("Gestational age is required (LMP or scan)")
    for key, label in (("efw_percentile", "EFW centile"), ("ac_percentile", "AC centile")):
        v = _num(visit.get(key))
        if visit.get(key) not in (None, "") and (v is None or not 0 <= v <= 100):
            errs.append(f"{label} must be between 0 and 100")
    for v in visit.get("vessels", []):
        pi = _num(v.get("pi"))
        if pi is not None and not 0.1 <= pi <= 5.0:
            errs.append(f"{v.get('vessel')} PI {pi} is outside the plausible range 0.1-5.0")
    return errs


# ---------------------------------------------------------------- main
def evaluate(visit: dict) -> dict:
    r = Result()
    errs = _validate(visit)
    if errs:
        r.status, r.severity = "invalid_input", "info"
        r.headline = "Please correct the inputs - no recommendation produced"
        r.warnings = [(e, "INPUT") for e in errs]
        return r.to_dict()

    # ---- dating
    lmp, scan = parse_ga(visit.get("weeks_by_lmp")), parse_ga(visit.get("weeks_by_scan"))
    ga = lmp if lmp is not None else scan
    r.ga_used = fmt_ga(ga)
    if lmp is None:
        r.warnings.append(("LMP age not given: using scan age, which can hide growth restriction", "DATING"))
    elif scan is not None and abs(lmp - scan) >= 2:
        r.warnings.append((f"Dating gap of {abs(lmp - scan):.1f} weeks (LMP {fmt_ga(lmp)} vs scan {fmt_ga(scan)}). "
                           "LMP age used; a scan age this far behind suggests a small baby", "DATING"))
    lim = charts.limits(ga)

    # ---- vessel values
    vessels = {v.get("vessel"): v for v in visit.get("vessels", []) if v.get("vessel")}
    ua = vessels.get("umbilical_artery", {})
    ua_pi = _num(ua.get("pi"))
    ua_flow = (ua.get("flow_between_beats") or "present").lower()
    mca_pi = _num(vessels.get("mca", {}).get("pi"))
    ut = [p for p in (_num(vessels.get("uterine_left", {}).get("pi")), _num(vessels.get("uterine_right", {}).get("pi"))) if p is not None]
    ut_mean = round(sum(ut) / len(ut), 2) if ut else None
    cpr = round(mca_pi / ua_pi, 2) if (mca_pi and ua_pi) else None
    ua_high = ua_pi is not None and ua_pi > lim["ua_hi"]
    mca_low = mca_pi is not None and mca_pi < lim["mca_lo"]
    cpr_low = cpr is not None and cpr < lim["cpr_lo"]
    r.values = {"ua_pi": ua_pi, "ua_flow": ua_flow, "mca_pi": mca_pi, "cpr": cpr, "uterine_mean_pi": ut_mean,
                "limits": lim, "ua_high": ua_high, "mca_low": mca_low, "cpr_low": cpr_low}

    # ---- findings (always shown)
    if ua_pi is None:
        r.missing.append("umbilical artery PI")
    elif ua_flow in ("absent", "reversed"):
        r.findings.append((f"Umbilical artery: {ua_flow.upper()} end-diastolic flow (PI {ua_pi})", "STEP2-C"))
    elif ua_high:
        r.findings.append((f"Umbilical artery PI {ua_pi} is high (above {lim['ua_hi']} for {r.ga_used}); flow between beats present", "STEP2-B"))
    else:
        r.findings.append((f"Umbilical artery PI {ua_pi} within normal range (limit {lim['ua_hi']})", "STEP2-A"))
    if mca_pi is not None:
        r.findings.append((f"MCA PI {mca_pi}{' - LOW (below ' + str(lim['mca_lo']) + ')' if mca_low else ' within normal range'}", "M2"))
    if cpr is not None:
        r.findings.append((f"CPR {cpr}{' - LOW: brain-sparing pattern' if cpr_low else ' within normal range'}", "M2"))
    if ut_mean is not None:
        r.findings.append((f"Mean uterine artery PI {ut_mean}{' - high' if ut_mean > lim['ut_hi'] else ''} "
                           "(limited value in the third trimester; reported only)", "M5"))
    fluid = (visit.get("amniotic_fluid") or "").lower()
    if fluid in ("low", "reduced", "oligohydramnios"):
        r.findings.append(("Amniotic fluid reduced (never used alone for surveillance)", "M4"))

    # ---- step 1: SGA
    efw, ac = _num(visit.get("efw_percentile")), _num(visit.get("ac_percentile"))
    known = [x for x in (efw, ac) if x is not None]
    if not known:
        r.sga = "unknown"
        r.missing.append("EFW or AC centile")
    elif min(known) < 3:
        r.sga = "severe_sga"
    elif min(known) < 10:
        r.sga = "sga"
    else:
        r.sga = "not_sga"
    sga_text = {"severe_sga": "Severe SGA (EFW/AC below 3rd centile)", "sga": "SGA (EFW/AC below 10th centile)",
                "not_sga": "Not SGA (EFW/AC at or above 10th centile)", "unknown": "SGA status unknown: EFW or AC centile needed"}[r.sga]
    r.findings.insert(0, (sga_text, "STEP1"))

    # ---- not SGA: outside pathway
    if r.sga == "not_sga":
        if ua_flow in ("absent", "reversed") or ua_high:
            r.severity = "watch"
            r.headline = "Baby not small, but umbilical artery Doppler is abnormal - obstetrician review needed"
            r.warnings.append(("RCOG GTG-31 covers SGA babies only; this pattern is outside its pathway", "SCOPE"))
        elif ua_pi is None:
            r.severity = "info"
            r.headline = "Not SGA, but umbilical artery PI is missing - cannot confirm a normal Doppler"
        else:
            r.severity = "normal"
            r.headline = "Not SGA, umbilical artery Doppler normal - routine obstetric care"
            r.other_actions.append(("Outside the RCOG SGA pathway; no SGA-specific surveillance needed", "STEP1"))
        return r.to_dict()

    # ---- step 2: branch
    if ua_pi is None and ua_flow not in ("absent", "reversed"):
        r.severity = "info"
        r.headline = "Cannot choose a management branch: umbilical artery PI is needed"
        return r.to_dict()
    r.branch = "C" if ua_flow in ("absent", "reversed") else ("B" if ua_high else "A")
    pre = "" if r.sga != "unknown" else "If SGA is confirmed: "

    if r.branch == "A":
        r.severity = "watch"
        r.surveillance += [(pre + "Growth scan (AC, EFW) and umbilical artery Doppler every 2 weeks", "STEP2-A")]
        if r.sga == "severe_sga":
            r.surveillance.append(("More frequent Doppler may be appropriate (severe SGA)", "STEP2-A"))
        if ga >= 32:
            r.surveillance.append((pre + "Add MCA Doppler (after 32 weeks)", "M2"))
        if ga >= 32 and mca_low:
            r.delivery.append((pre + "RECOMMEND delivery by 37 weeks (MCA PI below 5th centile)", "M2"))
        else:
            r.delivery.append((pre + "OFFER delivery by 37 weeks, with a senior obstetrician involved", "STEP2-A"))
        r.delivery.append((pre + "Consider delivery after 34 weeks if growth is static over 3 weeks", "STEP2-A"))
        deliver_by = 37
    elif r.branch == "B":
        r.severity = "urgent"
        r.surveillance += [(pre + "Growth scan weekly; umbilical artery Doppler twice weekly", "STEP2-B")]
        r.delivery.append((pre + "RECOMMEND delivery by 37 weeks", "STEP2-B"))
        r.delivery.append((pre + "Consider delivery after 34 weeks if growth is static over 3 weeks", "STEP2-B"))
        deliver_by = 37
    else:
        r.severity = "critical"
        r.other_actions.append((pre + "Refer to a fetal medicine specialist", "STEP2-C"))
        r.surveillance += [(pre + "Umbilical artery Doppler daily; growth scan weekly", "STEP2-C"),
                           (pre + "Ductus venosus Doppler (computerised CTG if DV unavailable)", "STEP2-C")]
        dv = vessels.get("ductus_venosus", {})
        if not dv or _num(dv.get("pi")) is None:
            r.missing.append("ductus venosus Doppler")
        r.delivery.append((pre + "Deliver BEFORE 32 weeks, after steroids, if DV Doppler is abnormal or cCTG STV < 3 ms "
                                 "(provided at least 24 weeks and EFW over 500 g)", "STEP2-C"))
        r.delivery.append((pre + "Otherwise RECOMMEND delivery by 32 weeks after steroids; consider from 30 weeks even if DV is normal", "STEP2-C"))
        r.other_actions.append((pre + "Caesarean section recommended", "M3"))
        deliver_by = 32

    if ga >= deliver_by:
        r.delivery.insert(0, (pre + f"Already at {r.ga_used}: the 'deliver by {deliver_by} weeks' point has been reached - delivery is due now", "M7"))

    # ---- modifiers
    if 24 <= ga < 36:
        r.other_actions.append((pre + "Single course of antenatal steroids if delivery is being considered (24+0 to 35+6 weeks)", "M1"))
    elif ga >= 36:
        r.other_actions.append((pre + "Steroids only if delivery is by caesarean section", "M1"))
    if r.branch in ("A", "B"):
        r.other_actions.append(("Induction of labour can be offered, with continuous fetal heart-rate monitoring", "M3"))
    if r.branch != "A" and cpr_low and ga < 37:
        r.warnings.append(("Brain-sparing (low CPR) noted; in the preterm baby MCA is not used to time delivery", "M2"))

    sga_word = {"sga": "SGA", "severe_sga": "Severe SGA", "unknown": "Possible SGA"}[r.sga]
    branch_word = {"A": "normal umbilical artery Doppler", "B": "high umbilical artery resistance",
                   "C": f"{ua_flow} end-diastolic flow"}[r.branch]
    r.headline = f"{sga_word} with {branch_word}"
    if r.sga == "unknown":
        r.headline += " - confirm EFW/AC to apply the plan"
    return r.to_dict()
