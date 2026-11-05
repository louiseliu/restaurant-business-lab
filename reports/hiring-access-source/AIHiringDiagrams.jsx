import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './ai-hiring-diagrams.css';
export function AIHiringDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`, workflow=diagram.layout==='ai-hiring-workflow';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`ai-hiring-diagram ${workflow?'ai-hiring-workflow':'ai-hiring-options'}`} aria-label={diagram.label}>
   <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
   <div className="ai-hiring-grid" data-reviewed-rows>{rows.map((row,index)=><section className="ai-hiring-card" key={row['环节']||row['经营情形']}>
    <header><span className="ai-hiring-number">{String(index+1).padStart(2,'0')}</span><h3>{row['环节']||row['经营情形']}</h3></header>
    {Object.entries(row).filter(([key])=>!['环节','经营情形'].includes(key)).map(([key,value])=><div className={`ai-hiring-cell ${key.includes('停')||key.includes('边界')?'ai-hiring-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}
    {workflow&&index<rows.length-1&&<span className="ai-hiring-arrow" aria-hidden="true">→</span>}
   </section>)}</div>
   <RichNarrative id={`${id}:completion`} className="ai-hiring-conclusion" value={diagram.completion}/>
   <RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
  </figure>
 </DataComponent>;
}
