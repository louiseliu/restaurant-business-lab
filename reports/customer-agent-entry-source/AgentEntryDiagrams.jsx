import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './agent-entry-diagrams.css';

export function AgentEntryDiagram({diagram,id,rows}) {
 const queryId=`diagram-${id}`;
 return <DataComponent id={queryId} queryId={queryId} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows}>
  <figure className="agent-entry-diagram" aria-label={diagram.label}>
   <figcaption><p>{diagram.scope}</p></figcaption>
   <div data-reviewed-rows>{diagram.layout==='agent-entry-paths'?<>
    <div className="agent-entry-paths">{rows.map((row,i)=><div className="agent-entry-route" key={row.title}>
     <h3><span>{i===0?'首次':'返回'}</span>{row.title}</h3>
     <div className="agent-entry-steps"><div className="agent-entry-prep"><small>准备条件</small><p>{row.preparation}</p></div><span aria-hidden="true" className="agent-entry-arrow">→</span><div><small>当次需求</small><p>{row.request}</p></div><span aria-hidden="true" className="agent-entry-arrow">→</span><div><small>确认结果</small><p>{row.result}</p></div></div>
     <p className="agent-entry-caveat">{row.caveat}</p>
    </div>)}</div><p className="agent-entry-fallback">{diagram.fallback}</p>
   </>:<div className="agent-entry-goals">{rows.map((row,i)=><section key={row.title} className="agent-entry-goal"><span className="agent-entry-number">目标 {String(i+1).padStart(2,'0')}</span><h3>{row.title}</h3><p className="agent-entry-question">{row.question}</p><dl><dt>需要什么证据</dt><dd>{row.evidence}</dd><dt>同时记下投入</dt><dd>{row.cost}</dd></dl><p className="agent-entry-limit">{row.limit}</p></section>)}</div>}</div>
   <RichNarrative id={`${id}:diagram-note`} value={diagram.note} className="study-figure-note"/>
  </figure>
 </DataComponent>;
}
