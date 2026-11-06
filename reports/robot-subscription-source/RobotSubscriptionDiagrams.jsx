import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './robotsubscription-diagrams.css';
import previews from './robotsubscription-source-previews.json';

export function RobotSubscriptionDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`,timelines=diagram.layout==='robotsubscription-timelines';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className="robotsubscription-diagram" aria-label={diagram.label}>
   <RichNarrative sourcePreviews={previews} id={`${id}:scope`} value={diagram.scope}/>
   {timelines ? <div data-reviewed-rows>
    <div className="robotsubscription-checkpoint"><strong>复查节点：能否结束，需要合同确认</strong><span>每月付款 ≠ 每月都能取消</span></div>
    {[['付款轨道','钱什么时候出去'],['使用轨道','试用是否有结论'],['退出轨道','停止后怎样接续']].map(([key,label])=><section className="robotsubscription-lane" key={key}><h3>{label}</h3><ol>{rows.map((row,i)=><li className={i===1?'robotsubscription-review':''} key={row['阶段']}><span>{row['阶段']}</span><p>{row[key]}</p>{i<rows.length-1&&<b aria-hidden="true">→</b>}</li>)}</ol></section>)}
   </div> : <div data-reviewed-rows>
    <div className="robotsubscription-grid">{rows.map((row,index)=><section className="robotsubscription-card" key={row['方式']}>
     <header><span className="robotsubscription-number">{String(index+1).padStart(2,'0')}</span><h3>{row['方式']}</h3></header>
     {Object.entries(row).filter(([key])=>key!=='方式').map(([key,value])=><div className="robotsubscription-cell" key={key}><h4>{key}</h4><p>{value}</p></div>)}
    </section>)}</div>
    <div className="robotsubscription-converge" aria-hidden="true">↓ 同一把尺子 ↓</div>
    <RichNarrative sourcePreviews={previews} id={`${id}:comparison`} className="robotsubscription-comparison" value={diagram.comparison}/>
    <RichNarrative sourcePreviews={previews} id={`${id}:questions`} className="robotsubscription-questions" value={diagram.questions}/>
   </div>}
   <RichNarrative sourcePreviews={previews} id={`${id}:completion`} className="robotsubscription-conclusion" value={diagram.completion}/>
   <figcaption><RichNarrative sourcePreviews={previews} id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
