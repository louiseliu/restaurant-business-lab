"""Build a frozen narrative with distinct product comparison and purchase decision visuals."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-05-membership-marketing-note';P='research/2026-11-05-membership-marketing/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[{'title':t,'url':u} for t,u in re.findall(r'\[([^\]]+)\]\((https://[^\s)]+)\)',body)]
dg={'kind':'compare','layout':'membership-marketing-gates','label':'先分清三种能力，再核对本店新增什么','scope':'普通规则、智能生日营销与意向客户托管分别比较。版本条件依据2026年3月公告，不是当前报价；能力存在不等于本店可用。','nodes':[
{'决定':'普通CRM生日规则','承担的工作':'按生日人群与时间，配置通知、优惠券和积分发放。','产品条件':'2024年教程说明已有自动化能力；须核对本店现有版本，不保证所有当前套餐包含。','采购含义':'先看现有规则是否已够用；自动发祝福和发券不能单独证明AI增量。'},
{'决定':'智能生日营销','承担的工作':'生日专项能力，与意向客户托管分列；不直接套用托管的选券及短信限制。','产品条件':'企助专业版、SCRM版或CRM配套；商城不支持微商城，门店旗舰/至尊包含，连锁旗舰/至尊包含、专业可增购。','采购含义':'同时核对企助、商城版本与能力开通初始化；不能仅凭一个菜单判断已购买可用。'},
{'决定':'意向客户托管','承担的工作':'按顾客资料、权益和交易情况选策略、生成内容并触达；生日只是其中一个场景。','产品条件':'企助SCRM版或CRM配套；商城侧微商城、门店或连锁的旗舰/至尊版。列表可见不等于已买到托管。','采购含义':'选券与短信问答针对这一产品；若主要用不上广泛托管能力，不能以整套清单证明生日升级划算。'}
],'completion':'ConnieHe案例同时补信息、做策划和触达，没有成熟规则对照。不能把整体升级的变化归因给AI，也不能把案例直接映射为某个SKU或全包价格。','note':'图1｜作者依据同厂商公开材料整理的产品边界，不是独立效果实验、产品实测或现行账号权限保证。'}
second={'kind':'flow','layout':'membership-marketing-delivery','label':'从现有规则出发，决定保留、试用还是扩大','scope':'以下为作者建议的决策路径，并非已实现经营结果。每一步都允许回到简单规则，不用归因订单或短期券核销替代增量价值。','nodes':[
{'决定':'① 现有规则是否留下具体工作？','继续条件':'关系人和购买场景多，持续整理、策略调整或人工漏记确实占用工作。','分支与动作':'若只是资料不全或无人执行，先完善记录和责任；若规则已够用，保留现状、不升级。'},
{'决定':'② 新增产品是否接过这项工作？','继续条件':'用本店实际版本演示，并区分一次性策划、后续规则执行与长期托管。','分支与动作':'核对双版本组合及全部增量费用。大量用不上的升级功能，不构成生日场景的购买理由。'},
{'决定':'③ 必要边界能否可靠控制？','继续条件':'优惠范围、重复触达、纠错、停用和退出能实际操作；只处理适当授权且必要的信息。','分支与动作':'不能满足必要边界时，保留规则、让AI仅给待审方案；文字提示未经测试不当权限开关。'},
{'决定':'④ 有限试用是否值得继续？','继续条件':'同一时期比较整组合格顾客，含未收到消息或未下单者；核对贡献、实际触达费与总工作。','分支与动作':'样本不足只支持有限继续观察；减负可持续且值得支付才扩大。优惠或返工吃掉改善，就缩小或停止。'}
],'completion':'订单贡献以实际结算起算，扣除尚未计入的相关成本并处理退款，避免重复扣费；再比较增量软件、实施、触达与维护成本。释放时间另记，未减工资或避免招聘时不列现金节省。','note':'图2｜原创采购决策示意。没有报价、门店账目、随机试验结果、净利润或回本期估算。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['已能自动发生日券的小店，先找规则未解决的具体工作，再决定是否为AI新增能力付费。','普通生日规则、智能生日营销和意向客户托管必须分开核对；版本组合与优惠控制会改变采购选择。','有限试用要比较整组合格顾客的新增贡献与总工作；核销、归因订单和省下分钟不自动等于现金利润。'],'diagram':dg,'secondDiagram':second,'sections':sections,'meaning':'让供应商在本店真实版本中证明新增能力接过什么工作，再以可控制的优惠、触达与成本边界决定试用和续费。','unknowns':['六个入口同属有赞，不是六项独立效果证据；未确认ConnieHe实际实施时间。','没有客户合同、全包报价、门店账目或后台实测；不能保证当前所有账号的可用性。','未新增Pro、采访或门店试验；没有小店净利润、回本期或年度复购验证。'],'actions':['规则够用先不升级；若只是资料不全或活动没执行，先完善必要记录与责任。','只试一项真实负担，先定合格人群、观察期、分组和成本投诉边界，优先随机固定归组。','只有净增贡献或可靠减负值得支付增量总成本才扩大；返工、优惠或版本支出抵消改善时收窄或停止。'],'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['business-model','ai'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'已有生日自动规则之后，AI还应接过哪项工作？区分三种产品、双版本条件与优惠控制，以新增贡献和总工作决定是否升级。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'产品边界与采购判断','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':s['title'],'detail':s['url']} for s in sources]+[{'title':'作者研究分析','detail':U}],'caveats':[diagram['completion'],diagram['note']]}}
summaries=['具名厂商案例，同时改变关系人信息记录、策划与触达；没有成熟生日规则对照和完整净利润。不采用其增长数字。','2024年普通CRM生日营销教程，说明按时间组织与发放的规则能力，不证明所有当前套餐都可用。','2025年意向客户托管教程，区分列表与托管。内测是当时描述，不证明2026年仍内测。','2026年3月版本公告，分列智能生日营销和意向客户托管的企助与商城条件；不是客户合同或全包报价。','2026年7月意向客户托管问答：不能按券获取来源限定推送，适用类型排除后在已有可用券中选择；不代表自动新建券，不外推智能生日。','2026年7月意向托管短信问答：长度还涉及链接、券名称和签名。没有本店单价或单条计费保证，不跨产品外推。']
write('membership-marketing-source-previews.json',{s['url']:{'title':s['title'],'summary':summary,'source':'2026-11-05公开资料核验；六个入口来自同一厂商','approvedForReport':True} for s,summary in zip(sources,summaries)})
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; two original diagrams')
