import React, { useMemo, useState } from "react";
import { DataComponent, EvidenceChart, ReportSection, RichNarrative, useDataApp } from "../../data-app-public.jsx";
import "./report.css";

const money=(v)=>Number(v).toLocaleString('zh-CN',{minimumFractionDigits:2,maximumFractionDigits:2});
const yuan=(v)=>money(v/100);
const percent=(v)=>(v*100).toFixed(2)+'%';
const DISCLAIMER='模拟数据；本包AI辅助编制并经计算回查，非门店实测；没有测得省时/准确率提升。';
const steps=[['01','先定口径','2 店 × 14 日 × 2 渠道。订单、退款和收入对应同一履约群。'],['02','本地算清楚','Python 实际清洗、汇总和勾稽。缺数或冲突即停止，不让 AI 猜。'],['03','AI 组织文字','本次助手读取计算结果起草。不是 Python 调用模型 API。'],['04','回查每个结论','数值断言 + 独立 SQL 复算；真实使用仍需人工核账和签字。'],['05','保留证据链','结论 → 汇总字段 → 原记录 ID / CSV 行号。没有伪造订单明细。']];

function RowTrace({ rows }) {
 const [store,setStore]=useState('all'); const [channel,setChannel]=useState('all'); const [week,setWeek]=useState('all');
 const [selected,setSelected]=useState('SIM-20261023-S02-DL');
 const filtered=rows.filter(r=>(store==='all'||r.store_id===store)&&(channel==='all'||r.channel===channel)&&(week==='all'||r.week===week));
 const row=filtered.find(r=>r.record_id===selected)||filtered[0];
 return <section className="sample-trace" aria-label="原记录追溯">
  <RichNarrative id="trace:intro" value={'## 04｜从一句结论，回到原始记录\n\n先看长青店 10 月 23 日外卖记录。可筛选其他记录；**下面的筛选只影响原记录区，不改变上方固定两周周报。** 原始粒度到日 × 店 × 渠道为止，没有逐笔订单证据。'} />
  <div className="sample-filters">
   <label>门店<select aria-label="追溯门店" value={store} onChange={e=>setStore(e.target.value)}><option value="all">全部门店</option><option value="S01">溪桥店（虚构）</option><option value="S02">长青店（虚构）</option></select></label>
   <label>渠道<select aria-label="追溯渠道" value={channel} onChange={e=>setChannel(e.target.value)}><option value="all">全部渠道</option><option value="dine_in">堂食</option><option value="delivery">外卖</option></select></label>
   <label>周次<select aria-label="追溯周次" value={week} onChange={e=>setWeek(e.target.value)}><option value="all">全部两周</option><option value="W1">前周 W1</option><option value="W2">本周 W2</option></select></label>
   <button onClick={()=>{setStore('all');setChannel('all');setWeek('all');setSelected('SIM-20261023-S02-DL')}}>重置追溯</button>
  </div>
  <DataComponent id="raw-trace-table" queryId="raw_daily" kind="table" title={`原记录：${filtered.length} 条`} sourceRows={filtered} displayRows={filtered}>
   <div className="sample-table-scroll"><table className="sample-table"><thead><tr><th>原 CSV 行</th><th>业务日 / 门店 / 渠道</th><th>履约单</th><th>退款单</th><th>净收入 / 元</th><th>贡献 / 元</th><th>追溯</th></tr></thead><tbody>{filtered.map(r=><tr key={r.record_id} className={row?.record_id===r.record_id?'sample-selected':''}><td>{r.raw_csv_line}</td><td>{r.business_date}<br/>{r.store_label} · {r.channel_label}</td><td>{r.fulfilled_orders}</td><td>{r.refunded_orders}</td><td>{yuan(r.merchant_net_revenue_cents)}</td><td>{yuan(r.contribution_cents)}</td><td><button aria-label={`追溯 ${r.record_id}`} onClick={()=>setSelected(r.record_id)}>查看</button></td></tr>)}</tbody></table></div>
   <p className="sample-note">筛选汇总：{filtered.reduce((s,r)=>s+r.fulfilled_orders,0).toLocaleString('zh-CN')} 单；净收入 {yuan(filtered.reduce((s,r)=>s+r.merchant_net_revenue_cents,0))} 元；贡献 {yuan(filtered.reduce((s,r)=>s+r.contribution_cents,0))} 元。</p>
  </DataComponent>
  {row&&<DataComponent id="single-record-trace" queryId="raw_daily" kind="table" title="这一条金额怎样走到贡献" sourceRows={[row]} displayRows={[row]}>
   <div data-reviewed-rows="true"><p className="sample-record-id">{row.record_id}</p><p>data/simulated_daily_raw.csv · 第 {row.raw_csv_line} 行（含表头） · {row.fulfilled_orders} 履约单 / {row.refunded_orders} 部分退款单</p>
   <div className="sample-equation"><span>标价<br/><b>{yuan(row.gross_sales_cents)}</b></span><i>−</i><span>商家优惠<br/><b>{yuan(row.merchant_discount_cents)}</b></span><i>−</i><span>顾客退款<br/><b>{yuan(row.refund_cents)}</b></span><i>=</i><span className="sample-accent">商家净收入<br/><b>{yuan(row.merchant_net_revenue_cents)}</b></span></div>
   <p className="sample-note">另一条核对路径：顾客退款前实付 {yuan(row.customer_paid_cents)} − 退款 {yuan(row.refund_cents)} + 平台补贴 {yuan(row.platform_subsidy_cents)} = {yuan(row.merchant_net_revenue_cents)} 元。平台优惠 {yuan(row.platform_discount_cents)} 元已由补贴补足，不能重复扣除。</p>
   <dl className="sample-costs">{[['食材','food_cost_cents'],['包装','packaging_cost_cents'],['平台服务','platform_fee_cents'],['支付','payment_fee_cents'],['商家配送','delivery_cost_cents'],['广告','advertising_cost_cents']].map(([label,key])=><div key={key}><dt>{label}</dt><dd>{yuan(row[key])}</dd></div>)}</dl>
   <p className="sample-result">净收入 {yuan(row.merchant_net_revenue_cents)} − 六项成本 {yuan(row.specified_costs_cents)} = <strong>贡献 {yuan(row.contribution_cents)} 元</strong></p><p className="sample-note">仍未扣人工、租金、税费、折旧等。日汇总自洽不等于已经核实真实平台账单。</p></div>
  </DataComponent>}
 </section>;
}

export function ReportContent(){
 const {snapshot,reviewedRows,visible,canEdit,mode,appTitle,setAppTitle}=useDataApp();
 const pkg=snapshot.samplePackage;
 const weekly=reviewedRows('weekly'); const channels=reviewedRows('channel_weekly'); const raw=reviewedRows('raw_daily');
 const sc=reviewedRows('store_channel_weekly'); const bridge=reviewedRows('channel_bridge');
 const a=weekly.find(x=>x.week==='W1'),b=weekly.find(x=>x.week==='W2');
 const narrative=pkg.narrative.split('## 一、')[1];
 return <article className="report-content sample-report" aria-label="经营数据到AI周报离线实战样板">
  <header className="report-hero">
   <div className="sample-kicker">餐饮经营研究院 · 实战样板 02</div>
   <h1 data-data-app-title contentEditable={canEdit&&mode==='edit'} suppressContentEditableWarning onBlur={canEdit&&mode==='edit'?e=>setAppTitle(e.currentTarget.textContent.trim()||appTitle):undefined}>{appTitle}</h1>
   <RichNarrative id="sample:intro" value="把经营数据变成一份能回查的周报：**计算交给代码，叙事由 AI 辅助，口径和行动由人把关。**" className="report-deck"/>
   <div className="sample-disclaimer"><strong>教学样本，不是经营实测</strong><p>{DISCLAIMER}</p><p>本次没有调用外部模型 API，没有上传私有经营数据；页面只展示预计算结果，不提供模型调用或真实 CSV 上传。</p></div>
  </header>
  <ReportSection id="sample-summary" title="本周结论" queryId="weekly" sourceRows={weekly} showHeading={false}>
   <RichNarrative id="sample:summary" value={`## 订单增加了，但所列成本后贡献下降了\n\n在这组模拟数据里，W2 履约订单 **${b.fulfilled_orders.toLocaleString('zh-CN')} 单（+10.50%）**，商家净收入 **${money(b.merchant_net_revenue_yuan)} 元（+3.17%）**；所列成本后贡献 **${money(b.contribution_yuan)} 元（-6.59%）**。先核外卖优惠、费用与退款，而不是只凭订单增长扩大活动。\n\n比较 W1：2026-10-12—18；W2：2026-10-19—25。两家虚构门店、完整同店周。贡献尚未扣人工、租金、税费、折旧等，**不是净利润**。`} />
  </ReportSection>
  <section className="sample-process"><RichNarrative id="sample:process-title" value="## 01｜本次真正执行了什么"/><div className="sample-steps">{steps.map(([n,title,text])=><div className="sample-step" key={n}><span>{n}</span><RichNarrative id={`step:${n}`} value={`### ${title}\n\n${text}`}/></div>)}</div><p className="sample-note">这是一条已执行的“模拟 CSV → 本地代码结果 → AI 辅助文稿 → 计算回查”链，不是假装接入模型的自动演示。</p></section>
  <ReportSection id="sample-cleaning" title="输入与质量" queryId="raw_daily" sourceRows={raw} showHeading={false}>
   <RichNarrative id="sample:cleaning" value="## 02｜先把输入变成可信的计算底稿\n\n57 行原始导出包含故意注入的一条重复、三处空白和一个渠道别名。只做可解释的规范处理后，保留 **56 条日 × 店 × 渠道记录**，并保留原 CSV 行号。缺值、冲突重复、漏分区或金额桥不平都停止，不插值、不补零。" />
   <div className="sample-quality" data-reviewed-rows="true"><div><b>57 → 56</b><span>删除 1 条完全重复</span></div><div><b>78 项</b><span>金额与汇总勾稽通过</span></div><div><b>独立 SQL</b><span>从原始 CSV 复算周合计</span></div></div>
   <details><summary>查看真实清洗动作（含原 CSV 行号）</summary><div className="sample-table-scroll"><table className="sample-table"><thead><tr><th>CSV 行号</th><th>记录 ID</th><th>动作</th><th>字段/保留行</th></tr></thead><tbody>{pkg.quality.actions.map((x,i)=><tr key={i}><td>{x.csv_line}</td><td>{x.record_id}</td><td>{{trim_whitespace:'去首尾空白',documented_alias:'明示别名映射',drop_exact_duplicate:'删除完全重复'}[x.action]}</td><td>{x.field||`保留第 ${x.kept_csv_line} 行`}</td></tr>)}</tbody></table></div></details>
  </ReportSection>
  <section className="sample-evidence"><RichNarrative id="sample:chart-intro" value="## 03｜先看两幅图，再读 AI 周报\n\n下面图表只使用已计算结果。每个图的来源菜单保留对应汇总与口径。"/>
   {visible('weekly-amounts')&&<EvidenceChart id="weekly-amounts" queryId="weekly" title="净收入增加，贡献反而下降" description="人民币元；W1 10/12–18，W2 10/19–25；同店完整周" rows={weekly} sourceRows={weekly} height={320} spec={{type:'bar',x:'week_label',y:'merchant_net_revenue_yuan',fields:['merchant_net_revenue_yuan','contribution_yuan'],currency:'CNY',valueDecimals:2,startAtZero:true,stackable:false,legend:{labels:{merchant_net_revenue_yuan:'商家净收入',contribution_yuan:'所列成本后贡献'}}}}/>}
   <div className="sample-table-scroll"><table className="sample-table" data-reviewed-rows="true"><caption>图 1 精确值（元）</caption><thead><tr><th>指标</th><th>前周</th><th>本周</th><th>变化</th></tr></thead><tbody><tr><th>商家净收入</th><td>{money(a.merchant_net_revenue_yuan)}</td><td>{money(b.merchant_net_revenue_yuan)}</td><td>+1,966.05</td></tr><tr><th>所列成本后贡献</th><td>{money(a.contribution_yuan)}</td><td>{money(b.contribution_yuan)}</td><td>−2,165.90</td></tr></tbody></table></div>
   <RichNarrative id="sample:chart-interpretation" value="外卖增加 168 单、堂食减少 7 单，合计增加 161 单；但外卖每单贡献由 11.14 元降至 6.39 元。**这说明增长与贡献可以背离，不说明前后变化由某一活动造成。**"/>
   {visible('channel-unit-contribution')&&<EvidenceChart id="channel-unit-contribution" queryId="channel_weekly" title="外卖每单贡献下降，堂食基本持平" description="人民币元 / 履约单；先加总金额再除同群订单，不平均每日单均" rows={channels} sourceRows={channels} height={320} spec={{type:'bar',x:'channel_label',y:'contribution_per_order_yuan',series:'week_label',currency:'CNY',valueDecimals:2,startAtZero:true,stackable:false}}/>}
   <div className="sample-table-scroll"><table className="sample-table" data-reviewed-rows="true"><caption>图 2 精确值（元 / 单，展示两位小数）</caption><thead><tr><th>渠道</th><th>前周</th><th>本周</th></tr></thead><tbody>{['dine_in','delivery'].map(c=><tr key={c}><th>{c==='delivery'?'外卖':'堂食'}</th>{['W1','W2'].map(w=><td key={w}>{money(channels.find(r=>r.channel===c&&r.week===w).contribution_per_order_yuan)}</td>)}</tr>)}</tbody></table></div>
  </section>
  <ReportSection id="actual-ai-weekly" title="AI辅助周报全文" queryId="weekly" queryIds={['weekly','channel_weekly','store_channel_weekly','channel_bridge']} sourceRowsByQuery={{weekly,channel_weekly:channels,store_channel_weekly:sc,channel_bridge:bridge}} showHeading={false}>
   <div className="sample-draft-label">已完成的 AI 辅助草稿 · 经计算回查 · 待真实使用者核账签字</div>
   <RichNarrative id="actual-ai-weekly:body" value={'## AI 辅助周报全文\n\n以下是本次助手依据实际执行结果起草的完整经营周报，不是未执行的提示词示例。\n\n### 一、'+narrative.replace(/^计算事实/,'计算事实').replace(/\n## /g,'\n### ')}/>
  </ReportSection>
  <RowTrace rows={raw}/>
  <section className="sample-appendix"><RichNarrative id="sample:appendix-intro" value="## 05｜复制操作时，保留这些约束\n\n离线复算只用 Python 标准库。更换输入后要先重算，再重新审读文稿；脚本不会调用 AI，也不会自动证明文稿仍正确。"/>
   <div className="sample-command"><code>python src/generate_sample.py<br/>python src/analyze.py<br/>python src/test_analysis.py</code></div>
   <details><summary>操作提示词：先检查口径，再起草，再独立回查</summary><RichNarrative id="sample:prompts" value={pkg.prompts}/></details>
   <details><summary>人工复核清单与尚未签署的放行表</summary><RichNarrative id="sample:checklist" value={pkg.checklist}/></details>
   <details><summary>完整数据字典：收入、退款、优惠承担与成本</summary><RichNarrative id="sample:dictionary" value={pkg.dictionary}/></details>
   <RichNarrative id="sample:closing" value="**效果边界：** 本次验证了样本计算可复跑、关键数值可回查；没有真实门店对照，没有人工耗时基准，没有测得准确率、节时率或成本改善。AI 文稿不是经营指令，真实应用仍需授权、核账与人审。"/>
  </section>
  <footer className="sample-footer">{DISCLAIMER}</footer>
 </article>
}
