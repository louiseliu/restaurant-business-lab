import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './accounting-diagrams.css';
export function AccountingDiagram({diagram,id,rows}){
 const q=`diagram-${id}`;
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className="accounting-mechanism"><RichNarrative id={`${id}:scope`} value={diagram.scope}/><div className={`accounting-grid ${rows.length===3?'accounting-three':'accounting-two'}`} data-reviewed-rows>{rows.map((r,i)=><section className="accounting-lane" key={r.title}><header><span>0{i+1}</span><h3>{r.title}</h3></header>{r.cells.map(c=><div className="accounting-cell" key={c.label}><h4>{c.label}</h4><p>{c.text}</p></div>)}</section>)}</div><RichNarrative id={`${id}:note`} value={diagram.note} className="study-figure-note"/></figure></DataComponent>;
}
