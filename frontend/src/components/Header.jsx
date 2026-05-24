import React from 'react';
import { Ship } from 'lucide-react';

export function Header({ t }) {
  return (
    <header className='hero'>
      <div className='heroText'>
        <p>Radio Medical Record intelligence</p>
        <h1>{t.title}</h1>
        <span>{t.subtitle}</span>
      </div>
      <Ship size={58} />
    </header>
  );
}
