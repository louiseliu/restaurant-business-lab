"""Build a full narrative and two reviewed, non-numeric diagrams from a frozen note."""
import hashlib,json,re,sys
from pathlib import Path
A=Path(__file__).resolve().parent; NOTE=Path(sys.argv[1]); META=json.loads(Path(sys.argv[2]).read_text())
body=NOTE.read_text();ID='research-2026-11-05-model-update-acceptance-note';COMMIT=META['commit'];TIME=META['time'];PATH='research/2026-11-05-model-update-acceptance/note.md';URL=f'https://github.com/louiseliu/restaurant-business-lab/blob/{COMMIT}/{PATH}'
assert hashlib.sha256(body.encode()).hexdigest()==META['sha256'],'Input is not the frozen public note'
def write(name,v):(A/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:]
intro=parts[0].split('\n\n')[1:];lead='\n\n'.join(intro).strip()
sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1)
 if h=='研究说明':continue
 sections.append({'title':h,'body':t.strip().split('\n\n')})
sources=[{'title':'虎嗅访百胜中国CTO张雷｜凤凰网署名转载（2026-08-29）','url':'https://tech.ifeng.com/c/8vzHZXKo5Jc'}, {'title':'阿里云 qwen-plus｜本轮可读动态更新说明','url':'https://help.aliyun.com/zh/model-studio/qwen-plus'}, {'title':'阿里云｜2025-06-15模型更新历史公告','url':'https://www.alibabacloud.com/zh/notice/model_studio_update_of_qwenplusturbo_4f8?_p_lc=1'}]
diagram={'kind':'flow','layout':'model-comparison','label':'换了模型，仍用同一份任务基准比较','scope':'作者验收建议：现行规则、同组问题和处理边界保持一致，再比较现用方式或已留存基准与候选方式。图中没有实测结果，也不是百胜或阿里云的部署图。','nodes':[
 {'环节':'固定本店任务基准','性质':'比较前保持一致','规则依据':'使用同一份现行营业或活动规则，记录当时适用的范围。','问题样本':'常见问法与关键例外都保留，例如缺少门店、问到已结束活动或规则外要求。','处理边界':'先写清哪些条件必须保留，何时应追问、转人或停止自动动作。'},
 {'环节':'对照候选方式与可用基准','性质':'新旧面对同样输入','现用方式或留存基准':'保留回答、依据与准备执行的动作；旧版不能重跑时，用既有记录或业务基准核对。','候选方式':'在合成材料、模拟环境或已获授权的非营业样本中检查，不把真实顾客用作升级试验。','比较前提':'留存记录不等于同期对照；缺少历史记录时，不能声称测得新旧差异。规则、提示词与模型同时变化也会影响判断。'},
 {'环节':'由业务判定完整任务','性质':'通了接口还要看结果','关键条件':'检查必要限制是否保留，信息不足时能否追问或按约定转人。','动作与授权':'涉及工具时，连同准备执行的动作和授权边界一起核对。','继续或收窄':'完整任务与维护负担可承受再扩大；反复依赖人工解释时，先缩小自动处理范围。'}
 ],'note':'图1｜原创研究示意，未执行测试。百胜访谈只说明使用方反复评测的做法；qwen-plus-latest文档只说明特定动态版本的更新机制。两者不是同一项目证据，不支持推定百胜使用该托管接口。'}
second={'kind':'flow','layout':'model-recovery','label':'旧版不能继续用时，也要有人接住任务','scope':'作者恢复建议：先限制受影响的自动处理，再判断旧版是否可用且应用能切换。下面两种条件分支不是已经核实的产品能力，也不是实际事故还原。','nodes':[
 {'环节':'发现关键条件不再满足','性质':'先控制受影响的任务范围','技术维护':'记录变化、重复测试并检查适配；确认问题影响哪一段处理。','业务判定':'由懂经营规则的人判断是否还能接受，必要时限制相关自动动作。'},
 {'环节':'旧版可用，应用也能切换','性质':'条件分支 A：两项都成立','处理办法':'复核后再切换，并重新确认任务结果；不能只凭调用成功宣布恢复。','负责人员':'技术维护者负责切换与适配，业务负责人判定可否继续。'},
 {'环节':'旧版不可用，或应用不能切换','性质':'条件分支 B：任一项不成立','处理办法':'按业务容忍度转人工、人工确认后发送，或暂停相关自动动作。','负责人员':'当班人员知道接手办法及联系人；原搭建者不在时仍能处理。'},
 {'环节':'先前已经产生的事项，单独核对','性质':'与恢复后续处理并行','另查旧事项':'检查哪些回复或动作需要解释、纠正或继续跟进。模型切换不会自动撤回这些结果。','人员安排':'技术维护、业务判定和当班接手可以由一人承担，也可以由服务方与店长分担。'}
 ],'note':'图2｜原创研究示意。2025年公告只提供“快照并非永久保留”的历史边界，不证明任何旧版今天仍可调用。分支和分工属于作者建议，本文未演练恢复、测量响应时限或验证平台撤回能力。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['持续复测和临时接手有人负责，才值得逐步扩大自动处理范围。','动态版本、可安排的切换与固定快照，分别对应不同维护工作；不能只靠一次上线验收。','把初始搭建、日常抽查、升级复测、适配和异常接手放在一起比较，不只看调用单价。'],'diagram':diagram,'secondDiagram':second,'sections':sections,'meaning':'频繁重复、范围稳定的任务，可能值得由持续服务方承接维护；低频草稿本来就逐份人工阅读时，轻量人工确认可能更省事。费用比较要包括复测与接手，不能把工时变化直接换算为工资节省。','unknowns':['百胜高管自述未提供评测样本、通过标准、维护费用或独立结果，也没有证明某次升级发生故障。','两份阿里云资料同属供应商来源链；当前latest机制与2025年历史迁移安排不能混用，更不能当作百胜部署证据。',f'未核验当前旧快照可用性、合同报价或小店结果。未新增Pro、产品调用、门店实测或收益计算。详见[固定版本来源与证据边界]({URL.replace("note.md","sources.md")})。'],'actions':['先选一个低风险、重复较多的任务，写清变更记录、业务通过判定和当班接手各由谁负责。','用同一组非敏感样本比较，并模拟版本不能继续使用时的接手；观察完整任务质量、复核负担与恢复过程。','关键条件保持、例外可转人且总负担可承受时再扩大；否则收窄范围。稳定服务能证明维护完成时，也不必仅因会升级就放弃使用。'],'sources':sources}
entry={'id':ID,'path':PATH,'title':title,'section':'research','topics':['ai','business-model'],'publishedAt':TIME,'updatedAt':TIME,'excerpt':'模型升级后，首次验收不会自动延续。把版本记录、完整任务复测和无法回退时的当班接手分清，才能比较AI的持续维护负担。','body':body,'originalBodySha256':hashlib.sha256(body.encode()).hexdigest(),'sourceUrl':URL,'firstGit':COMMIT}
queries={}
for dg,suffix,refs in [(diagram,'',sources[:2]),(second,':second',[sources[2]])]:
 q='diagram-'+ID+suffix
 queries[q]={'rows':dg['nodes'],'source':{'label':dg['label'],'files':[PATH],'metricDefinitions':[{'label':'作者复测与接手建议','definition':dg['scope']+' '+dg['note'],'componentIds':[q]}],'evidenceFlow':[{'title':'固定公开正文','detail':URL}]+[{'title':s['title'],'detail':s['url']} for s in refs]+[{'title':'图文整理','detail':'依据冻结正文转写为非数值机制图；建议、合成情景与具名主体的已披露做法分开。'}],'caveats':['百胜与阿里云不是同一部署证据，未确认百胜使用所述托管接口。','未运行产品测试、恢复演练或收益测算。','历史快照提示不证明旧版本今天仍可用。']}}
reviewed={'surface':'report','title':title,'generatedAt':TIME,'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries}
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',reviewed)
print(entry['originalBodySha256'],len(sections),'complete narrative sections; 2 scoped diagrams')
