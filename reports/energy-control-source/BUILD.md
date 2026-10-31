# AI节能溢价：独立图文与本地增量

完整冻结正文与两幅原创机制图在energy-control目录，首次提交和时间见article-entry.json。图一并列时间、状态与自学习，不是升级阶梯；图二比较相对可行替代方案的增量价值与成本，不是品牌收益测算。没有节能百分比、回收期或电气改造/排烟关停等运行参数。

本目录只含小型作者源、测试与验收记录，不提交大型HTML或私人标识。米尺直接URL读取失败而缓存可回查、深圳指南正文与截图访问状态分别保留，不声称持续可用。

本篇待上站，原站保持上次v19的20篇/40原文/2样板、AI9。待同步本地累计含采购篇、视觉同ID修订、知识撤回、菜单翻译、排队与本篇，为25/45/2、AI13，不能当作当前公开站点数量。旧视觉附件与费用归档问题独立保留，不重试受限依赖。

复用reports/batch-2026-10-30/shared/prepare_article.py与官方Data separate-data、export-offline流程；sanitize_export.py只清理可选本地线程元数据。全站隔离增量用apply_batch.py与sync_illustrated_queries.py，不改受保护运行时。

```sh
python test_article.py "$OFFLINE_HTML"
node test_reader_routes.mjs "$REPORT_DIR"
```

旧文、UI、Legacy、样板及5下载载荷应保持完整；正式同步仍须恢复公开验收条件并核对当时用户编辑与访问范围。本目录不自动发布，不改权限绕过限制，不把认证读取冒充公开验收。

本篇独立HTML已保存为新附件；完整原文展开、两图桌面排版及固定来源/首次时间已实际核对。旧44原文、24故事、50查询以及UI/Legacy/5下载保持完整；路由计数排序、53解码载荷脱敏、样板HTML/ZIP、最终构建hash通过。未声称移动端或本轮全站浏览器验收。
