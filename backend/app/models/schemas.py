from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class PatientInfo(BaseModel):
    name_title: str = ""
    birthdate_cpr: str = ""
    gender: str = ""
    nationality: str = ""
    date: str = ""
    utc: str = ""
    shipping_company: str = ""
    ship_name: str = ""
    ship_email: str = ""
    satellite_call_no: str = ""
    call_signal: str = ""
    coordinates: str = ""
    destination_eta: str = ""
    nearest_port_eta: str = ""
    medicine_chest: str = ""
    page: str = "1 of 1"
    has_allergies: str = "unknown"
    allergies_details: str = ""
    takes_medicine: str = "unknown"
    medicine_details: str = ""
    problem_description: str = ""

class ABCDEAssessment(BaseModel):
    airway_clear: Optional[bool] = None
    jaw_lift: bool = False
    suction_applied: bool = False
    guedel_airway: bool = False
    cpr_initiated_at: str = ""
    oxygen_l_min: Optional[float] = None
    oxygen_method: str = ""
    neck_back_injury_suspected: Optional[bool] = None
    breathing_description_fast: bool = False
    breathing_description_slow: bool = False
    breathing_description_shallow: bool = False
    breathing_description_deep: bool = False
    breathing_description_normal: bool = False
    breathing_other: str = ""
    breathing_rate: Optional[int] = None
    oxygen_saturation: Optional[int] = None
    capillary_response_seconds: Optional[float] = None
    venous_cannula_inserted: Optional[bool] = None
    skin_color: str = ""
    skin_feel: str = ""
    pulse: Optional[int] = None
    pulse_measured_at: str = ""
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    consciousness_level: Optional[int] = None
    convulsions: Optional[bool] = None
    paralysis: Optional[bool] = None
    pupil_reaction_normal: Optional[bool] = None
    pupil_reaction_description: str = ""
    expose_exam_performed: Optional[bool] = None
    expose_findings: str = ""
    hypothermia_overheating_checked: Optional[bool] = None
    hypothermia_overheating_findings: str = ""
    temperature_measured: Optional[bool] = None
    temperature_mouth: Optional[float] = None
    temperature_alternative: str = ""
    performed_actions: str = ""
    medication_given: str = ""
    action_time_1: str = ""
    action_time_2: str = ""
    action_time_3: str = ""
    action_time_4: str = ""
    medical_officer_name_title: str = ""
    where: str = ""

class ObservationRow(BaseModel):
    date: str = ""
    time: str = ""
    general_condition: Optional[int] = None
    consciousness_level: Optional[int] = None
    oxygen_l_min: Optional[float] = None
    breathing_rate: Optional[int] = None
    capillary_response_seconds: Optional[float] = None
    oxygen_saturation: Optional[int] = None
    heart_rate: Optional[int] = None
    blood_pressure: str = ""
    temperature_mouth: Optional[float] = None
    pupil_reaction: str = ""
    venous_cannula_inserted: str = ""
    intravenous_fluid_drops_min: str = ""
    fluid_intake_drink: str = ""
    urine_24h: str = ""
    urine_sticks: str = ""
    blood_sugar: Optional[float] = None
    malaria_test: str = ""
    crp_test: str = ""

class UploadedDocument(BaseModel):
    filename: str
    characters: int
    preview: str

class RMRSubmission(BaseModel):
    patient: PatientInfo
    assessment: ABCDEAssessment
    observations: List[ObservationRow] = Field(default_factory=list)
    language: str = "both"
    uploaded_context: str = ""

class Finding(BaseModel):
    severity: str
    section: str
    message_en: str
    message_da: str
    recommendation_en: str
    recommendation_da: str

class ReviewResponse(BaseModel):
    score: int
    summary_en: str
    summary_da: str
    findings: List[Finding]
    advice_en: List[str] = Field(default_factory=list)
    advice_da: List[str] = Field(default_factory=list)
    llm_feedback_en: str = ""
    llm_feedback_da: str = ""
    retrieved_context: List[str] = Field(default_factory=list)
    raw_debug: Dict[str, Any] = Field(default_factory=dict)
