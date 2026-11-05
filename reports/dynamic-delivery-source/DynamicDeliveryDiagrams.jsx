import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './dynamic-delivery-diagrams.css';

export function DynamicDeliveryDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,chain=diagram.layout==='dynamic-delivery-chain';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`dynamic-delivery-diagram ${chain?'dynamic-delivery-chain':'dynamic-delivery-options'}`} aria-label={diagram.label}>
   <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
   <div className="dynamic-delivery-grid" data-reviewed-rows>{rows.map((row,index)=><section className="dynamic-delivery-card" key={row['环节']||row['方案']}>
    <header><span className="dynamic-delivery-number">{String(index+1).padStart(2,'0')}</span><h3>{row['环节']||row['方案']}</h3>{chain&&index<rows.length-1&&<span aria-hidden="true" className="dynamic-delivery-arrow">↓</span>}</header>
    {Object.entries(row).filter(([key])=>!['环节','方案'].includes(key)).map(([key,value])=><div className={`dynamic-delivery-cell ${key.includes('边界')||key==='不满足时'?'dynamic-delivery-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}
   </section>)}</div>
   <RichNarrative id={`${id}:completion`} className="dynamic-delivery-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
