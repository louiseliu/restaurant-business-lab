import React from 'react';
import {DataComponent,RichNarrative,useDataApp} from '../../data-app-public.jsx';
import './vision-revision.css';
const R=({id,children,className})=><RichNarrative id={id} value={children} className={className}/>;
export function VisionRevision({item,revision}) {
 const {reviewedRows}=useDataApp();
 const prefix=`${item.id}:revision-2026-11-06`;
 const mq=`diagram-${prefix}:menu`,tq=`diagram-${prefix}:threshold`;
 const menu=reviewedRows(mq),threshold=reviewedRows(tq);
 return <section className="vision-revision" id={`read-${item.id}-revision-2026-11-06`} tabIndex={-1}>
  <R id={`${prefix}:heading`}>{`## ${revision.title}\n\n${revision.intro}`}</R>
  <R id={`${prefix}:menu-heading`}>{'### 清单外的菜，未必会被留给人工'}</R>
  <R id={`${prefix}:menu:0`}>{revision.paragraphsBeforeMenu[0]}</R>
  <DataComponent id={mq} queryId={mq} kind="custom" title={revision.menu.label} description={revision.menu.scope} sourceRows={menu} displayRows={menu}>
   <figure className="vision-figure" aria-label={revision.menu.label}>
    <R id={`${prefix}:menu-scope`} className="vision-scope">{revision.menu.scope}</R>
    <div className="vision-path" data-reviewed-rows>
     <div className="vision-path-start"><span className="vision-badge">厂商说明</span><h3>加入今日菜单</h3><p>清单内商品优先匹配</p></div><span className="vision-arrow" aria-hidden="true">→</span>
     <div className="vision-path-end"><h3>当天识别候选范围</h3><p>需要跟当班出品核对</p><small>核对是本文建议</small></div>
     <div className="vision-path-start vision-exception"><span className="vision-badge">厂商提醒</span><h3>出现清单外菜品</h3><p>不一定转交人工</p></div><span className="vision-arrow vision-warning" aria-hidden="true">→</span>
     <div className="vision-path-end vision-exception"><h3>仍选择清单内相近商品</h3><p>不能把“未录入”当作拦截</p></div>
    </div>
    <div className="vision-time" data-reviewed-rows><div><span>当日</span><strong>清单有效</strong></div><span className="vision-time-arrow" aria-hidden="true">→</span><div className="vision-midnight"><span>零点</span><strong>清单失效</strong></div><span className="vision-time-arrow" aria-hidden="true">→</span><div className="vision-time-unknown"><span>此后</span><strong>候选与恢复行为未披露</strong></div></div>
    <figcaption><R id={`${prefix}:menu-note`}>{'**本文建议：**开餐或交班时对照实际出品、当班候选清单和例外负责人。人工加购前核对并处理相近识别结果，避免重复计入。零点使用何种时区未披露，应向适用版本核实。'}</R></figcaption>
   </figure>
  </DataComponent>
  {revision.paragraphsBeforeMenu.slice(1).map((p,i)=><R key={i} id={`${prefix}:menu:${i+1}`}>{p}</R>)}
  <R id={`${prefix}:threshold-heading`}>{'### 一道难认的菜，不宜只按它来验收全局调节'}</R>
  <R id={`${prefix}:threshold:0`}>{revision.paragraphsBeforeThreshold[0]}</R>
  <DataComponent id={tq} queryId={tq} kind="custom" title={revision.threshold.label} description={revision.threshold.scope} sourceRows={threshold} displayRows={threshold}>
   <figure className="vision-figure" aria-label={revision.threshold.label}>
    <R id={`${prefix}:threshold-scope`} className="vision-scope">{revision.threshold.scope}</R>
    <div className="vision-global" data-reviewed-rows><span className="vision-badge">厂商说明</span><h3>检测框分数阈值</h3><p>调整影响所有商品</p><small>分数参数 ≠ 实测准确率</small></div>
    <div className="vision-fan" aria-hidden="true"><span>↓</span><span>↓</span><span>↓</span></div>
    <div className="vision-review" data-reviewed-rows><div><span className="vision-badge">建议复查</span><h3>原本正常商品</h3><p>不只盯着刚解决的单品</p></div><div><span className="vision-badge">建议复查</span><h3>外观接近商品</h3><p>对照结果与人工确认</p></div><div><span className="vision-badge">建议复查</span><h3>临时新增商品</h3><p>把变动一起纳入比较</p></div></div>
    <R id={`${prefix}:threshold-note`} className="vision-decision">{'**厂商建议：**先检查是否正确学习；大部分菜品都识别不出时，才考虑调低。\n\n**本文建议：**若确需调整，与技术人员一起复查受影响商品，交接改动原因、检查范围和异常负责人。错误类型与幅度、参数历史和自动回退均未验证。'}</R>
   </figure>
  </DataComponent>
  {revision.paragraphsBeforeThreshold.slice(1).map((p,i)=><R key={i} id={`${prefix}:threshold:${i+1}`}>{p}</R>)}
  <details className="study-original"><summary>本次补充的来源与适用边界</summary><div><R id={`${prefix}:research-note`}>{revision.researchNote}</R><R id={`${prefix}:source-note`}>{revision.sourceNote+`\n\n[查看安卓版手册](${revision.sourceUrl})`}</R></div></details>
 </section>;
}
