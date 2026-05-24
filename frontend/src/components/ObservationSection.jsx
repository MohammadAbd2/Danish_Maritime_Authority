import React from 'react';
import { Trash2 } from 'lucide-react';
import { Field } from './FormFields';
import { conditions } from '../utils/constants';

export function ObservationSection({ observations, setObs, addObs, removeObs, t, ob, emptyObs }) {
  return (
    <section className='card'>
      <h2>{t.obs}</h2>
      {observations.map((r, i) => (
        <div className='obsRow' key={i}>
          <div className='obs'>
            {Object.keys(emptyObs).map(k => {
              // Add dropdown for general_condition field
              if (k === 'general_condition') {
                return (
                  <Field key={k} label={ob[k]}>
                    <select value={r[k]} onChange={e => setObs(i, k, e.target.value)}>
                      <option value=""></option>
                      {conditions.map(condition => (
                        <option key={condition} value={condition}>{condition}</option>
                      ))}
                    </select>
                  </Field>
                );
              }
              return <Field key={k} label={ob[k]} value={r[k]} onChange={v => setObs(i, k, v)} />;
            })}
          </div>
          {observations.length > 1 && (
            <button className='removeObsBtn' onClick={() => removeObs(i)} title={t.removeObs || 'Remove observation row'}>
              <Trash2 size={18} />
            </button>
          )}
        </div>
      ))}
      <button className='secondary' onClick={addObs}>{t.addObs}</button>
    </section>
  );
}
