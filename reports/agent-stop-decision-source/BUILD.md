# 离线任务停止：完整图文与第54篇本地门户增量

固定正文：research/2026-11-05-agent-stop/note.md，首次提交7eac8a2769fd0c80d587c74162ef6fee370d85a4，首次UTC 2026-11-05T16:09:05Z，正文SHA256 a129b3a9ebc954eccc8832117ee98ba3d4937512de1ac6638d94730773076ddb。首次入库显示北京时间2026-11-06 00:09，不冒充资料发布日期。完整保留五节论证、研究说明及原文。

图一对照账号登录、任务授权及既有经营结果；图二呈现作者建议的交接、授权收窄和停止核查路径。只使用一个美团官方协议，不伪造多个独立来源。协议页面发布日期2026年10月7日与正文生效日期2025年6月16日的关系未核明；功能开放、暂停恢复、在途处理和历史结果处置未实测。不承诺自动回滚，也不反向断言历史券、活动与订单一定保留。

## 复建

1. 取得固定提交正文，运行 `python make_article.py NOTE_MD frozen.json`；校验哈希，生成完整叙事、单源预览和两项reviewed queries。
2. 用官方prepare-data-app.mjs以article-reviewed-data.json准备新的单篇report，保存准备后指纹standalone-prepared-sha256.json，再运行prepare_standalone.py；保留官方身份和运行时。
3. 复制完整53篇门户为隔离基线及工作副本；基线HTML哈希应为9a1287a49d1527ed1a4e51d013e790a392328a8a2b95ecf190f08e0946e86a1e。保存源文件指纹baseline-sha256.json，运行 `python integrate54.py PORTAL/src SOURCE`。基线须为53研究、73全文、AI35、109queries，重复或冲突在写入前拒绝，不覆盖旧文章、图文和用户编辑。
4. 运行既有公共脱敏测试与sanitize_site_content.py及--check；设buildStatus为complete，运行官方data-app.mjs prepare、build --separate-data和export-offline。导出位于工程.data-app-offline/exports；交付副本只移除可选本地thread元数据。
5. 执行test_preservation.py（制作目录、基线、冻结正文）、test_merge_guard.py（源码、基线）和test_reader_routes.mjs（门户report目录）。完整HTML、dist、ZIP和缓存不入Git，仅归档小型公开源码与回执。

## 核验范围

官方构建、完整离线导出、冻结正文与完整六节、单源绑定、query一致性、manifest、递归隐私、旧内容保护、合并冲突拒绝和路由函数测试通过。门户54研究/74全文/2样板、AI36、111queries。旧73份全文、53篇图文和109queries保持，5下载载荷和2ZIP校验完整；非必要变更文件及单篇受保护运行时检查数量以build-qa.json为准。

单篇通过支持的管理式本地预览完成有限桌面检查：首屏、两幅原创图、目录和图解跳转、完整原文展开、图二来源面板、四行数据与证据流。截图未见图示裁切或重叠。浏览器日志样本存在扩展元数据错误，未观察到报告渲染失败，不声称浏览器完全无错。窄屏/手机、完整门户浏览器、逐节截图、主题/编辑持久化、全部下载点击、打印及真实断网未测。具体见visual-qa-status.json，静态检查不能替代未做验收。

保留检查仅证明可读归档53篇基线被保持，不证明缺失历史或未归档编辑已恢复。原公开站仍只能引用最后核验v19的20/40/2、AI9；本轮未访问受限原站、发布或改变权限。第21—54篇34项新增，加视觉收银与菜品图两项同ID修订，共36项待同步。历史附件和站点待办独立保留。附件保存及发送由后续真实回执确认。

独立静态QA提出图1日期说明主体应为“协议页面”，已修正图文与query、重建双输出并重跑全部静态测试；修正结语已重新桌面预览，未见遮挡。
