# AI盘点输入与库存生效：独立图文增量

首次正文提交7754605220237525f8e76c522d747b2ade7efe41，首次入库2026-11-01T13:03:33Z。inventory-capture目录保留完整冻结原文、两幅原创机制图及固定来源。AI产品机制不是成功效果案例；图1解释识别、计量、提交和生效边界，不规定所有物料必须串行称重拍照；图2呈现四类对象的证据要求，非全品类支持清单或准确率比较。

本篇独立HTML已保存新附件，未上站。原站保持上次v19的20篇/40原文/2样板、AI9；本地累计30/50/2、AI16。新增21—30十篇加视觉同ID修订，共十一项待同步。旧费用归档问题独立保留。

复用reports/batch-2026-10-30/shared/prepare_article.py及官方Data separate-data、export-offline流程；sanitize_export.py只清理可选本地线程元数据。全站隔离增量复用apply_batch.py和sync_illustrated_queries.py，不修改受保护运行时。

```sh
python test_article.py "$OFFLINE_HTML"
node test_reader_routes.mjs "$REPORT_DIR"
```

本轮实际确认29篇累计基线后复制增量。旧49原文、29故事、60查询及UI、Legacy、5下载载荷保持；全文实际展开、两图桌面布局与固定来源/首次时间已检查。路由、计数、排序、53解码载荷、样板HTML/ZIP、隐私及构建哈希通过。不声称移动端或本轮全站浏览器验收。公共目录仅9个小文件，无HTML或私人信息。

正式同步仍须恢复公开验收条件并核对当时用户编辑及访问范围；不改权限、不绕过限制、不以认证读回替代公开验收。本目录不自动触发发布。
