from io import BytesIO
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image

try:
    from svglib.svglib import svg2rlg
except Exception:
    svg2rlg = None

DMA_RED = colors.HexColor("#990000")
DMA_BLUE = colors.HexColor("#003b5c")
LIGHT = colors.HexColor("#fff3e5")
LINE = colors.HexColor("#e1c4a5")
MUTED = colors.HexColor("#5b6770")

DA = {
    "title": "AI-understøttet klinisk evalueringssystem for maritim sygepleje",
    "summary": "Radio Medical Record oversigt",
    "details": "Patient- og skibsoplysninger",
    "problem": "Problembeskrivelse",
    "abcde": "ABCDE-vurdering",
    "obs": "Observationsskema",
    "clinical": "Klinisk gennemgang",
    "advice": "Råd og næste handlinger",
    "context": "Uploadet dokumentkontekst",
    "name_title": "Navn / titel", "birthdate_cpr": "Fødselsdato / CPR", "gender": "Køn", "nationality": "Nationalitet", "date": "Dato", "utc": "UTC", "shipping_company": "Rederi", "ship_name": "Skibsnavn", "ship_email": "Skibs-e-mail", "satellite_call_no": "Satellittelefon", "call_signal": "Kaldesignal", "coordinates": "Koordinater", "destination_eta": "Destination/ETA", "nearest_port_eta": "Nærmeste havn/ETA", "medicine_chest": "Medicinkiste", "page": "Side",
    "A": "A Luftvej", "B": "B Vejrtrækning", "C": "C Kredsløb", "D": "D Neurologisk status", "E": "E Eksponering", "Actions": "Handlinger", "Medication": "Medicin",
    "obs_heads": ["Dato", "Tid", "Almentilstand", "Bevidsthed", "Ilt", "Resp.", "SpO2", "Puls", "BT", "Temp", "Blodsukker"],
}
EN = {
    "title": "AI-Assisted Clinical Evaluation System for Maritime Nursing",
    "summary": "Radio Medical Record Summary",
    "details": "Patient and ship details",
    "problem": "Problem description",
    "abcde": "ABCDE assessment",
    "obs": "Observation chart",
    "clinical": "Clinical review",
    "advice": "Advice and next actions",
    "context": "Uploaded document context",
    "name_title": "Name / title", "birthdate_cpr": "Birthdate / CPR", "gender": "Gender", "nationality": "Nationality", "date": "Date", "utc": "UTC", "shipping_company": "Shipping company", "ship_name": "Ship name", "ship_email": "Ship e-mail", "satellite_call_no": "Satellite call no.", "call_signal": "Call signal", "coordinates": "Coordinates", "destination_eta": "Destination/ETA", "nearest_port_eta": "Nearest port/ETA", "medicine_chest": "Medicine chest", "page": "Page",
    "A": "A Airway", "B": "B Breathing", "C": "C Circulation", "D": "D Disability", "E": "E Expose", "Actions": "Actions", "Medication": "Medication",
    "obs_heads": ["Date", "Time", "General", "LOC", "O2", "Breath", "SpO2", "HR", "BP", "Temp", "Sugar"],
}

def _dict(record):
    return DA if record.language == "da" else EN

def _show_en(record):
    return record.language in ("en", "both", "")

def _show_da(record):
    return record.language in ("da", "both")

def _p(text):
    return str(text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")

def _logo_flowable(max_width=7.0*cm):
    logo_path = Path(__file__).resolve().parents[1] / "static" / "dma-logo-crop.svg"
    if svg2rlg and logo_path.exists():
        drawing = svg2rlg(str(logo_path))
        if drawing:
            scale = max_width / max(drawing.width, 1)
            drawing.width *= scale
            drawing.height *= scale
            drawing.scale(scale, scale)
            return drawing
    return Paragraph("DANISH MARITIME AUTHORITY", getSampleStyleSheet()["Heading2"])

def _table(rows, col_widths):
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.25, LINE),
        ("BACKGROUND", (0,0), (0,-1), LIGHT),
        ("BACKGROUND", (2,0), (2,-1), LIGHT),
        ("FONT", (0,0), (-1,-1), "Helvetica", 8),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ]))
    return t

def build_pdf(record, review=None) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.25*cm, leftMargin=1.25*cm, topMargin=1.05*cm, bottomMargin=1.05*cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleDMA", parent=styles["Title"], textColor=DMA_RED, fontSize=17, leading=22, alignment=TA_CENTER, spaceBefore=10, spaceAfter=10))
    styles.add(ParagraphStyle(name="SubDMA", parent=styles["Normal"], textColor=MUTED, fontSize=9, leading=12, alignment=TA_CENTER, spaceAfter=14))
    styles.add(ParagraphStyle(name="SectionDMA", parent=styles["Heading2"], textColor=DMA_RED, fontSize=13, alignment=TA_CENTER, spaceBefore=14, spaceAfter=8))
    styles.add(ParagraphStyle(name="CenterBody", parent=styles["Normal"], alignment=TA_CENTER, leading=13, spaceAfter=6))
    styles.add(ParagraphStyle(name="LeftSmall", parent=styles["Normal"], alignment=TA_LEFT, fontSize=7.5, leading=10))
    styles.add(ParagraphStyle(name="SmallCenter", parent=styles["Normal"], fontSize=8.3, textColor=MUTED, alignment=TA_CENTER, leading=11))
    styles.add(ParagraphStyle(name="ContactLeft", parent=styles["Normal"], fontSize=8.3, textColor=MUTED, alignment=TA_LEFT, leading=11))
    D = _dict(record)
    story = []
    story.append(_logo_flowable())
    story.append(Paragraph("Danish Maritime Authority / Søfartsstyrelsen", styles["ContactLeft"]))
    story.append(Paragraph("Batterivej 2, 4220 Korsør, Denmark", styles["ContactLeft"]))
    story.append(Paragraph("+45 72 19 60 00 · sfs@dma.dk · dma.dk", styles["ContactLeft"]))
    story.append(Spacer(1, 0.8*cm))
    if record.language == "both":
        title = EN["title"] + " / " + DA["title"]
        subtitle = EN["summary"] + " / " + DA["summary"]
    else:
        title, subtitle = D["title"], D["summary"]
    story.append(Paragraph(_p(title), styles["TitleDMA"]))
    story.append(Paragraph(_p(subtitle), styles["SubDMA"]))
    p, a = record.patient, record.assessment
    story.append(Paragraph(D["details"] if record.language != "both" else "Patient and ship details / Patient- og skibsoplysninger", styles["SectionDMA"]))
    info = [
        [D["name_title"], p.name_title, D["birthdate_cpr"], p.birthdate_cpr],
        [D["gender"], p.gender, D["nationality"], p.nationality],
        [D["date"], p.date, D["utc"], p.utc],
        [D["shipping_company"], p.shipping_company, D["ship_name"], p.ship_name],
        [D["ship_email"], p.ship_email, D["satellite_call_no"], p.satellite_call_no],
        [D["call_signal"], p.call_signal, D["coordinates"], p.coordinates],
        [D["destination_eta"], p.destination_eta, D["nearest_port_eta"], p.nearest_port_eta],
        [D["medicine_chest"], p.medicine_chest, D["page"], p.page],
    ]
    story.append(_table(info, [3.2*cm, 4.2*cm, 3.2*cm, 5.2*cm]))
    story.append(Paragraph(D["problem"] if record.language != "both" else "Problem description / Problembeskrivelse", styles["SectionDMA"]))
    story.append(Paragraph(_p(p.problem_description), styles["CenterBody"]))
    story.append(Paragraph(D["abcde"] if record.language != "both" else "ABCDE assessment / ABCDE-vurdering", styles["SectionDMA"]))
    abc = [
        [D["A"], f"Clear/free: {a.airway_clear}; Jaw lift: {a.jaw_lift}; Suction: {a.suction_applied}; Guedel: {a.guedel_airway}; CPR: {a.cpr_initiated_at}; Oxygen: {a.oxygen_l_min} l/min {a.oxygen_method}"],
        [D["B"], f"Rate: {a.breathing_rate}; SpO2: {a.oxygen_saturation}; Other: {a.breathing_other}"],
        [D["C"], f"Capillary: {a.capillary_response_seconds}s; Cannula: {a.venous_cannula_inserted}; Skin: {a.skin_color} {a.skin_feel}; Pulse: {a.pulse}; BP: {a.systolic_bp}/{a.diastolic_bp}"],
        [D["D"], f"Consciousness: {a.consciousness_level}; Convulsions: {a.convulsions}; Paralysis: {a.paralysis}; Pupils normal: {a.pupil_reaction_normal}; {a.pupil_reaction_description}"],
        [D["E"], f"Top-to-toe: {a.expose_exam_performed}; Findings: {a.expose_findings}; Temperature: {a.temperature_mouth}; Alternative: {a.temperature_alternative}"],
        [D["Actions"], a.performed_actions],
        [D["Medication"], a.medication_given],
    ]
    t2 = Table([[x, Paragraph(_p(y), styles["CenterBody"])] for x,y in abc], colWidths=[3*cm, 13*cm])
    t2.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.25, LINE),("BACKGROUND", (0,0), (0,-1), LIGHT),("FONT", (0,0), (-1,-1), "Helvetica", 8),("VALIGN", (0,0), (-1,-1), "TOP"),("ALIGN", (0,0), (-1,-1), "CENTER")]))
    story.append(t2)
    if record.observations:
        story.append(Paragraph(D["obs"] if record.language != "both" else "Observation chart / Observationsskema", styles["SectionDMA"]))
        rows = [D["obs_heads"]]
        for r in record.observations:
            rows.append([r.date, r.time, r.general_condition, r.consciousness_level, r.oxygen_l_min, r.breathing_rate, r.oxygen_saturation, r.heart_rate, r.blood_pressure, r.temperature_mouth, r.blood_sugar])
        ot = Table(rows, repeatRows=1)
        ot.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.25, LINE),("BACKGROUND", (0,0), (-1,0), DMA_RED),("TEXTCOLOR", (0,0), (-1,0), colors.white),("FONT", (0,0), (-1,-1), "Helvetica", 7),("ALIGN", (0,0), (-1,-1), "CENTER")]))
        story.append(ot)
    if record.uploaded_context:
        story.append(Paragraph(D["context"] if record.language != "both" else "Uploaded document context / Uploadet dokumentkontekst", styles["SectionDMA"]))
        story.append(Paragraph(_p(record.uploaded_context[:2200]), styles["LeftSmall"]))
    if review:
        story.append(PageBreak())
        story.append(Paragraph(D["clinical"] if record.language != "both" else "Clinical review / Klinisk gennemgang", styles["SectionDMA"]))
        story.append(Paragraph(f"Score: {review.score}/100", styles["CenterBody"]))
        if _show_en(record): story.append(Paragraph(_p(review.summary_en), styles["CenterBody"]))
        if _show_da(record): story.append(Paragraph(_p(review.summary_da), styles["CenterBody"]))
        for f in review.findings:
            story.append(Paragraph(_p(f"{f.severity.upper()} · {f.section}"), styles["SectionDMA"]))
            if _show_en(record): story.append(Paragraph(_p(f.message_en + " " + f.recommendation_en), styles["CenterBody"]))
            if _show_da(record): story.append(Paragraph(_p(f.message_da + " " + f.recommendation_da), styles["CenterBody"]))
        story.append(Paragraph(D["advice"] if record.language != "both" else "Advice / Råd", styles["SectionDMA"]))
        if _show_en(record):
            for en in review.advice_en: story.append(Paragraph("• " + _p(en), styles["CenterBody"]))
        if _show_da(record):
            for da in review.advice_da: story.append(Paragraph("• " + _p(da), styles["CenterBody"]))
    doc.build(story)
    return buffer.getvalue()
