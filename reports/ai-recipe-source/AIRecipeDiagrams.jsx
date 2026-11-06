import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './ai-recipe-development-diagrams.css';
import previews from './ai-recipe-development-source-previews.json';

export function AIRecipeDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,budget=diagram.layout==='ai-recipe-development-budget';
 const field=(row,key)=><div className="ai-recipe-cell" key={key}><h4>{key}</h4><p>{row[key]}</p></div>;
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className={`ai-recipe-diagram ${budget?'ai-recipe-budget':'ai-recipe-studies'}`} aria-label={diagram.label}>
   <RichNarrative sourcePreviews={previews} id={`${id}:scope`} value={diagram.scope}/>
   <div className="ai-recipe-grid" data-reviewed-rows>{rows.map((row,index)=><section className="ai-recipe-row" key={row['研究']||row['缺口']}>
    <header><span className="ai-recipe-number">{String(index+1).padStart(2,'0')}</span><h3>{row['研究']||row['缺口']}</h3></header>
    {budget?<div className="ai-recipe-branch">{['预算用途','要看到的证据','不扩大投入的条件'].map(k=>field(row,k))}</div>:<div className="ai-recipe-research-body"><div className="ai-recipe-flow">{['AI提出','厨师工作','调查'].map((k,i)=><React.Fragment key={k}>{i>0&&<span className="ai-recipe-arrow" aria-hidden="true">→</span>}{field(row,k)}</React.Fragment>)}</div><div className="ai-recipe-boundaries">{field(row,'比较基准')}{field(row,'外推边界')}</div></div>}
   </section>)}</div>
   <RichNarrative sourcePreviews={previews} id={`${id}:completion`} className="ai-recipe-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative sourcePreviews={previews} id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
