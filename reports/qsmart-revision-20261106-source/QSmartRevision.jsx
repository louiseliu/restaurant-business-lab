import React from 'react';
import {DataComponent, RichNarrative, useDataApp} from '../../data-app-public.jsx';
import './qsmart-revision.css';

export function QSmartRevision({item, revision}) {
 const {reviewedRows}=useDataApp();
 const q=`diagram-${item.id}:revision-2026-11-06`, rows=reviewedRows(q), d=revision.diagram;
 return <section className="qsmart-revision" id={`read-${item.id}-revision-2026-11-06`} tabIndex={-1}>
  <RichNarrative id={`${item.id}:revision-2026-11-06:heading`} value={`## ${revision.title}\n\n${revision.intro}`}/>
  {revision.paragraphs.slice(0,2).map((p,i)=><RichNarrative key={i} id={`${item.id}:revision-2026-11-06:paragraph:${i}`} value={p}/>)}
  <DataComponent id={q} queryId={q} kind="custom" title={d.label} sourceRows={rows} displayRows={rows} description={d.scope}>
   <figure className="qsmart-revision-figure" aria-label={d.label}>
    <RichNarrative id={`${item.id}:revision-2026-11-06:scope`} value={d.scope}/>
    <div className="qsmart-revision-options" data-reviewed-rows>{rows.map(row=><section key={row['方案']}>
     <h3>{row['方案']}</h3>
     {Object.entries(row).filter(([k])=>k!=='方案').map(([k,v])=><div key={k}><h4>{k}</h4><p>{v}</p></div>)}
    </section>)}</div>
    <RichNarrative id={`${item.id}:revision-2026-11-06:completion`} className="qsmart-revision-conclusion" value={d.completion}/>
    <figcaption><RichNarrative id={`${item.id}:revision-2026-11-06:diagram-note`} value={d.note}/></figcaption>
   </figure>
  </DataComponent>
  {revision.paragraphs.slice(2).map((p,i)=><RichNarrative key={i} id={`${item.id}:revision-2026-11-06:paragraph:${i+2}`} value={p}/>)}
  <details className="study-original"><summary>本次补充的研究说明与来源边界</summary><div>
   <RichNarrative id={`${item.id}:revision-2026-11-06:research-note`} value={revision.researchNote}/>
   <RichNarrative id={`${item.id}:revision-2026-11-06:ledger-context`} value={revision.ledgerContext}/>
   <RichNarrative id={`${item.id}:revision-2026-11-06:source-ledger`} value={revision.sourceLedger}/>
  </div></details>
 </section>;
}
