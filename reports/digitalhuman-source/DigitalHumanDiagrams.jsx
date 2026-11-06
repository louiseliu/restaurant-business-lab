import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './digitalhuman-diagrams.css';
import previews from './digitalhuman-source-previews.json';

export function DigitalHumanDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,timelines=diagram.layout==='digitalhuman-timelines';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`digitalhuman-diagram ${timelines?'digitalhuman-timelines':'digitalhuman-decisions'}`} aria-label={diagram.label}>
   <RichNarrative sourcePreviews={previews} id={`${id}:scope`} value={diagram.scope}/>
   {timelines ? <div data-reviewed-rows>
    {[['销售记录','直播与买券'],['履约记录','到店与履约']].map(([key,label])=><section className="digitalhuman-lane" key={key}><h3>{label}</h3><ol>{rows.map((row,i)=><li key={row['阶段']}><span>{row['阶段']}</span><p>{row[key]}</p>{i<rows.length-1&&<b aria-hidden="true">→</b>}</li>)}</ol></section>)}
    <section className="digitalhuman-check"><h3>把两条记录接起来核对</h3><ul>{rows.map(row=><li key={row['阶段']}>{row['应核对']}</li>)}</ul></section>
   </div> : <div className="digitalhuman-grid" data-reviewed-rows>{rows.map((row,index)=><section className="digitalhuman-card" key={row['环节']}>
    <header><span className="digitalhuman-number">{String(index+1).padStart(2,'0')}</span><h3>{row['环节']}</h3></header>
    {Object.entries(row).filter(([key])=>key!=='环节').map(([key,value])=><div className={`digitalhuman-cell ${key==='不足时'?'digitalhuman-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}
   </section>)}</div>}
   <RichNarrative sourcePreviews={previews} id={`${id}:completion`} className="digitalhuman-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative sourcePreviews={previews} id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
