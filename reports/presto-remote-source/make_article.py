"""Generate frozen full narrative and source-bound personnel/timeline diagrams."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-05-presto-remote-note';P='research/2026-11-05-presto-remote/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[{'title':'Presto｜2023年12月14日8-K，Item 7.01','url':'https://www.sec.gov/Archives/edgar/data/1822145/000121390023095635/ea190049-8k_presto.htm'},{'title':'SEC｜2025年1月14日和解行政令','url':'https://www.sec.gov/files/litigation/admin/2025/33-11352.pdf'}]
dg={'kind':'compare','layout':'presto-remote-gates','label':'同一份披露，观察的是不同的人工','scope':'2023年12月14日公司8-K的不同指标并列解读。三张卡不是同一组订单的互斥分类，不表示准确率，也不能相减或画成性能趋势。','nodes':[
{'决定':'85%：平均非干预率','人员边界':'餐厅员工是否接过订单；与后台人工代理的使用无关。','版本与门店':'部署自研技术的门店平均值。','仍然不知道':'后台录单、审核和监督情况；店内补救、待命及总负担。'},
{'决定':'95%或以上：部分门店','人员边界':'同样只观察餐厅员工接手。','版本与门店':'公司披露的部分门店，不代表全部门店。','仍然不知道':'不能据此证明全程无人参与，或作为所有门店的平均结果。'},
{'决定':'约30%：无需后台录单','人员边界':'无需人工代理录入，但仍由人工监督，准备审核、验证和纠正。','版本与门店':'选定试点门店的先进版本，不涵盖所有自研部署。','仍然不知道':'监督耗时、端到端自主完成及准确率；不能从30%推断无人看管。'}
],'completion':'门店接手、后台录入与持续监督是三种不同工作。若要验收自主能力，需固定同一版本和订单范围，并记录每种人工作用；不同记录可能重叠。','note':'图1｜依据公司历史披露制作的原创指标解释。无同口径差值、人工成本或经营收益计算。'}
second={'kind':'flow','layout':'presto-remote-delivery','label':'历史版本与披露修正，必须按时间分开读','scope':'依据SEC行政令第12—14、25—26、29—38段及2023年12月8-K整理。时间线不表示性能改进速度；2025年监管认定回看历史事实，不是产品版本升级。','nodes':[
{'决定':'2021年11月—2022年9月','技术与范围':'商业部署均由第三方技术支持。','证据边界':'不能把这一阶段能力归为全部自研；此后第三方版本继续在用。'},
{'决定':'2022年9月起','技术与范围':'开始部署自研早期版本：语音转文字，异地代理录单，系统语音确认。','证据边界':'行政令认定早期版设计上依赖人工，每单需要人工介入。'},
{'决定':'2023年6月起试点','技术与范围':'先进版本增加可在部分情况下自行完成点单的AI组件。','证据边界':'从试点开始至至少当年12月，约70%订单仍需人工代理录入；不代表2026年能力。'},
{'决定':'2023年10月、11月、12月','技术与范围':'补充异地人工参与；披露超过70%订单需要人工介入；再澄清版本范围及非干预率定义。','证据边界':'各次披露口径须分别阅读，不把这些数字串成同一指标变化。'},
{'决定':'2025年1月14日','技术与范围':'SEC发布投资者披露案件的和解行政令，认定此前存在重大虚假或误导性陈述。','证据边界':'除管辖权外公司不承认也不否认；接受停止违法命令，所列处分无民事罚款，不是刑事定罪。'}
],'completion':'历史案件支持核对服务定义与人员依赖。它不证明所有餐厅或顾客都不知情，也不能单独解释公司后续经营变化。','note':'图2｜原创历史时间线。没有对2026年产品能力、门店效果、合同缺口或后续经营原因作判断。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['无需本店员工接手，不等于后台无人录单或监督；先明确购买的是店内减负服务还是系统自主能力。','有人兜底的混合服务也可能有价值，但须核验支持时段、高峰安排、完整收费和支持中断时的接续。','店内工作改善、供应商履约与系统自主完成需要不同证据；订单数不能直接换成可取消的付薪班次。'],'diagram':dg,'secondDiagram':second,'sections':sections,'meaning':'把付款依据与本店目标对应，查清谁仍在工作和待命，再决定试用范围、续费及是否有证据改变排班。','unknowns':['没有完整客户报价、合同、订单级记录、后台工时或可归因经营收益，不计算人工成本、利润与回本。','公司历史披露和监管和解认定不是两项独立门店效果实验，不评价2026年产品能力。','未新增Pro、门店实验或采访；中国门店语言、流程、集成及适用合规要求仍需核实。'],'actions':['固定版本、门店、餐段与订单范围，分别记录店员接手、后台录入或修改、监督和最终正确完成。','试用前明确支持不可用时谁发现、从何处接续信息、是否需要顾客重说以及谁确认完成。','按本店目标决定续费；频繁转回或补救抵消改善时收窄试用，只有确认付薪或现金支出实际减少才列现金节省。'],'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['business-model','ai'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'Presto历史披露说明：店员未接手与后台无人录单不是同一指标。采购须分清混合服务与自主能力，再验收持续交付。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'人员边界与历史版本','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':s['title'],'detail':s['url']} for s in sources]+[{'title':'作者研究分析','detail':U}],'caveats':[diagram['completion'],diagram['note']]}}
summaries=['公司自身披露。非干预率只看餐厅员工接手，与后台代理无关；85%为平均、95%或以上为部分门店。先进试点约30%无需人工代理录单，但仍监督；不能当作全程自主或准确率。','监管和解行政令，认定历史技术归属、人工参与和完成率披露问题，并区分第三方、自研早期与先进试点。除管辖权外公司不承认也不否认；不是刑事定罪或2026年产品效果测试。']
write('presto-remote-source-previews.json',{s['url']:{'title':s['title'],'summary':summary,'source':'2026-11-05公开资料核验；证据身份见标题与摘要','approvedForReport':True} for s,summary in zip(sources,summaries)})
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; two original diagrams')
