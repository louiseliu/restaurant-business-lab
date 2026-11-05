import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './forecast-reimport-diagrams.css';
import previews from './forecast-reimport-source-previews.json';

export function ForecastReimportDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,chain=diagram.layout==='forecast-reimport-chain';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`forecast-reimport-diagram ${chain?'forecast-reimport-chain':'forecast-reimport-options'}`} aria-label={diagram.label}>
   <RichNarrative sourcePreviews={previews} id={`${id}:scope`} value={diagram.scope}/>
   <div className="forecast-reimport-grid" data-reviewed-rows>{rows.map((row,index)=><section className="forecast-reimport-card" key={row['环节']||row['方案']}>
    <header><span className="forecast-reimport-number">{String(index+1).padStart(2,'0')}</span><h3>{row['环节']||row['方案']}</h3>{chain&&index<rows.length-1&&<span aria-hidden="true" className="forecast-reimport-arrow">↓</span>}</header>
    {Object.entries(row).filter(([key])=>!['环节','方案'].includes(key)).map(([key,value])=><div className={`forecast-reimport-cell ${key.includes('边界')||key==='不满足时'?'forecast-reimport-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}
   </section>)}</div>
   <RichNarrative sourcePreviews={previews} id={`${id}:completion`} className="forecast-reimport-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative sourcePreviews={previews} id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
