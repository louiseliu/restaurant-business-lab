import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './aipractice-diagrams.css';
import previews from './aipractice-source-previews.json';

const Copy=({id,value,className})=><RichNarrative id={id} value={value} className={className} sourcePreviews={previews}/>;
function EvidenceCard({row,index}){
 return <section className={`aipractice-evidence-card aipractice-evidence-card-${index}`}>
  <header><span className="aipractice-number">{String(index+1).padStart(2,'0')}</span><h3>{row['材料']}</h3></header>
  <div className="aipractice-cell"><h4>材料支持到这里</h4><p>{row['能确认']}</p></div>
  <div className="aipractice-cell aipractice-limit"><h4>这里仍然未知</h4><p>{row['不能补写']}</p></div>
 </section>;
}
function StepCard({row,variant}){
 return <section className={`aipractice-step aipractice-step-${variant||'main'}`}>
  <header><span className="aipractice-stage">{row['阶段']}</span><h3>{row['方法']}</h3></header>
  <p>{row['观察']}</p><p className="aipractice-step-limit">{row['限制']}</p>
 </section>;
}
export function AIPracticeDiagram({diagram,id,rows}){
 const q=`diagram-${id}`,evidence=diagram.layout==='aipractice-evidence';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className="aipractice-diagram" aria-label={diagram.label}>
   <Copy id={`${id}:scope`} value={diagram.scope}/>
   {evidence?<div className="aipractice-evidence">
    <div className="aipractice-official-pair" data-reviewed-rows>{rows.slice(0,2).map((row,index)=><EvidenceCard key={row['材料']} row={row} index={index}/>)}</div>
    <div className="aipractice-uncertain"><span aria-hidden="true">┄ ? ┄</span><Copy id={`${id}:relationship`} value={diagram.relationship}/></div>
    <div className="aipractice-vendor" data-reviewed-rows><EvidenceCard row={rows[2]} index={2}/></div>
    <div className="aipractice-uncertain"><span aria-hidden="true">?</span><Copy id={`${id}:vendor-relationship`} value={diagram.vendorRelationship}/></div>
   </div>:<div className="aipractice-validation" data-reviewed-rows>
    <StepCard row={rows[0]} variant="start"/>
    <div className="aipractice-arrow" aria-hidden="true">↓</div>
    <div className="aipractice-practice-options">{rows.slice(1,4).map(row=><StepCard key={row['方法']} row={row} variant="option"/>)}</div>
    <Copy id={`${id}:comparability`} className="aipractice-comparability" value={diagram.comparability}/>
    <div className="aipractice-merge" aria-hidden="true"><span>↓</span><span>↓</span><span>↓</span></div>
    <StepCard row={rows[4]} variant="test"/>
    <div className="aipractice-arrow" aria-hidden="true">↓</div>
    <StepCard row={rows[5]} variant="decision"/>
   </div>}
   <Copy id={`${id}:completion`} className="aipractice-conclusion" value={diagram.completion}/>
   <figcaption><Copy id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
