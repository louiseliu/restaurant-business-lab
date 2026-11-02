# 出菜口 AI 确认与现场交付：独立图文增量

首次正文提交 9cd2b63f454602c3af0a3f562f1fe0fa944de575，首次入库 2026-11-02T03:10:39Z。pass-confirmation 目录保留完整冻结原文、两幅原创机制图及固定来源。图1区分产品文档中的系统操作链与研究建议观察的现场交付；图2将识菜划单、出品提示与交付记录并列，不表示等级或统一产品套餐。资料均属同一供应商，不作为独立验证或已证实的利润效果。

独立 HTML 已保存为新附件，未上站。原站仍为上次已核 v19 的20篇/40原文/2样板、AI9；本地33/53/2、AI19。新增21—33十三篇及视觉同ID修订，共十四项待同步。GitHub HTML 归档未完成，未新发大型 HTML blob；旧费用归档问题独立保留。

复用 reports/batch-2026-10-30/shared/prepare_article.py 及官方 Data separate-data、export-offline 流程；sanitize_export.py 仅清理可选本地线程元数据。全站隔离增量复用 apply_batch.py 和 sync_illustrated_queries.py，不修改受保护运行时。

```sh
python test_article.py "$OFFLINE_HTML"
node test_reader_routes.mjs "$REPORT_DIR"
```

原52原文、32故事、66查询及 UI、Legacy、5下载载荷保持不变。实际检查独立全文展开、两幅图桌面布局及390px宽度 iframe 响应式布局、固定来源与首次时间；未声称真实手机设备测试或本轮全站浏览器历史/滚动验收。路由解析与URL往返、计数与排序、全部作者正文/数据、7项解码载荷、样板 HTML/ZIP、隐私及构建哈希通过。公共目录只含9个小源码/说明文件，不含大型 HTML 或私人资料。

正式同步前仍须恢复公开验收条件并核对当时用户编辑和访问范围。不改权限、不绕过限制、不用认证读回替代公开验收。本目录不触发发布。
