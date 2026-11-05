import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './pickup-diagrams.css';
export function PickupDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, gates=diagram.layout==='pickup-gates';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className={`pickup-diagram ${gates?'pickup-gates':'pickup-delivery'}`}>
 <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
 <div className="pickup-grid" data-reviewed-rows>{rows.map((row,index)=><section className="pickup-step" key={row['决定']}><header><span className="pickup-number">{String(index+1).padStart(2,'0')}</span><h3>{row['决定']}</h3></header>{Object.entries(row).filter(([key])=>key!=='决定').map(([key,value])=><div className={`pickup-cell ${key==='暂不付款的信号'?'pickup-stop':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}</section>)}</div>
 <RichNarrative id={`${id}:completion`} className="pickup-conclusion" value={diagram.completion}/><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
 </figure></DataComponent>;
}
