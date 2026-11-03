import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './cancellation-diagrams.css';
export function CancellationDiagram({diagram,id,rows}){
 const q=`diagram-${id}`;
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows}>
  <figure className="cancellation-diagram" aria-label={diagram.label}>
   <figcaption><h2>{diagram.label}</h2><p>{diagram.scope}</p></figcaption>
   {diagram.layout==='cancellation-stages'?<div className="cancellation-stage-grid" data-reviewed-rows>{rows.map((r,i)=><section className="cancellation-stage" key={r.title}><span className="cancellation-time">取消发生时点 {i+1}</span><h3>{r.title}</h3><dl><div className="cancellation-spent"><dt>已经投入</dt><dd>{r.spent}</dd></div><div className="cancellation-remaining"><dt>仍待执行</dt><dd>{r.remaining}</dd></div></dl><p className="cancellation-check">↓ {r.check}</p></section>)}</div>:
    <><p className="cancellation-origin">已决定取消的订单</p><div className="cancellation-lanes" data-reviewed-rows>{rows.map(r=><section className="cancellation-lane" key={r.title}><h3>{r.title}</h3><div className="cancellation-steps"><p>{r.start}</p><span aria-hidden="true">→</span><p>{r.middle}</p><span aria-hidden="true">→</span><p>{r.end}</p></div><p className="cancellation-detail">{r.detail}</p></section>)}</div><RichNarrative id={`${id}:caution`} className="cancellation-result" value={diagram.caution}/></>}
   <RichNarrative id={`${id}:diagram-note`} className="study-figure-note" value={diagram.note}/>
  </figure>
 </DataComponent>;
}
