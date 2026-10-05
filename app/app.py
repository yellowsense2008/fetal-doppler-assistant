"""Fetal Doppler Assistant - Streamlit app.  Run from repo root:  streamlit run app/app.py"""
import base64
import json
import sys
import tempfile
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(__file__).resolve().parent / "assets"
sys.path.insert(0, str(ROOT))

from engine.rules import evaluate  # noqa: E402
from app.report import build_pdf  # noqa: E402

st.set_page_config(page_title="Fetal Doppler Assistant · YellowSense", page_icon=str(ASSETS / "ys_logo.png"), layout="wide")


def b64(p):
    return base64.b64encode((ASSETS / p).read_bytes()).decode()


LOGO = b64("ys_logo.png")
st.markdown(f"""
<style>
@font-face {{font-family:'Space Grotesk'; font-weight:500; src:url(data:font/woff2;base64,{b64('space-grotesk-latin-500-normal.woff2')}) format('woff2');}}
@font-face {{font-family:'Space Grotesk'; font-weight:700; src:url(data:font/woff2;base64,{b64('space-grotesk-latin-700-normal.woff2')}) format('woff2');}}
:root {{--ink:#1F2430; --amber:#F2A900; --orange:#EE7F22; --cream:#FFFBF2; --line:#F0E2BF;}}
.stApp {{background: radial-gradient(1200px 500px at 85% -10%, #FFE9A8 0%, rgba(255,233,168,0) 60%), var(--cream);}}
.block-container, [data-testid="stMainBlockContainer"] {{padding-top: 2.2rem; max-width: 1280px;}}
h1,h2,h3,.ys-h {{font-family:'Space Grotesk', 'Segoe UI', sans-serif !important; letter-spacing:-.01em; color:var(--ink);}}
.hero {{display:flex; align-items:center; gap:18px; padding:18px 24px; border-radius:18px; background:#fff;
        border:1px solid var(--line); box-shadow:0 8px 30px rgba(242,169,0,.12); margin-bottom:22px}}
.hero img {{width:58px; height:56px}}
.hero .t {{font-family:'Space Grotesk',sans-serif; font-size:30px; font-weight:700; line-height:1.05; color:var(--ink)}}
.hero .s {{font-size:14.5px; color:#5b6170; margin-top:4px}}
.hero .pill {{margin-left:auto; font-size:12.5px; font-weight:600; padding:6px 12px; border-radius:999px;
             background:#FFF3D9; color:#8a5b00; border:1px solid #F5D98F; white-space:nowrap}}
.step {{display:flex; align-items:center; gap:10px; margin:6px 0 10px}}
.step .n {{width:30px; height:30px; border-radius:50%; background:linear-gradient(135deg,var(--amber),var(--orange));
          color:#fff; font-weight:700; display:flex; align-items:center; justify-content:center; font-family:'Space Grotesk',sans-serif}}
.step .l {{font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:700; color:var(--ink)}}
.card {{background:#fff; border:1px solid var(--line); border-radius:14px; padding:16px 18px; margin-bottom:12px;
       box-shadow:0 2px 10px rgba(31,36,48,.04)}}
.card .h {{font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:16px; margin-bottom:6px; color:var(--ink)}}
.item {{padding:7px 0; border-bottom:1px dashed #EFE6D2; font-size:15px; color:#2b3040}}
.item:last-child {{border-bottom:none}}
.rule {{font-size:10.5px; font-weight:700; padding:2px 8px; border-radius:10px; background:#FFF3D9; color:#8a5b00; margin-left:8px; white-space:nowrap}}
.banner {{border-radius:16px; padding:18px 22px; margin-bottom:14px; font-family:'Space Grotesk',sans-serif; font-size:21px; font-weight:700; color:var(--ink)}}
.sevlabel {{font-family:'Source Sans Pro',sans-serif; font-size:12px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; margin-bottom:4px}}
.sev-normal  {{background:#E9F8EF; border:1px solid #BDE8CD}} .sev-normal .sevlabel {{color:#15803D}}
.sev-watch   {{background:#FFF4E5; border:1px solid #FBD7A6}} .sev-watch .sevlabel {{color:#B45309}}
.sev-urgent  {{background:#FFEDE3; border:1px solid #F9C3A3}} .sev-urgent .sevlabel {{color:#C2410C}}
.sev-critical{{background:#FDE8E8; border:1px solid #F5B5B5}} .sev-critical .sevlabel {{color:#B91C1C}}
.sev-info    {{background:#EEF4FF; border:1px solid #C9D8F5}} .sev-info .sevlabel {{color:#1D4ED8}}
.kpis {{display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-bottom:12px}}
.kpi {{background:#fff; border:1px solid var(--line); border-radius:12px; padding:10px 14px}}
.kpi .k {{font-size:12.5px; color:#6b7080}} .kpi .v {{font-family:'Space Grotesk',sans-serif; font-size:26px; font-weight:700; color:var(--ink)}}
.tag {{font-size:11px; font-weight:700; padding:1px 8px; border-radius:8px; margin-left:6px; vertical-align:middle}}
.tag.hi {{background:#FDE8E8; color:#B91C1C}} .tag.ok {{background:#E9F8EF; color:#15803D}}
.readrow {{display:flex; align-items:center; gap:10px; padding:8px 10px; border-radius:10px; background:#fff; border:1px solid var(--line); margin-bottom:6px; font-size:14.5px}}
.badge {{font-size:11px; font-weight:700; padding:2px 9px; border-radius:9px}}
.badge.ok {{background:#E9F8EF; color:#15803D}} .badge.bad {{background:#FDE8E8; color:#B91C1C}}
[data-testid="stToolbar"], [data-testid="stDecoration"] {{display:none !important}}
.foot {{margin-top:30px; padding-top:12px; border-top:1px solid var(--line); font-size:12.5px; color:#6b7080; text-align:center}}
div[data-testid="stFileUploaderDropzone"] {{background:#fff; border:2px dashed #F5D98F}}
</style>
<div class="hero"><img src="data:image/png;base64,{LOGO}"/>
<div><div class="t">Fetal Doppler Assistant</div>
<div class="s">Reads fetal Doppler screens and applies RCOG Green-top Guideline 31 · Powered by YellowSense</div></div>
<div class="pill">Research prototype</div></div>
""", unsafe_allow_html=True)


def step(n, label):
    st.markdown(f'<div class="step"><div class="n">{n}</div><div class="l">{label}</div></div>', unsafe_allow_html=True)


FIELDS = dict(pid="", lmp="", scan="", efw="", ac="", fluid="normal", ua=None, ua_flow="present",
              mca=None, utl=None, utr=None, dv=None)
for k, v in FIELDS.items():
    st.session_state.setdefault(k, v)
DEMO = {c["id"]: c for c in json.loads((ROOT / "tests" / "cases" / "test_cases.json").read_text()) if c["type"] == "real"}
KEYMAP = {"umbilical_artery": "ua", "mca": "mca", "uterine_left": "utl", "uterine_right": "utr", "ductus_venosus": "dv"}
VNAME = {"umbilical_artery": "Umbilical artery", "mca": "Middle cerebral artery", "uterine_left": "Uterine artery (left)",
         "uterine_right": "Uterine artery (right)", "ductus_venosus": "Ductus venosus", None: "Vessel not recognised"}


def load_demo():
    c = DEMO.get(st.session_state.demo)
    if not c:
        return
    st.session_state.pop("result", None)
    st.session_state.pop("read_rows", None)
    st.session_state.update(pid=c["id"], lmp=c["lmp"], scan=c["scan"], efw="" if c["efw"] is None else str(c["efw"]),
                            ac="", fluid=c["fluid"], ua=c["ua"], ua_flow=c["flow"] or "present",
                            mca=c["mca"], utl=c["utl"], utr=c["utr"], dv=None)


@st.cache_resource(show_spinner=False)
def ocr_engine():
    from reader.ocr_backend import make_engine
    return make_engine()


left, right = st.columns([1, 1.12], gap="large")

with left:
    step(1, "Upload Doppler screens")
    tab_up, tab_demo = st.tabs(["Upload scans", "Saved cases"])
    with tab_up:
        files = st.file_uploader("One photo per vessel: umbilical, MCA, uterine left and right", type=["jpg", "jpeg", "png"],
                                 accept_multiple_files=True, label_visibility="visible")
        if files:
            cols = st.columns(min(len(files), 4))
            for i, f in enumerate(files[:8]):
                cols[i % len(cols)].image(f, use_container_width=True)
            use_llm = st.toggle("Vision model for difficult images (needs local GPU/Ollama)", value=False)
            if st.button("Read scans", type="primary", use_container_width=True):
                from reader.read_scan import read_scan
                rows, bar = [], st.progress(0.0, text="Starting reader...")
                st.session_state.pop("result", None)
                for i, f in enumerate(files):
                    bar.progress(i / len(files), text=f"Reading scan {i + 1} of {len(files)} · {f.name}")
                    with tempfile.NamedTemporaryFile(suffix=Path(f.name).suffix, delete=False) as tmp:
                        tmp.write(f.getvalue())
                    try:
                        for rec in read_scan(tmp.name, ocr_engine=ocr_engine(), with_llm=use_llm):
                            rows.append({"file": f.name, **rec})
                            key = KEYMAP.get(rec.get("vessel"))
                            if key and rec.get("ocr_check") == "passed" and rec.get("pi") is not None:
                                st.session_state[key] = rec["pi"]
                                if key == "ua" and rec.get("flow_between_beats"):
                                    st.session_state.ua_flow = rec["flow_between_beats"]
                            if rec.get("weeks_on_screen") and not st.session_state.lmp:
                                st.session_state.lmp = rec["weeks_on_screen"]
                    except Exception as exc:
                        rows.append({"file": f.name, "vessel": None, "ocr_check": "failed", "error": str(exc)})
                bar.progress(1.0, text=f"Done · {len(files)} scans read")
                st.session_state.read_rows = rows
        if st.session_state.get("read_rows"):
            html = ""
            for r in st.session_state.read_rows:
                ok = r.get("ocr_check") == "passed"
                hr = r.get('heart_rate'); hr = int(hr) if isinstance(hr, (int, float)) else hr
                vals = f"PI <b>{r.get('pi')}</b> · RI {r.get('ri')} · S/D {r.get('sd')} · HR {hr} bpm" if ok else "could not be read reliably - enter manually"
                badge = '<span class="badge ok">✓ formula check passed</span>' if ok else '<span class="badge bad">needs manual entry</span>'
                html += f'<div class="readrow"><b>{VNAME.get(r.get("vessel"), r.get("vessel"))}</b><span style="flex:1">{vals}</span>{badge}</div>'
            st.markdown(html, unsafe_allow_html=True)
    with tab_demo:
        st.selectbox("Anonymised cases from our clinical partner", ["—"] + list(DEMO), key="demo", on_change=load_demo)

    step(2, "Check the values")
    with st.form("visit", border=False):
        with st.container(border=True):
            a, b = st.columns(2)
            a.text_input("Patient ID", key="pid")
            b.selectbox("Amniotic fluid", ["normal", "low", "high"], key="fluid")
            a.text_input("Gestational age by LMP", key="lmp", placeholder="e.g. 34w2d")
            b.text_input("Gestational age by scan", key="scan", placeholder="e.g. 32w5d")
            a.text_input("EFW centile", key="efw", placeholder="blank if unknown")
            b.text_input("AC centile", key="ac", placeholder="blank if unknown")
            a, b = st.columns(2)
            a.number_input("Umbilical artery PI", key="ua", min_value=0.0, step=0.01, format="%.2f", value=None)
            b.selectbox("Umbilical flow between beats", ["present", "absent", "reversed"], key="ua_flow")
            a.number_input("MCA PI", key="mca", min_value=0.0, step=0.01, format="%.2f", value=None)
            b.number_input("Ductus venosus PI (optional)", key="dv", min_value=0.0, step=0.01, format="%.2f", value=None)
            a.number_input("Uterine artery left PI", key="utl", min_value=0.0, step=0.01, format="%.2f", value=None)
            b.number_input("Uterine artery right PI", key="utr", min_value=0.0, step=0.01, format="%.2f", value=None)
        go = st.form_submit_button("Apply RCOG guideline", type="primary", use_container_width=True)


def items(title, rows):
    if not rows:
        return ""
    body = "".join(f'<div class="item">{t}<span class="rule">{r}</span></div>' for t, r in rows)
    return f'<div class="card"><div class="h">{title}</div>{body}</div>'


def kpi(label, val, flag=None):
    tag = f'<span class="tag {"hi" if flag in ("high", "low") else "ok"}">{flag}</span>' if flag else ""
    return f'<div class="kpi"><div class="k">{label}</div><div class="v">{val}{tag}</div></div>'


with right:
    step(3, "Guideline result")
    if go:
        ss = st.session_state
        visit = {"patient_id": ss.pid, "weeks_by_lmp": ss.lmp, "weeks_by_scan": ss.scan,
                 "efw_percentile": ss.efw.strip() or None, "ac_percentile": ss.ac.strip() or None, "amniotic_fluid": ss.fluid,
                 "vessels": [{"vessel": "umbilical_artery", "pi": ss.ua, "flow_between_beats": ss.ua_flow},
                             {"vessel": "mca", "pi": ss.mca}, {"vessel": "uterine_left", "pi": ss.utl},
                             {"vessel": "uterine_right", "pi": ss.utr}, {"vessel": "ductus_venosus", "pi": ss.dv}]}
        st.session_state.result = (visit, evaluate(visit))

    if "result" not in st.session_state:
        st.markdown('<div class="card"><div class="h">Waiting for scans</div>'
                    '<div class="item">Upload the Doppler screen photos, check the values, then apply the guideline.</div></div>',
                    unsafe_allow_html=True)
    else:
        visit, res = st.session_state.result
        label = {"normal": "Routine", "watch": "Needs attention", "urgent": "Urgent", "critical": "Critical", "info": "Incomplete"}[res["severity"]]
        html = f'<div class="banner sev-{res["severity"]}"><div class="sevlabel">{label}</div>{res["headline"]}</div>'
        if res["status"] == "ok":
            v = res["values"]
            dash = lambda x: x if x is not None else "–"  # noqa: E731
            html += '<div class="kpis">' + kpi("Gestational age", res["ga_used"]) + \
                kpi("Umbilical PI", dash(v.get("ua_pi")), "high" if v.get("ua_high") else ("normal" if v.get("ua_pi") else None)) + \
                kpi("CPR", dash(v.get("cpr")), "low" if v.get("cpr_low") else ("normal" if v.get("cpr") else None)) + \
                kpi("Mean uterine PI", dash(v.get("uterine_mean_pi"))) + "</div>"
        html += items("Warnings", res["warnings"]) + items("Findings", res["findings"]) + \
            items("Surveillance", res["surveillance"]) + items("Delivery", res["delivery"]) + items("Other actions", res["other_actions"])
        if res["missing"]:
            html += f'<div class="card"><div class="h">Still needed</div><div class="item">{", ".join(res["missing"])}</div></div>'
        st.markdown(html, unsafe_allow_html=True)
        st.caption(f"Basis: {res['guideline']} · Reference chart: {res['chart']}")
        if res["status"] == "ok":
            st.download_button("Download doctor's PDF report", build_pdf(visit, res), use_container_width=True, type="primary",
                               file_name=f"doppler_report_{visit.get('patient_id') or 'patient'}.pdf", mime="application/pdf")

st.markdown('<div class="foot">© YellowSense Technologies Pvt. Ltd. · Decision support only - the treating obstetrician decides · '
            'Does not detect or disclose fetal sex (PCPNDT)</div>', unsafe_allow_html=True)
