"""Generate a complete article and scoped conceptual diagrams from the frozen public note."""
import hashlib,json,re,sys
from pathlib import Path
A=Path(__file__).resolve().parent;NOTE=Path(sys.argv[1]);META=json.loads(Path(sys.argv[2]).read_text())
body=NOTE.read_text();ID='research-2026-11-05-self-built-release-validation-note';COMMIT=META['commit'];TIME=META['time'];PATH='research/2026-11-05-self-built-release-validation/note.md';URL=f'https://github.com/louiseliu/restaurant-business-lab/blob/{COMMIT}/{PATH}'
assert hashlib.sha256(body.encode()).hexdigest()==META['sha256'],'Input is not the frozen public note'
def write(name,v):(A/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
parts=re.split(r'^## ',body,flags=re.M);title=body.splitlines()[0][2:]
lead='\n\n'.join(parts[0].split('\n\n')[1:]).strip();sections=[]
for p in parts[1:]:
 h,t=p.split('\n',1)
 if h=='研究说明':continue
 sections.append({'title':h,'body':t.strip().split('\n\n')})
base='https://github.com/lofty14/restaurant-digitalization-blueprint/blob/e1df960b1f09cd478e24564c7f698773d32d3050/'
sources=[{'title':'项目README｜主体和资料范围的作者声明','url':base+'README.md'},{'title':'AI产出的质量纪律｜鉴权漏测的项目自述','url':base+'04-ai-engineering/ai-review-discipline.md'},{'title':'部署链路｜旧构建与版本防回退的项目自述','url':base+'01-architecture/deployment.md'},{'title':'机器人体系｜人工审批流程与限定自动修复例外','url':base+'04-ai-engineering/bots-architecture.md'}]
diagram={'kind':'compare','layout':'release-auth','label':'一次权限修复，要同时证明谁能用、谁不能用','scope':'作者合成验收情景，不是案例事故记录或已执行测试。下列权限约定须按本店真实系统替换；总部账号不意味着拥有全部权限。只用隔离环境的专用身份与合成记录。','nodes':[
 {'验收环节':'未登录的匿名者','性质':'示例权限约定','权限约定':'没有访问受限操作的权限。','预期检查':'拒绝受限请求。','谁来解释':'跨入口负责人说明应当拒绝的范围。'},
 {'验收环节':'合法门店A账号','性质':'示例权限约定','权限约定':'有权限完成A店范围内的指定任务。','预期检查':'允许并完成本店任务，确认原问题消失。','谁来解释':'报障人确认原问题；跨入口负责人确认权限范围。'},
 {'验收环节':'合法总部账号','性质':'示例权限约定','权限约定':'只拥有该账号实际获授的操作与数据范围。','预期检查':'按已授权范围允许操作，不推定拥有全部权限。','谁来解释':'跨入口负责人解释授权范围，并核对实际任务结果。'},
 {'验收环节':'门店B账号读取A店限定记录','性质':'示例权限约定','权限约定':'该示例约定B店无权读取A店限定记录。','预期检查':'拒绝这次跨店越权读取。','谁来解释':'跨入口负责人核对不同门店边界。'}
 ],'completion':'不应访问的被拒绝 ＋ 应当访问的能完成操作 → 两类证据共同支持权限验收。报障人确认原问题，跨入口负责人解释其他合法使用与越权边界。','note':'图1｜原创研究示意。S2只支持“漏测正常门店身份”的项目方自述；具体身份矩阵、权限约定和分工均为作者建议。没有独立事故日志、日期、门店范围或损失核验。'}
second={'kind':'flow','layout':'release-chain','label':'批准到运行，要沿同一个发布版本查到底','scope':'作者验收建议：下面四层分别留下可核对的结果。任何一层通过都不能替代下一层；没有执行生产发布或恢复测试。','nodes':[
 {'验收环节':'已运行版本与现有功能','性质':'作者建议 · 起点','核对内容':'先记录当前运行版本，以及这次发布后应当保留的关键功能。','判定边界':'不能只验新修复，却把原来工作的功能退掉。'},
 {'验收环节':'本次源码与改动范围','性质':'作者建议 · 批准对象','核对内容':'确认本次改动对应的源码版本、受影响入口和已获批准的范围。','判定边界':'生成修改不等于获准上线，版本标识也不能单独证明功能正确。'},
 {'验收环节':'最终构建及对应测试','性质':'作者建议 · 不能偷换产物','核对内容':'最终产物包含此前应保留的改动，并与通过测试的内容对应。','判定边界':'测试后若再合入改动或更换构建包，先核对变化，再重验受影响路径。'},
 {'验收环节':'实际入口的版本与关键流程','性质':'作者建议 · 营业端确认','核对内容':'实际入口提供预期版本，相关前后端能配合，由合法身份完成关键任务。','判定边界':'部署回执不能代替门店可用；恢复有人接手，才考虑扩大同类自动放行。'},
 {'验收环节':'S2：鉴权漏测','性质':'同一项目自述 · 不是测试结果','核对内容':'只验证未登录请求被拒，遗漏门店独立登录态，正常使用者受阻。','判定边界':'没有独立日志、发生日期、影响门店或损失核验。'},
 {'验收环节':'S4：旧构建覆盖','性质':'同一项目自述 · 不同事故','核对内容':'旧源码构建包覆盖较新入口，已上线的改动退回，部署表面成功。','判定边界':'固定版本的防回退只告警、不强制拦截；与S2不拼成一次事故。'}
 ],'completion':'测试后又合入改动／更换构建包 → 返回核对变化，并重验受影响路径。证据完整、原有功能保留且恢复有人接手，再扩大同类放行；否则维持人工放行并收窄范围。','note':'图2｜原创研究示意。四层主线与重新验收条件为作者建议，下方两则自述均来自同一项目，不是独立佐证。机器人页新增限定免确认路径，但首次真实触发仍在观察，不画成成熟的自动发布闭环。'}
story={'id':ID,'headline':title,'lead':lead,'findings':['反复的小改动确实积压，且有人能覆盖各端验收和异常接手，才值得逐步扩大AI辅助改码。','鉴权修改要同时确认不该进的人被拒、该办的事仍能办；生成、测试、构建、发布和当班可用分开判断。','比较到“确认可用”为止的总投入，计入审核、返工、版本核对和支持，不能只看订阅或服务器。'],'diagram':diagram,'secondDiagram':second,'sections':sections,'meaning':'技术负责人和门店验收人员可以协作，但报障人确认自己的问题已修好，不等于全部受影响入口已经通过。低频需求、缺少持续维护责任时，稳定软件加人工补充可能更合适；有技术接手和重复需求的小连锁才适合逐步试。','unknowns':['公开蓝图自称由原串技术团队维护，本研究没有独立确认维护者身份、实际部署范围或当前运行状态。','四页均属同一项目来源链。没有产品源码、独立事故日志、完整费用或经营收益证据，不能以多个页面当多份独立佐证。',f'自动修复真实触发仍待观察。未新增Pro、产品调用、门店实测或收益计算。详见[固定版本来源与证据边界]({URL.replace("note.md","sources.md")})。'],'actions':['在非生产环境挑一个低影响改动，列清受影响入口、通过条件、上线批准人与异常接手人。','记录从提出需求到确认可用的总时间、返工和支持负担，检查实际版本及原先正常的任务。','完整任务可稳定通过且有人接手时再扩大；无人解释版本或反复靠临时救火时，先收窄自动上线范围。'],'sources':sources}
entry={'id':ID,'path':PATH,'title':title,'section':'research','topics':['ai','business-model'],'publishedAt':TIME,'updatedAt':TIME,'excerpt':'AI改码提速后，跨端登录、构建版本和实际营业流程仍需分别验收。以一个公开项目的失败自述，讨论小连锁何时值得自建、何时应限制自动上线。','body':body,'originalBodySha256':hashlib.sha256(body.encode()).hexdigest(),'sourceUrl':URL,'firstGit':COMMIT}
queries={}
for dg,suffix,refs in [(diagram,'',[sources[0],sources[1]]),(second,':second',[sources[1],sources[2],sources[3]])]:
 q='diagram-'+ID+suffix
 queries[q]={'rows':dg['nodes'],'source':{'label':dg['label'],'files':[PATH],'metricDefinitions':[{'label':'作者发版验收建议与同源自述边界','definition':dg['scope']+' '+dg['note'],'componentIds':[q]}],'evidenceFlow':[{'title':'固定公开正文','detail':URL}]+[{'title':s['title'],'detail':s['url']} for s in refs]+[{'title':'图文整理','detail':'将固定正文整理为非数值验收示意；项目自述只支持机制线索，建议不表示已完成测试。'}],'caveats':['来源均为同一项目自述，不是独立事故调查或效果验证。','身份、实际部署规模、完整成本与经营收益未独立确认。','生成改动、测试、构建、发布与实际任务可用不相互替代。','新自动修复首次真实触发仍待观察，不能称成熟无人发布。']}}
reviewed={'surface':'report','title':title,'generatedAt':TIME,'status':'reviewed','buildStatus':'creating','exportPreferences':{'selected':None,'destinations':[]},'filters':[],'report':{'asOf':'2026-11-05'},'queries':queries}
write('article-entry.json',entry);write('illustrated-story.json',story);write('article-reviewed-data.json',reviewed)
print(entry['originalBodySha256'],len(sections),'complete narrative sections; 2 scoped diagrams')
