import React from 'react';

export function Field({ label, value, onChange, type = 'text', children, wide = false }) {
  return (
    <label className={'field ' + (wide ? 'wide' : '')}>
      <span>{label}</span>
      {children || <input type={type} value={value ?? ''} onChange={e => onChange(e.target.value)} />}
    </label>
  );
}

export function SelectBool({ value, onChange, t }) {
  return (
    <select value={value === null ? '' : String(value)} onChange={e => onChange(e.target.value === '' ? null : e.target.value === 'true')}>
      <option value=''>{t.select}</option>
      <option value='true'>{t.yes}</option>
      <option value='false'>{t.no}</option>
    </select>
  );
}

export function Check({ label, checked, onChange }) {
  return (
    <label className='check'>
      <input type='checkbox' checked={!!checked} onChange={e => onChange(e.target.checked)} />
      {label}
    </label>
  );
}
