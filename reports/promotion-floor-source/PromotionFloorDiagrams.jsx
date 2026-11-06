import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import previews from './promotionfloor-source-previews.json';
import './promotionfloor-diagrams.css';

export function PromotionFloorDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`, isControls=diagram.layout==='promotionfloor-controls';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}>
  <figure className="promotionfloor-diagram" aria-label={diagram.label}>
   <RichNarrative id={`${id}:scope`} value={diagram.scope} sourcePreviews={previews}/>
   <div className={`promotionfloor-grid ${isControls?'promotionfloor-controls':''}`} data-reviewed-rows>
    {rows.map((row,i)=><section key={row['要看什么']} className="promotionfloor-panel">
     <span className="promotionfloor-index">{String(i+1).padStart(2,'0')}</span><h3>{row['要看什么']}</h3>
     {Object.entries(row).filter(([k])=>k!=='要看什么').map(([k,v])=><div className="promotionfloor-cell" key={k}><h4>{k}</h4><p>{v}</p></div>)}
    </section>)}
   </div>
   <RichNarrative id={`${id}:completion`} value={diagram.completion} className="promotionfloor-conclusion" sourcePreviews={previews}/>
   <figcaption><RichNarrative id={`${id}:note`} value={diagram.note} className="study-figure-note" sourcePreviews={previews}/></figcaption>
  </figure>
 </DataComponent>;
}
