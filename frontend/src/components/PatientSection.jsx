import React from 'react';
import { Stethoscope } from 'lucide-react';
import { Field } from './FormFields';

export function PatientSection({ form, setPatient, t, f }) {
  return (
    <section className='card'>
      <h2><Stethoscope /> {t.rmr}</h2>
      <h3>{t.details}</h3>
      <div className='grid'>
        {['name_title', 'birthdate_cpr', 'gender', 'nationality', 'date', 'utc',
          'shipping_company', 'ship_name', 'ship_email', 'satellite_call_no',
          'call_signal', 'coordinates', 'destination_eta', 'nearest_port_eta',
          'medicine_chest', 'page'].map(k => (
          <Field key={k} label={f[k]} value={form.patient[k]} onChange={v => setPatient(k, v)} />
        ))}

        <Field label={f.has_allergies}>
          <select value={form.patient.has_allergies} onChange={e => setPatient('has_allergies', e.target.value)}>
            <option value='yes'>{t.yes}</option>
            <option value='no'>{t.no}</option>
            <option value='unknown'>{t.unknown}</option>
          </select>
        </Field>
        <Field label={f.allergies_details} value={form.patient.allergies_details} onChange={v => setPatient('allergies_details', v)} />

        <Field label={f.takes_medicine}>
          <select value={form.patient.takes_medicine} onChange={e => setPatient('takes_medicine', e.target.value)}>
            <option value='yes'>{t.yes}</option>
            <option value='no'>{t.no}</option>
            <option value='unknown'>{t.unknown}</option>
          </select>
        </Field>
        <Field label={f.medicine_details} value={form.patient.medicine_details} onChange={v => setPatient('medicine_details', v)} />
      </div>

      <Field wide label={t.problem}>
        <textarea
          placeholder={t.problemPh}
          value={form.patient.problem_description}
          onChange={e => setPatient('problem_description', e.target.value)}
        />
      </Field>
    </section>
  );
}
