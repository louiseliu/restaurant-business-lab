# 旧套餐规则撤回：独立图文与本地增量

首次正文提交c9978c300b1a8acb4c5b597c097e08022d9fd55f，首次入库2026-10-31T09:01:42Z。完整冻结正文、两幅原创机制图及来源绑定在knowledge-withdrawal目录。图一为假设维护情景，图二区分FAQ直接匹配、FAQ生成材料和知识空间过滤；不是同一开关，不代表餐企真实部署，不保证答案采用旧句。

独立HTML已作为本篇新附件保存；不是视觉收银旧附件的替代品。该旧附件修订仍未交付，未重新尝试被拒访问。本目录只含小型作者源、测试及验收记录，不提交大型HTML、第三方截图或私人运行时信息。

本篇尚未上站。原站保持上次v19的20篇／40原文／2样板、AI9；本地累计含采购篇、视觉同ID修订和本篇，为22／42／2、AI10。三项待同步改动不能写成当前公开站点内容。旧费用归档待核实问题独立保留。

复用reports/batch-2026-10-30/shared/prepare_article.py制作独立官方Data report，再按官方separate-data构建和export-offline导出；sanitize_export.py仅清理可选本地线程元数据。全站隔离增量使用apply_batch.py和sync_illustrated_queries.py，不改保护运行时。

```sh
python test_article.py "$OFFLINE_HTML"
node test_reader_routes.mjs "$REPORT_DIR"
```

本地检查保留原41份原文、21篇图文、44查询、UI、Legacy与5下载载荷；路由、首次时间排序、计数、53解码载荷脱敏和HTML/ZIP样板检查通过。正式同步仍须恢复公开验收条件并核对当时用户编辑与访问范围；不改权限绕过限制，不自动触发发布。此目录不包含新的发布令牌或远端操作。
