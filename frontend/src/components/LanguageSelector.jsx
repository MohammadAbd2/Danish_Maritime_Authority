import React from 'react';
import { Globe2 } from 'lucide-react';

export function LanguageSelector({ language, onChange, t }) {
  return (
    <div className="languageSelector">
      <Globe2 size={18} />
      <button
        className={language === 'en' ? 'active' : ''}
        onClick={() => onChange('en')}
      >
        English
      </button>
      <button
        className={language === 'da' ? 'active' : ''}
        onClick={() => onChange('da')}
      >
        Dansk
      </button>
    </div>
  );
}
