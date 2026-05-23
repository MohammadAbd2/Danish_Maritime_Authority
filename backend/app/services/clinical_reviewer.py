import json
import os
from app.core.clinical_rules import evaluate_rules
from app.models.schemas import RMRSubmission, ReviewResponse
from app.services.rag_store import RAGStore

SYSTEM_PROMPT = """
You are a careful bilingual clinical documentation auditor for maritime nursing simulation training.
You do not diagnose. You review whether the Radio Medical Record is complete, consistent, and safe to communicate to Radio Medical.
Use ABCDE structure. Provide practical advice in English and Danish.
""".strip()

try:
    import ollama
    OLLAMA_AVAILABLE = True
except:
    OLLAMA_AVAILABLE = False

class ClinicalReviewer:
    def __init__(self):
        self.rag = RAGStore()

    def review(self, record: RMRSubmission) -> ReviewResponse:
        # Get rule-based findings first
        rule_findings = evaluate_rules(record)
        
        # Generate AI-enhanced findings with actual LLM
        findings = self._generate_ai_findings(record, rule_findings)
        
        query = " ".join([
            record.patient.problem_description,
            record.assessment.performed_actions,
            record.uploaded_context[:800],
            "ABCDE vitals oxygen pulse blood pressure observation chart"
        ])
        context = self.rag.retrieve(query)
        
        penalty = sum({"critical": 25, "major": 15, "minor": 7}.get(f.severity, 5) for f in findings)
        score = max(0, 100 - penalty)
        
        # Generate AI advice
        advice_en, advice_da = self._generate_ai_advice(record, findings)
        
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

    def _generate_ai_findings(self, record: RMRSubmission, rule_findings):
        """Generate AI-enhanced findings using LLM if available"""
        if not OLLAMA_AVAILABLE:
            return rule_findings
        
        try:
            # Create context about the patient data
            a = record.assessment
            p = record.patient
            obs_text = f"Observations: {len(record.observations)} rows recorded"
            if record.observations:
                obs = record.observations[0]
                obs_text += f" - Latest: BR {obs.breathing_rate}, SpO2 {obs.oxygen_saturation}, HR {obs.heart_rate}, BP {obs.blood_pressure}"
            
            prompt = f"""Given this maritime patient assessment, generate clinical findings with severity levels and bilingual recommendations:

Patient: {p.name_title}
Problem: {p.problem_description}
Assessment: Breathing {a.breathing_rate}/min, SpO2 {a.oxygen_saturation}%, Pulse {a.pulse}, BP {a.systolic_bp}/{a.diastolic_bp}, Temp {a.temperature_mouth}C
{obs_text}
Actions taken: {a.performed_actions}

Generate 3-5 findings in JSON format with fields: severity (critical/major/minor), section (A-E), message_en, message_da, recommendation_en, recommendation_da
Focus on what's abnormal and clinically relevant. Make findings specific to this patient's data."""

            response = ollama.generate(model="mistral", prompt=prompt, stream=False)
            
            if response and response.get("response"):
                ai_advice = response["response"].strip()
                # Try to parse JSON findings from response
                try:
                    import re
                    json_match = re.search(r'\[.*\]', ai_advice, re.DOTALL)
                    if json_match:
                        ai_findings_data = json.loads(json_match.group())
                        from app.models.schemas import Finding
                        # Combine rule findings with AI findings
                        ai_findings = []
                        for item in ai_findings_data[:5]:  # Max 5 findings
                            if all(k in item for k in ["severity", "section", "message_en", "message_da", "recommendation_en", "recommendation_da"]):
                                ai_findings.append(Finding(
                                    severity=item.get("severity", "minor"),
                                    section=item.get("section", "General"),
                                    message_en=item.get("message_en", ""),
                                    message_da=item.get("message_da", ""),
                                    recommendation_en=item.get("recommendation_en", ""),
                                    recommendation_da=item.get("recommendation_da", "")
                                ))
                        if ai_findings:
                            return ai_findings + rule_findings[:3]  # AI findings first, then rules
                except:
                    pass
        except Exception:
            pass
        
        return rule_findings

    def _generate_ai_advice(self, record: RMRSubmission, findings):
        """Generate AI-based advice using LLM"""
        if not OLLAMA_AVAILABLE:
            # Fallback to template-based advice
            return self._build_template_advice(record, findings)
        
        try:
            a = record.assessment
            p = record.patient
            
            prompt = f"""As a maritime clinical advisor, generate practical clinical advice for this Radio Medical case in English and Danish.

Patient presentation: {p.problem_description}
Actions taken: {a.performed_actions}
Current vitals: BR {a.breathing_rate}/min, SpO2 {a.oxygen_saturation}%, Pulse {a.pulse}/min, BP {a.systolic_bp}/{a.diastolic_bp}, Temp {a.temperature_mouth}C
Consciousness: Level {a.consciousness_level}

Generate 5-7 specific, actionable pieces of advice. Return as:
EN: [advice items separated by |]
DA: [Danish advice items separated by |]

Be specific with actual vital values. Focus on what needs to be done next and what to monitor."""

            response = ollama.generate(model="mistral", prompt=prompt, stream=False)
            
            if response and response.get("response"):
                advice_text = response["response"].strip()
                en_list = []
                da_list = []
                
                # Parse EN and DA sections
                lines = advice_text.split("\n")
                for line in lines:
                    if line.startswith("EN:"):
                        en_text = line.replace("EN:", "").strip()
                        en_list = [x.strip() for x in en_text.split("|") if x.strip()]
                    elif line.startswith("DA:"):
                        da_text = line.replace("DA:", "").strip()
                        da_list = [x.strip() for x in da_text.split("|") if x.strip()]
                
                if en_list and da_list:
                    return en_list[:7], da_list[:7]
        except Exception:
            pass
        
        # Fallback
        return self._build_template_advice(record, findings)

    def _build_template_advice(self, record, findings):
        """Template-based advice as fallback"""
        a = record.assessment
        en = []
        da = []
        
        if a.breathing_rate and a.breathing_rate > 16:
            en.append(f"Breathing rate is elevated at {a.breathing_rate}/min. Document oxygen saturation trends and re-assess after interventions.")
            da.append(f"Respirationsfrekvensen er forhøjet ved {a.breathing_rate}/min. Dokumentér udvikling i iltmætning og revurdér efter indsats.")
        
        if a.pulse and a.pulse > 80:
            en.append(f"Pulse is elevated at {a.pulse}/min. Monitor for symptoms and compare with blood pressure and skin findings.")
            da.append(f"Puls er forhøjet ved {a.pulse}/min. Overvåg symptomer og sammenlign med blodtryk og hudfund.")
        
        if a.systolic_bp and a.systolic_bp > 140:
            en.append(f"Blood pressure elevated at {a.systolic_bp}/{a.diastolic_bp}. Re-check after rest and document trend.")
            da.append(f"Blodtryk forhøjet ved {a.systolic_bp}/{a.diastolic_bp}. Mål igen efter hvile og dokumentér udvikling.")
        
        if a.temperature_mouth and a.temperature_mouth > 38:
            en.append("Fever noted. Document exposure history and any infections. Consider active cooling if >39C.")
            da.append("Feber konstateret. Dokumentér eksponering og infektioner. Overvej aktiv nedkøling hvis >39C.")
        
        if a.consciousness_level and a.consciousness_level >= 2:
            en.append("Reduced consciousness recorded. Ensure pupil reaction is documented and escalate to Radio Medical.")
            da.append("Nedsat bevidsthed registreret. Sikr pupilfund dokumenteret og eskalér til Radio Medical.")
        
        if not en:
            en = ["Record is mostly complete. Continue monitoring vital signs and document trends.", 
                  "Prepare concise handover summary focusing on changes since first assessment."]
            da = ["Journal er overvejende komplet. Fortsæt med at overvåge vitale værdier og dokumentér udvikling.",
                  "Forbered præcis overleveringstekst fokuseret på ændringer siden første vurdering."]
        
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

    def _translate_text(self, text, target_lang="en"):
        """Translate Danish text to English or vice versa using Ollama if available."""
        if not OLLAMA_AVAILABLE or not text or not text.strip():
            return text
        
        try:
            if target_lang == "en":
                prompt = f"Translate this Danish text to English. Only return the translation, nothing else:\n{text}"
            else:
                prompt = f"Translate this English text to Danish. Only return the translation, nothing else:\n{text}"
            
            response = ollama.generate(model="mistral", prompt=prompt, stream=False)
            if response and response.get("response"):
                return response["response"].strip()
        except Exception:
            pass
        return text

    def langchain_prompt_payload(self, record: RMRSubmission, findings):
        return {
            "system": SYSTEM_PROMPT,
            "human": json.dumps(record.model_dump(), indent=2),
            "rule_findings": [f.model_dump() for f in findings],
        }
