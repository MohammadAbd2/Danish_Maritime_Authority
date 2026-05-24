function num(v) {
  if (v === '' || v === null || v === undefined) return null;
  // Handle range formats like "60-90"
  if (typeof v === 'string' && v.includes('-')) {
    const parts = v.split('-');
    return Number(parts[parts.length - 1]) || null; // Take the last number
  }
  return Number(v);
}

function bool(v) {
  if (v === 'true' || v === true) return true;
  if (v === 'false' || v === false) return false;
  return null;
}

export function prep(form) {
  const clean = JSON.parse(JSON.stringify(form));
  ['oxygen_l_min', 'breathing_rate', 'oxygen_saturation', 'capillary_response_seconds', 'pulse',
    'systolic_bp', 'diastolic_bp', 'consciousness_level', 'temperature_mouth'].forEach(k =>
    clean.assessment[k] = num(clean.assessment[k]));
  ['airway_clear', 'neck_back_injury_suspected', 'venous_cannula_inserted', 'convulsions',
    'paralysis', 'pupil_reaction_normal', 'expose_exam_performed', 'hypothermia_overheating_checked',
    'temperature_measured'].forEach(k => clean.assessment[k] = bool(clean.assessment[k]));
  clean.observations = clean.observations.map(r => ({
    ...r,
    general_condition: num(r.general_condition),
    consciousness_level: num(r.consciousness_level),
    oxygen_l_min: num(r.oxygen_l_min),
    breathing_rate: num(r.breathing_rate),
    capillary_response_seconds: num(r.capillary_response_seconds),
    oxygen_saturation: num(r.oxygen_saturation),
    heart_rate: num(r.heart_rate),
    temperature_mouth: num(r.temperature_mouth),
    blood_sugar: num(r.blood_sugar)
  }));
  return clean;
}

export function langCode(form) {
  return form.language === 'da' ? 'da' : 'en';
}
