import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './platform-appeals-diagrams.css';

export function PlatformAppealsDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`, responsibility=diagram.layout==='platform-appeals-responsibility';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`platform-appeals-diagram ${responsibility?'platform-appeals-responsibility':'platform-appeals-routes'}`} aria-label={diagram.label}>
   <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
   <div className="platform-appeals-grid" data-reviewed-rows>{rows.map((row,index)=><section className="platform-appeals-card" key={row['责任层次']||row['经营情形']}>
    <header><span className="platform-appeals-number">{String(index+1).padStart(2,'0')}</span><h3>{row['责任层次']||row['经营情形']}</h3></header>
    {Object.entries(row).filter(([key])=>!['责任层次','经营情形'].includes(key)).map(([key,value])=><div className={`platform-appeals-cell ${key.includes('边界')||key.includes('限制')?'platform-appeals-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}
   </section>)}</div>
   <RichNarrative id={`${id}:completion`} className="platform-appeals-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
