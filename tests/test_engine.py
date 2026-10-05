"""Engine tests: check structure (SGA status, branch, severity, key actions),
not copied sentences. Cases come from tests/cases/test_cases.json."""
import json
from pathlib import Path

import pytest

from engine.rules import evaluate, parse_ga

CASES = {c["id"]: c for c in json.loads((Path(__file__).parent / "cases" / "test_cases.json").read_text())}


def visit(c, **extra):
    v = {"weeks_by_lmp": c["lmp"], "weeks_by_scan": c["scan"], "efw_percentile": c["efw"],
         "amniotic_fluid": c["fluid"], "vessels": [
             {"vessel": "umbilical_artery", "pi": c["ua"], "flow_between_beats": c["flow"]},
             {"vessel": "mca", "pi": c["mca"]},
             {"vessel": "uterine_left", "pi": c["utl"]},
             {"vessel": "uterine_right", "pi": c["utr"]}]}
    v.update(extra)
    return v


def run(cid, **extra):
    return evaluate(visit(CASES[cid], **extra))


def texts(res, key):
    return " | ".join(t for t, _ in res[key])


def test_parse_ga():
    assert parse_ga("33w2d") == pytest.approx(33 + 2 / 7)
    assert parse_ga("36w") == 36 and parse_ga("34") == 34
    assert parse_ga("abc") is None and parse_ga("") is None


def test_r1_not_sga_routine():
    r = run("R1-normal")
    assert r["sga"] == "not_sga" and r["branch"] is None and r["severity"] == "normal"
    assert "reversed" not in (texts(r, "findings") + r["headline"]).lower()


def test_r2_possible_sga_branch_b_due_now():
    r = run("R2-caseA")
    assert r["sga"] == "unknown" and r["branch"] == "B"
    assert "EFW or AC centile" in r["missing"]
    assert any("Dating gap" in t for t, _ in r["warnings"])
    d = texts(r, "delivery")
    assert d.startswith("If SGA is confirmed:") and "RECOMMEND delivery by 37 weeks" in d
    assert "caesarean" in texts(r, "other_actions")          # steroids only if CS at 36w


def test_r3_branch_b_steroids_window():
    r = run("R3-caseB")
    assert r["branch"] == "B" and r["values"]["cpr_low"]
    assert "24+0 to 35+6" in texts(r, "other_actions")
    assert "due now" not in texts(r, "delivery")


def test_s1_missing_ua_never_normal():
    r = run("S1-missing-ua")
    assert r["severity"] != "normal" and "doppler normal" not in r["headline"].lower()
    assert "umbilical artery PI" in r["missing"]


def test_s2_absent_flow_branch_c_due_now():
    r = run("S2-absent-flow")
    assert r["sga"] == "severe_sga" and r["branch"] == "C" and r["severity"] == "critical"
    assert "fetal medicine" in texts(r, "other_actions") and "Caesarean" in texts(r, "other_actions")
    assert "due now" in texts(r, "delivery") and "ductus venosus Doppler" in r["missing"]


def test_s3_reversed_before_32():
    r = run("S3-reversed-flow")
    assert r["branch"] == "C" and "due now" not in texts(r, "delivery")
    assert "BEFORE 32 weeks" in texts(r, "delivery")


def test_s4_term_not_sga_no_rescan():
    r = run("S4-term-40w")
    assert r["sga"] == "not_sga" and "rescan" not in (texts(r, "surveillance") + r["headline"]).lower()


def test_s5_sga_branch_a_offer():
    r = run("S5-SGA")
    assert r["sga"] == "sga" and r["branch"] == "A"
    assert "OFFER delivery by 37 weeks" in texts(r, "delivery")
    assert "every 2 weeks" in texts(r, "surveillance")


def test_s6_severe_sga_more_frequent():
    r = run("S6-efw-below-3")
    assert r["sga"] == "severe_sga" and r["branch"] == "A"
    assert "More frequent" in texts(r, "surveillance")


def test_s7_dating_gap_flag():
    r = run("S7-age-gap-only")
    assert any("Dating gap" in t for t, _ in r["warnings"]) and r["ga_used"] == "34w0d"


def test_s8_bad_input_rejected():
    r = run("S8-bad-input")
    assert r["status"] == "invalid_input" and not r["delivery"]


def test_unseen_patient_generated_not_looked_up():
    """A patient that exists in no test file."""
    v = {"weeks_by_lmp": "35w0d", "weeks_by_scan": "34w0d", "efw_percentile": 6, "amniotic_fluid": "normal",
         "vessels": [{"vessel": "umbilical_artery", "pi": 1.4, "flow_between_beats": "present"},
                     {"vessel": "mca", "pi": 1.9}]}
    r = evaluate(v)
    assert r["sga"] == "sga" and r["branch"] == "B"
    assert "24+0 to 35+6" in texts(r, "other_actions")


def test_not_sga_but_abnormal_ua_flags_review():
    v = {"weeks_by_lmp": "34w0d", "efw_percentile": 40,
         "vessels": [{"vessel": "umbilical_artery", "pi": 1.6, "flow_between_beats": "present"}]}
    r = evaluate(v)
    assert r["sga"] == "not_sga" and r["severity"] == "watch" and "review" in r["headline"]
