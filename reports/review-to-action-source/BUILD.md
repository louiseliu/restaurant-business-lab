# 评价分析如何进入改菜决定：图文增量

正文首次提交`95ec37357d02ff957e86f36f720210b15c0feaeb`，首次入库时间`2026-10-31T00:01:07Z`。完整正文、两幅原创示意图与独立来源绑定均在review-to-action目录内。图1是自编假设评价，不是真实顾客记录或模型实测；图2是出品偏差与预期差异的研究分叉，不是品牌已执行的统一流程。

本目录只含小型作者源码、测试及发布验收记录，不含大型HTML、运行时、私人协作链接或发布凭据。独立HTML通过Library附件交付，不提交GitHub HTML blob。仍保留旧v4整站离线快照，不声称有最新全站离线包。

以实际最新v18完整作者源为基线，仅新增本篇，已发布验收为20篇图文/40份原文/2项样板、AI9；旧19图文/39原文/UI/Legacy/5下载应保持一致。费用证据归档未完成的问题独立保留，本增量不重试原操作。

复用已归档reports/batch-2026-10-30/shared/和public-site-sanitization流程：

```sh
python test_article.py
python "$REPO_ROOT/reports/batch-2026-10-30/shared/apply_batch.py" . "$REPORT_DIR"
python "$REPO_ROOT/reports/batch-2026-10-30/shared/sync_illustrated_queries.py" "$PROJECT_DIR/src"
```

合并主题规则并运行本目录路由测试、完整脱敏与旧内容哈希检查，再按官方Data流程build separate-data。独立导出使用另建官方report工程及shared/prepare_article.py，export-offline后用shared/sanitize_export.py清除可选本地线程meta，保留完整原文。test_article.py可接最终HTML路径追加隐私检查。

公开发布沿用同一Site及其用户presentation、DB/R2、环境与公开访问，不能通过更改受保护运行时或绕过审批修复失败。仅在原生部署明确succeeded后上传，完整HTML与数据快照回读匹配后才称上线。实际本轮发布状态见publication-receipt.json。

本轮原站v19已通过官方完整HTML/快照哈希回读、匿名200与只读检查；两图、完整原文、固定来源、首次时间、时间线和AI9筛选实际验证。用户presentation、原访问范围及既有内容保留。一次成功不代表全天候稳定，也未确定早前上传错误根因。
