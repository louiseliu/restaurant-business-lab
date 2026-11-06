import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './siteselection-diagrams.css';
import previews from './siteselection-source-previews.json';

export function SiteSelectionDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`;
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className="siteselection-diagram" aria-label={diagram.label}>
   <RichNarrative sourcePreviews={previews} id={`${id}:scope`} value={diagram.scope}/>
   <ol className="siteselection-stages" data-reviewed-rows>{rows.map((row,i)=><li key={row['任务']}>
    <header><span>{String(i+1).padStart(2,'0')}</span><h3>{row['任务']}</h3></header>
    <p>{row['能回答什么']}</p><div className="siteselection-question"><h4>进入下一步前，还要核对</h4><p>{row['还缺什么']}</p></div>
    {i<rows.length-1&&<span className="siteselection-arrow" aria-hidden="true">↓</span>}
   </li>)}</ol>
   <RichNarrative sourcePreviews={previews} id={`${id}:completion`} className="siteselection-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative sourcePreviews={previews} id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
