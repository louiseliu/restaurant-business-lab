import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './supplier-alias-diagrams.css';
import previews from './supplier-alias-source-previews.json';

export function SupplierAliasDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,chain=diagram.layout==='supplier-alias-chain';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`supplier-alias-diagram ${chain?'supplier-alias-chain':'supplier-alias-options'}`} aria-label={diagram.label}>
   <RichNarrative sourcePreviews={previews} id={`${id}:scope`} value={diagram.scope}/>
   <div className="supplier-alias-grid" data-reviewed-rows>{rows.map((row,index)=><section className="supplier-alias-card" key={row['环节']||row['方案']}>
    <header><span className="supplier-alias-number">{String(index+1).padStart(2,'0')}</span><h3>{row['环节']||row['方案']}</h3>{chain&&index<rows.length-1&&<span aria-hidden="true" className="supplier-alias-arrow">↓</span>}</header>
    {Object.entries(row).filter(([key])=>!['环节','方案'].includes(key)).map(([key,value])=><div className={`supplier-alias-cell ${key.includes('边界')||key==='不满足时'?'supplier-alias-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}
   </section>)}</div>
   <RichNarrative sourcePreviews={previews} id={`${id}:completion`} className="supplier-alias-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative sourcePreviews={previews} id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
