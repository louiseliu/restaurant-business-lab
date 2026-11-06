import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './camera-reuse-diagrams.css';
import previews from './camera-reuse-source-previews.json';

export function CameraReuseDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,chain=diagram.layout==='camera-reuse-chain';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`camera-reuse-diagram ${chain?'camera-reuse-chain':'camera-reuse-options'}`} aria-label={diagram.label}>
   <RichNarrative sourcePreviews={previews} id={`${id}:scope`} value={diagram.scope}/>
   <div className="camera-reuse-grid" data-reviewed-rows>{rows.map((row,index)=><section className="camera-reuse-card" key={row['环节']||row['方案']}>
    <header><span className="camera-reuse-number">{String(index+1).padStart(2,'0')}</span><h3>{row['环节']||row['方案']}</h3>{chain&&index<rows.length-1&&<span aria-hidden="true" className="camera-reuse-arrow">↓</span>}</header>
    {Object.entries(row).filter(([key])=>!['环节','方案'].includes(key)).map(([key,value])=><div className={`camera-reuse-cell ${key.includes('边界')||key==='不满足时'?'camera-reuse-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}
   </section>)}</div>
   <RichNarrative sourcePreviews={previews} id={`${id}:completion`} className="camera-reuse-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative sourcePreviews={previews} id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
