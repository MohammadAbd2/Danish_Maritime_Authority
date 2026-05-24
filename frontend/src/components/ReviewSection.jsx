import React from 'react';
import { AlertTriangle, Globe2 } from 'lucide-react';

export function ReviewSection({ review, t, showEn, showDa }) {
  if (!review) return null;

  return (
    <section className='card result'>
      <h2>{t.findings}</h2>
      <div className='score'>{t.score}: {review.score}/100</div>
      {showEn && <p>{review.summary_en}</p>}
      {showDa && <p>{review.summary_da}</p>}

      <div className='findings'>
        {review.findings.map((r, i) => (
          <article className={'finding ' + r.severity} key={i}>
            <b>
              <AlertTriangle size={16} />
              {r.severity} · {r.section}
            </b>
            {showEn && (
              <>
                <p>{r.message_en}</p>
                <small>{r.recommendation_en}</small>
              </>
            )}
            {showDa && (
              <>
                <p>{r.message_da}</p>
                <small>{r.recommendation_da}</small>
              </>
            )}
          </article>
        ))}
      </div>

      <h3>{t.advice}</h3>
      <div className='advice'>
        {showEn && (
          <div>
            <h4><Globe2 size={16} /> English</h4>
            {review.advice_en.map((x, i) => <p key={i}>• {x}</p>)}
          </div>
        )}
        {showDa && (
          <div>
            <h4><Globe2 size={16} /> Dansk</h4>
            {review.advice_da.map((x, i) => <p key={i}>• {x}</p>)}
          </div>
        )}
      </div>
    </section>
  );
}
