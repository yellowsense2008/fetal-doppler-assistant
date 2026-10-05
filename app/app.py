"""Fetal Doppler Assistant - Streamlit app.  Run from repo root:  streamlit run app/app.py"""
import json
import sys
import tempfile
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.rules import evaluate  # noqa: E402
from app.report import build_pdf  # noqa: E402

st.set_page_config(page_title="Fetal Doppler Assistant", page_icon="🩺", layout="wide")

# ------------------------------------------------------------------ style
st.markdown("""
<style>
.block-container, [data-testid="stMainBlockContainer"] {padding-top: 3.2rem; max-width: 1250px;}
.brand {display:flex; align-items:center; gap:14px; padding-bottom:14px; border-bottom:1px solid rgba(128,128,128,.25); margin-bottom:18px}
.brand .bar {width:8px; height:46px; border-radius:3px; background:#F5C518}
.brand .name {font-size:30px; font-weight:700; line-height:1.1}
.brand .sub {font-size:13.5px; opacity:.7}
.card {border:1px solid rgba(128,128,128,.25); border-radius:12px; padding:18px 20px; margin-bottom:14px}
.banner {border-radius:12px; padding:16px 20px; margin-bottom:14px; font-size:19px; font-weight:650}
.sev-normal  {background:rgba(34,197,94,.13);  border-left:6px solid #22C55E}
.sev-watch   {background:rgba(245,158,11,.14); border-left:6px solid #F59E0B}
.sev-urgent  {background:rgba(249,115,22,.16); border-left:6px solid #F97316}
.sev-critical{background:rgba(239,68,68,.16);  border-left:6px solid #EF4444}
.sev-info    {background:rgba(59,130,246,.12); border-left:6px solid #3B82F6}
.sevlabel {font-size:12px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; opacity:.75; margin-bottom:4px}
.item {padding:6px 0; border-bottom:1px dashed rgba(128,128,128,.2); font-size:15px}
.rule {font-size:11px; padding:1px 7px; border-radius:10px; background:rgba(128,128,128,.18); margin-left:6px; white-space:nowrap}
.h {font-weight:700; font-size:16px; margin:2px 0 6px}
.foot {margin-top:30px; padding-top:10px; border-top:1px solid rgba(128,128,128,.25); font-size:12px; opacity:.65; text-align:center}
</style>""", unsafe_allow_html=True)

st.markdown("""<div class="brand"><div class="bar"></div><div>
<div class="name">Fetal Doppler Assistant</div>
<div class="sub">Reads fetal Doppler scans and applies RCOG Green-top Guideline 31 &nbsp;·&nbsp; Powered by YellowSense &nbsp;·&nbsp; Research prototype</div>
</div></div>""", unsafe_allow_html=True)

FIELDS = dict(pid="", lmp="", scan="", efw="", ac="", fluid="normal", ua=None, ua_flow="present",
              mca=None, utl=None, utr=None, dv=None)
for k, v in FIELDS.items():
    st.session_state.setdefault(k, v)

DEMO = {c["id"]: c for c in json.loads((ROOT / "tests" / "cases" / "test_cases.json").read_text())
        if c["type"] == "real"}


def load_demo():
    c = DEMO.get(st.session_state.demo)
    if not c:
        return
    st.session_state.pop("result", None)
    st.session_state.update(pid=c["id"], lmp=c["lmp"], scan=c["scan"], efw="" if c["efw"] is None else str(c["efw"]),
                            ac="", fluid=c["fluid"], ua=c["ua"], ua_flow=c["flow"] or "present",
                            mca=c["mca"], utl=c["utl"], utr=c["utr"], dv=None)


KEYMAP = {"umbilical_artery": "ua", "mca": "mca", "uterine_left": "utl", "uterine_right": "utr", "ductus_venosus": "dv"}

left, right = st.columns([1, 1.15], gap="large")

# ------------------------------------------------------------------ input
with left:
    st.markdown("### 1 · Scans")
    tab_up, tab_demo = st.tabs(["Upload Doppler screens", "Load a demo case"])
    with tab_up:
        files = st.file_uploader("One photo per vessel (umbilical, MCA, uterine left/right)", type=["jpg", "jpeg", "png"],
                                 accept_multiple_files=True)
        use_llm = st.toggle("Use local vision model for difficult images (slower)", value=False)
        if files and st.button("Read scans", type="primary"):
            try:
                from reader.read_scan import read_scan
            except Exception as exc:  # reader deps (PaddleOCR) not installed
                st.error(f"Scan reader not available on this machine: {exc}")
            else:
                rows = []
                with st.spinner("Reading scans..."):
                    for f in files:
                        with tempfile.NamedTemporaryFile(suffix=Path(f.name).suffix, delete=False) as tmp:
                            tmp.write(f.getvalue())
                        try:
                            for rec in read_scan(tmp.name, with_llm=use_llm):
                                rows.append({"file": f.name, **rec})
                                key = KEYMAP.get(rec.get("vessel"))
                                if key and rec.get("pi") is not None:
                                    st.session_state[key] = rec["pi"]
                                    if key == "ua" and rec.get("flow_between_beats"):
                                        st.session_state.ua_flow = rec["flow_between_beats"]
                        except Exception as exc:
                            rows.append({"file": f.name, "vessel": None, "ocr_check": f"error: {exc}"})
                st.session_state.read_rows = rows
        if st.session_state.get("read_rows"):
            st.dataframe([{k: r.get(k) for k in ("file", "vessel", "pi", "ps", "ed", "heart_rate", "flow_between_beats", "ocr_check")}
                          for r in st.session_state.read_rows], hide_index=True, use_container_width=True)
            st.caption("Values below were filled from the scans. Check them against the screen before calculating.")
    with tab_demo:
        st.selectbox("Anonymised cases from our clinical partner", ["—"] + list(DEMO), key="demo", on_change=load_demo)

    st.markdown("### 2 · Check the values")
    with st.form("visit"):
        a, b = st.columns(2)
        a.text_input("Patient ID", key="pid")
        b.selectbox("Amniotic fluid", ["normal", "low", "high"], key="fluid")
        a.text_input("Gestational age by LMP", key="lmp", placeholder="e.g. 34w2d")
        b.text_input("Gestational age by scan", key="scan", placeholder="e.g. 32w5d")
        a.text_input("EFW centile", key="efw", placeholder="blank if unknown")
        b.text_input("AC centile", key="ac", placeholder="blank if unknown")
        st.markdown("**Doppler PI**")
        a, b = st.columns(2)
        a.number_input("Umbilical artery PI", key="ua", min_value=0.0, step=0.01, format="%.2f", value=None)
        b.selectbox("Umbilical flow between beats", ["present", "absent", "reversed"], key="ua_flow")
        a.number_input("MCA PI", key="mca", min_value=0.0, step=0.01, format="%.2f", value=None)
        b.number_input("Ductus venosus PI (optional)", key="dv", min_value=0.0, step=0.01, format="%.2f", value=None)
        a.number_input("Uterine artery left PI", key="utl", min_value=0.0, step=0.01, format="%.2f", value=None)
        b.number_input("Uterine artery right PI", key="utr", min_value=0.0, step=0.01, format="%.2f", value=None)
        go = st.form_submit_button("Apply guideline", type="primary", use_container_width=True)

# ------------------------------------------------------------------ output
def items(title, rows):
    if not rows:
        return ""
    body = "".join(f'<div class="item">{t}<span class="rule">{r}</span></div>' for t, r in rows)
    return f'<div class="card"><div class="h">{title}</div>{body}</div>'


with right:
    st.markdown("### 3 · Guideline result")
    if go:
        ss = st.session_state
        visit = {"patient_id": ss.pid, "weeks_by_lmp": ss.lmp, "weeks_by_scan": ss.scan,
                 "efw_percentile": ss.efw.strip() or None, "ac_percentile": ss.ac.strip() or None,
                 "amniotic_fluid": ss.fluid,
                 "vessels": [{"vessel": "umbilical_artery", "pi": ss.ua, "flow_between_beats": ss.ua_flow},
                             {"vessel": "mca", "pi": ss.mca}, {"vessel": "uterine_left", "pi": ss.utl},
                             {"vessel": "uterine_right", "pi": ss.utr}, {"vessel": "ductus_venosus", "pi": ss.dv}]}
        st.session_state.result = (visit, evaluate(visit))

    if "result" not in st.session_state:
        st.info("Upload scans or load a demo case, check the values, then press **Apply guideline**.")
    else:
        visit, res = st.session_state.result
        label = {"normal": "Routine", "watch": "Needs attention", "urgent": "Urgent", "critical": "Critical", "info": "Incomplete"}[res["severity"]]
        st.markdown(f'<div class="banner sev-{res["severity"]}"><div class="sevlabel">{label}</div>{res["headline"]}</div>',
                    unsafe_allow_html=True)
        if res["status"] == "ok":
            v = res["values"]
            m = st.columns(4)
            m[0].metric("GA used", res["ga_used"] or "–")
            m[1].metric("Umbilical PI", v.get("ua_pi") if v.get("ua_pi") is not None else "–",
                        "high" if v.get("ua_high") else None, delta_color="inverse")
            m[2].metric("CPR", v.get("cpr") if v.get("cpr") is not None else "–",
                        "low" if v.get("cpr_low") else None, delta_color="normal")
            m[3].metric("Mean uterine PI", v.get("uterine_mean_pi") if v.get("uterine_mean_pi") is not None else "–")
        html = items("Warnings", res["warnings"]) + items("Findings", res["findings"]) + \
            items("Surveillance", res["surveillance"]) + items("Delivery", res["delivery"]) + items("Other actions", res["other_actions"])
        if res["missing"]:
            html += f'<div class="card"><div class="h">Still needed</div>{", ".join(res["missing"])}</div>'
        st.markdown(html, unsafe_allow_html=True)
        st.caption(f"Basis: {res['guideline']} · Reference chart: {res['chart']}")
        if res["status"] == "ok":
            st.download_button("Download PDF report", build_pdf(visit, res), use_container_width=True,
                               file_name=f"doppler_report_{visit.get('patient_id') or 'patient'}.pdf", mime="application/pdf")

st.markdown('<div class="foot">© YellowSense Technologies Pvt. Ltd. · Decision support only - the treating obstetrician decides · '
            'Does not detect or disclose fetal sex (PCPNDT)</div>', unsafe_allow_html=True)
