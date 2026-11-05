import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './override-diagrams.css';
export function OverrideDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, experiment=diagram.layout==='override-experiment';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className={`override-diagram ${experiment?'override-experiment':'override-decision'}`}>
 <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
 <div className="override-grid" data-reviewed-rows>{rows.map((row,index)=><section className="override-step" key={Object.values(row)[0]}><header><span className="override-number">{String(index+1).padStart(2,'0')}</span><h3>{row[experiment?'试验政策':'判断环节']}</h3></header>{Object.entries(row).filter(([key])=>key!==(experiment?'试验政策':'判断环节')).map(([key,value])=><div className="override-cell" key={key}><h4>{key}</h4><p>{value}</p></div>)}</section>)}</div>
 <RichNarrative id={`${id}:completion`} className="override-conclusion" value={diagram.completion}/><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
 </figure></DataComponent>;
}
