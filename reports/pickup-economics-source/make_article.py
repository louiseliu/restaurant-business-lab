"""Generate full frozen narrative and two explicitly analytical diagrams."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text())
ID='research-2026-11-05-pickup-economics-note';P='research/2026-11-05-pickup-economics/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[{'title':'红餐网｜三位经营者自述（2026-02-06）','url':'https://m.canyin88.com/zixun/2026/02/06/110798.html'},{'title':'京东开放平台｜订单小票打印规范','url':'https://opendj.jd.com/staticnew/widgets/introduce/orderPrintReceiptsRules.html'},{'title':'上观新闻｜历史配送业务用工与补贴个案（2025-07-28）','url':'https://www.shobserver.cn/wx/detail.do?id=953327'}]
dg={'kind':'compare','layout':'pickup-gates','label':'同样一笔自提单，原本会发生什么，决定怎么比较','scope':'作者提出的三种订单来源假设，不是三类订单的实测占比。红餐网中的柜台引导动作提供问题线索；以下比较方法均为研究分析。','nodes':[
{'决定':'原本在柜台买','原订单基线':'顾客已到店，原本会直接购买同一份餐品。','比较什么':'自提净结算相对柜台实收的差异，加减商品、包装、引导及交付工作的变化。','不要记错':'原本没有骑手，不能将省下配送费算作这次改道的收益；整单实收不等于新增收入。'},
{'决定':'原本叫配送','原订单基线':'顾客原本会在本店下配送订单，现改为自提。','比较什么':'两种订单的真实结算、商家承担的费用及交付工作差异。','不要记错':'顾客少付配送费，不证明商家等额省钱；以自己的账单判断。'},
{'决定':'原本不会发生的购买','原订单基线':'没有这次展示或优惠就不会发生的购买，也可能是老客真实增购或保住的需求；均需验证。','比较什么':'新增实收扣除新增食材、包装、操作和活动支出，并关注挤占其他订单。','不要记错':'平台新客未必是门店新客；来源分不清时保留未知，不把自提增长全部记为增量。'}
],'completion':'先识别原订单基线，再比较差额。平台、柜台和其他渠道要合起来看，并考虑天气、周末、菜单与其他活动等变化；全店变化本身仍不证明渠道因果效果。','note':'图1｜原创机制比较。无订单占比、费率、利润或因果收益估计；不是案例门店已采用的方法。'}
second={'kind':'flow','layout':'pickup-delivery','label':'优惠确认期短，用工承诺却可能更长','scope':'作者提出的扩班决策示意。上观新闻的历史配送个案仅提示期限错配的可能性，不证明当前自提项目将撤补。各阶段没有设定实际天数或金额。','nodes':[
{'决定':'先核活动条件','观察区间':'区分已确认优惠条件与尚未发生的需求；确认优惠期不是保证订单。','核对证据':'适用商品与订单、优惠出资方、净结算、终止日期及允许收缩的方式。','决策边界':'不从顾客券面额推断门店补贴，也不预先计入未收到的款项。'},
{'决定':'再看全部用工承诺','观察区间':'覆盖这次人手安排的全部承诺期。','核对证据':'新增付薪、加班、调班对原时段的影响及活动结束后的合法可行安排。','决策边界':'已有员工和老板补位也有任务代价；临时用工不是免费且随时可撤。'},
{'决定':'优惠改变以后','观察区间':'超出已确认优惠期的部分，单列为风险情景。','核对证据':'在不同优惠条件下，新增需求和贡献能否覆盖仍需承担的支出。','决策边界':'未知不填成当前补贴自动续期；假设变化不写成撤补预测。'},
{'决定':'分别决定推荐与扩班','观察区间':'先小范围观察，再决定是否作更长承诺。','核对证据':'推荐看实际贡献与服务体验；扩班看全店新增需求、忙时工时和全期承诺支出。','决策边界':'已有需求证据支持的审慎情景可覆盖全部承诺、后续安排可行且承受得起不足时，短期扩班也可能合理。'}
],'completion':'一笔柜台订单改道合算，不代表已经有理由长期增员。把推荐动作与扩班决定拆开，避免用短期补贴默认支持长期支出。','note':'图2｜原创期限与决策示意，全部核查条件是作者建议，不是实际补贴规则、用工安排或收益测算。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['已到店顾客转为平台自提，要与原本的柜台贡献比较，不能把整笔订单算成新增生意。','是否继续推荐，看实际净结算与服务负担；是否扩班，还要看全店增量和用工承诺期限。','已有需求证据支持的审慎情景能覆盖全部人手承诺且可承受不足时，短期加配可能合理；不能默认优惠或订单延续。'],'diagram':dg,'secondDiagram':second,'sections':sections,'meaning':'先辨订单来源，再接通结算和忙时工作。利用合算的优惠，不等于提前承担缺乏长期证据的固定支出。','unknowns':['未取得现行商家合同、完整结算账单、跨渠道顾客记录或用工成本，不能给出利润或费率结论。','三位受访者自述不能拼成同一家门店的投入产出链，历史配送个案不能代替当前自提规则。','未开展门店试验，复购、真实新增需求与服务时间改善均未得到验证。'],'actions':['限定商品与可承受时段观察，保留原收款选择，记录净结算差异、额外工作与其他渠道变化。','出现贡献侵蚀或高峰解释负担而无额外购买证据时，缩小或停止主动引导；关系维护支出单列。','扩班前比较已确认优惠期与全部用工承诺期，优惠变动、需求替代或新增工时过高时重新判断。'],'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['business-model'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'顾客已经到店，转为平台自提是否合算，要先辨订单原本会在哪里成交，再把短期优惠与用工承诺分开。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'订单比较基线与期限核查建议','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':s['title'],'detail':s['url']} for s in sources]+[{'title':'作者研究分析','detail':U}],'caveats':[diagram['completion'],diagram['note']]}}
summaries=['报道中三位经营者分别谈及引导柜台顾客自提、忙时两班支援和补贴相关投入意愿。属于具名自述，不是完整损益或独立因果验证，不采用增长数字估算收益。','适用于开放平台对接服务商及相关商户的小票规范，要求标识到店自提并限制打印优惠承担等对账信息。不证明后台缺少记录，不提供当前费率或优惠出资比例。','2025年配送业务店主自述，提及订单补贴增长后加雇帮厨及后来的补贴分担变化。仅说明期限错配可能性，不移植当时金额或比例到2026年自提。']
write('pickup-source-previews.json',{s['url']:{'title':s['title'],'summary':summary,'source':'2026-11-05公开资料核验；证据身份见标题与摘要','approvedForReport':True} for s,summary in zip(sources,summaries)})
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; two original diagrams')
