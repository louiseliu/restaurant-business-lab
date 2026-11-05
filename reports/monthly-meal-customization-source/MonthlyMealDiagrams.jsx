import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './monthly-meal-diagrams.css';

export function MonthlyMealDiagram({diagram,id,rows}){
  const q=`diagram-${id}`;
  const change=diagram.layout==='meal-change';
  return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
    <figure className={`meal-mechanism ${change?'meal-change':'meal-context'}`}>
      <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
      <div className="meal-stages" data-reviewed-rows>
        {rows.map((row,index)=><section className="meal-stage" key={row['环节']}>
          <header><span className="meal-index">{String(index+1).padStart(2,'0')}</span><div><p className="meal-tag">{row['性质']}</p><h3>{row['环节']}</h3></div></header>
          <div className="meal-cells">{Object.entries(row).filter(([key])=>!['环节','性质'].includes(key)).map(([label,text])=><div className="meal-cell" key={label}><h4>{label}</h4><p>{text}</p></div>)}</div>
        </section>)}
      </div>
      <RichNarrative id={`${id}:note`} value={diagram.note} className="study-figure-note"/>
    </figure>
  </DataComponent>;
}
