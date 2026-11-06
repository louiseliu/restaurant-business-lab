import React from 'react';
import {DataComponent, RichNarrative} from '../../data-app-public.jsx';
import './nutrition-data-diagrams.css';
import previews from './nutrition-data-source-previews.json';
const Copy=({id,value,className})=><RichNarrative id={id} value={value} className={className} sourcePreviews={previews}/>;
function Card({row,variant=''}){return <section className={`nutrition-data-card nutrition-data-${variant}`}><header><span>{row['阶段']}</span><h3>{row['标题']}</h3></header><p>{row['内容']}</p><p className="nutrition-data-limit">{row['边界']}</p><small>{row['性质']}</small></section>;}
function RouteIcon({lab}){return <svg className="nutrition-data-icon" viewBox="0 0 160 90" aria-hidden="true"><g fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">{lab?<><path d="M66 14h28M71 14v29L49 73q-4 6 4 6h54q8 0 4-6L89 43V14"/><path d="M61 58h38"/><circle cx="73" cy="67" r="2"/><circle cx="89" cy="72" r="2"/></>:<><rect x="47" y="11" width="66" height="70" rx="6"/><path d="M59 24h42v12H59zM61 48h6m12 0h6m12 0h6M61 60h6m12 0h6m12 0h6M61 72h6m12 0h6m12 0h6"/></>}</g></svg>;}
function PlateBoundary({row}){return <section className="nutrition-data-boundary"><div className="nutrition-data-plate-scene" aria-hidden="true"><div><span className="nutrition-data-plate"><i/><i/><i/></span><small>取餐记录</small></div><span className="nutrition-data-not-equal">≠</span><div><span className="nutrition-data-plate nutrition-data-unknown">?</span><small>实际摄入</small></div></div><Card row={row} variant="boundary-copy"/></section>;}
export function NutritionDataDiagram({diagram,id,rows}){
 const q=`diagram-${id}`,paths=diagram.layout==='nutrition-data-paths';
 return <DataComponent id={q} queryId={q} kind="custom" title={diagram.label} sourceRows={rows} displayRows={rows} description={diagram.scope}><figure className="nutrition-data-diagram" aria-label={diagram.label}>
 <Copy id={`${id}:scope`} value={diagram.scope}/>
 {paths?<div className="nutrition-data-paths">
  <div className="nutrition-data-route-grid" data-reviewed-rows>{[0,2].map((start,i)=><div className={`nutrition-data-route nutrition-data-route-${i}`} key={start}><RouteIcon lab={i===1}/><Card row={rows[start]}/><span className="nutrition-data-arrow" aria-hidden="true">↓</span><Card row={rows[start+1]}/></div>)}</div>
  <div className="nutrition-data-converge" aria-hidden="true"><span>↘</span><span>↙</span></div>
  <div data-reviewed-rows><Card row={rows[4]} variant="merge"/></div>
 </div>:<div className="nutrition-data-change">
  <div data-reviewed-rows><Card row={rows[0]} variant="trigger"/></div>
  <div className="nutrition-data-questions" data-reviewed-rows>{rows.slice(1,4).map((row,i)=><div className="nutrition-data-question" key={row['标题']}><span className="nutrition-data-step" aria-hidden="true">{String(i+1).padStart(2,'0')}</span><Card row={row}/></div>)}</div>
  <div className="nutrition-data-decision" data-reviewed-rows>{rows.slice(4,6).map((row,i)=><Card row={row} key={row['标题']} variant={i===0?'continue':'pause'}/>)}</div>
  <div data-reviewed-rows><PlateBoundary row={rows[6]}/></div>
 </div>}
 <Copy id={`${id}:completion`} className="nutrition-data-conclusion" value={diagram.completion}/>
 <figcaption><Copy id={`${id}:note`} className="study-figure-note" value={diagram.note}/></figcaption>
 </figure></DataComponent>;
}
