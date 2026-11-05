import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './presto-remote-diagrams.css';
export function PrestoDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, gates=diagram.layout==='presto-remote-gates';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className={`presto-remote-diagram ${gates?'presto-remote-gates':'presto-remote-delivery'}`}>
 <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
 <div className="presto-remote-grid" data-reviewed-rows>{rows.map((row,index)=><section className="presto-remote-step" key={row['决定']}><header><span className="presto-remote-number">{String(index+1).padStart(2,'0')}</span><h3>{row['决定']}</h3></header>{Object.entries(row).filter(([key])=>key!=='决定').map(([key,value])=><div className={`presto-remote-cell ${key==='暂不付款的信号'?'presto-remote-stop':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}</section>)}</div>
 <RichNarrative id={`${id}:completion`} className="presto-remote-conclusion" value={diagram.completion}/><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
 </figure></DataComponent>;
}
