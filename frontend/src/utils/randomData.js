import { empty, emptyObs, conditions } from './constants';

export function randomData() {
  const names = ['Mohammad Abd Al Rahem', 'James Patterson', 'Anna Christensen', 'Roberto Silva', 'Emma Hansen', 'Chen Wei', 'Aisha Okafor', 'Jan Kowalski', 'Sophia Rossi', 'Ahmed Hassan'];
  const genders = ['Male', 'Female'];
  const nationalities = ['Syrian', 'British', 'Danish', 'Portuguese', 'Swedish', 'Chinese', 'Nigerian', 'Polish', 'Italian', 'Egyptian'];
  const ships = ['MV Ocean Explorer', 'Titanic Training Vessel', 'Nordic Star', 'Northern Wind', 'Sea Guardian', 'Coastal Voyager', 'Pacific Breeze', 'Atlantic Wave'];
  const companies = ['Denmark Ship', 'Nordic Shipping', 'Global Maritime', 'North Sea Lines', 'European Vessels', 'Ocean Corp', 'Maritime Services'];
  const destinations = ['Copenhagen/14:00', 'Korsør/16:00', 'Hamburg/18:00', 'Oslo/12:00', 'Stockholm/20:00', 'Amsterdam/15:00'];
  const skinColors = ['Normal', 'Pale', 'Reddish', 'Bluish'];

  const randItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
  const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

  return {
    ...empty,
    language: 'en',
    patient: {
      ...empty.patient,
      name_title: randItem(names),
      birthdate_cpr: `${rand(1, 28)}/${rand(1, 12)}/${rand(1950, 2010)}`,
      gender: randItem(genders),
      nationality: randItem(nationalities),
      date: new Date().toLocaleDateString('en-GB'),
      utc: `${String(rand(0, 23)).padStart(2, '0')}:${String(rand(0, 59)).padStart(2, '0')}`,
      shipping_company: randItem(companies),
      ship_name: randItem(ships),
      ship_email: `ship${rand(1, 999)}@dma.dk`,
      satellite_call_no: `+${rand(10000, 99999)} ${rand(10000, 99999)} ${rand(1000, 9999)}`,
      call_signal: `${String.fromCharCode(rand(65, 90))}${String.fromCharCode(rand(65, 90))}${rand(100, 999)}`,
      coordinates: `${(rand(50, 60) + Math.random()).toFixed(3)}, ${(rand(0, 15) + Math.random()).toFixed(3)}`,
      destination_eta: randItem(destinations),
      nearest_port_eta: randItem(destinations.slice(0, 3)),
      medicine_chest: randItem(['Category A', 'Category B', 'Category C']),
      page: '1 of 1',
      has_allergies: randItem(['yes', 'no', 'unknown']),
      allergies_details: ['Penicillin', 'Shellfish', 'Latex', ''][rand(0, 3)],
      takes_medicine: randItem(['yes', 'no', 'unknown']),
      medicine_details: ['Aspirin', 'Metoprolol', 'Insulin', ''][rand(0, 3)],
      problem_description: ['Patient reports chest pain and shortness of breath.', 'Head injury after fall on deck. Minor bleeding.', 'Severe gastrointestinal symptoms with fever.', 'Injury to left leg with swelling and bruising.', 'Suspected allergic reaction with rash.'][rand(0, 4)]
    },
    assessment: {
      ...empty.assessment,
      airway_clear: Math.random() > 0.3,
      jaw_lift: Math.random() > 0.7,
      suction_applied: Math.random() > 0.7,
      guedel_airway: Math.random() > 0.8,
      cpr_initiated_at: '',
      oxygen_l_min: Math.random() > 0.7 ? rand(1, 8) : null,
      oxygen_method: ['Nasal cannula ≤ 5 l/min', 'Hudson mask >10 l/min', ''][rand(0, 2)],
      neck_back_injury_suspected: Math.random() > 0.7 ? Math.random() > 0.5 : null,
      breathing_description_fast: Math.random() > 0.5,
      breathing_description_slow: Math.random() > 0.8,
      breathing_description_shallow: Math.random() > 0.8,
      breathing_description_deep: Math.random() > 0.7,
      breathing_description_normal: Math.random() > 0.5,
      breathing_other: '',
      breathing_rate: rand(12, 30),
      oxygen_saturation: rand(92, 100),
      capillary_response_seconds: rand(1, 4),
      venous_cannula_inserted: Math.random() > 0.7 ? Math.random() > 0.5 : null,
      skin_color: randItem(skinColors),
      skin_feel: ['Warm', 'Cold', 'Clammy', 'Dry'][rand(0, 3)],
      pulse: rand(55, 120),
      pulse_measured_at: ['wrist', 'neck', 'groin'][rand(0, 2)],
      systolic_bp: rand(110, 160),
      diastolic_bp: rand(60, 95),
      consciousness_level: rand(1, 2),
      convulsions: Math.random() > 0.9 ? Math.random() > 0.5 : false,
      paralysis: Math.random() > 0.9 ? Math.random() > 0.5 : false,
      pupil_reaction_normal: Math.random() > 0.3,
      pupil_reaction_description: ['Equal and reactive', 'Dilated', 'Constricted', 'Slow to react'][rand(0, 3)],
      expose_exam_performed: Math.random() > 0.4,
      expose_findings: ['No signs of injury', 'Bruising on left leg', 'Rash on trunk', 'Minor lacerations'][rand(0, 3)],
      hypothermia_overheating_checked: Math.random() > 0.6,
      hypothermia_overheating_findings: '',
      temperature_measured: Math.random() > 0.3,
      temperature_mouth: parseFloat((36.5 + (Math.random() - 0.5) * 3).toFixed(1)),
      temperature_alternative: '',
      performed_actions: ['Patient was placed in recovery position and monitored.', 'IV line established, fluids administered.', 'Oxygen therapy initiated, vital signs monitored.', 'Wound cleaned and bandaged.'][rand(0, 3)],
      medication_given: ['Aspirin 500mg', 'Paracetamol 1000mg', 'Ibuprofen 400mg', 'None'][rand(0, 3)],
      action_time_1: '',
      action_time_2: '',
      action_time_3: '',
      action_time_4: '',
      medical_officer_name_title: randItem(names) + ', Medical Officer',
      where: 'Deck'
    },
    observations: [{
      ...emptyObs,
      date: new Date().toLocaleDateString('en-GB'),
      time: `${String(rand(0, 23)).padStart(2, '0')}:${String(rand(0, 59)).padStart(2, '0')}`,
      general_condition: randItem(conditions),
      consciousness_level: rand(1, 2),
      oxygen_l_min: Math.random() > 0.6 ? rand(1, 5) : null,
      breathing_rate: rand(12, 28),
      capillary_response_seconds: rand(1, 3),
      oxygen_saturation: rand(94, 100),
      heart_rate: rand(60, 110),
      blood_pressure: `${rand(110, 160)}/${rand(60, 95)}`,
      temperature_mouth: parseFloat((36.5 + (Math.random() - 0.5) * 2).toFixed(1)),
      pupil_reaction: '+ / +',
      venous_cannula_inserted: Math.random() > 0.6 ? 'yes' : 'no',
      intravenous_fluid_drops_min: Math.random() > 0.7 ? `${rand(10, 30)}` : '',
      fluid_intake_drink: ['Water given', 'Juice given', 'No fluids', 'Tea given'][rand(0, 3)],
      urine_24h: 'Normal',
      urine_sticks: 'Normal',
      blood_sugar: parseFloat((5 + Math.random() * 4).toFixed(1)),
      malaria_test: 'Negative',
      crp_test: 'Normal'
    }]
  };
}
