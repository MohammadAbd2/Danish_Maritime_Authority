import React from 'react';
import { Field, SelectBool, Check } from './FormFields';

export function AirwaySection({ assessment, setAssessment, t, f, L }) {
  return (
    <section className='card'>
      <h2>{t.airway}</h2>
      <div className='grid'>
        <Field label={f.clear}>
          <SelectBool t={t} value={assessment.airway_clear} onChange={v => setAssessment('airway_clear', v)} />
        </Field>
        <Check label={f.jaw} checked={assessment.jaw_lift} onChange={v => setAssessment('jaw_lift', v)} />
        <Check label={f.suction} checked={assessment.suction_applied} onChange={v => setAssessment('suction_applied', v)} />
        <Check label={f.guedel} checked={assessment.guedel_airway} onChange={v => setAssessment('guedel_airway', v)} />
        <Field label={f.cpr} value={assessment.cpr_initiated_at} onChange={v => setAssessment('cpr_initiated_at', v)} />
        <Field label={f.oxygen} type='number' value={assessment.oxygen_l_min} onChange={v => setAssessment('oxygen_l_min', v)} />
        <Field label={f.oxygenMethod}>
          <select value={assessment.oxygen_method} onChange={e => setAssessment('oxygen_method', e.target.value)}>
            <option></option>
            <option>Nasal cannula ≤ 5 l/min</option>
            <option>Hudson mask &gt;10 l/min</option>
          </select>
        </Field>
        <Field label={f.injury}>
          <SelectBool t={t} value={assessment.neck_back_injury_suspected} onChange={v => setAssessment('neck_back_injury_suspected', v)} />
        </Field>
      </div>
    </section>
  );
}

export function BreathingSection({ assessment, setAssessment, t, f }) {
  return (
    <section className='card'>
      <h2>{t.breathing}</h2>
      <div className='grid'>
        <Check label={f.fast} checked={assessment.breathing_description_fast} onChange={v => setAssessment('breathing_description_fast', v)} />
        <Check label={f.slow} checked={assessment.breathing_description_slow} onChange={v => setAssessment('breathing_description_slow', v)} />
        <Check label={f.shallow} checked={assessment.breathing_description_shallow} onChange={v => setAssessment('breathing_description_shallow', v)} />
        <Check label={f.deep} checked={assessment.breathing_description_deep} onChange={v => setAssessment('breathing_description_deep', v)} />
        <Check label={f.normal} checked={assessment.breathing_description_normal} onChange={v => setAssessment('breathing_description_normal', v)} />
        <Field label={f.other} value={assessment.breathing_other} onChange={v => setAssessment('breathing_other', v)} />
        <Field label={f.breaths} type='number' value={assessment.breathing_rate} onChange={v => setAssessment('breathing_rate', v)} />
        <Field label={f.spo2} type='number' value={assessment.oxygen_saturation} onChange={v => setAssessment('oxygen_saturation', v)} />
      </div>
    </section>
  );
}

export function CirculationSection({ assessment, setAssessment, t, f, L }) {
  return (
    <section className='card'>
      <h2>{t.circulation}</h2>
      <div className='grid'>
        <Field label={f.cap} type='number' value={assessment.capillary_response_seconds} onChange={v => setAssessment('capillary_response_seconds', v)} />
        <Field label={f.cannula}>
          <SelectBool t={t} value={assessment.venous_cannula_inserted} onChange={v => setAssessment('venous_cannula_inserted', v)} />
        </Field>
        <Field label={f.skinColor}>
          <select value={assessment.skin_color} onChange={e => setAssessment('skin_color', e.target.value)}>
            <option>Normal</option>
            <option>Pale</option>
            <option>Reddish</option>
            <option>Bluish</option>
          </select>
        </Field>
        <Field label={f.skinFeel} value={assessment.skin_feel} onChange={v => setAssessment('skin_feel', v)} />
        <Field label={f.pulse} type='number' value={assessment.pulse} onChange={v => setAssessment('pulse', v)} />
        <Field label={f.measured}>
          <select value={assessment.pulse_measured_at} onChange={e => setAssessment('pulse_measured_at', e.target.value)}>
            <option value='wrist'>{L === 'da' ? 'håndled' : 'wrist'}</option>
            <option value='neck'>{L === 'da' ? 'hals' : 'neck'}</option>
            <option value='groin'>{L === 'da' ? 'lyske' : 'groin'}</option>
          </select>
        </Field>
        <Field label={f.sys} type='number' value={assessment.systolic_bp} onChange={v => setAssessment('systolic_bp', v)} />
        <Field label={f.dia} type='number' value={assessment.diastolic_bp} onChange={v => setAssessment('diastolic_bp', v)} />
      </div>
    </section>
  );
}

export function DisabilitySection({ assessment, setAssessment, t, f, L }) {
  return (
    <section className='card'>
      <h2>{t.disability}</h2>
      <div className='grid'>
        <Field label={f.loc}>
          <select value={assessment.consciousness_level} onChange={e => setAssessment('consciousness_level', e.target.value)}>
            <option value='1'>{L === 'da' ? '1 Vågen, klar og orienteret' : '1 Awake, alert and well orientated'}</option>
            <option value='2'>{L === 'da' ? '2 Uklar, svarer på spørgsmål' : '2 Unclear, responds to questions'}</option>
            <option value='3'>{L === 'da' ? '3 Reagerer på smertestimuli' : '3 Responds to pain stimuli'}</option>
            <option value='4'>{L === 'da' ? '4 Bevidstløs, reagerer ikke' : '4 Unconscious/unresponsive'}</option>
          </select>
        </Field>
        <Field label={f.conv}>
          <SelectBool t={t} value={assessment.convulsions} onChange={v => setAssessment('convulsions', v)} />
        </Field>
        <Field label={f.para}>
          <SelectBool t={t} value={assessment.paralysis} onChange={v => setAssessment('paralysis', v)} />
        </Field>
        <Field label={f.pupil}>
          <SelectBool t={t} value={assessment.pupil_reaction_normal} onChange={v => setAssessment('pupil_reaction_normal', v)} />
        </Field>
      </div>
      <Field wide label={f.pupilDesc} value={assessment.pupil_reaction_description} onChange={v => setAssessment('pupil_reaction_description', v)} />
    </section>
  );
}

export function ExposeSection({ assessment, setAssessment, t, f }) {
  return (
    <section className='card'>
      <h2>{t.expose}</h2>
      <div className='grid'>
        <Field label={f.top}>
          <SelectBool t={t} value={assessment.expose_exam_performed} onChange={v => setAssessment('expose_exam_performed', v)} />
        </Field>
        <Field label={f.hypo}>
          <SelectBool t={t} value={assessment.hypothermia_overheating_checked} onChange={v => setAssessment('hypothermia_overheating_checked', v)} />
        </Field>
        <Field label={f.tempMeasured}>
          <SelectBool t={t} value={assessment.temperature_measured} onChange={v => setAssessment('temperature_measured', v)} />
        </Field>
        <Field label={f.tempMouth} type='number' value={assessment.temperature_mouth} onChange={v => setAssessment('temperature_mouth', v)} />
        <Field label={f.altTemp} value={assessment.temperature_alternative} onChange={v => setAssessment('temperature_alternative', v)} />
        <Field label={f.where} value={assessment.where} onChange={v => setAssessment('where', v)} />
      </div>
      <Field wide label={f.injuryFind} value={assessment.expose_findings} onChange={v => setAssessment('expose_findings', v)} />
      <Field wide label={f.hypoFind} value={assessment.hypothermia_overheating_findings} onChange={v => setAssessment('hypothermia_overheating_findings', v)} />
      <Field wide label={f.actions} value={assessment.performed_actions} onChange={v => setAssessment('performed_actions', v)} />
      <Field wide label={f.meds} value={assessment.medication_given} onChange={v => setAssessment('medication_given', v)} />
      <div className='grid'>
        <Field label={f.time1} value={assessment.action_time_1} onChange={v => setAssessment('action_time_1', v)} />
        <Field label={f.time2} value={assessment.action_time_2} onChange={v => setAssessment('action_time_2', v)} />
        <Field label={f.time3} value={assessment.action_time_3} onChange={v => setAssessment('action_time_3', v)} />
        <Field label={f.time4} value={assessment.action_time_4} onChange={v => setAssessment('action_time_4', v)} />
        <Field label={f.officer} value={assessment.medical_officer_name_title} onChange={v => setAssessment('medical_officer_name_title', v)} />
      </div>
    </section>
  );
}
