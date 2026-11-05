"""Build reviewed diagrams and complete narrative from the verified public note."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text())
ID='research-2026-11-05-dq-robot-experience-note';P='research/2026-11-05-dq-robot-experience/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[{'title':'CFB集团｜DQ与Sharpa项目公告（参与方）','url':'https://www.cfbgroup.net/zh-hant/news/dq-sharpa-blizzard-robot-restaurant-ai-new-scene'}, {'title':'每日经济新闻｜开业报道与专家判断','url':'https://www.nbd.com.cn/articles/2026-08-29/4565917.html'}, {'title':'第一财经｜开业现场有限观察与参与方采访','url':'https://www.yicai.com/news/103339884.html'}, {'title':'南方周末行业动态｜CEO访谈（参与方口径）','url':'https://www.infzm.com/contents/329884'}, {'title':'Sharpa｜到店指南（官方服务安排）','url':'https://www.sharpa.com/pages/visitor-guide'}]
dg={'kind':'compare','layout':'dqrobot-gates','label':'一台机器，三笔预算，各自需要继续投入的证据','scope':'作者提出的预算分工，不是DQ已采用的财务制度。探索、体验与替岗可以并存，不代表必然依次升级。','nodes':[
 {'决定':'技术探索','购买什么':'真实门店中的任务学习与能力改进。','继续投入的证据':'目标任务逐步可交付，异常与干预负担有可追踪变化。','先约定':'总部、供应商与门店分别承担哪些费用，支持到何时。','停止或调整':'投入增加而接管负担未降时，收窄任务或停止扩店。'},
 {'决定':'顾客体验','购买什么':'带来可核实的新增购买、复购或减少流失的体验理由。','继续投入的证据':'新鲜感减弱后仍有可归因的新增贡献，且不挤压正常服务。','先约定':'保留普通取餐渠道，计入展示、空间和额外接待支出。','停止或调整':'贡献达不到原定要求时，缩短展示时段或结束合作。'},
 {'决定':'单店替岗','购买什么':'能够独立交接的一段工作，而非一次制作动作。','继续投入的证据':'本店正常订单与完整餐段下稳定交付，干预可安排，实际付薪安排可以改变。','先约定':'完整成本、补料清洁、故障恢复、接管人及支持期限。','停止或调整':'若须偏离正常需求限量、未计价的额外看护或未落实降价才能成立，留在有上限的试验预算中。'}
 ],'completion':'技术团队学到东西 ≠ 门店新增收入；顾客愿意等待 ≠ 忙时岗位可以退出。三种价值不能用同一项指标互相替代。','note':'图1｜原创决策示意，全部验收条件为作者建议；不是已经实现的经营效果，也不估算采购回本期。'}
second={'kind':'flow','layout':'dqrobot-delivery','label':'预约通道完成了订单，普通柜台的工作却未必退出','scope':'以开业报道披露的服务安排说明比较边界；下半部的工时与现金核验是作者建议。不同日期的有限观察和访谈数字不拼成速度趋势。','nodes':[
 {'决定':'机器人体验通道','已披露安排':'开业探访记录单一奥利奥口味、专属预约；CEO访谈介绍当时每日限量50至60单。','可以支持':'在真实门店内，以受控任务范围开展探索。','不能直接推出':'限量不是实际销量，完成预约不是正常柜台已少排一个人。'},
 {'决定':'人工正常通道','已披露安排':'开业探访记录人工仍接临时订单；官方指南分别介绍机器人预约与24小时人工柜台。','可以支持':'体验预约与日常取餐并行，顾客仍有普通服务通道。','不能直接推出':'24小时门店营业不等于机器人全天运行，不能据此算夜班工资节省。'},
 {'决定':'先核完整工作周期','已披露安排':'公开资料未给出全部人工干预工时及成本承担方。','可以支持':'下一步记录看护、补料、清洁、接管、恢复和对其他工作的打断。','不能直接推出':'列出待核工种，不等于断言本案例每项都有人工介入。'},
 {'决定':'再核现金与贡献','已披露安排':'公开资料未提供可归因工资减少或净增利润。','可以支持':'核对实际可避免的付薪支出，或扣除变动支出后的新增订单贡献。','不能直接推出':'释放的零碎时间不是工资节省；同一订单不能重复记为引流和产能收益。'}
 ],'completion':'若正常订单和完整工作周期尚未验证，预约体验的完成率不能直接用于替岗采购。反之，稳定预约单品本就是本店需求时，有限任务也可能有价值。','note':'图2｜原创经营机制示意。来源只支持标明的安排与证据缺口；不表示真实客流比例、人工配置或已测得的因果关系。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['DQ与Sharpa的公开资料支持真实门店中的有限探索，尚不足以证明可按“少排一个人”复制采购。','探索、顾客体验与替岗可以共享设备，但应分别约定预算、责任与继续投入的证据。','比较正常订单和完整工作周期，并核对可改变的付薪安排，才有理由从试验转入替岗采购。'],'diagram':dg,'secondDiagram':second,'sections':sections,'meaning':'先决定下一笔钱购买什么，再选择相应证据。不能用技术进步代替体验贡献，也不能用预约热度代替单店替岗的现金账。','unknowns':['长期可靠性、完整项目报价、人工接管工时及各方承担费用仍未公开。','未见可归因的工资减少或净增利润，不能估算回本期或宣称AI经营成功。','文章分析2026年8月开业阶段与本次可读官方指南，不声称掌握数月后的实际运行表现。'],'actions':['探索项目限定预算、支持人员和复查节点，干预负担不降时收窄任务。','体验项目保留正常取餐，检查新增购买扣除额外投入后是否值得持续。','替岗采购先验证本店正常订单与完整餐段，再评估确实可改变的付薪安排和完整成本。'],'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['ai','business-model'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'DQ机器人体验店提供了有限探索的真实场景；从探索预算转向单店替岗采购，还需正常订单、完整人工工时和现金成本证据。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'事实边界与作者提出的预算核验条件','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':s['title'],'detail':s['url']} for s in sources]+[{'title':'作者研究分析','detail':U}],'caveats':[diagram['completion'],diagram['note']]}}
summaries=['项目方说明沿用原有原料、设备与制作流程完成冰淇淋制作，是方案与目标说明，未验证经营效果。','报道中的专家判断认为短期营销价值可能高于劳动力价值；未提供经审计的营销回报。','记者约一小时有限观察记录单一口味、专属预约与人工通道；约六分钟不是持续吞吐测试。关于训练难点的解释属于参与方说法。','行业动态栏目CEO访谈介绍当时每日预约限量50至60单、机器人单份约七分钟、人工约三分钟。为受访者口径，不是实际销量或独立效果验证。','官方指南分别介绍机器人体验预约与24小时人工点单柜台；不能解释为机器人全天运行或夜班节省。']
write('dqrobot-source-previews.json',{s['url']:{'title':s['title'],'summary':summary,'source':'2026-11-05公开资料核验；证据身份见标题与摘要','approvedForReport':True} for s,summary in zip(sources,summaries)})
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; two original diagrams')
