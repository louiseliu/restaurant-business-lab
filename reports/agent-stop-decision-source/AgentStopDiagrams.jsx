import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './agent-stop-decision-diagrams.css';
export function AgentStopDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, gates=diagram.layout==='agent-stop-decision-gates';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className={`agent-stop-decision-diagram ${gates?'agent-stop-decision-gates':'agent-stop-decision-delivery'}`}>
 <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
 <div className="agent-stop-decision-grid" data-reviewed-rows>{rows.map((row,index)=><section className="agent-stop-decision-step" key={row['决定']}><header><span className="agent-stop-decision-number">{String(index+1).padStart(2,'0')}</span><h3>{row['决定']}</h3></header>{Object.entries(row).filter(([key])=>key!=='决定').map(([key,value])=><div className={`agent-stop-decision-cell ${key==='暂不付款的信号'?'agent-stop-decision-stop':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}</section>)}</div>
 <RichNarrative id={`${id}:completion`} className="agent-stop-decision-conclusion" value={diagram.completion}/><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
 </figure></DataComponent>;
}
