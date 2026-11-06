import React from 'react';
import {DataComponent, RichNarrative, ChartMark, ChartTooltip} from '../../data-app-public.jsx';
import previews from './table-turnover-source-previews.json';
import './table-turnover-diagrams.css';
const pct=n=>`${n/16*100}%`;
function MinuteMark({row,field,label,className,children}){
 const value=row[field];
 return <ChartMark className={className} style={{left:pct(value)}} aria-label={`${row.variantLabel}，${label}：离席后第${value}分钟`} tooltip={<ChartTooltip active label={`${row.variantLabel} · ${label}`} details={[{label:'离席后的时点',value:`第${value}分钟`},{label:'性质',value:'作者假设，非测量'}]}/>} context={{kind:'chart',chartType:'timeline',label,value,row}}>{children}</ChartMark>;
}
function TimelineRow({row}){
 return <div className="table-turnover-track-row">
  <strong className="table-turnover-row-label">{row.variantLabel}</strong>
  <div className="table-turnover-plot" data-chart-interaction-root>
   {[0,4,8,12,16].map(n=><span className="table-turnover-gridline" style={{left:pct(n)}} key={n}/>)}
   <span className="table-turnover-segment notice" style={{left:0,width:pct(row.noticed)}}/>
   {row.cleaningStart>row.noticed&&<span className="table-turnover-segment staff" style={{left:pct(row.noticed),width:pct(row.cleaningStart-row.noticed)}}/>}
   <span className="table-turnover-segment cleaning" style={{left:pct(row.cleaningStart),width:pct(row.tableReady-row.cleaningStart)}}>清理摆台 4分</span>
   {row.seated>row.tableReady&&<span className="table-turnover-segment guest" style={{left:pct(row.tableReady),width:pct(row.seated-row.tableReady)}}/>}
   <MinuteMark row={row} field="noticed" label="负责人收到信息" className="table-turnover-notice-mark">▼</MinuteMark>
   <MinuteMark row={row} field="tableReady" label="桌位准备好，门迎立即得知" className="table-turnover-ready-mark">◆</MinuteMark>
   <MinuteMark row={row} field="seated" label="实际入座" className="table-turnover-seat-mark">●</MinuteMark>
  </div>
  <p className="table-turnover-row-values">收到信息 <b>{row.noticed}</b> → 开始清台 <b>{row.cleaningStart}</b> → 准备好／门迎立即得知 <b>{row.tableReady}</b> → 入座 <b>{row.seated}</b> 分钟</p>
 </div>;
}
function ScenarioTimeline({rows}){
 const groups=[...new Set(rows.map(r=>r.scenario))];
 return <div data-reviewed-rows>
  <div className="table-turnover-legend" aria-label="图例">
   <span><i className="notice"/>离席后等信息</span><span><i className="staff"/>已知后等清台人</span><span><i className="cleaning"/>清理与摆台</span><span><i className="guest"/>桌好后等合适顾客</span>
  </div>
  <p className="table-turnover-mark-legend">▼ 收到信息　◆ 桌位准备好／门迎立即得知　● 入座</p>
  {groups.map((key,i)=>{const pair=rows.filter(r=>r.scenario===key), first=pair[0];return <section className="table-turnover-scenario" key={key}>
   <header><span className="table-turnover-index">假设 {i+1}</span><h3>{first.label}</h3><strong className="table-turnover-saved">入座提前 {first.saved} 分钟</strong></header>
   <p className="table-turnover-availability">清台人员第 {first.cleanerAvailable} 分钟可用 · 匹配顾客第 {first.guestReady} 分钟就绪</p>
   <div className="table-turnover-axis" aria-hidden="true">{[0,4,8,12,16].map(n=><span style={{left:pct(n)}} key={n}>{n}</span>)}</div>
   {pair.map(row=><TimelineRow row={row} key={row.variant}/>)}
  </section>})}
  <p className="table-turnover-unit">共用刻度：上一组离席后分钟。第0分钟为离席；准备好 → 门迎得知之间不画等待，因为本模型假设立即同步。</p>
 </div>;
}
export function TableTurnoverDiagram({diagram,id,rows}){
 const q=`diagram-${id}`, timeline=diagram.layout==='table-turnover-timeline';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows}>
  <figure className="table-turnover-figure" aria-label={diagram.label}>
   <RichNarrative id={`${id}:scope`} value={diagram.scope} sourcePreviews={previews}/>
   {timeline?<ScenarioTimeline rows={rows}/>:<div className="table-turnover-branches" data-reviewed-rows>{rows.map((r,i)=><section key={r.title}><span className="table-turnover-index">{String(i+1).padStart(2,'0')}</span><h3>{r.title}</h3><p>{r.condition}</p><div className="table-turnover-action"><span>优先核查</span><p>{r.action}</p></div><small>{r.boundary}</small></section>)}</div>}
   {!timeline&&<div className="table-turnover-merge" aria-hidden="true">↓　回到整个餐段　↓</div>}
   <RichNarrative id={`${id}:completion`} value={diagram.completion} className="table-turnover-conclusion" sourcePreviews={previews}/>
   <figcaption><RichNarrative id={`${id}:note`} value={diagram.note} className="study-figure-note" sourcePreviews={previews}/></figcaption>
  </figure>
 </DataComponent>;
}
