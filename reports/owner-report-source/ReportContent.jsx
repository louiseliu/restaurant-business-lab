import React from 'react';
import { EvidenceChart, ReportSection, RichNarrative, useDataApp } from '../../data-app-public.jsx';
import { ReportDisclosure } from '../shared/ReportDisclosure.jsx';
const url25='https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0923/2025092300255_c.pdf';
const url26='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0923/2026092300280.pdf';
const annual='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0423/2026042301901.pdf';
const previews={ [url25]:{title:'蜜雪集团 2025 中期报告',summary:'期初、开业、闭店和期末加盟店数，以及集团商品收入；见 p16、46–47。',approvedForReport:true},[url26]:{title:'蜜雪集团 2026 中期报告',summary:'对照期门店桥与商品收入；见 p18、59–60。不能据此读取加盟商利润。',approvedForReport:true},[annual]:{title:'蜜雪集团 2025 年报',summary:'p13 披露 2025-12-01 收购完成时鲜啤福鹿家有 1,354 家加盟店。',approvedForReport:true}};
const N=({id,children,...props})=><RichNarrative id={id} value={children} sourcePreviews={previews} {...props}/>;
function Shop({label}){return <div className="owner-shop"><svg viewBox="0 0 120 90" aria-hidden="true"><path d="M15 40h90v44H15zM10 40l12-28h76l12 28" fill="none" stroke="currentColor" strokeWidth="3"/><path d="M10 40h100M38 14l-5 26m27-26v26m22-26 5 26M30 56h24v28m13-28h24v17H67z" fill="none" stroke="currentColor" strokeWidth="3"/></svg><span>{label}</span></div>}
export function ReportContent(){
 const {reviewedRows,appTitle,canEdit,mode,setAppTitle,visible}=useDataApp(); const rows=reviewedRows('comparison'); const net=reviewedRows('network');
 return <article className="report-content owner-report" aria-label="餐饮老板研究报告">
 <header className="report-hero"><N id="eyebrow" className="owner-eyebrow">{`餐饮商业模式研究院 / 老板读本 001`}</N><h1 data-data-app-title contentEditable={canEdit&&mode==='edit'} suppressContentEditableWarning onBlur={canEdit&&mode==='edit'?e=>setAppTitle(e.currentTarget.textContent.trim()||appTitle):undefined}>{appTitle}</h1><N id="deck" className="report-deck">{`扩店是网络的故事，赚钱是门店的账。用蜜雪集团的公开披露，练习一种不被增长数字带偏的看账方法。`}</N></header>
 <section className="owner-summary"><N id="summary">{`## 老板先看这三句话

- **不要用总部增长，替代你自己的回本判断。** 总部卖货更多，与门店实收、利润、现金回收，是不同问题。
- **“只是新店开得晚”解释不了全部差距。** 在披露门店增减记录完整的前提下，本案例商品收入增长 **3.05%**，而在网店日增长的数学下界仍为 **7.96%**；这是一个需要继续查证的信号，不是门店亏损结论。
- **决定扩店、提价或补贴之前，先拿同口径的门店账。** 看同一批店、实际营业天数和补贴承担方，再把收入一路算到现金。`}</N></section>
 <section className="report-section"><N id="two-books">{`## 01 / 看起来都是“收入”，其实是两本账

顾客买一杯饮品，门店获得销售收入；门店向总部进货，总部获得相应收入。两条链有关联，却不在同一时点，也不必同比例变化。`}</N>
 <figure className="owner-flow" aria-label="概念图：消费者付款到门店，门店进货到总部，不是等额或同步资金流"><div className="owner-flow-row"><div className="owner-actor">顾客<span>买饮品</span></div><div className="owner-arrow">付款 →<small>门店的销售账</small></div><Shop label="加盟门店"/><div className="owner-arrow">进货付款 →<small>总部的供货账</small></div><div className="owner-actor">总部<span>供货与服务</span></div></div><N id="flow-caption" className="owner-note">{`概念示意，箭头不代表等额或同步确认。门店进货还可能成为库存，不能直接当成顾客已经消费。`}</N></figure>
 <N id="two-books-implication">{`**总部数字能帮助你了解网络和供货生意，却不能替你回答“房租人工付完后还剩多少”。** 即使两边收入都增加，促销、损耗、平台费用或新增投入，也可能改变老板的现金回收。`}</N></section>
 <section className="report-section"><N id="evidence-intro">{`## 02 / 把“新店开得晚”这个解释，推到极限

半年收入不能直接除以半年末门店数：最后一天新开的店，不能当成已经贡献了半年。因此，我们改问：把每家店在网络里待的天数加起来，增长最少会是多少？`}</N>
 <div className="owner-calendar"><div className="owner-calendar-grid" aria-hidden="true">{Array.from({length:10},(_,i)=><span key={i}>店 {i+1}<b>10 天</b></span>)}</div><N id="store-days">{`**10 家店 × 各在网 10 天 = 100 店日**

示例，非品牌实测。店日把门店数量和在网时间一起考虑；**在网不等于真的营业**，临时停业仍可能在网。`}</N></div>
 <N id="timing">{`我们故意给“时间问题”最有利的条件：让 **2026 上半年的新店尽量晚开、闭店尽量早关**，让 2025 上半年反过来。即使如此，2026 的在网店日仍至少增长 7.96%。`}</N>
 {visible('network-comparison')&&<EvidenceChart id="network-comparison" queryId="comparison" title="收入增幅，低于在网店日增幅的最低边界" description="2026H1 对比 2025H1；各指标自身 2025H1 = 100。门店为集团境内外加盟网络。" rows={rows} sourceRows={rows} height={300} spec={{type:'horizontalBar',x:'measure',y:'index',valueDecimals:2,stackable:false,colors:['var(--chart-1)'],startAtZero:true}}><N id="chart-exact" className="owner-note">{`**商品收入：103.046（披露值）｜在网店日：至少 107.960（下界）**

在网店日指数的完整可能区间为 **107.960—144.097**；图上第二条只画最低边界，不代表实际观测量。两期均为 181 天。`}</N></EvidenceChart>}
 <div className="owner-boundary"><N id="boundary">{`### 差距意味着什么？也不意味着什么？

若披露门店桥覆盖全部入退网事件，“**集团商品收入 ÷ 在网加盟店日**”这一自定义指标，同比**至少下降 4.55%**。单独改变开闭店日期，不能抹掉这个方向。

**不能把它写成“单店营业额下降 4.55%”或“加盟商利润下降 4.55%”。** 分子是集团商品收入，分母是在网加盟店日；没有做恒品牌、恒渠道调整，也不是终端同店销售或实际营业店日。`}</N></div></section>
 <section className="report-section"><N id="unknowns">{`## 03 / 排除一个解释，不等于找到了真正原因

本轮排除的是：**仅靠开闭店时点变化，让集团加总每在网店日商品收入强度完全不变。** 下面这些仍是待查解释，不能画成已经证实的原因占比。`}</N>
 <div className="owner-two-col"><N id="unknown-operation">{`### 门店怎样营业？

新店是否还在爬坡？部分门店是否临时停业？同样在网半年，实际开门做生意的天数可能不同。`}</N><N id="unknown-money">{`### 总部怎样确认收入？

供货净价、产品结构、首批备货、库存和补贴安排，可能改变总部收入与门店销售之间的关系。`}</N><N id="unknown-scope">{`### 比较的是同一类店吗？

并购和品牌组合变化没有被排除。收购日的门店数量，不是下一半年的平均门店数。`}</N><N id="unknown-demand">{`### 顾客有没有少买？

需求变化也可能影响结果，但本轮资料不足以判定。需要终端订单、客单价、复购与同店数据。`}</N></div>
 <N id="decision">{`**所以，不能从这一个差距直接选择“继续扩店”“涨价”或“加大补贴”。** 如果问题是新店爬坡，要看成熟路径；如果是净价或补贴，要看边际贡献；如果是实际营业天数，要先解释为什么没开门。不同原因，对应完全不同的经营动作。`}</N></section>
 <section className="report-section"><N id="cash-intro">{`## 04 / 回到老板的账：流水不是可拿走的钱

下面是对账路径，不是任何品牌的真实利润表，也没有假设利润率。用你自己的收银、平台结算、采购和银行流水逐层核对。`}</N>
 <div className="owner-cash"><N id="cash-bridge">{`**门店销售与结算**

扣退款、折扣，核对平台结算差额；总部补贴、平台补贴与门店自担优惠分开记。

↓

**经营贡献**

扣食材、包装、损耗、平台与配送等随订单变化的成本；避免把结算单里已扣项目再扣一遍。

↓

**门店经营结果**

再扣房租、人工、水电及其他固定支出。老板亲自干的工作也要计入合理人工，别把自己的工资当利润。

↓

**现金与回收**

调整库存、应收应付、税费和付款时点；再看装修设备、押金、借款还本付息。经营利润与可拿走的现金分开判断。`}</N></div></section>
 <section className="report-section"><N id="owner-actions">{`## 05 / 下次听到“增长很好”，就追问这三件事

### ① 增长到底落在哪本账？

索取总部供货收入、门店顾客实付、平台净结算和老板净现金的口径说明。补贴由谁承担、是否一次性、退货如何处理，都写清楚。

### ② 换成同一批店、同样的天数，还增长吗？

把新店与成熟店拆开；同时保留闭店、转让和暂闭记录，不能只看留下来的好店。需要实际营业店日，而不是期末营业状态或简单平均比例。

### ③ 增加一单、再开一家，真正多留下多少？

先用已有门店的真实结算和成本，做每单贡献与月度现金对账，再讨论促销或扩张。不要拿总部增速替代自己的租金、人工和投入约束。`}</N>
 <div className="owner-action"><N id="next-evidence">{`### 最值得补的一项证据

对研究者：取得**同一网络范围、同一营业日定义**下，两期“实际营业店日 ÷ 在网店日”的总量加权比例。目前已审查资料还没有提供这项可用证据。

对单店老板：先导出已有结算周期的收银、平台结算与采购流水，和会计一起做一遍上述现金桥；再向品牌方要可对照的同批门店、包含退出门店的统计。先把钱对上，再判断故事。

这些是建议的取证动作，不是已经做过的门店试验，也不构成具体加盟投资建议。`}</N></div></section>
 <ReportSection id="methods" queryId="network" title="证据、算法与判断修订" sourceRows={net} showHeading={false}>
 <N id="appendix-title">{`## 留给想查到底的人`}</N>
 <ReportDisclosure id="method-details" label="展开：原始数据与边界公式"><N id="method-copy">{`### 原始输入与复算

2025H1：期初 46,462 家，开业 7,721 家，闭店 1,187 家，期末 52,996 家；商品收入 13,843,184 千元。

2026H1：期初 59,785 家，开业 5,455 家，闭店 1,289 家，期末 63,951 家；商品收入 14,264,907 千元。

设期初店数 S、开业 O、闭店 C、天数 T，在事件列完整前提下：**T × max(0,S−C) ≤ 在网店日 D ≤ T × (S+O)**。

2025 店日区间为 [8,194,775，9,807,123]；2026 为 [10,587,776，11,808,440]。收入比率 = 14,264,907 ÷ 13,843,184；最低店日比率 = 10,587,776 ÷ 9,807,123。前者除以后者 = 0.9544865891，故构造指标至少下降 4.551341%。

这是确定性会计边界检查，不是统计显著性检验或因果识别。极端时点是给定披露下的宽松边界，不是对真实开闭日期的估计。`}</N></ReportDisclosure>
 <ReportDisclosure id="scope-details" label="展开：并购与营业天数为什么还不能排除"><N id="scope-copy">{`### 并购不能只减店数，不减收入

2025 年报 p13 披露，2025-12-01 收购完成时鲜啤福鹿家有 1,354 家加盟店。这是收购日数量，不是 2026H1 平均数量或店日。恒品牌调整需要同时剔除相关商品收入和店日。

在最有利时点组合下，若完全不扣收入，至少需扣约 481,885.80 店日，相当于 2,662.35 家完整在网 181 天的门店，才能让边界不再强制指向下降。这是必要数学下界，不是实际停业或并购门店估计，也不是充分反转条件。不能拿 1,354 与 2,662.35 直接比较，就宣布并购已被排除。

### 实际营业日的必要条件，不是充分条件

令 R 为真实的“商品收入/在网店日”同比比率，f 为两期“实际营业店日占在网店日比例”的比值，则每实际营业店日商品收入比率 = R/f；持平要求 f=R。

仅知道 f≤0.9544865891 不足以判断持平。连续且不约束逐店营业安排的模型中，持平存在的 f 区间为 [0.7151175885，0.9544865891]；实际店日确定后，还必须匹配对应的 R。研究代码保留了 f=0.5 等反例检查。`}</N></ReportDisclosure>
 <ReportDisclosure id="sources-details" label="展开：来源、Pro 协作与可复算记录"><N id="source-copy">{`### 一手来源

- [蜜雪 2025 中报 p16、46–47](${url25})：2025H1 门店桥与商品收入。
- [蜜雪 2026 中报 p18、59–60](${url26})：2026H1 门店桥与商品收入，2026-09-23 发布。
- [蜜雪 2025 年报 p13](${annual})：收购完成日与加盟店数量。

### 真实协作不是“请模型赞同我”

两轮 GPT Pro 协作已实际完成。第一轮把宽泛提醒改为可反驳的问题：“仅仅开闭店时间不同，能否解释差距？”随后独立复核原始披露并运行计算。第二轮纠正了“必要条件被写成充分条件”的推论；代码与报告同步修订。

[Pro 研究会话](https://chatgpt.com/g/g-p-6ae041119bd0819197e8e4c230b38feb/c/6ae04748-c2dc-83e8-a520-9a760fb0281b)（需相应账号访问）。模型回复不是原始事实来源，数值仍以财报和可复算代码为准。

[研究仓库中的最终报告与计算文件](https://github.com/louiseliu/restaurant-business-lab/tree/e855c67e53e80165f968efed9ef7ba91029cdc1a/research/2026-10-27-franchise-evidence)。执行 bounds-check.py 可复算边界。

研究日期：2026-10-27。本 HTML 是已完成研究的老板阅读版，没有新增加盟商真实账目。`}</N></ReportDisclosure>
 </ReportSection>
 <footer><N id="closing">{`**好的商业判断，不是把话说满，而是知道哪一步证据还没跟上。**

餐饮商业模式研究院 · 公开资料研究 / 非具体项目投资建议`}</N></footer>
 </article>;
}
