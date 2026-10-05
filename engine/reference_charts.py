"""Reference thresholds by gestational week.

PLACEHOLDER VALUES: these approximate numbers were entered by hand and are NOT
yet taken from a published chart. Replace them with a published reference
(e.g. Indian IRIA Samrakshan / Umarwal & Kumar 2019, or an international chart
the clinical partner approves) before any clinical use. The app shows this
status on every result.
"""
CHART_NAME = "Approximate placeholder chart (to be replaced with published reference)"
CHART_IS_PLACEHOLDER = True

# week: upper limit for UA PI (~ +2 SD / 95th), lower limit for MCA PI (5th),
#       upper limit for mean uterine PI (95th), lower limit for CPR (5th)
TABLE = {
    28: {"ua_hi": 1.36, "mca_lo": 1.25, "ut_hi": 1.10, "cpr_lo": 1.08},
    30: {"ua_hi": 1.31, "mca_lo": 1.20, "ut_hi": 1.05, "cpr_lo": 1.08},
    32: {"ua_hi": 1.25, "mca_lo": 1.15, "ut_hi": 1.00, "cpr_lo": 1.08},
    34: {"ua_hi": 1.18, "mca_lo": 1.10, "ut_hi": 0.95, "cpr_lo": 1.08},
    36: {"ua_hi": 1.10, "mca_lo": 1.05, "ut_hi": 0.90, "cpr_lo": 1.08},
    38: {"ua_hi": 1.05, "mca_lo": 1.02, "ut_hi": 0.88, "cpr_lo": 1.08},
    40: {"ua_hi": 1.00, "mca_lo": 1.00, "ut_hi": 0.85, "cpr_lo": 1.08},
}


def limits(ga_weeks: float) -> dict:
    """Linear interpolation between tabulated weeks; clamped at the ends."""
    weeks = sorted(TABLE)
    if ga_weeks <= weeks[0]:
        return dict(TABLE[weeks[0]])
    if ga_weeks >= weeks[-1]:
        return dict(TABLE[weeks[-1]])
    for lo, hi in zip(weeks, weeks[1:]):
        if lo <= ga_weeks <= hi:
            f = (ga_weeks - lo) / (hi - lo)
            return {k: round(TABLE[lo][k] + f * (TABLE[hi][k] - TABLE[lo][k]), 3) for k in TABLE[lo]}
