"""PDF report for the doctor (fpdf2)."""
from datetime import datetime

from fpdf import FPDF

PRODUCT = "Fetal Doppler Assistant"


def _t(s) -> str:
    s = str(s).replace("–", "-").replace("—", "-").replace("≥", ">=").replace("≤", "<=")
    return s.encode("latin-1", "replace").decode("latin-1")


class _PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(30, 58, 95)
        self.cell(0, 8, _t(PRODUCT), new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(110, 110, 110)
        self.cell(0, 5, _t("Fetal Doppler decision-support report  |  Powered by YellowSense Technologies  |  Research prototype"),
                  new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(6)

    def footer(self):
        self.set_y(-18)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(120, 120, 120)
        self.multi_cell(0, 4, _t("Decision support only: the treating obstetrician makes all decisions. "
                                 "This system does not detect, record or disclose fetal sex (PCPNDT Act)."), align="C")


def _section(pdf, title):
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_fill_color(234, 240, 247)
    pdf.set_text_color(30, 58, 95)
    pdf.cell(0, 7, _t(" " + title), fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(30, 30, 30)
    pdf.ln(1)


def _lines(pdf, items, bold_first=False):
    pdf.set_font("Helvetica", "", 9.5)
    for text, rule in items:
        pdf.multi_cell(0, 5, _t(f"- {text}   [{rule}]"), new_x="LMARGIN", new_y="NEXT")


def build_pdf(visit: dict, res: dict) -> bytes:
    pdf = _PDF()
    pdf.set_auto_page_break(True, 22)
    pdf.add_page()
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(30, 30, 30)
    rows = [("Patient ID", visit.get("patient_id") or "-"), ("Report date", datetime.now().strftime("%d %b %Y %H:%M")),
            ("GA by LMP", visit.get("weeks_by_lmp") or "Not provided"), ("GA by scan", visit.get("weeks_by_scan") or "Not provided"),
            ("GA used", res.get("ga_used") or "-"),
            ("EFW centile", visit.get("efw_percentile") if visit.get("efw_percentile") not in (None, "") else "Not provided"),
            ("AC centile", visit.get("ac_percentile") if visit.get("ac_percentile") not in (None, "") else "Not provided"),
            ("Amniotic fluid", visit.get("amniotic_fluid") or "Not provided")]
    for i in range(0, len(rows), 2):
        for k, v in rows[i:i + 2]:
            pdf.set_font("Helvetica", "B", 9.5); pdf.cell(30, 6, _t(k + ":"))
            pdf.set_font("Helvetica", "", 9.5); pdf.cell(65, 6, _t(v))
        pdf.ln(6)

    _section(pdf, "Summary")
    pdf.set_font("Helvetica", "B", 11)
    pdf.multi_cell(0, 6, _t(res.get("headline", "")), new_x="LMARGIN", new_y="NEXT")
    if res.get("warnings"):
        _section(pdf, "Warnings")
        _lines(pdf, res["warnings"])
    _section(pdf, "Findings")
    _lines(pdf, res.get("findings", []))
    plan = res.get("surveillance", []) + res.get("delivery", []) + res.get("other_actions", [])
    if plan:
        _section(pdf, "Management per guideline")
        _lines(pdf, plan)
    if res.get("missing"):
        _section(pdf, "Information still needed")
        pdf.set_font("Helvetica", "", 9.5)
        pdf.multi_cell(0, 5, _t(", ".join(res["missing"])), new_x="LMARGIN", new_y="NEXT")
    _section(pdf, "Basis")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.multi_cell(0, 4.5, _t(f"Guideline: {res.get('guideline')}.  Reference chart: {res.get('chart')}.  "
                              f"Rules applied: {', '.join(res.get('rules_fired', []))}."), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(95, 5, "______________________________"); pdf.cell(0, 5, "______________________________", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(95, 5, "Reviewing obstetrician"); pdf.cell(0, 5, "Date / time", new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())
