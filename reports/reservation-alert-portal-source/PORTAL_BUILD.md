# 订座订金与外卖来单提醒：73篇本地门户

这是从可读71篇本地门户追加第72、73篇的小型增量作者源、保护测试与真实QA，不是完整历史镜像。旧正文、图文、数据、用户编辑、下载和运行时保留；不可读原站的编辑与历史未恢复、未验证。研究原稿与已接受附件请求的单篇作者源、成品均不改写。

## 输入与复建

开始读取最新main `1a22b1142a3265d25f504f3fcccb44bd471fc6de`、仓库AGENTS、餐饮研究Skill、历史current及 `state/2026-11-06-portal71.json`。上一轮22项本地门户小源码与该head的Git树blob匹配；本轮四份正文/来源远端逐字回读一致，首次Git对象的author和committer时间另核。

- 订座首提 `fdb6fd9e3c9e34d4afc772a14bd82dc8e6a8d349`，`2026-11-06T06:16:18Z`。
- 来单提醒首提 `40d7d709015ed753668b52e22c0dd8d49ff96db9`，`2026-11-06T06:20:11Z`。

排序依据首入库时间，不用构建时间代替首提或来源发布日期。订座原标签ai/business；来单提醒原标签operations，不算AI。旧选址ID的界面分类适配保持，原始AI标签48、有效AI筛选49分别记载，不表示已验证AI收益。

完整复建需要369项指纹匹配的71篇本地门户、相邻 `../reservation-policy-source` 与 `../order-alert-source`、Python 3、Node和兼容官方Data工具。仅此小目录不能复原未收录的历史大文件、样板或运行时。

1. 复制本目录为新建 `PRODUCTION_DIR/portal-archive-source`。
2. 执行 `python portal-archive-source/prepare_portal.py PRODUCTION_DIR BASELINE71`。新目标必须不存在；先校验所有基线指纹，再复制baseline71与portal73，不改输入。
3. 执行 `python portal-archive-source/build_portal.py PRODUCTION_DIR RESERVATION_SOURCE ORDER_ALERT_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR`。脱敏目录可用单篇support。
4. 18项冻结输入、数量/身份/query/文件/符号链接冲突、reader锚点全部通过才写入。只新增两篇、5项query与6个组件/样式/预览文件。4个既有文件必要增量为articles.json、illustrated-stories.json、data.json和IllustratedArticle.jsx；ReportContent.jsx原字节保持，不用单篇reader覆盖门户。
5. 完整七节订座与六节来单正文、三图与两图保持。只在新篇渲染层解析相对链接至固定Git首提、继承单篇zh-CN及新增历史台账说明，不改冻结文字。订座第三图沿用旧reader既有第三图分支。
6. 脱敏只读检查后将buildStatus设为complete，官方prepare、build --separate-data、export-offline。构建子进程不带可选会话标记；成品原字节复制为timeline73-reservation-alert.html，不手改编译HTML。

## 已完成核验

本地成品为 **73研究/93全文/73图文/2样板、有效AI49、151项query**。HTML **14,298,346字节**，SHA256 `e8fa0bf3c02d52ff25df61dafef0950dfe880de4ba6b17b7b22d4b40b270038b`，只留本地，未上传、发送或Git归档。

- 原91全文、71图文、146项query逐对象不变，365项无需修改文件及369项基线指纹复核通过。ReportContent、Legacy、保护文件和清单保持。
- 33项合并保护：正文、摘要、图文、query、两个reader注释及导出偏好保留；重复整合、数量、身份、query、文件/符号链接、reader锚点冲突及18项冻结输入变化均在写入前拒绝。测试用一次性副本。
- 主检查207项文本载荷、5下载、2个递归ZIP及release manifest、编译JSON、拆分数据/manifest通过；666项实际JavaScript路由/分类/相对链接辅助函数通过。它们不是浏览器点击或历史验收。
- 两单篇静态、各8项防覆盖和各3项脱敏单测重跑通过。60项原作者源和HTML文件指纹保持。冻结四稿远端回读与首提时间再核通过。
- 独立审计、干净复建及其限制见independent-audit。复建必须是无dist、缓存和node_modules的新目录，使用同一准备身份与冻结输入；全新准备身份的HTML不保证相同。

**继承的旧全项目运行时限制：** 上轮71篇及其基线的旧自带完整校验已在未变 `.openai/hosting.json` 配置失败。本轮逐字保持hosting、保护文件和完整性清单，没有重试旧失败校验或修改清单消除差异。当前官方installed/prebuilt作者边界、构建与离线导出通过，不称“全量运行时验证通过”。

两份单篇附件发送请求于 **2026-11-06T06:24:20Z** 被接受，不等于送达、打开或下载。版本身份见相邻单篇delivery-status.json。本轮没有重发、替换旧附件或发送完整门户。早先单篇QA中的“门户未整合”是当时状态，完整历史文字保留。

## 未验收与保留事项

浏览器桌面/窄屏、深浅主题、图形实际呈现、目录/全文展开/来源面板、历史/滚动、编辑持久化、下载点击、打印、真实断网、日志和屏幕阅读器未验。既有HTTP/file/原站限制未重试、换路、重托管或改权限；静态、构建与复建不能替代浏览器验收。本轮未联网重查来源、重新计算历史样板业务数据或进行门店实验。

原站未同步，当前可读性未复核，只沿用最后核验v19的20研究/40全文/2样板、AI9。第21—73篇53项新增及3项既有同ID修订，共 **56项待同步**。旧Fourth共享S2标题缺第19页展示问题保留。历史4项未确认审计写入及1项同字节JSON继续开放，见baseline-known-gaps.json；未重试、改名同内容上传或换接口。

HTML归档、门户附件、历史附件替换、费用原归档、原站编辑保护、旧全站离线快照和既有视觉待办独立保留。只归档公开小型作者源、状态和QA，不提交HTML/ZIP、缓存、完整运行时、私人路径/会话/交付标识或凭据。README.md与state/current.md原字节保持，仍为历史快照；新状态为 `../../state/2026-11-06-portal73.json`。

## 本轮远端归档范围收窄

完整运行时路径/摘要清单不纳入本轮公开小型归档：两份单篇 `standalone-prepared-sha256.json` 以及本目录 `baseline71-sha256.json` 仅保留本地。第一份摘要创建被拒后未重试，也不以其他路径、等价内容或接口上传。其他两份同类清单未尝试上传。参见 `archive-scope-limits.json`。

上述清单实际用于本地保护验证，全部本地检查与独立复建结果仍有效。远端小型归档**不是自足验证包**：门户prepare与完整保留测试还需本地保留的369项基线摘要；已准备单篇的保护测试还需其本地准备摘要。单篇全新官方准备流程可在本地生成新的准备摘要，但不等于恢复本轮报告身份。订座原作者manifest因引用被排除的摘要清单，也仅留本地，不作等价路径上传。原作者源未改写；本次实际范围以archive-manifest.json为准。没有声称仅从这次远端归档可逐字复原整站或已交付单篇。
