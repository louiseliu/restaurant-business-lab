# 视觉收银同篇修订：本地待交付增量

原文章ID research-2026-10-30-vision-checkout-note，首次入库2026-10-30T15:02:15Z、首次提交98b377faa73538f6fd0168ceba7e7ec2f53faf8d保持。正文修订提交ffb0f400d7b4adae112e4a84b99e8d2eddca70ed，修订时间2026-10-31T06:01:35Z单独显示。不是新增文章。

新增银豹餐饮PC手册的模式互斥、同价错品替换与成功收款后学习资料风险、可选会员识别次数计费边界。两图均为原创机制示意，不是化府实测，也不推断关闭学习开关后的行为。

本目录仅小型作者源、修订保护条件、测试与状态。新版HTML仅本地完成，尚未交付或替换原附件，也未上站；原附件与原站v19视觉篇仍为旧版。保留历史report.html，不提交或更新大型HTML blob。原站上次发布20篇／40原文／2样板、AI9；本地已合入待同步采购篇的版本保持21／41／2、AI9，本修订不增加数量。

复用已归档reports/batch-2026-10-30/shared/update_article.py，用update-guard.json核对旧正文及元数据，意外用户变更会停止覆盖；再运行sync_illustrated_queries.py。独立工程沿用原报告稳定ID，通过prepare_article.py导入后使用官方Data separate-data构建和export-offline，再清理可选本地线程元数据。不更改受保护运行时。

```sh
python test_article.py
python test_article.py "$LOCAL_HTML"
python "$SHARED/update_article.py" vision-checkout "$REPORT_DIR"
python "$SHARED/sync_illustrated_queries.py" "$PROJECT_DIR/src"
```

后续恢复交付条件时应更新同一附件并检查当前版本，不能另建副本绕过访问限制。原站已有发布授权，但当前仍待公开验收条件恢复；同步前核对当时用户编辑、保留旧内容/UI/Legacy/5下载及访问范围，不自动发站。旧费用归档待核实问题保持独立，不重试原操作。
