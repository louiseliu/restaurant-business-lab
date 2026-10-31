# 菜单翻译范围：独立图文与本地增量

首次正文提交0a3ceaf0796e824d919723b4156ccfaef99a051f，首次入库2026-10-31T11:01:35Z。menu-translation-scope目录保留完整冻结正文、两幅原创机制图、来源和地域限制。图一对照iCHEF顾客展示与Bee写入范围；图二为研究建议的人工核对路径，不是两产品相同流程，不推断打印译名、自动更新、大陆可用或经营收益。

独立HTML已作为本篇新附件保存，不是视觉旧附件的替代品；旧附件依赖未重试。本目录仅小型作者源、测试和记录，不含大型HTML或私人运行时信息。

本篇未上站。原站仍为上次v19的20篇／40原文／2样板、AI9。本地累计加入采购篇、视觉同ID修订、知识撤回篇及本篇，为23／43／2、AI11，不代表当前公开站点数量。旧费用归档待核实问题独立保留。

复用reports/batch-2026-10-30/shared/prepare_article.py制作独立官方Data report；官方separate-data构建和export-offline之后用sanitize_export.py清理可选本地线程元数据。隔离全站增量使用apply_batch.py和sync_illustrated_queries.py，不修改受保护运行时。

```sh
python test_article.py "$OFFLINE_HTML"
node test_reader_routes.mjs "$REPORT_DIR"
```

本地检查保留全部旧42原文、22图文、46查询、UI、Legacy及5下载载荷；首次时间排序、计数、路由、53解码载荷脱敏与样板HTML/ZIP通过。正式同步前仍需恢复公开验收条件、核对最新用户编辑和访问范围；不改权限绕过限制，不自动触发发布。
