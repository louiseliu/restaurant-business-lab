import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './supplier-recommendation-diagrams.css';
import previews from './supplier-recommendation-source-previews.json';
const Copy=({id,value,className})=><RichNarrative id={id} value={value} className={className} sourcePreviews={previews}/>;
function Card({row,variant=''}){
 return <section className={`supplier-recommendation-card supplier-recommendation-${variant}`}>
  <header><span>{row['阶段']}</span><h3>{row['标题']}</h3></header>
  <p>{row['内容']}</p><p className="supplier-recommendation-limit">{row['边界']}</p>
 </section>;
}
const Arrow=()=> <div className="supplier-recommendation-arrow" aria-hidden="true">↓</div>;
export function SupplierRecommendationDiagram({diagram,id,rows}){
 const q=`diagram-${id}`,boundary=diagram.layout==='supplier-recommendation-boundary';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className="supplier-recommendation-diagram" aria-label={diagram.label}>
   <Copy id={`${id}:scope`} value={diagram.scope}/>
   {boundary?<div className="supplier-recommendation-boundary">
    <div className="supplier-recommendation-views" data-reviewed-rows>
     <Card row={rows[0]} variant="supplier"/>
     <div className="supplier-recommendation-dotted" aria-hidden="true"><span>?</span></div>
     <Card row={rows[1]} variant="store"/>
    </div>
    <Copy id={`${id}:visibility`} className="supplier-recommendation-visibility" value={diagram.visibility}/>
    <Arrow/>
    <div data-reviewed-rows><Card row={rows[2]} variant="reconcile"/></div>
    <div className="supplier-recommendation-branch-label">核对后，走向不同决定</div>
    <div className="supplier-recommendation-branches" data-reviewed-rows>{rows.slice(3).map((row,i)=><Card key={row['标题']} row={row} variant={`choice-${i}`}/>)}</div>
   </div>:<div className="supplier-recommendation-trial">
    <div className="supplier-recommendation-lanes" data-reviewed-rows>
     <section className="supplier-recommendation-lane" aria-label="新增原料的比较路线"><h3 className="supplier-recommendation-lane-heading">这次是在增加新品类</h3>{rows.slice(0,3).map((row,i)=><React.Fragment key={row['标题']}>{i>0&&<Arrow/>}<Card row={row} variant="new"/></React.Fragment>)}</section>
     <section className="supplier-recommendation-lane" aria-label="替代原料的比较路线"><h3 className="supplier-recommendation-lane-heading">这次是在比较替代品</h3>{rows.slice(3,6).map((row,i)=><React.Fragment key={row['标题']}>{i>0&&<Arrow/>}<Card row={row} variant="substitute"/></React.Fragment>)}</section>
    </div>
    <div className="supplier-recommendation-merge" aria-hidden="true"><span>↓</span><span>↓</span></div>
    <div data-reviewed-rows><Card row={rows[6]} variant="destinations"/></div>
    <Arrow/>
    <div data-reviewed-rows><Card row={rows[7]} variant="decision"/></div>
   </div>}
   <Copy id={`${id}:completion`} className="supplier-recommendation-conclusion" value={diagram.completion}/>
   <figcaption><Copy id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
  </figure>
 </DataComponent>;
}
