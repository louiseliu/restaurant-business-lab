import React from 'react';
import {DataComponent,RichNarrative} from '../../data-app-public.jsx';
import './waste-diagrams.css';
// Only opted-in article layouts use this component; existing figures are unchanged.
export function WasteDiagram({diagram,id,rows}) {
 const q=`diagram-${id}`;
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows}><figure className="waste-diagram" aria-label={diagram.label}><figcaption><p>{diagram.scope}</p></figcaption><div data-reviewed-rows>
 {diagram.layout==='waste-origins'?<><div className="waste-origin-head" aria-hidden="true"><span>来源环节</span><span>记录对象</span><span>优先核查 · 研究建议</span></div><div className="waste-origins">{rows.map((row,i)=><div className="waste-origin-row" key={row.title}><h3><span>{String(i+1).padStart(2,'0')}</span>{row.title}</h3><p><small>记录对象</small>{row.text}</p><p><small>优先核查</small>{row.check}</p></div>)}</div><p className="waste-warning">{diagram.warning}</p></>:<><div className="waste-paths">{rows.filter(r=>r.stage==='input').map(row=><div className="waste-path" key={row.title}><h3>{row.title}</h3><p>{row.text}</p></div>)}</div><div className="waste-merge" aria-hidden="true">↘　↙</div>{rows.filter(r=>r.stage==='condition').map(row=><div className="waste-condition" key={row.title}><strong>{row.title}</strong><p>{row.text}</p></div>)}<div className="waste-review">{rows.filter(r=>['review','action'].includes(r.stage)).map((row,i)=><React.Fragment key={row.title}>{i>0&&<span className="waste-arrow" aria-hidden="true">→</span>}<div><h3>{row.title}</h3><p>{row.text}</p></div></React.Fragment>)}</div><aside className="waste-planning">{diagram.planning}</aside><p className="waste-cost">{diagram.cost}</p></>}
 </div><RichNarrative id={`${id}:diagram-note`} value={diagram.note} className="study-figure-note"/></figure></DataComponent>;
}
