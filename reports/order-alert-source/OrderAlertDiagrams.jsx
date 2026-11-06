import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './order-alert-diagrams.css';
import previews from './order-alert-source-previews.json';
const Copy=({id,value,className})=><RichNarrative id={id} value={value} className={className} sourcePreviews={previews}/>;
function Card({row,variant=''}){return <section className={`order-alert-card order-alert-${variant}`}><header><span>{row['阶段']}</span><h3>{row['标题']}</h3></header><p>{row['内容']}</p><p className="order-alert-limit">{row['边界']}</p><small>{row['性质']}</small></section>;}
function Printer({active}){return <div className={`order-alert-printer-scene ${active?'has-ticket':'ticket-taken'}`} aria-hidden="true"><div className="order-alert-printer"><span className="order-alert-slot"/><span className="order-alert-ticket"><i/><i/><i/></span></div><span className="order-alert-signal-wire"/><div className="order-alert-lamp"><span/></div></div>;}
export function OrderAlertDiagram({diagram,id,rows}){
 const q=`diagram-${id}`,boundary=diagram.layout==='order-alert-boundary';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className="order-alert-diagram" aria-label={diagram.label}>
  <Copy id={`${id}:scope`} value={diagram.scope}/>
  {boundary?<div className="order-alert-boundary">
   <div className="order-alert-state-pair" data-reviewed-rows>{rows.slice(0,2).map((row,i)=><section className="order-alert-state" key={row['标题']}><Printer active={i===0}/><Card row={row} variant={i===0?'waiting':'taken'}/></section>)}</div>
   <Copy id={`${id}:visibility`} className="order-alert-divider" value={diagram.visibility}/>
   <div className="order-alert-business-states" data-reviewed-rows>{rows.slice(2,5).map(row=><Card row={row} key={row['标题']} variant="business"/>)}</div>
   <div data-reviewed-rows><Card row={rows[5]} variant="no-signal"/></div>
  </div>:<div className="order-alert-trial">
   <div data-reviewed-rows><Card row={rows[0]} variant="safe-path"/></div>
   <div className="order-alert-test-grid" data-reviewed-rows>{rows.slice(1,7).map((row,i)=><div className="order-alert-test" key={row['标题']}><span className="order-alert-test-number" aria-hidden="true">{String(i+1).padStart(2,'0')}</span><Card row={row} variant="test"/></div>)}</div>
   <div data-reviewed-rows><Card row={rows[7]} variant="record"/></div>
  </div>}
  <Copy id={`${id}:completion`} className="order-alert-conclusion" value={diagram.completion}/>
  <figcaption><Copy id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
 </figure></DataComponent>;
}
