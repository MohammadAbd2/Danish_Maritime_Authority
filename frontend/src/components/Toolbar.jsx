import React from 'react';
import { Upload, Server, WifiOff, CheckCircle2, Trash2, Wand2 } from 'lucide-react';
import { LanguageSelector } from './LanguageSelector';

export function Toolbar({ form, setForm, t, upload, randomData, serverStatus, uploadInfo, clearUpload }) {
  return (
    <section className='toolbar card'>
      <LanguageSelector
        language={form.language}
        onChange={(lang) => setForm({ ...form, language: lang })}
        t={t}
      />

      <label className='upload'>
        <Upload size={18} />
        {t.upload}
        <input
          type='file'
          accept='.pdf,.docx,.txt,.png,.jpg,.jpeg,.webp,.tif,.tiff'
          onChange={upload}
        />
      </label>

      <button className='secondary smallBtn' onClick={randomData}>
        <Wand2 size={18} />
        {t.random}
      </button>

      <div className={'serverStatus ' + serverStatus}>
        {serverStatus === 'running' ? <Server size={16} /> : <WifiOff size={16} />}
        {t.server}: {serverStatus}
      </div>

      {uploadInfo && (
        <div className='uploadChip'>
          <CheckCircle2 size={16} />
          <span>{uploadInfo.filename}: {uploadInfo.characters} chars</span>
          <button onClick={clearUpload} title={t.remove}>
            <Trash2 size={15} />
          </button>
        </div>
      )}
    </section>
  );
}
