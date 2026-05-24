import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ClipboardCheck, Download } from 'lucide-react';
import './styles.css';

// Components
import { Header } from './components/Header';
import { Toolbar } from './components/Toolbar';
import { PatientSection } from './components/PatientSection';
import { AirwaySection, BreathingSection, CirculationSection, DisabilitySection, ExposeSection } from './components/AssessmentSections';
import { ObservationSection } from './components/ObservationSection';
import { ReviewSection } from './components/ReviewSection';

// Utils
import { API, empty, emptyObs } from './utils/constants';
import { prep, langCode } from './utils/dataUtils';
import { randomData } from './utils/randomData';
import { i18n, fieldLabels, obsLabels } from './utils/i18n';

function App() {
  const [form, setForm] = useState(empty);
  const [review, setReview] = useState(null);
  const [uploadInfo, setUploadInfo] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [serverStatus, setServerStatus] = useState('checking');

  const L = langCode(form);
  const t = i18n[L];
  const f = fieldLabels[L];
  const ob = obsLabels[L];
  const showEn = form.language === 'en';
  const showDa = form.language === 'da';

  // Server health check
  async function checkServer() {
    try {
      const r = await fetch(`${API}/health`, { cache: 'no-store' });
      setServerStatus(r.ok ? 'running' : 'down');
    } catch {
      setServerStatus('down');
    }
  }

  useEffect(() => {
    checkServer();
    const id = setInterval(checkServer, 4000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    if (uploadInfo) setForm(x => ({ ...x, uploaded_context: uploadInfo.preview || '' }));
  }, [uploadInfo]);

  // Form state setters
  const setPatient = (k, v) => setForm(x => ({ ...x, patient: { ...x.patient, [k]: v } }));
  const setAssessment = (k, v) => setForm(x => ({ ...x, assessment: { ...x.assessment, [k]: v } }));
  const setObs = (i, k, v) => setForm(x => ({ ...x, observations: x.observations.map((r, idx) => idx === i ? { ...r, [k]: v } : r) }));

  // API calls
  async function submit() {
    setBusy(true);
    setError('');
    try {
      const r = await fetch(`${API}/review`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(prep(form)) });
      if (!r.ok) { let e = await r.text(); throw new Error(e || 'Review failed'); }
      setReview(await r.json());
    } catch (e) {
      setError(e.message || 'Could not connect to backend');
      setServerStatus('down');
    } finally {
      setBusy(false);
    }
  }

  async function upload(e) {
    const file = e.target.files[0];
    if (!file) return;
    const fd = new FormData();
    fd.append('file', file);
    setBusy(true);
    setError('');
    try {
      const r = await fetch(`${API}/files/upload`, { method: 'POST', body: fd });
      if (!r.ok) throw new Error(await r.text());
      const data = await r.json();
      setUploadInfo(data);
      setForm(x => ({ ...x, uploaded_context: data.preview || '' }));
      if (data.extracted_data) { autoFillFromExtracted(data.extracted_data); }
    } catch (err) {
      setError(err.message || 'Upload failed');
      setServerStatus('down');
    } finally {
      setBusy(false);
      e.target.value = '';
    }
  }

  function autoFillFromExtracted(extracted) {
    setForm(x => {
      const updated = { ...x };
      if (extracted.name_title) updated.patient.name_title = extracted.name_title;
      if (extracted.birthdate_cpr) updated.patient.birthdate_cpr = extracted.birthdate_cpr;
      if (extracted.gender) updated.patient.gender = extracted.gender;
      if (extracted.nationality) updated.patient.nationality = extracted.nationality;
      if (extracted.ship_name) updated.patient.ship_name = extracted.ship_name;
      if (extracted.coordinates) updated.patient.coordinates = extracted.coordinates;
      if (extracted.problem_description) updated.patient.problem_description = extracted.problem_description;
      if (extracted.breathing_rate) updated.assessment.breathing_rate = extracted.breathing_rate;
      if (extracted.oxygen_saturation) updated.assessment.oxygen_saturation = extracted.oxygen_saturation;
      if (extracted.pulse) updated.assessment.pulse = extracted.pulse;
      if (extracted.systolic_bp) updated.assessment.systolic_bp = parseInt(extracted.systolic_bp);
      if (extracted.diastolic_bp) updated.assessment.diastolic_bp = parseInt(extracted.diastolic_bp);
      if (extracted.temperature_mouth) updated.assessment.temperature_mouth = extracted.temperature_mouth;
      if (extracted.airway_clear !== undefined) updated.assessment.airway_clear = extracted.airway_clear;
      if (extracted.breathing_description_fast !== undefined) updated.assessment.breathing_description_fast = extracted.breathing_description_fast;
      if (extracted.breathing_description_slow !== undefined) updated.assessment.breathing_description_slow = extracted.breathing_description_slow;
      if (extracted.breathing_description_shallow !== undefined) updated.assessment.breathing_description_shallow = extracted.breathing_description_shallow;
      if (extracted.breathing_description_deep !== undefined) updated.assessment.breathing_description_deep = extracted.breathing_description_deep;
      if (extracted.pupil_reaction_normal !== undefined) updated.assessment.pupil_reaction_normal = extracted.pupil_reaction_normal;
      if (extracted.consciousness_level) updated.assessment.consciousness_level = extracted.consciousness_level;
      return updated;
    });
  }

  async function clearUpload() {
    setUploadInfo(null);
    setForm(x => ({ ...x, uploaded_context: '' }));
    try { await fetch(`${API}/files/clear`, { method: 'DELETE' }); } catch { }
  }

  async function exportPdf() {
    setBusy(true);
    setError('');
    try {
      const r = await fetch(`${API}/export/pdf`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(prep(form)) });
      if (!r.ok) throw new Error(await r.text());
      const blob = await r.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = form.language === 'da' ? 'radio-medical-journal.pdf' : 'radio-medical-record-review.pdf';
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(e.message || 'PDF export failed');
      setServerStatus('down');
    } finally {
      setBusy(false);
    }
  }

  function addObservation() {
    setForm(x => ({ ...x, observations: [...x.observations, { ...emptyObs }] }));
  }

  function removeObservation(index) {
    if (form.observations.length <= 1) return; // Keep at least one row
    setForm(x => ({ ...x, observations: x.observations.filter((_, i) => i !== index) }));
  }

  return (
    <main>
      <Header t={t} />

      <Toolbar
        form={form}
        setForm={setForm}
        t={t}
        upload={upload}
        randomData={() => setForm(randomData())}
        serverStatus={serverStatus}
        uploadInfo={uploadInfo}
        clearUpload={clearUpload}
      />

      {uploadInfo && (
        <section className='card contextBox'>
          <h3>{t.contextPreview}</h3>
          <p>{t.pdfNote}</p>
          <pre>{uploadInfo.preview}</pre>
        </section>
      )}

      <PatientSection form={form} setPatient={setPatient} t={t} f={f} />

      <AirwaySection assessment={form.assessment} setAssessment={setAssessment} t={t} f={f} L={L} />
      <BreathingSection assessment={form.assessment} setAssessment={setAssessment} t={t} f={f} />
      <CirculationSection assessment={form.assessment} setAssessment={setAssessment} t={t} f={f} L={L} />
      <DisabilitySection assessment={form.assessment} setAssessment={setAssessment} t={t} f={f} L={L} />
      <ExposeSection assessment={form.assessment} setAssessment={setAssessment} t={t} f={f} />

      <ObservationSection
        observations={form.observations}
        setObs={setObs}
        addObs={addObservation}
        removeObs={removeObservation}
        t={t}
        ob={ob}
        emptyObs={emptyObs}
      />

      {error && (
        <section className='card errorBox'>
          <b>{t.conn}</b>
          <p>{error}</p>
        </section>
      )}

      <div className='actions'>
        <button className='primary' onClick={submit} disabled={busy || serverStatus === 'down'}>
          <ClipboardCheck /> {busy ? t.working : t.review}
        </button>
        <button className='secondary' onClick={exportPdf} disabled={busy || serverStatus === 'down'}>
          <Download /> {busy ? t.working : t.export}
        </button>
      </div>

      <ReviewSection review={review} t={t} showEn={showEn} showDa={showDa} />
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
