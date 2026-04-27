from app.core.clinical_rules import evaluate_rules
from app.models.schemas import RMRSubmission, PatientInfo, ABCDEAssessment


def test_low_saturation_is_flagged():
    record = RMRSubmission(patient=PatientInfo(problem_description="shortness of breath"), assessment=ABCDEAssessment(oxygen_saturation=91))
    findings = evaluate_rules(record)
    assert any(f.section == "B: Breathing" for f in findings)


def test_high_oxygen_requires_hudson_mask():
    record = RMRSubmission(patient=PatientInfo(), assessment=ABCDEAssessment(oxygen_l_min=12, oxygen_method="nasal cannula"))
    findings = evaluate_rules(record)
    assert any("Hudson" in f.message_en for f in findings)


def test_fast_heart_after_running_gets_advice_flag():
    record = RMRSubmission(
        patient=PatientInfo(problem_description="the hart is beating too fast"),
        assessment=ABCDEAssessment(performed_actions="running")
    )
    findings = evaluate_rules(record)
    assert any(f.section == "Clinical context" for f in findings)
