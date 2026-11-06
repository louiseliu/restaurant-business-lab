import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './menu-retention-diagrams.css';
import previews from './menu-retention-source-previews.json';
const Copy=({id,value,className})=><RichNarrative id={id} value={value} className={className} sourcePreviews={previews}/>;
function Card({row,index,boundary=false}){return <section className={`menu-retention-card ${boundary?'menu-retention-unresolved':''}`}><span className="menu-retention-index" aria-hidden="true">{String(index+1).padStart(2,'0')}</span><div className="menu-retention-stage">{row['阶段']}</div><h3>{row['标题']}</h3><p>{row['内容']}</p><p className="menu-retention-limit">{row['边界']}</p><small>{row['性质']}</small></section>;}
export function MenuRetentionDiagram({diagram,id,rows}){
 const q=`diagram-${id}`,evidence=diagram.layout==='menu-retention-evidence';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className="menu-retention-diagram" aria-label={diagram.label}>
  <Copy id={`${id}:scope`} value={diagram.scope}/>
  <div className={`menu-retention-cards ${evidence?'menu-retention-evidence':'menu-retention-options'}`} data-reviewed-rows>{rows.map((row,i)=><Card row={row} index={i} boundary={evidence&&i===2} key={row['标题']}/>)}</div>
  <Copy id={`${id}:completion`} className="menu-retention-conclusion" value={diagram.completion}/>
  <figcaption><Copy id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
 </figure></DataComponent>;
}
