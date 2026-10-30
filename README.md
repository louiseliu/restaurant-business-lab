# 餐饮商业模式研究院

以可验证证据推进餐饮商业问题研究，持续维护研究成果、商业分析方法、研究记录与 `restaurant-business-model-lab` Skill。

## 研究重点

在餐饮商业模式研究之外，重点增加 **AI 在餐饮中的实际应用**：优先核验真实使用场景、实施与持续运营成本、经营效果及可复制条件。区分供应商宣称、试点结果与独立验证；普通自动化、广告实验或流程优化不因新方向而改标为 AI，不补造尚无证据的文章。

## 当前状态

初始化日期：2026-10-27。

- 已接收并检查上传的 Skill v0.3：仅含四个 Markdown 文件，无可执行脚本、二进制或依赖。
- 仓库级 Skill 位于 [`.agents/skills/restaurant-business-model-lab/`](.agents/skills/restaurant-business-model-lab/SKILL.md)。这是版本化的项目配置，不等同于宿主全局注册或已启动后台进程。
- 首次实际研究已由通用口径边界推进到[蜜雪商品收入与加盟网络店日的条件性检验](research/2026-10-27-franchise-evidence/final-report.md)：构造指标至少下降约 4.55%，不能推断终端需求或加盟商利润下降。
- 两轮真实 Pro 回复、公开原始资料回查、独立计算和措辞纠错已完成，详见[协作记录](research/2026-10-27-franchise-evidence/pro-collaboration.md)与[判断修订](research/2026-10-27-franchise-evidence/judgment-revision.md)。[最终研究提交](https://github.com/louiseliu/restaurant-business-lab/commit/e855c67e53e80165f968efed9ef7ba91029cdc1a)已在远端核验。
- [老板版图文 HTML 归档提交](https://github.com/louiseliu/restaurant-business-lab/commit/b9150cb2369b2d6add851a112ae5256b4b43cfb1)已在远端核验，原研究与离线报告均保留。
- 2026-10-28 首次每日早间定时研究已实际执行（Asia/Shanghai）：完成蜜雪证据缺口的有界复查，以及[古茗盈亏平衡与加盟回本口径研究](research/2026-10-28-franchise-payback-definitions/research-note.md)。这是历史招股书核验，不是当天新闻；本轮没有新的 Pro 请求或回复。
- 按用户要求，研究检查现已改为每小时；2026-10-28 05:00 UTC（上海时间 13:00）的首轮小时研究已实际执行，完成[古茗后续加盟商人数桥与留存辨识核验](research/2026-10-28-franchise-payback-definitions/continuation-note.md)。本轮未新增 Pro 请求或回复。
- 按证据价值和可用额度选择 Pro，不是 24 小时后台进程。首次执行不等于未来每次运行均已验证。没有新增付费资源。

## 工作原则

1. 先提出值得解决的商业问题，再按证据选择调查、计算、Pro 协作和验证动作，不机械套用固定流程。
2. 事实、计算、假设和建议分开记录；公开原始资料优先，重复转载不算独立证据。
3. 总部收入、利润、终端交易额与加盟商单店收益分别分析，不能相互替代。
4. Pro 是共同思考伙伴，其回答不是事实证明。核验来源和计算，并保留分歧与判断修订。
5. 外部操作只在明确授权范围内进行；本公开仓库不得存放凭据、私有经营资料或个人敏感信息。

## 全文与图文时间线

原站已升级为文章时间线：10 篇研究均有独立图文读本（每篇至少两幅有信息价值的图），同时保留 30 份 Markdown 全文、方法及历史记录和原蜜雪老板版。当前原站研究内容基准已增量更新至 `5c14b9b034b8ecab34fbae4c38523126b0c4cb6c`；按首次 Git 提交时间倒序、显示北京时间，不冒充来源发布日期。

[下载公共安全图文 HTML](reports/restaurant-illustrated-public/restaurant-research-illustrated.html)，用启用 JavaScript 的现代浏览器打开；无需外部 CDN。[作者源码与维护流程](reports/restaurant-illustrated-public/source-final/BUILD.md)。这是静态同步，不是实时抓取，不新增定时任务；AI 专题已有首篇[食物减损机制研究](research/2026-10-29-ai-food-waste/note.md)，[独立离线图文](research/2026-10-29-ai-food-waste/report.html)与[作者增量源](reports/ai-food-waste-site-source/BUILD.md)已归档；原站 v6 已发布验收。后续研究须先核验证据，再制作逐篇图文与来源/未知/行动说明，不能用装饰图或虚构数字替代分析。

公共导出将私人协作链接替换为“私人协作会话，未公开”，不改写既有仓库历史。原文字段 `originalBodySha256` 仅标识脱敏前来源；[脱敏正文校验清单](reports/restaurant-illustrated-public/rendered-article-manifest.json)另记录导出正文哈希，不能将两者混同。已做桌面与窄屏浏览器检查，未宣称 iPhone 真机或打印实测。

## 实战样板（研究者示范，非经营成效实测）

- [外卖活动条件计算器](tools/delivery-campaign/README.md)：可离线替换假设、查看贡献情景；默认值仅演示，活动归因订单不自动等于增量。
- [AI 辅助经营周报](examples/ai-weekly-report/README.md)：完整模拟输入、实际执行的 Python 清洗/分析、AI 辅助文稿及逐记录追溯；不是客户实测，没有外部模型 API、真实数据上传或节时/准确率收益测量。
- [站内样板承载源码与复建说明](reports/samples-site-source/BUILD.md)：从本仓库相对路径读取已核验 HTML/ZIP，检查哈希后生成站内载荷，不自动发布。

两个样板可在原站阅读并下载各自完整包，单独计为示范，不增加 10 篇研究的计数。样板包中的“local-only／未发布”描述保留其制作冻结时状态；当前公开归档以提交历史为准。此前整站离线 HTML 仍是 **v4 固定快照**，不含 v5 样板入口或 v6 新文章；后续分别归档两份独立样板、可复建承载源及新文章独立 HTML/增量源，不声称另有最新整站离线包。v5 的连接与发布仍须官方 Data runtime 和实际验收。

新增第 10 篇 [AI 加购研究](research/2026-10-29-ai-cart-recommendations/note.md)，附[独立离线图文](research/2026-10-29-ai-cart-recommendations/report.html)与[作者增量源](reports/ai-cart-site-source/BUILD.md)。原站 v8 已发布并验收，10 篇研究/30 份全文/2 项样板，保留 v7 阅读体验。历史平台 A/B 是作者报告，不是本项目门店实测；不能将客单提升视为小店利润提升。当前更新是静态增量，不是自动同步；旧 v4 整站离线 HTML 快照保持不变，也不含本篇。

## 阅读界面维护

原站 v7 阅读体验更新已发布并验收：研究、实战样板、全部资料分区；搜索与主题筛选、文章目录、邻篇导航、返回列表和浏览器前进/后退状态恢复。正式站核验了 AI＋厨房筛选及返回查询状态，保留 9 篇研究、29 份全文、2 项样板与原访问范围。

[UI/UX 作者源与路由测试](reports/restaurant-ux-source/BUILD.md)仅为界面增量，依赖既有 Data runtime 与现有正文/样板数据；不自动发布。原文事实、数据与既有独立/整站 HTML 快照均未追溯改写，不把源码测试当成手机真机验证。

## 目录

- [给餐饮老板的图文 HTML 报告](reports/README.md)：下载后浏览器打开，含图解、经营问题与证据边界。

- [Skill 与参考文件](.agents/skills/restaurant-business-model-lab/SKILL.md)
- [研究规范](methods/research-standard.md)
- [来源发现方法与16主体扩充登记](methods/source-discovery.md)：中文中小餐饮与AI线索，逐项标明本轮可读范围、利益和证据边界。
- [当前进度](state/current.md)
- [研究日志](logs/2026-10-27-initialization.md)
- [本轮研究结论](research/2026-10-27-franchise-evidence/final-report.md)：条件性边界结果、反例、经营意义与未解问题。
- [原始初查稿](research/2026-10-27-franchise-evidence/provisional-research.md)：历史初始判断，保留其写作时状态；不要将其中尚未咨询的描述当作当前状态。
- [独立边界复核](research/2026-10-27-franchise-evidence/bounds-check-findings.md)、[来源补充](research/2026-10-27-franchise-evidence/source-additions.json)、[可运行代码](research/2026-10-27-franchise-evidence/bounds-check.py)。

## 首次闭环验收

必须能够提供：真实研究问题与来源、实际执行的验证、真实 GPT Pro 模型及会话使用证据、因核验而保留或修订的判断，以及已在远端核实的 GitHub 提交。任一环节未完成都应明确标注，不以计划或模拟代替成功。

## 使用 Skill

将仓库的 `.agents/skills/restaurant-business-model-lab/` 作为项目级 Skill 交给支持相应目录约定的宿主；应以宿主实际发现结果为准。本文件不承诺跨宿主自动加载。需要全局安装时，使用宿主支持的安装方式，并另外核验发现结果。





