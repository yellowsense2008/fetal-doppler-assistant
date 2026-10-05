"""Doctor's PDF report (fpdf2): clean table layout."""
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

LOGO = Path(__file__).resolve().parent / "assets" / "ys_logo.png"
INK, MUTED, LINE, TINT = (31, 36, 48), (100, 106, 120), (225, 214, 190), (255, 246, 222)
SEV = {"normal": ((233, 248, 239), (21, 128, 61), "ROUTINE"), "watch": ((255, 244, 229), (180, 83, 9), "NEEDS ATTENTION"),
       "urgent": ((255, 237, 227), (194, 65, 12), "URGENT"), "critical": ((253, 232, 232), (185, 28, 28), "CRITICAL"),
       "info": ((238, 244, 255), (29, 78, 216), "INCOMPLETE")}


def _t(s) -> str:
    s = str(s).replace("–", "-").replace("—", "-").replace("≥", ">=").replace("≤", "<=").replace("✓", "")
    return s.encode("latin-1", "replace").decode("latin-1")


class _PDF(FPDF):
    def header(self):
        if LOGO.exists():
            self.image(str(LOGO), 10, 9, 13)
        self.set_xy(26, 9)
        self.set_font("Helvetica", "B", 15); self.set_text_color(*INK)
        self.cell(0, 7, "Fetal Doppler Assistant", new_x="LMARGIN", new_y="NEXT")
        self.set_x(26); self.set_font("Helvetica", "", 9); self.set_text_color(*MUTED)
        self.cell(0, 5, "Doppler decision-support report  |  Powered by YellowSense", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(242, 169, 0); self.set_line_width(0.6); self.line(10, 25, 200, 25); self.set_line_width(0.2)
        self.set_y(29)

    def footer(self):
        self.set_y(-16); self.set_font("Helvetica", "I", 7.5); self.set_text_color(*MUTED)
        self.cell(0, 4, _t("Decision support only - the treating obstetrician decides. No fetal sex is detected or disclosed (PCPNDT Act)."),
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 4, f"Page {self.page_no()}", align="C")


def _head(pdf, title):
    pdf.ln(3); pdf.set_font("Helvetica", "B", 10); pdf.set_text_color(*INK); pdf.set_fill_color(*TINT); pdf.set_draw_color(*LINE)
    pdf.cell(0, 7, _t("  " + title.upper()), border=1, fill=True, new_x="LMARGIN", new_y="NEXT")


def _kv(pdf, pairs):
    pdf.set_draw_color(*LINE)
    for i in range(0, len(pairs), 2):
        for k, v in pairs[i:i + 2]:
            pdf.set_font("Helvetica", "B", 9); pdf.set_text_color(*MUTED); pdf.cell(32, 7, _t(" " + k), border="LB")
            pdf.set_font("Helvetica", "", 9.5); pdf.set_text_color(*INK); pdf.cell(63, 7, _t(v), border="RB")
        pdf.ln(7)


def _rows(pdf, rows, widths, header=None):
    pdf.set_draw_color(*LINE)
    if header:
        pdf.set_font("Helvetica", "B", 9); pdf.set_text_color(*MUTED)
        for h, w in zip(header, widths):
            pdf.cell(w, 7, _t(" " + h), border="LRB")
        pdf.ln(7)
    pdf.set_text_color(*INK)
    for row in rows:
        y0, x0 = pdf.get_y(), pdf.l_margin
        heights = []
        for txt, w in zip(row, widths):
            pdf.set_font("Helvetica", "", 9.5)
            lines = pdf.multi_cell(w, 5.2, _t(" " + str(txt)), dry_run=True, output="LINES")
            heights.append(len(lines) * 5.2 + 2)
        h = max(heights)
        if y0 + h > pdf.h - 22:
            pdf.add_page(); y0 = pdf.get_y()
        x = x0
        for i, (txt, w) in enumerate(zip(row, widths)):
            pdf.set_xy(x, y0 + 1)
            pdf.set_font("Helvetica", "B" if i == 0 else "", 9.5)
            pdf.multi_cell(w, 5.2, _t(" " + str(txt)))
            pdf.rect(x, y0, w, h)
            x += w
        pdf.set_xy(x0, y0 + h)


def build_pdf(visit: dict, res: dict) -> bytes:
    pdf = _PDF(); pdf.set_auto_page_break(True, 20); pdf.add_page()
    nv = lambda k: visit.get(k) if visit.get(k) not in (None, "") else "Not provided"  # noqa: E731
    _head(pdf, "Patient")
    _kv(pdf, [("Patient ID", visit.get("patient_id") or "-"), ("Report date", datetime.now().strftime("%d %b %Y, %H:%M")),
              ("GA by LMP", nv("weeks_by_lmp")), ("GA by scan", nv("weeks_by_scan")),
              ("GA used", res.get("ga_used") or "-"), ("Amniotic fluid", nv("amniotic_fluid")),
              ("EFW centile", nv("efw_percentile")), ("AC centile", nv("ac_percentile"))])

    # impression box
    bg, fg, label = SEV[res["severity"]]
    pdf.ln(4); y = pdf.get_y()
    pdf.set_fill_color(*bg); pdf.set_draw_color(*fg)
    pdf.set_font("Helvetica", "B", 12)
    lines = pdf.multi_cell(186, 6, _t(res.get("headline", "")), dry_run=True, output="LINES")
    h = 10 + 6 * len(lines)
    pdf.rect(10, y, 190, h, style="DF")
    pdf.set_xy(13, y + 2.5); pdf.set_font("Helvetica", "B", 8.5); pdf.set_text_color(*fg); pdf.cell(0, 4, label)
    pdf.set_xy(13, y + 7); pdf.set_font("Helvetica", "B", 12); pdf.set_text_color(*INK); pdf.multi_cell(184, 6, _t(res.get("headline", "")))
    pdf.set_y(y + h + 1)

    if res["status"] == "ok":
        v, lim = res["values"], res["values"]["limits"]
        def st_(flag, val):  # noqa: E306
            return "-" if val is None else ("ABNORMAL" if flag else "Normal range")
        dop = [["Umbilical artery PI", v.get("ua_pi") if v.get("ua_pi") is not None else "-", f"< {lim['ua_hi']}",
                ("Flow " + (v.get("ua_flow") or "-")) + " | " + st_(v.get("ua_high") or v.get("ua_flow") in ("absent", "reversed"), v.get("ua_pi"))],
               ["Middle cerebral artery PI", v.get("mca_pi") if v.get("mca_pi") is not None else "-", f"> {lim['mca_lo']}", st_(v.get("mca_low"), v.get("mca_pi"))],
               ["Cerebroplacental ratio", v.get("cpr") if v.get("cpr") is not None else "-", f"> {lim['cpr_lo']}",
                ("Brain sparing" if v.get("cpr_low") else st_(False, v.get("cpr")))],
               ["Mean uterine artery PI", v.get("uterine_mean_pi") if v.get("uterine_mean_pi") is not None else "-", f"< {lim['ut_hi']}",
                "Reported only (3rd trimester)"]]
        _head(pdf, "Doppler findings")
        _rows(pdf, dop, [62, 28, 30, 70], header=["Vessel / index", "Value", "Limit", "Interpretation"])
    if res.get("warnings"):
        _head(pdf, "Warnings")
        _rows(pdf, [[r, t] for t, r in res["warnings"]], [28, 162])
    plan = [["Surveillance", t, r] for t, r in res.get("surveillance", [])] + [["Delivery", t, r] for t, r in res.get("delivery", [])] + \
           [["Other", t, r] for t, r in res.get("other_actions", [])]
    if plan:
        _head(pdf, "Management per RCOG Green-top 31")
        _rows(pdf, plan, [30, 140, 20], header=["Area", "Recommendation", "Rule"])
    if res.get("missing"):
        _head(pdf, "Still needed")
        pdf.set_font("Helvetica", "", 9.5); pdf.set_text_color(*INK)
        pdf.multi_cell(0, 6, _t("  " + ", ".join(res["missing"])), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3); pdf.set_font("Helvetica", "I", 8); pdf.set_text_color(*MUTED)
    pdf.multi_cell(0, 4.2, _t(f"Guideline: {res.get('guideline')}. Reference chart: {res.get('chart')}. "
                              f"Rules applied: {', '.join(res.get('rules_fired', []))}."), new_x="LMARGIN", new_y="NEXT")
    if pdf.get_y() > pdf.h - 45:
        pdf.add_page()
    pdf.ln(12); pdf.set_font("Helvetica", "", 9); pdf.set_text_color(*INK)
    pdf.cell(95, 5, "______________________________"); pdf.cell(0, 5, "______________________________", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(95, 5, "Reviewing obstetrician"); pdf.cell(0, 5, "Date / time", new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())
