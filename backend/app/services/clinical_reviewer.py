import json
from app.core.clinical_rules import evaluate_rules
from app.models.schemas import RMRSubmission, ReviewResponse
from app.services.rag_store import RAGStore

SYSTEM_PROMPT = """
You are a careful bilingual clinical documentation auditor for maritime nursing simulation training.
You do not diagnose. You review whether the Radio Medical Record is complete, consistent, and safe to communicate to Radio Medical.
Use ABCDE structure. Provide practical advice in English and Danish.
""".strip()

class ClinicalReviewer:
    def __init__(self):
        self.rag = RAGStore()

    def review(self, record: RMRSubmission) -> ReviewResponse:
        findings = evaluate_rules(record)
        query = " ".join([
            record.patient.problem_description,
            record.assessment.performed_actions,
            record.uploaded_context[:800],
            "ABCDE vitals oxygen pulse blood pressure observation chart"
        ])
        context = self.rag.retrieve(query)
        penalty = sum({"critical": 25, "major": 15, "minor": 7}.get(f.severity, 5) for f in findings)
        score = max(0, 100 - penalty)
        advice_en, advice_da = self._build_advice(record, findings)
        summary_en = "The record is ready for review with only minor improvements." if score >= 80 else "The record needs improvements before it is sent to Radio Medical."
        summary_da = "Journalen er klar til gennemgang med få mindre forbedringer." if score >= 80 else "Journalen bør forbedres, før den sendes til Radio Medical."
        return ReviewResponse(
            score=score,
            summary_en=summary_en,
            summary_da=summary_da,
            findings=findings,
            advice_en=advice_en,
            advice_da=advice_da,
            llm_feedback_en=self._format_feedback(findings, advice_en, "en"),
            llm_feedback_da=self._format_feedback(findings, advice_da, "da"),
            retrieved_context=context,
        )

    def _build_advice(self, record, findings):
        a = record.assessment
        p = record.patient
        text = f"{p.problem_description} {a.performed_actions} {record.uploaded_context[:1500]}".lower()
        en = []
        da = []
        def add(en_text, da_text):
            if en_text not in en:
                en.append(en_text)
            if da_text not in da:
                da.append(da_text)
        if any(f.section.startswith("A") for f in findings):
            add("Start the Radio Medical handover with airway status, interventions already performed, oxygen flow and CPR start time if relevant.", "Start overleveringen til Radio Medical med luftvejsstatus, udførte interventioner, iltflow og CPR-starttidspunkt hvis relevant.")
        if a.breathing_rate or a.oxygen_saturation or any(f.section.startswith("B") for f in findings):
            add(f"Breathing should be rechecked and trended: current rate {a.breathing_rate or 'not recorded'}/min and SpO2 {a.oxygen_saturation or 'not recorded'}%.", f"Vejrtrækningen bør revurderes og følges over tid: aktuel frekvens {a.breathing_rate or 'ikke angivet'}/min og SpO2 {a.oxygen_saturation or 'ikke angivet'}%.")
        if a.pulse or any(w in text for w in ["heart", "hart", "hjerte", "palpitation", "hurtig puls", "hjertebanken"]):
            add("Because the case describes possible tachycardia, document pulse rate, rhythm regularity, blood pressure, SpO2, chest pain, dizziness and shortness of breath, then repeat after rest.", "Da casen beskriver mulig takykardi, dokumentér puls, regelmæssighed, blodtryk, SpO2, brystsmerter, svimmelhed og åndenød, og gentag efter hvile.")
        if any(w in text for w in ["running", "ran", "løb", "løber", "jogging"]):
            add("Recent running may explain a fast pulse, but it is only safe to use that explanation after reassessment. Record time since running, hydration, rest period and whether the pulse decreases.", "Nylig løb kan forklare hurtig puls, men forklaringen bør først bruges efter revurdering. Dokumentér tid siden løb, væskeindtag, hvileperiode og om pulsen falder.")
        if a.systolic_bp or a.diastolic_bp or any(f.section.startswith("C") for f in findings):
            add(f"For circulation, compare pulse {a.pulse or 'not recorded'} with blood pressure {a.systolic_bp or '?'}/{a.diastolic_bp or '?'} and skin findings; write whether values improve or worsen.", f"For kredsløb, sammenhold puls {a.pulse or 'ikke angivet'} med blodtryk {a.systolic_bp or '?'}/{a.diastolic_bp or '?'} og hudfund; skriv om værdierne forbedres eller forværres.")
        if a.consciousness_level and int(a.consciousness_level) >= 2:
            add("Reduced or unclear consciousness should be paired with pupil findings, blood sugar if possible, and clear escalation to Radio Medical.", "Nedsat eller uklar bevidsthed bør kobles med pupilfund, blodsukker hvis muligt, og tydelig eskalering til Radio Medical.")
        if a.temperature_mouth or a.hypothermia_overheating_checked is not None:
            add("When temperature is relevant, document exposure, wet clothing, environment and whether active warming/cooling was started.", "Når temperatur er relevant, dokumentér eksponering, vådt tøj, omgivelser og om aktiv opvarmning/køling er startet.")
        if record.uploaded_context:
            snippet = record.uploaded_context.strip().replace("\n", " ")[:220]
            add("Use the uploaded document as supporting context, but verify the extracted text against the original file before sending: " + snippet, "Brug det uploadede dokument som støtte, men kontrollér den udtrukne tekst mod originalfilen før afsendelse: " + snippet)
        for f in findings[:3]:
            add("Priority correction: " + f.recommendation_en, "Prioriteret rettelse: " + f.recommendation_da)
        if not en:
            add("The record is mostly complete. During presentation, focus on the timeline, current vital signs and what changed after interventions.", "Journalen er overvejende komplet. Ved præsentation bør fokus være tidslinje, aktuelle vitale værdier og hvad der ændrede sig efter interventioner.")
        return en[:7], da[:7]

    def _format_feedback(self, findings, advice, lang):
        if not findings:
            return "No major issues found. Continue documenting objective findings and trends." if lang == "en" else "Ingen større problemer fundet. Fortsæt med at dokumentere objektive fund og udvikling."
        title = "Clinical review feedback" if lang == "en" else "Klinisk dokumentationsfeedback"
        lines = [title + ":"]
        for i, f in enumerate(findings, 1):
            msg = f.message_en if lang == "en" else f.message_da
            rec = f.recommendation_en if lang == "en" else f.recommendation_da
            lines.append(f"{i}. {f.section}: {msg} {rec}")
        lines.append("Advice:" if lang == "en" else "Råd:")
        lines.extend([f"- {x}" for x in advice])
        return "\n".join(lines)

    def langchain_prompt_payload(self, record: RMRSubmission, findings):
        return {
            "system": SYSTEM_PROMPT,
            "human": json.dumps(record.model_dump(), indent=2),
            "rule_findings": [f.model_dump() for f in findings],
        }
