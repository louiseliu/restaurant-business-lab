# 视觉收银研究图文增量

## 发布状态

本篇独立图文已生成，但尚未同步到公开站。尝试发布的 v16 在数据资产上传时返回 HTTP 400，未通过完整回读；现已恢复并核验原 v15。当前公开站仍为 17 篇研究、37 份全文、2 项样板，AI 研究 6 篇。本目录中的 18/38/2/7 是待同步增量的目标与本地测试计数，不代表线上状态。后续须先修复资产上传并重新核验，再更新公开状态，不能仅凭版本部署成功声称新文已上站。

固定正文提交 `98b377faa73538f6fd0168ceba7e7ec2f53faf8d`，首次入库 `2026-10-30T15:02:15Z`。本地新增第18篇，AI/商业模式双分类；本次尚未上站。具名案例为供应商申报材料，不是协会独立效果测量；不采用准确率、排队或财务成效数字。

本增量以实际公开站 v15 为基线，保留17篇研究、37份原文及2项样板。此前费用证据文章的独立HTML/源码GitHub归档仍待原操作结果，本目录不补交或重试该批文件。因此，仅从当前GitHub旧归档不能声称已完整恢复v15；须先取得并核对实际最新作者源及该依赖状态。

`vision-checkout/` 含 entry、story、reviewed-data及独立 report.html。HTML映射至 `research/2026-10-30-vision-checkout/report.html`；其余文件置于 reports 下。若HTML已映射，测试前复制回主题目录。复用 `reports/batch-2026-10-30/shared/` 已归档UI、样式和生成器，不重复打包旧文章。

```sh
python test_article.py
python "$REPO_ROOT/reports/batch-2026-10-30/shared/apply_batch.py" . "$REPORT_DIR"
python "$REPO_ROOT/reports/batch-2026-10-30/shared/sync_illustrated_queries.py" "$PROJECT_DIR/src"
```

合并分类文件新增vision-checkout规则；路由测试本轮为18图文/38全文/2样板/7 AI，后续按真实增量更新。生成后运行public-site-sanitization检查全部正文、Legacy、嵌入HTML及ZIP下载，设置正确generatedAt/buildStatus，官方Data separate-data构建、浏览器检查及同站发布。保留用户presentation、公开只读访问、DB/R2与protected runtime。非实时同步。

独立HTML复建只使用另建的官方Data导出工程：

```sh
python "$REPO_ROOT/reports/batch-2026-10-30/shared/prepare_article.py" vision-checkout "$EXPORT_PROJECT/src"
```

官方export-offline至`.data-app-offline/exports/report.html`后，复制回主题目录，以shared/sanitize_export.py移除可选本地线程meta。需JavaScript，可离线阅读，无外部模型调用。

图1是认菜与认盘的机制对照，图2是建议的例外观察流程，不是化府完整部署图；付款前取消与付款后退款分开。完整原文保留。跨年代、跨厂商、跨业态手册不能拼成同一套已部署系统。无新Pro或门店实测，不推算回本期。

## 本次发布状态（2026-10-30）

新图文和完整离线HTML已完成校验。v16原生部署成功，但随后数据资产上传返回HTTP400，公开数据端点返回503，因此未达到发布就绪。已恢复同站v15，匿名数据端点返回200，完整快照SHA256与原v15记录一致；线上仍为17/37/2、AI6。新稿18/38/2、AI7为本地已验证结果，不是当前线上数量。

恢复待办：保留原站和访问设置，在官方Data/Sites流程中排查资产上传失败并重新验证完整HTML及快照回读；未确定根因，不归咎内容或平台持续故障，不绕过上传门、不改受保护运行时、不另建站。此前费用文章归档待办独立保留。
