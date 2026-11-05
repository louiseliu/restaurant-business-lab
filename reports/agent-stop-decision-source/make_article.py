"""Create frozen full narrative and two evidence-scoped original mechanism diagrams."""
from pathlib import Path
import hashlib,json,re,sys
A=Path(__file__).resolve().parent;body=Path(sys.argv[1]).read_text();meta=json.loads(Path(sys.argv[2]).read_text());ID='research-2026-11-05-agent-stop-decision-note';P='research/2026-11-05-agent-stop/note.md';U=f"https://github.com/louiseliu/restaurant-business-lab/blob/{meta['commit']}/{P}"
assert hashlib.sha256(body.encode()).hexdigest()==meta['sha256']
def write(n,v):(A/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1);sections.append({'title':h,'body':t.strip().split('\n\n')})
url='https://rules-center.meituan.com/m/detail/guize/1516?activeRule=1'
sources=[{'title':'美团《商家账号中心服务协议》：智能助手服务与终止条款','url':url}]
dg={'kind':'compare','layout':'agent-stop-decision-gates','label':'登录、任务授权、既有结果：三个问题分别核对','scope':'依据具名官方协议区分状态；第三列为需要另查的经营结果，不把任务停止画成历史影响自动消失。','nodes':[
{'决定':'账号登录状态','协议已说明':'退出登录、修改密码不影响已授权的离线任务。','能回答什么':'谁仍能进入商家端，需要独立进行账号安全核查。','不能代替什么':'改密码不能证明持续任务已经停止，也不等于完成经营交接。'},
{'决定':'任务授权与任务状态','协议已说明':'可在相关入口查看、暂停或终止；终止授权后相应任务停止。账号注销或协议终止时任务授权同时终止。','能回答什么':'按对应任务入口核对现状、记录反馈；日常停用不应直接扩大成注销整个账号。','仍须核实':'暂停期限、恢复条件和在途任务处置未说明；功能开放及具体入口未实测。'},
{'决定':'已经形成的经营结果','已有证据边界':'协议内容不足以判断此前的券、活动、订单会否撤销，也不足以确定在途步骤何时结束。','核对什么':'最近可见执行记录、相关经营页面与未解决事项，应由明确的人接手。','不能作的推断':'不承诺自动回滚，也不反向断言一定保留；结果处置需查对应规则与实际记录。'}
],'completion':'协议页面标注发布日期2026年10月7日，正文生效日期2025年6月16日。版本关系尚未核明，不能据此推断上线日期或具体商家适用版本。','note':'图1｜原创机制对照。一个官方协议来源，不是三项独立实测；账号与任务分开，不代表已验证任何商户后台。'}
second={'kind':'flow','layout':'agent-stop-decision-delivery','label':'交接或停用时，如何作出保留、收窄与停止的决定','scope':'作者提出的管理路径，不代表产品已有这些字段或已完成经营实验。账号安全与持续任务应同时检查。','nodes':[
{'决定':'① 原经营目的仍有效吗？','判断依据':'任务服务什么决定，门店、对象、活动条件和目标是否改变。','分支与动作':'目标仍有效且接手人能查明现状，可考虑保留；目的失效则考虑终止，无人承接或暂不明则先收窄或暂停。'},
{'决定':'② 需要分析，还是需要经营变更？','判断依据':'离线任务及调价、发券、修改营销策略等敏感操作需另行明示授权；范围以已开通权限及功能页面为准。','分支与动作':'只需要分析就控制在该目的内。对象、约束与例外责任说不清，保留人工决定，不扩大自动执行。'},
{'决定':'③ 停止动作是否有可见反馈？','判断依据':'记录停止对象、操作时间和页面反馈，并核对最近可见执行结果。','分支与动作':'反馈不明、时间异常或找不到入口时，通过官方支持核实；不把点过按钮或再次改密码当作停止验收。'},
{'决定':'④ 剩余事项是否有人接手？','判断依据':'将任务状态与停前的经营影响分别记录；已有券、活动、订单及在途步骤的处理仍待核实。','分支与动作':'明确接手人及未解决事项。恢复或重新授权前另查规则与新条件，不假定暂停后必然无缝恢复。'}
],'completion':'是否值得持续授权，要连同核查、交接、返工与退出工作一起看。本文没有净节时、费用或利润证据，不能把少登录几次等同于已经获得经营收益。','note':'图2｜原创条件决策示意。交接情景与经营汇总均为分析示例，不是真实事故、产品测评或功能承诺。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['退出登录与改密码不能据此视为离线任务停止；应核对对应任务授权与可见结果。','目标仍有效且有人接手，可考虑保留；目的失效、无人负责或状态不清，应收窄、暂停或终止相应安排。','任务停止与历史影响处置是两个问题；已有券、活动、订单及在途步骤的处理仍须另查。'],'diagram':dg,'secondDiagram':second,'sections':sections,'meaning':'交接不止交出账号。先确定哪些安排仍服务经营目的、由谁检查，再决定保留或停止；任务反馈与遗留事项都应有人承接。','unknowns':['仅依据美团具名官方协议，不证明所有商家端已开放同一AI功能。','发布日期与生效日期并存，版本关系未核明；未验证具体入口、权限、暂停恢复或在途处置。','不判断历史券、活动及订单会否撤销；没有净节时、费用或利润证据，未新增Pro、真实授权变更或门店实验。'],'actions':['交接时分别检查账号安全和持续任务；只保留目标仍有效且有人负责检查的安排。','对不再适用或暂不能核清的任务，按对应入口暂停或终止并记录反馈，必要时由官方支持确认。','把最近执行结果与遗留问题交给明确负责人，恢复或重新授权前核对规则，不急于扩大操作范围。'],'sources':sources}
entry={'id':ID,'path':P,'title':title,'section':'research','topics':['business-model','ai'],'publishedAt':meta['time'],'updatedAt':meta['time'],'excerpt':'退出账号或改密码为什么不能代替停止任务？以美团具名协议区分登录、任务授权和既有经营结果，判断交接时何时保留、收窄或停止。','body':body,'originalBodySha256':meta['sha256'],'sourceUrl':U,'firstGit':meta['commit']}
queries={}
for diagram,suffix in [(dg,''),(second,':second')]:
 q='diagram-'+ID+suffix;queries[q]={'rows':diagram['nodes'],'source':{'label':diagram['label'],'files':[P],'metricDefinitions':[{'label':'任务状态与交接决策','definition':diagram['scope']+' '+diagram['note'],'componentIds':[q]}],'evidenceFlow':[{'title':s['title'],'detail':s['url']} for s in sources]+[{'title':'作者条件性经营分析','detail':U}],'caveats':[diagram['completion'],diagram['note']]}}
write('agent-stop-decision-source-previews.json',{url:{'title':sources[0]['title'],'summary':'智能助手离线任务与登录状态分离，相关操作另行授权；终止授权后相应任务停止。具体功能以已开通权限与页面为准。页面发布日期2026年10月7日与正文生效日2025年6月16日并存，版本关系未核明；不据此判断历史结果回滚或在途步骤结束时间。','source':'2026-11-05官方公开协议核验；单一来源，未实测商户后台','approvedForReport':True}})
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',{'surface':'report','title':title,'generatedAt':meta['time'],'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries})
print(meta['sha256'],len(sections),'complete sections; two original diagrams')
