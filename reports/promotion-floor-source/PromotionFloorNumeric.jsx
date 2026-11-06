import React from 'react';
import {RichNarrative,EvidenceChart,useDataApp} from '../../data-app-public.jsx';
import './promotionfloor-diagrams.css';
const R=({id,children,className})=><RichNarrative id={id} value={children} className={className}/>;
export function PromotionFloorNumeric({chart,id}){
 const {reviewedRows}=useDataApp();const componentId=`visual-${id}`,rows=reviewedRows(componentId);
 const signed=n=>(n>0?'+':'')+n+'元';
 return <EvidenceChart id={componentId} queryId={componentId} title={chart.title} description={chart.subtitle} rows={rows} sourceRows={rows} height={350} spec={{type:'horizontalBar',x:'scenario',y:'orderContribution',fields:['orderContribution','relativeContribution'],legend:{labels:{orderContribution:'活动单自身贡献',relativeContribution:'考虑挤占后的相对贡献'}},currency:'CNY',valueDecimals:0,stackable:false,startAtZero:true,colors:{orderContribution:'var(--chart-1)',relativeContribution:'var(--chart-2)'}}}>
 <div className="promotionfloor-scenarios" data-reviewed-rows>{rows.map((r,i)=><section key={r.scenario}><span className="promotionfloor-index">假设 {i+1}</span><h3>{r.scenario}</h3><p>结算 {r.settlementNet}元 − 未扣变动成本 {r.remainingCost}元</p><strong>活动单自身贡献 {signed(r.orderContribution)}</strong><p>{r.displacedContribution===0?'假设没有挤掉原有订单。':`假设严格一换一，挤掉原有订单贡献 ${r.displacedContribution}元。`}</p><b>相对贡献 {signed(r.relativeContribution)}</b></section>)}</div>
 <R id={`${id}:chart-note`} className="study-figure-note">{chart.note}</R></EvidenceChart>;
}
