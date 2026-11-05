import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './fitout-diagrams.css';
export function FitoutDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, gates=diagram.layout==='fitout-gates';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className={`fitout-diagram ${gates?'fitout-gates':'fitout-delivery'}`}>
 <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
 <div className="fitout-grid" data-reviewed-rows>{rows.map((row,index)=><section className="fitout-step" key={row['决定']}><header><span className="fitout-number">{String(index+1).padStart(2,'0')}</span><h3>{row['决定']}</h3></header>{Object.entries(row).filter(([key])=>key!=='决定').map(([key,value])=><div className={`fitout-cell ${key==='暂不付款的信号'?'fitout-stop':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}</section>)}</div>
 <RichNarrative id={`${id}:completion`} className="fitout-conclusion" value={diagram.completion}/><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
 </figure></DataComponent>;
}
