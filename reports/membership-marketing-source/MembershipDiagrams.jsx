import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './membership-marketing-diagrams.css';
export function MembershipDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, gates=diagram.layout==='membership-marketing-gates';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className={`membership-marketing-diagram ${gates?'membership-marketing-gates':'membership-marketing-delivery'}`}>
 <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
 <div className="membership-marketing-grid" data-reviewed-rows>{rows.map((row,index)=><section className="membership-marketing-step" key={row['决定']}><header><span className="membership-marketing-number">{String(index+1).padStart(2,'0')}</span><h3>{row['决定']}</h3></header>{Object.entries(row).filter(([key])=>key!=='决定').map(([key,value])=><div className={`membership-marketing-cell ${key==='暂不付款的信号'?'membership-marketing-stop':''}`} key={key}><h4>{key}</h4><p>{value}</p></div>)}</section>)}</div>
 <RichNarrative id={`${id}:completion`} className="membership-marketing-conclusion" value={diagram.completion}/><RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
 </figure></DataComponent>;
}
