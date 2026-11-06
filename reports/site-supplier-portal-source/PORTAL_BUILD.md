# AI选址与供应商推荐：71篇本地门户

本目录是在可读69篇本地门户上追加第70、71篇的小型增量作者源与核验记录，不是完整历史镜像。既有正文、图文、数据、用户编辑、运行时和两份已接受附件请求的作者输入不被覆盖。不可读原站的编辑与历史未恢复、未验证。

## 输入与复建

在供应商研究状态提交完成后读取main `aca97b01e6a98cd24ba8c4dd633a38ca154f2b00`、仓库AGENTS、研究Skill、历史current与 `state/2026-11-06-portal69.json`。核验上一轮24项门户小型源与最新树blob一致，四份研究正文/来源在该head远端逐字回读与本地一致。完整69篇基线重跑保留检查；363项指纹见baseline69-sha256.json。

两个相邻输入目录为 `../site-selection-source` 与 `../supplier-recommendation-source`。20项真实合并输入含选址计算脚本与结果，见input-fingerprints.json。选址首提 `c905ca1df6c8587d76b5f7e66dae7c57d5a342ce`，真实时间 `2026-11-06T05:15:46Z`；供应商首提 `1496fce49b261cb108102b83dec501cea82cd5b4`，真实时间 `2026-11-06T05:23:47Z`。不把构建时间写成研究首提或来源发布日期。

需要完整、指纹相符的69篇本地门户、两份作者源、Python 3、Node与兼容官方Data工具。仅本目录不能复原未收录的历史大文件、样板或运行时。

1. 将本目录复制至新建 `PRODUCTION_DIR/portal-archive-source`。
2. 运行 `python portal-archive-source/prepare_portal.py PRODUCTION_DIR BASELINE69`。目标须不存在；先校验所有指纹，再复制到baseline69和portal71，不改输入。
3. 运行 `python portal-archive-source/build_portal.py PRODUCTION_DIR SITE_SELECTION_SOURCE SUPPLIER_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR`。脱敏目录可用任一单篇support。
4. 全部输入、冲突、reader锚点检查先通过才写入。只新增两篇、四项query及六个作者图示/来源预览文件；五个旧文件作必要增量：articles.json、illustrated-stories.json、data.json、IllustratedArticle.jsx、ReportContent.jsx。不得把单篇reader覆盖到门户。
5. 冻结正文、图文、查询与分类标签不改。只对选址新ID添加AI与business-model分类兼容，并在列表和文章主题标签保持一致。原始AI标签47篇、有效AI筛选48篇分别记载。它是主题分类，不是已验证AI成效；旧文章筛选行为保持。
6. 两篇相对Markdown链接在渲染时解析至各自固定Git首提，涵盖sources.md和选址计算文件。只对新选址继承单篇的article `zh-CN`，供应商沿用原单篇根语言继承；旧语言属性保持。新篇台账前解释“未提交”等为历史文字，不改冻结台账。
7. 只读脱敏检查后设buildStatus=complete，执行官方prepare、build --separate-data、export-offline。构建子进程去除可选会话标记；成品原字节复制为timeline71-site-supplier.html，不编辑编译HTML。

## 核验结果

本地成品为 **71研究/91全文/71图文/2样板、有效AI48、146项queries**。原始AI标签为47篇，新增选址仅有明确记录的界面分类适配。HTML **14,180,136字节**，SHA256 `8054f693f8cf9bcaa2206eb964262f3e0384fd6e055be63e8b7e131cc81e7d06`，未上传、发送或Git归档。

- 原89全文、69图文、142 queries逐对象保持，358项无需变更文件与363项基线指纹复核通过。选址六节、供应商七节的完整原文与来源台账、四图及真实首提保持。
- 35项合并保护：正文、摘要、图文、query、两个reader注释和导出偏好保留；重复整合、身份、数量、query、文件/符号链接、reader锚点冲突及20项冻结输入字节变更都在写入前拒绝。测试只用一次性副本。
- 主检查扫描199项文本载荷，核5项下载、2个递归ZIP、release manifest、编译JSON与分离数据/manifest。实际路由和分类/链接辅助函数665项检查通过；不代表浏览器历史或点击验收。
- 选址模拟逐行复算得到+2,400、−960、−1,500元/月，均为作者假设，87%没有进入计算。供应商两图分别绑定S1与作者方法，不以Sysco补证恒天然或中国小店效果。
- 全新无dist、缓存或node_modules目录按官方流程复建，HTML逐字一致；八项执行输入逐字相同。两单篇静态、各8项防覆盖与各3项脱敏单测重跑通过，原作者源及成品未改。
- 独立审计结果及脚本见independent-audit；它独立核验产物，不代替联网研究或浏览器测试。

**旧全项目运行时校验限制：** 在69篇基线和71篇新产物直接运行自带的 `scripts/verify-protected-runtime.mjs`，均因 `.openai/hosting.json` 与旧清单差异失败；两个配置逐字相同，非本次新增变更。当前官方installed/prebuilt流程的作者边界检查、构建与离线导出通过。没有修改保护文件或完整性清单来消除旧差异，不把旧全项目校验写成通过。

两份单篇附件发送请求于 **2026-11-06T05:27:03Z** 被接受，未确认送达、打开或下载。成品身份见相邻输入的delivery-status.json。此次没有重发、替换旧附件或发送门户。

## 未验收与保留事项

浏览器桌面/窄屏、深浅主题、实际图形、来源面板、点击/历史/滚动、编辑持久化、下载点击、打印、真实断网、浏览器日志与屏幕阅读器未验。既有HTTP/file/原站限制未重试、换路、重托管或改权限；静态与复建不能替代浏览器验收。没有重新联网查证来源或复算历史样板的业务计算。

原站未同步、当前可读性未复核，只沿用最后核验v19的20研究/40全文/2样板、AI9。第21—71篇51项新增与三项既有同ID修订，共 **54项待同步**。旧Fourth共享S2标题缺第19页展示问题保留。历史四项未确认审计写入及一项同字节JSON继续开放，见baseline-known-gaps.json，未重试、改名同内容上传或换接口。

HTML归档、门户附件、旧附件替换、费用原归档、原站编辑保护、旧全站离线快照与既有视觉待办独立保留。只归档小型公开作者输入、真实状态与QA，不提交HTML/ZIP、缓存、完整运行时、私人路径/会话/交付标识或凭据。README.md与state/current.md保持原字节，仍为历史快照；当前小型状态见 ../../state/2026-11-06-portal71.json。
