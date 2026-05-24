export const API = 'http://localhost:8000/api';

export const emptyObs = {
  date: '', time: '', general_condition: '', consciousness_level: '', oxygen_l_min: '',
  breathing_rate: '', capillary_response_seconds: '', oxygen_saturation: '', heart_rate: '',
  blood_pressure: '', temperature_mouth: '', pupil_reaction: '', venous_cannula_inserted: '',
  intravenous_fluid_drops_min: '', fluid_intake_drink: '', urine_24h: '', urine_sticks: '',
  blood_sugar: '', malaria_test: '', crp_test: ''
};

export const empty = {
  language: 'en',
  uploaded_context: '',
  patient: {
    name_title: '', birthdate_cpr: '', gender: '', nationality: '', date: '', utc: '',
    shipping_company: '', ship_name: '', ship_email: '', satellite_call_no: '', call_signal: '',
    coordinates: '', destination_eta: '', nearest_port_eta: '', medicine_chest: '', page: '1 of 1',
    has_allergies: 'unknown', allergies_details: '', takes_medicine: 'unknown', medicine_details: '',
    problem_description: ''
  },
  assessment: {
    airway_clear: null, jaw_lift: false, suction_applied: false, guedel_airway: false,
    cpr_initiated_at: '', oxygen_l_min: '', oxygen_method: '', neck_back_injury_suspected: null,
    breathing_description_fast: false, breathing_description_slow: false, breathing_description_shallow: false,
    breathing_description_deep: false, breathing_description_normal: true, breathing_other: '',
    breathing_rate: '', oxygen_saturation: '', capillary_response_seconds: '', venous_cannula_inserted: null,
    skin_color: 'Normal', skin_feel: '', pulse: '', pulse_measured_at: 'wrist', systolic_bp: '',
    diastolic_bp: '', consciousness_level: 1, convulsions: null, paralysis: null, pupil_reaction_normal: true,
    pupil_reaction_description: '', expose_exam_performed: null, expose_findings: '',
    hypothermia_overheating_checked: null, hypothermia_overheating_findings: '', temperature_measured: null,
    temperature_mouth: '', temperature_alternative: '', performed_actions: '', medication_given: '',
    action_time_1: '', action_time_2: '', action_time_3: '', action_time_4: '', medical_officer_name_title: '',
    where: ''
  },
  observations: [emptyObs]
};

// General condition options for dropdowns
export const conditions = ['Good', 'Fair', 'Poor', 'Critical'];
