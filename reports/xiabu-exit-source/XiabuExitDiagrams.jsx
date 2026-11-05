import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './xiabu-exit-diagrams.css';
export function XiabuExitDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, scenarios=diagram.layout==='xiabu-exit-scenarios';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
 <figure className={`xiabu-exit-diagram ${scenarios?'xiabu-exit-scenarios':'xiabu-exit-ledgers'}`} aria-label={diagram.label}>
 <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
 {scenarios&&<div className="xiabu-exit-horizon" aria-label="各方案使用同一现金预测期间"><span>同一决策日</span><span aria-hidden="true">→</span><span>同一比较终点</span></div>}
 <div className="xiabu-exit-grid" data-reviewed-rows>{rows.map((row,index)=><section className="xiabu-exit-card" key={row['项目']}>
 <header><span className="xiabu-exit-number">{String(index+1).padStart(2,'0')}</span><h3>{row['项目']}</h3></header>
 {Object.entries(row).filter(([key])=>key!=='项目').map(([key,value],i)=><div className={`xiabu-exit-cell ${i===0?'xiabu-exit-first':''} ${key.includes('边界')||key.includes('判断')?'xiabu-exit-boundary':''}`} key={key}>
 <h4>{key}</h4><p>{value}</p></div>)}
 </section>)}</div>
 <RichNarrative id={`${id}:completion`} className="xiabu-exit-conclusion" value={diagram.completion}/>
 <RichNarrative id={`${id}:note`} className="study-figure-note" value={diagram.note}/>
 </figure></DataComponent>;
}
