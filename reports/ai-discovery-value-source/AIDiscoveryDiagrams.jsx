import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './ai-discovery-value-diagrams.css';
import previews from './ai-discovery-value-source-previews.json';

export function AIDiscoveryDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,budget=diagram.layout==='ai-discovery-value-budget';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`ai-discovery-value-diagram ${budget?'ai-discovery-value-budget':'ai-discovery-value-evidence'}`} aria-label={diagram.label}>
   <RichNarrative sourcePreviews={previews} id={`${id}:scope`} value={diagram.scope}/>
   <div className="ai-discovery-value-grid" data-reviewed-rows>{rows.map((row,index)=><section className="ai-discovery-value-card" key={row['口径']||row['预算']}>
    <header><span className="ai-discovery-value-number">{String(index+1).padStart(2,'0')}</span><h3>{row['口径']||row['预算']}</h3></header>
    {Object.entries(row).filter(([key])=>!['口径','预算'].includes(key)).map(([key,value])=><div className={`ai-discovery-value-cell ${key==='不能推出'||key==='暂停或缩小条件'?'ai-discovery-value-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}
   </section>)}</div>
   <RichNarrative sourcePreviews={previews} id={`${id}:completion`} className="ai-discovery-value-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative sourcePreviews={previews} id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
