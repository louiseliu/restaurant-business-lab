"""Create two evidence-scoped diagrams and full narrative from the frozen public note."""
import hashlib,json,re,sys
from pathlib import Path
A=Path(__file__).resolve().parent; NOTE=Path(sys.argv[1]); body=NOTE.read_text();ID='research-2026-11-05-monthly-meal-customization-note';COMMIT='d819c713ba57d611170f531848e33aa15c6e50b9';TIME='2026-11-05T04:05:13Z';PATH='research/2026-11-05-monthly-meal-customization/note.md';URL=f'https://github.com/louiseliu/restaurant-business-lab/blob/{COMMIT}/{PATH}'
assert hashlib.sha256(body.encode()).hexdigest()=='2c43f7b73c0314a0b9d68faceb7dfad8e881d03e1872c4d66d66c47aecd6ddd9','Input is not the frozen public note'
def write(name,v):(A/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:];lead=body.split('\n\n')[1]
sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1)
 if h=='研究说明':continue
 sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[{'title':'武进新闻｜记者到店观察与王晖自述（2026-09-30）','url':'https://www.wjyanghu.com/yhw/hotspot/wjxw/2026-09-30/174229.html'}, {'title':'常州科教城｜月餐转型及工作流的刊载采访（2026-08-24）','url':'https://kjc.changzhou.gov.cn/index.php?a=show&c=phone&catid=12443&id=10901'}]
diagram={'kind':'compare','layout':'meal-context','label':'业务转向、整理任务和现场使用，证据各到哪一步','scope':'研究示意：分开阅读王晖轻食店的公开材料。报道中的先后叙述不是因果识别，三个层次不能合成为AI扭亏结论。','nodes':[
{'title':'服务与配送先收敛','label':'刊载采访的业务叙述','cells':[{'label':'报道写了什么','text':'团餐询盘、暖餐与月餐，以及收窄配送范围、固定线路。'},{'label':'经营上应问什么','text':'先确认自己愿意出售哪些选择，哪些安排能够稳定交付。'},{'label':'证据边界','text':'各项调整的贡献未被分离，不能把转型后的销售归给AI。'}]},
{'title':'差异变成每日整理任务','label':'刊载采访的工作流说明','cells':[{'label':'报道写了什么','text':'个性化要求需要汇总，工作流处理需求并生成标签和份量清单。'},{'label':'经营上应问什么','text':'剩余负担来自大量自由表达，还是有限选项表就能解决？'},{'label':'证据边界','text':'模型与代码未公开，汇总和打印也可能由普通规则完成。'}]},
{'title':'清单进入实际打包','label':'现场工作动作与店主自报分开','cells':[{'label':'记者看见什么','text':'配餐员依据系统清单打包，支持“流程被使用”的判断。'},{'label':'经营上应问什么','text':'高峰时能否按确认要求装配，并在约定时间交付？'},{'label':'证据边界','text':'成本及承载量说法属店主自报，未核验持续准确率或AI净收益。'}]}
],'note':'图1｜原创证据与经营问题示意。业务与流程叙述来自两篇主源；“经营上应问什么”为作者分析，不是门店已完成的对照或验收。'}
second={'kind':'flow','layout':'meal-change','label':'“只改今天，明天照旧”需要四处保持一致','scope':'作者设计的合成验收情景：熟客长期选择甲种主食，临时要求今天换乙种、明天恢复。下列能力尚未在该店核实，不是事故还原或上线功能清单。','nodes':[
{'title':'区分长期偏好与当天例外','label':'先判断这句话适用哪一天','cells':[{'label':'可检查的草稿','text':'保留原话，列出今天的例外及结束日期，不直接覆盖长期偏好。'},{'label':'人工确认','text':'核对日期、允许的替换项和不完整信息，不能由系统先承诺无法执行的改动。'}]},
{'title':'汇总和个人标签用同一版本','label':'确认后再更新出餐依据','cells':[{'label':'可检查的草稿','text':'把同一次已确认改动对应到备餐汇总、个人标签及配送安排，标清最新版本。'},{'label':'人工确认','text':'核对改动是否在各处一致，旧清单与旧标签不继续混用；确认后的整理也可由普通规则完成。'}]},
{'title':'打包前核对已经执行的工作','label':'标签正确仍要核对实物','cells':[{'label':'可检查的草稿','text':'列出需要接手的改动和原始依据，让员工看见哪些要求仍待处理。'},{'label':'人工确认','text':'判断食材、制作和打包是否已经完成，是否来得及更改，并核对实际餐品。'}]},
{'title':'配送承诺和次日恢复一起收尾','label':'不能只核当天聊天回复','cells':[{'label':'可检查的草稿','text':'把当天交付安排和次日恢复条件呈现给负责人员，不从一条回复推定履约完成。'},{'label':'人工确认','text':'确认本次变化不会超出厨房与配送余量；翌日仍按原长期偏好，异常有人接手。'}]}
],'note':'图2｜原创研究示意，本文未执行该演练。涉及过敏或健康限制的要求转交胜任人员核对，不能让模型保证食材安全、替代配方或没有交叉接触。'}
for dg in [diagram,second]:
 dg['nodes']=[{'环节':n['title'],'性质':n['label'],**{('材料支持' if c['label'] in ['报道写了什么','记者看见什么'] else c['label']):c['text'] for c in n['cells']}} for n in dg['nodes']]
story={'id':ID,'headline':title,'lead':lead,'findings':['选择和配送范围已收敛、重复自由表达仍造成整理负担时，可以小范围试用。','把长期偏好与当天例外分开，人工确认后让汇总、标签和交接保持一致。','厨房和配送没有余量时，整理更快也不能作为扩大接单的理由。'],'diagram':diagram,'secondDiagram':second,'sections':sections,'meaning':'比较对象是当前同一订单结构下的人工办法。把初始整理、日常确认、返工、故障接手和工具费用一起看；时间释放、避免增聘与实际工资支出减少分别记录。','unknowns':['两篇主源支持被报道的使用场景，不分离业务转型与AI各自的效果。店主自报不能升级为独立审计。','长期偏好、当日例外和联动核对是作者建议，未取得逐单记录、代码、完整费用或持续准确率。',f'同稿传播及活动回顾只用于来源排除，详见[固定版本来源与判断边界](https://github.com/louiseliu/restaurant-business-lab/blob/{COMMIT}/research/2026-11-05-monthly-meal-customization/sources.md)。未新增Pro或门店实验。'],'actions':['用已获授权的脱敏样本比较有限选项表与辅助整理；简单规则已够用时，不另加一层流程。','在不影响真实出餐的情景中检查“只改今天”和信息不完整的要求，确认员工能追到原始依据。','重复工作减少、确认和返工可接受且后厨与配送仍有余量时再扩大；否则收窄选项或退回人工确认。'],'sources':sources}
entry={'id':ID,'path':PATH,'title':title,'section':'research','topics':['ai','business-model'],'publishedAt':TIME,'updatedAt':TIME,'excerpt':'月餐选择与配送已收敛、反复整理熟客要求成为负担时，可小范围试用AI；先区分长期偏好和当日例外，再核对汇总、标签与实际交付。','body':body,'originalBodySha256':hashlib.sha256(body.encode()).hexdigest(),'sourceUrl':URL,'firstGit':COMMIT}
queries={}
for dg,suffix in [(diagram,''),(second,':second')]:
 q='diagram-'+ID+suffix
 queries[q]={'rows':dg['nodes'],'source':{'label':dg['label'],'files':[PATH],'metricDefinitions':[{'label':'报道、店主自报与作者示意分开','definition':dg['scope']+' '+dg['note'],'componentIds':[q]}],'evidenceFlow':[{'title':'固定公开正文','detail':URL}]+[{'title':s['title'],'detail':s['url']} for s in sources]+[{'title':'图文整理','detail':'依据冻结正文转写为非数值机制图；作者建议不表示具名门店已经上线或通过测试。'}],'caveats':['没有独立经营效果验证，不把自报节省与容量绘为收益图。','原始业务转型与工具使用的贡献未分离。','作者合成验收情景不是实际事故或门店功能说明。']}}
reviewed={'surface':'report','title':title,'generatedAt':TIME,'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries}
if (A/'article-reviewed-data.json').exists():
 old=json.loads((A/'article-reviewed-data.json').read_text())
 if old.get('id'):reviewed['id']=old['id']
 reviewed['buildStatus']=old.get('buildStatus','creating')
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',reviewed)
print(entry['originalBodySha256'],len(sections),'complete narrative sections; 2 scoped diagrams')
