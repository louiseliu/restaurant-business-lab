# 模型升级后谁复测：独立图文与第46篇门户增量

冻结正文提交 `ead32eeaa3cb4204bb266554fcf86b956d42d8d9`，首次入库时间 `2026-11-05T06:08:35Z`，正文SHA256 `fcea1d375fbfd83abe58446d3fa275a0b804841bd783285a0d0265010590d33e`。文章ID为 `research-2026-11-05-model-update-acceptance-note`。

本篇讨论上线之后的版本记录、场景复测和接手责任。保留五节完整论证及冻结原文。图一是同一任务基准下的比较建议，旧版不能重跑时，历史记录不当作同期对照；图二区分可切换、不可切换以及先前事项另查。两图均为作者研究示意，不是产品实测、部署图、事故还原或费用测算。

## 证据边界

- 百胜高管访谈支持使用方反复评测的自述，不证明升级事故、维护费用或独立效果。
- 阿里云当前qwen-plus-latest动态更新说明与2025年主干迁移公告分别解释特定调用版本和历史安排。两份资料同属供应商来源链。
- 百胜与上述托管接口不是同一部署证据。历史公告不证明今天任何旧快照仍能调用。
- 复测样本、分工、恢复分支与活动问答是作者建议或合成情景，未开展产品调用、门店测试或新Pro咨询。

## 基线与保护

第45篇门户从可读22篇工程及固定公开小源恢复，包含菜品图、排班同ID修订、盘点第三图和reader修订。其44篇中间工程291项文件SHA256与上轮归档清单全部一致；第45篇完整HTML为13,032,425字节、SHA256 `bcc4fd1f300c31b0ef216804cc9af5ca9b00191fe340b89445a93844fa96e5b7`，与上轮最终归档回执完全一致。此核验恢复的是已归档版本，不证明更早未归档编辑存在或已恢复。

以该45篇工程作为本轮唯一保护基线，在隔离副本运行 `python integrate46.py PORTAL_SRC ARTICLE_SOURCE`。写入前校验45/65/2、AI28、93项query、新ID无冲突、全文hash及两图节点与query一致。只追加一篇、两项query、专用组件和样式，在原完整reader增加导入与布局分支；原文来源链接只为本篇扩展为固定提交URL，保留前篇同样行为。没有用单篇reader覆盖门户。

旧65份全文、45篇图文、93项query逐对象不变；289个非必要变更文件逐字不变，含既有下载、样板、代码和受保护运行时。门户身份、既有标题及主题不变。

## 独立文章与官方构建

1. 用 `python make_article.py NOTE_MD frozen.json` 从固定正文生成作者JSON。该命令检查正文SHA256，不推断首次入库时间。
2. 用当前官方Data `prepare-data-app.mjs --surface report --output NEW_PROJECT --snapshot article-reviewed-data.json` 创建独立文章身份，读取输出AGENTS和返回的组件文档。执行 `python prepare_standalone.py NEW_PROJECT` 安装作者内容。不得覆盖旧门户或已修改的单篇。
3. 两图各有稳定queryId、source.metricDefinitions作用域、完整来源流程；reviewed rows是扁平中文字符串列，来源预览不依赖嵌套对象。图中文字只读，正文和作者说明用RichNarrative。
4. 构建前运行公开脱敏脚本及`--check`。本轮两工程均未发现需要改写的载荷，全局脱敏回归测试通过。
5. 对两工程运行官方 `data-app.mjs prepare --project-dir PROJECT` 和 `build --project-dir PROJECT --separate-data`。只使用官方预编译runtime，不编辑受保护文件，不安装替代依赖。
6. 用官方 `export-offline` 导出至各工程 `.data-app-offline/exports/`，再复制为完整交付文件。本轮副本仅清除可选本地线程meta；split HTML单独不是完整离线交付。
7. 内容与静态检查完成后，两套buildStatus置为complete，重新构建、导出并重跑检查。独立浏览器验收另记，不能由静态成功推断。

## 可复核检查

运行 `python test_preservation.py WORK_ROOT BASELINE45 NOTE_MD`。将本目录的`baseline45-sha256.json`放至WORK_ROOT并命名为`baseline-sha256.json`，将单篇首次官方prepare后的指纹保留为`standalone-prepared-sha256.json`。测试核验冻结全文、所有旧内容、作者增量、最终HTML解码JSON与源JSON、snapshot字节及hash、递归隐私、五项下载和两个ZIP。

运行 `python test_merge_guard.py ARTICLE_SOURCE BASELINE45` 验证用户正文/摘要、图文和query已有编辑得到保留；重复合并、ID或query冲突、数量异常均在写入前拒绝。运行 `node test_reader_routes.mjs PORTAL_REPORT_DIR` 核验研究/全文/样板路由、AI分类、URL往返和首次入库倒序。

本轮静态结果见`build-qa.json`：门户46篇研究/66份全文/2样板、AI29、95queries；单篇1/1、2queries。门户82项文本载荷、单篇13项载荷通过递归隐私检查。单篇官方新壳241个非内容文件不变。来源行检查、原文固定版本、完整解码结果与split manifest均通过。

## 交付与发布边界

本目录只归档小型作者源、测试和回执，不含大型HTML、dist、凭据、私人附件ID或运行环境路径。完整单篇与完整门户分别生成；单篇附件发送请求于2026-11-05 06:14 UTC获接受，不代表已经打开或下载。门户仅在本地完成，未发送或同步原站。没有访问此前403原站、改变访问权限或重试旧受限附件。原站最近已验收状态仍为v19的20篇研究/40份全文/2样板、AI9；本地46篇不是线上数量。

独立事实和静态复核通过，详见`independent-qa.json`。桌面视觉与交互未完成：云浏览器无法连接本地预览，本地浏览器因socket限制不能启动；没有绕过该限制。手机视口、真机、打印、真实断网、全46篇逐篇视觉和全部下载点击未测，不把构建或静态检查写成视觉验收成功。
