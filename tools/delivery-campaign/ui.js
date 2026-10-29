(function () {
  'use strict';
  const M = window.DeliveryModel;
  const $ = id => document.getElementById(id);
  const fmt = new Intl.NumberFormat('zh-CN', {minimumFractionDigits:2,maximumFractionDigits:2});
  const count = new Intl.NumberFormat('zh-CN', {maximumFractionDigits:2});
  const money = n => (Math.abs(n) < 0.005 ? '0.00' : (n < 0 ? '−' : '') + fmt.format(Math.abs(n))) + ' 元';
  const signedMoney = n => (n >= 0.005 ? '+' : '') + money(n);
  const pct = n => new Intl.NumberFormat('zh-CN',{maximumFractionDigits:2}).format(n*100) + '%';
  let current = null;
  let custom = false;
  const embedded = window.self !== window.top;
  if (embedded) {
    $('export').hidden = true;
    $('print').hidden = true;
    const embedNote=document.createElement('p');embedNote.className='small muted';embedNote.textContent='这是嵌入预览；可直接改数。若需留存输入或打印，请通过外层页面下载独立 HTML，在自己的浏览器中打开。';$('inputs').appendChild(embedNote);
    document.querySelectorAll('footer a').forEach(a=>{a.removeAttribute('target');a.removeAttribute('href');});
  }
  const fields = ['N','alpha','cp','cb','F'];
  function read() {
    const values = Object.fromEntries(fields.map(key => [key,$(key).value]));
    values.alpha = M.number(values.alpha, '真实增量比例') / 100;
    return values;
  }
  function thresholdCopy(r) {
    if(r.N===0) return ['没有活动订单','N=0 时结果仅为 −F，与 α 无关；不计算持平比例。'];
    if(r.cb===0) return ['不适用标准阈值','cᵦ=0，结果为 N×cₚ−F，与 α 无关。请核对原价单贡献。'];
    if(r.cb<0) return ['不适用“至少达到”阈值','cᵦ<0 时曲线随 α 上升而下降。原价单本就亏贡献，先核对口径并单独分析，不套用正贡献阈值。'];
    if(r.thresholdState==='precision-limit') return ['无法可靠显示比例阈值','原价单均贡献过于接近 0，超过数值计算精度。请检查单位与输入；不要采用这个阈值。'];
    const approx='约 '+pct(r.threshold);
    if(r.thresholdState==='all-positive') return ['0%–100% 均为正值','代数持平点为 '+approx+'（低于 0%）；有效范围内不亏贡献。仍不等于证实了真实效果。'];
    if(r.thresholdState==='break-even-at-zero') return ['0% 时刚好持平','α>0% 时为正值；此结论仍以五个输入和适用条件成立为前提。'];
    if(r.thresholdState==='break-even-at-one') return ['100% 时才刚好持平','即使归因订单全是真增量，也只是持平；α<100% 时为负值。'];
    if(r.thresholdState==='unreachable') return ['0%–100% 内无法持平','代数持平点为 '+approx+'（超过 100%）；即使全部是真增量也不足以持平。'];
    return [approx,'仅在 N>0、cᵦ>0 时：α* = 1 − cₚ/cᵦ + F/(N×cᵦ)。达到该比例才持平，高于它才为正值。'];
  }
  function renderChart(r) {
    const W=Math.max(300,Math.round($('chart').clientWidth||620)),H=W<480?270:300,L=W<480?62:80,R=W<480?18:24,T=35,B=47,w=W-L-R,h=H-T-B;
    $('chart').setAttribute('viewBox','0 0 '+W+' '+H);
    let min=Math.min(r.atZero,r.atOne,0),max=Math.max(r.atZero,r.atOne,0);
    const span=max-min;
    if(span===0){min=-1;max=1;}else{min-=span*.16;max+=span*.16;}
    const x=a=>L+a*w,y=v=>T+(max-v)/(max-min)*h;
    const compact=v=>Math.abs(v)>=1e8?new Intl.NumberFormat('zh-CN',{maximumFractionDigits:2}).format(v/1e8)+'亿':Math.abs(v)>=1e4?new Intl.NumberFormat('zh-CN',{maximumFractionDigits:2}).format(v/1e4)+'万':new Intl.NumberFormat('zh-CN',{maximumFractionDigits:Math.abs(v)<1?2:0}).format(v);
    const parts=['<title id="chart-title">不同真实增量比例下的条件增量贡献</title><desc id="chart-desc">α 为 0% 时 '+money(r.atZero)+'，100% 时 '+money(r.atOne)+'。当前 '+pct(r.alpha)+' 时 '+money(r.delta)+'。这是条件情景。</desc>'];
    for(let i=0;i<=4;i++) {const value=min+(max-min)*i/4;parts.push('<line x1="'+L+'" y1="'+y(value)+'" x2="'+(W-R)+'" y2="'+y(value)+'" stroke="#e7ebef"/><text x="'+(L-10)+'" y="'+(y(value)+4)+'" text-anchor="end" class="chart-axis">'+compact(value)+'</text>');}
    parts.push('<line x1="'+L+'" y1="'+y(0)+'" x2="'+(W-R)+'" y2="'+y(0)+'" stroke="#73808e" stroke-dasharray="5 4" stroke-width="1.5"/>');
    for(const a of [0,.25,.5,.75,1]) parts.push('<text x="'+x(a)+'" y="'+(H-20)+'" text-anchor="middle" class="chart-axis">'+pct(a)+'</text>');
    parts.push('<path d="M '+x(0)+' '+y(r.atZero)+' L '+x(1)+' '+y(r.atOne)+'" fill="none" stroke="#126fc1" stroke-width="3"/>');
    if(r.threshold!==null && r.threshold>=0 && r.threshold<=1)parts.push('<circle cx="'+x(r.threshold)+'" cy="'+y(0)+'" r="5" fill="#fff" stroke="#171b22" stroke-width="2"/>');
    parts.push('<line x1="'+x(r.alpha)+'" y1="'+T+'" x2="'+x(r.alpha)+'" y2="'+(H-B)+'" stroke="#aac9e7" stroke-dasharray="3 4"/><circle cx="'+x(r.alpha)+'" cy="'+y(r.delta)+'" r="6" fill="#126fc1" stroke="#fff" stroke-width="2"/>');
    parts.push('<text x="'+Math.min(Math.max(x(r.alpha),L+80),W-R-80)+'" y="20" text-anchor="middle" class="chart-value">当前 '+pct(r.alpha)+' · '+(r.delta>0?'+':'')+compact(r.delta)+' 元</text>');
    $('chart').innerHTML=parts.join('');
  }
  function render() {
    fields.forEach(key=>$(key).removeAttribute('aria-invalid'));
    try {
      const r=M.evaluate(read());current=r;
      $('result').hidden=false;$('invalid-result').hidden=true;$('sensitivity').hidden=false;$('sensitivity-invalid').hidden=true;$('export').disabled=false;
      $('delta').textContent=signedMoney(r.delta);
      $('verdict').textContent=r.delta>=0.005?'在当前假设下，多贡献了这些钱。':r.delta<=-.005?'在当前假设下，活动反而少贡献了钱。':'在当前假设下，约为持平（显示精度内）。';
      $('decomposition').innerHTML=[['活动订单贡献 N×cₚ',money(r.promoContribution)],['减：被替代订单贡献',money(r.displacedContribution)],['减：固定增量支出',money(r.F)],['假设真正新增 / 替代订单',count.format(r.incrementalOrders)+' / '+count.format(r.replacedOrders)+' 单']].map(([k,v])=>'<dt>'+k+'</dt><dd>'+v+'</dd>').join('');
      const [title,note]=thresholdCopy(r);$('threshold').textContent=title;$('threshold-note').textContent=note;
      $('decision-note').textContent=r.N===0?'先核对为何无归因订单仍有支出。没有订单不代表没有活动成本。':r.cp<0?'活动单均贡献为负：每做一单，未扣固定费用前已亏贡献。先查结算、折扣与成本；不要只靠加单量。':r.cb<0?'原价单均贡献为负：本模型的替代效应方向会反转。请先确认这是真实可比基线，而非漏收入或重复扣费。':'下一步不是“直接投放”：先核对结算和成本，再用可解释的增量证据或保守情景与持平点比较。';
      const rows=r.scenarios.map(s=>({...s,current:Math.abs(s.alpha-r.alpha)<1e-10}));
      if(!rows.some(s=>s.current))rows.push({alpha:r.alpha,delta:r.delta,current:true});
      rows.sort((a,b)=>a.alpha-b.alpha);
      $('scenario-rows').innerHTML=rows.map(s=>'<tr'+(s.current?' class="current-row"':'')+'><td>'+pct(s.alpha)+(s.current?'（当前）':'')+'</td><td>'+signedMoney(s.delta)+'</td></tr>').join('');
      renderChart(r);
    } catch(error) {
      current=null;$('result').hidden=true;$('invalid-result').hidden=false;$('invalid-result').textContent=error.message;
      $('sensitivity').hidden=true;$('sensitivity-invalid').hidden=false;$('export').disabled=true;
      fields.forEach(key=>{if(!$(key).validity.valid || $(key).value.trim()==='')$(key).setAttribute('aria-invalid','true');});
    }
  }
  function markCustom(){custom=true;$('data-badge').textContent='自填情景 · 未经实测验证';$('state-note').textContent='仅当前页面内保留。刷新会恢复演示；下载测算记录可留存本次输入与限制。';}
  fields.forEach(key=>$(key).addEventListener('input',()=>{markCustom();if(key==='alpha'&&$('alpha').value!==''&&Number($('alpha').value)>=0&&Number($('alpha').value)<=100)$('alpha-range').value=$('alpha').value;render();}));
  $('alpha-range').addEventListener('input',()=>{$('alpha').value=$('alpha-range').value;markCustom();render();});
  $('inputs').addEventListener('submit',event=>event.preventDefault());
  const costFields=[['settlement','单均最终商户结算','起点：统一退款、补贴、含税口径；不是成交额。'],['food','食材成本','只填结算中未扣的食材成本。'],['packaging','包装成本','不要把顾客付的包装费与成本混为一项。'],['commission','佣金 / 支付手续费','结算已扣则填 0；不能再次扣除。'],['delivery','配送成本','结算已扣则填 0；店内自配送另行核对。'],['discount','商家承担折扣','结算已反映折扣则填 0；平台补贴不重复减。'],['labor','按单增量人工','只计新增变动部分；阶梯或固定支出放 F，勿重复。'],['other','其他按单变动成本','例如增量耗材/损耗；不含已计入 F 的支出。']];
  const builderDefaults={p:{settlement:22,food:11,packaging:2,commission:0,delivery:0,discount:0,labor:1,other:0},b:{settlement:26,food:11,packaging:2,commission:0,delivery:0,discount:0,labor:1,other:0}};
  $('builder-rows').innerHTML=costFields.map(([key,label,help])=>'<tr><td><label>'+label+'</label><span class="small">'+help+'</span></td>'+['p','b'].map(side=>'<td><input type="number" id="'+side+'-'+key+'" value="'+builderDefaults[side][key]+'" min="0" max="1000000" step="any" inputmode="decimal" aria-label="'+(side==='p'?'活动订单':'原价订单')+' '+label+'"></td>').join('')+'</tr>').join('');
  function builderValues(side){return Object.fromEntries(costFields.map(([key])=>[key,$(side+'-'+key).value]));}
  function renderBuilder(){try{const cp=M.contribution(builderValues('p')),cb=M.contribution(builderValues('b'));$('builder-totals').textContent='辅助结果：活动单均贡献 '+money(cp)+'；原价单均贡献 '+money(cb)+'。';$('builder-error').hidden=true;$('apply-builder').disabled=false;return {cp,cb};}catch(error){$('builder-totals').textContent='辅助结果暂不可用';$('builder-error').textContent=error.message;$('builder-error').hidden=false;$('apply-builder').disabled=true;return null;}}
  costFields.forEach(([key])=>['p','b'].forEach(side=>$(side+'-'+key).addEventListener('input',renderBuilder)));
  $('apply-builder').addEventListener('click',()=>{const v=renderBuilder();if(!v)return;$('cp').value=v.cp;$('cb').value=v.cb;markCustom();render();$('state-note').textContent='已应用单均贡献辅助结果；仍需自行核对结算是否已扣费。';$('cp').focus();});
  $('reset').addEventListener('click',()=>{fields.forEach(key=>$(key).value=key==='alpha'?M.DEFAULTS.alpha*100:M.DEFAULTS[key]);$('alpha-range').value=40;costFields.forEach(([key])=>['p','b'].forEach(side=>$(side+'-'+key).value=builderDefaults[side][key]));custom=false;$('data-badge').textContent='演示数据 · 非真实门店';$('state-note').textContent='已恢复全部演示输入。不是任何真实门店的结果。';renderBuilder();render();});
  $('print').addEventListener('click',()=>window.print());
  window.addEventListener('resize',()=>{if(current)renderChart(current);});
  $('export').addEventListener('click',()=>{
    if(!current)return;
    const r=current;
    const record={model:'delivery-incremental-contribution',version:'1.0.0',savedAt:new Date().toISOString(),status:custom?'用户自填条件情景，未经实测验证':'演示数据，非真实门店',currency:'CNY',inputs:{N:r.N,alpha:r.alpha,cp:r.cp,cb:r.cb,F:r.F},formula:'N * (cp - (1-alpha) * cb) - F',results:{delta:r.delta,threshold:r.threshold,thresholdState:r.thresholdState,scenarios:r.scenarios},restrictions:['仅非增量活动单替代同类原价订单；无其他渠道、时段、门店额外产能挤占。','单均贡献按真实结算减尚未扣除的变动成本；同一成本只扣一次。','α 未知时只作情景；平台归因订单不等于增量订单。','非门店净利润、非因果实测、非长期收益或投资回报。'],contributionBuilderDraft:{appliedAutomatically:false,p:builderValues('p'),b:builderValues('b')},privacy:'浏览器本地生成；未上传、未自动保存。'};
    const blob=new Blob([JSON.stringify(record,null,2)],{type:'application/json;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='外卖活动-条件测算记录.json';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);$('state-note').textContent='已生成本地 JSON 下载。请在浏览器下载列表确认；它不是实测经营结论。';
  });
  renderBuilder();render();
})();
