import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './model-update-diagrams.css';

export function ModelUpdateDiagram({diagram,id,rows}){
  const q=`diagram-${id}`;
  const responsibility=diagram.layout==='model-recovery';
  const Stage=({row,index})=><section className={`model-stage model-stage-${index}`}>
    <header><span className="model-index">{String(index+1).padStart(2,'0')}</span><div><p className="model-tag">{row['性质']}</p><h3>{row['环节']}</h3></div></header>
    <div className="model-cells">{Object.entries(row).filter(([key])=>!['环节','性质'].includes(key)).map(([label,text])=><div className="model-cell" key={label}><h4>{label}</h4><p>{text}</p></div>)}</div>
  </section>;
  return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
    <figure className={`model-update ${responsibility?'model-responsibility':'model-evidence'}`}>
      <RichNarrative id={`${id}:scope`} value={diagram.scope}/>
      <div className="model-stages" data-reviewed-rows>{rows.map((row,index)=><Stage row={row} index={index} key={row['环节']}/>)}</div>
      <RichNarrative id={`${id}:note`} value={diagram.note} className="study-figure-note"/>
    </figure>
  </DataComponent>;
}
