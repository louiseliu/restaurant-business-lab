import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './reservation-policy-diagrams.css';
import previews from './reservation-policy-source-previews.json';

export function ReservationPolicyDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,flow=diagram.layout==='reservation-policy-denominator';
 const R=({name,value,className})=><RichNarrative sourcePreviews={previews} id={`${id}:${name}`} value={value} className={className}/>;
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className="reservation-policy-diagram" aria-label={diagram.label}>
   <R name="scope" value={diagram.scope}/>
   {flow ? <div data-reviewed-rows>
    <div className="reservation-policy-start"><span>{rows[0]['层次']}</span><h3>{rows[0]['状态']}</h3><p>{rows[0]['记录']}</p><small>{rows[0]['判断边界']}</small></div>
    <div className="reservation-policy-fork-label" aria-hidden="true">↙ 确认前的去向　　确认后的队列 ↘</div>
    <div className="reservation-policy-fork">{rows.slice(1,3).map((row,i)=><section className={`reservation-policy-card ${i===0?'reservation-policy-unconfirmed':''}`} key={row['层次']}><span className="reservation-policy-kicker">{row['层次']}</span><h3>{row['状态']}</h3><p>{row['记录']}</p><small>{row['判断边界']}</small></section>)}</div>
    <div className="reservation-policy-flow-arrow" aria-hidden="true">↓ 继续观察座位，不止统计原订座人</div>
    {rows.slice(3).map(row=><section className="reservation-policy-outcome" key={row['层次']}><div><span className="reservation-policy-kicker">{row['层次']}</span><h3>{row['状态']}</h3></div><div><p>{row['记录']}</p><small>{row['判断边界']}</small></div></section>)}
   </div> : <div className="reservation-policy-comparison" data-reviewed-rows>{rows.map((row,index)=><section className="reservation-policy-card" key={row['方式']||row['证据层']}><header><span className="reservation-policy-number">{String(index+1).padStart(2,'0')}</span><h3>{row['方式']||row['证据层']}</h3></header>{Object.entries(row).filter(([key])=>!['方式','证据层'].includes(key)).map(([key,value])=><div className={`reservation-policy-cell ${key==='不能推出'?'reservation-policy-limit':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}</section>)}</div>}
   {diagram.ledger&&<R name="ledger" className="reservation-policy-ledger" value={diagram.ledger}/>}
   <R name="completion" className="reservation-policy-conclusion" value={diagram.completion}/>
   <figcaption><R name="note" className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
