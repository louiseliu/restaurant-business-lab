import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './handoff-diagrams.css';
export function HandoffDiagram({diagram,id,rows}){
 const q=`diagram-${id}`;
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows}>
  <figure className="handoff-diagram" aria-label={diagram.label}>
   <figcaption><span className="study-eyebrow">把机制画出来</span><p>{diagram.scope}</p></figcaption>
   {diagram.layout==='handoff-states'?<div className="handoff-state-grid" data-reviewed-rows>{rows.map((r,i)=><div className="handoff-state" key={r.title}><span className="handoff-number">{String(i+1).padStart(2,'0')}</span><h3>{r.title}</h3><dl><dt>发言控制</dt><dd>{r.speech}</dd><dt>处理责任</dt><dd>{r.owner}</dd></dl><p className="handoff-check">{r.check}</p>{i<rows.length-1&&<span className="handoff-arrow" aria-hidden="true">→</span>}</div>)}</div>:
    <><div className="handoff-line-grid" data-reviewed-rows><div className="handoff-time-labels" aria-hidden="true"><span>接手时</span><span>到期时的一个可能状态</span><span>下一步</span></div>{rows.map((r,i)=><div className={`handoff-track handoff-track-${i}`} key={r.title}><h3>{r.title}</h3><div className="handoff-track-cells"><p>{r.start}</p><p className="handoff-due">{r.middle}</p><p>{r.end}</p></div><p className="handoff-track-detail">{r.detail}</p></div>)}</div><RichNarrative id={`${id}:caution`} className="handoff-caution" value={diagram.caution}/><RichNarrative id={`${id}:platform`} className="handoff-platform" value={diagram.platform}/></>}
   <RichNarrative id={`${id}:diagram-note`} className="study-figure-note" value={diagram.note}/>
  </figure>
 </DataComponent>;
}
