import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './kitchen-label-diagrams.css';
export function KitchenLabelDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, chain=diagram.layout==='kitchen-label-chain';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className={`kitchen-label-diagram ${chain?'kitchen-label-chain':'kitchen-label-decision'}`} aria-label={diagram.label}>
 <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
 <div className="kitchen-label-grid" data-reviewed-rows>{rows.map((row,index)=><section className="kitchen-label-step" key={row['环节']}><header><span className="kitchen-label-number">{String(index+1).padStart(2,'0')}</span><h3>{row['环节']}</h3></header>{Object.entries(row).filter(([key])=>key!=='环节').map(([key,value])=><div className={`kitchen-label-cell ${['重点断点','停止或继续'].includes(key)?'kitchen-label-boundary':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}</section>)}</div>
 <RichNarrative id={`${id}:completion`} className="kitchen-label-conclusion" value={diagram.completion}/><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
 </figure></DataComponent>;
}
