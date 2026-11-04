import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './menu-diagrams.css';
export function MenuDiagram({diagram,id,rows}){
 const q=`diagram-${id}`;const release=diagram.layout==='menu-release';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className="menu-mechanism"><RichNarrative id={`${id}:scope`} value={diagram.scope}/><div className={`menu-grid ${release?'menu-three':'menu-two'}`} data-reviewed-rows>{rows.map((r,i)=><section className="menu-lane" key={r.title}><header><span>0{i+1}</span><h3>{r.title}</h3></header>{(release?[['文档明确',r.fact],['建议核查',r.check],['证据边界',r.limit]]:[['输入以前',r.before],['输入阶段',r.input],['输入以后',r.after],['何时改变取舍',r.decision]]).map(([label,value])=><div className="menu-cell" key={label}><h4>{label}</h4><p>{value}</p></div>)}</section>)}</div><RichNarrative id={`${id}:note`} value={diagram.note} className="study-figure-note"/></figure></DataComponent>;
}
