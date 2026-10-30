# Q-Smart任务兑现研究图文增量

固定正文提交 `2d35d3947a51ebafdf8097d393ce49d6db457411`，首次入库 `2026-10-30T07:29:17Z`（北京 15:29:17）。第 16 篇正式研究，AI/商业模式双分类。两份官方文字稿为公司披露，不是独立利润验证。

## 文件与复建

`qsmart/` 下为 entry、story、reviewed-data 和自包含 report.html。HTML 可映射至 `research/2026-10-30-qsmart/report.html`；其余文件保留相对结构置于 reports 下。运行测试前，若HTML已映射，请复制回主题目录。共享 UI/样式/生成器复用仓库 `reports/batch-2026-10-30/shared/`。

```sh
python test_article.py
python "$REPO_ROOT/reports/batch-2026-10-30/shared/apply_batch.py" . "$REPORT_DIR"
python "$REPO_ROOT/reports/batch-2026-10-30/shared/sync_illustrated_queries.py" "$PROJECT_DIR/src"
```

目标必须是恢复到当前版本、保留用户修改的作者工程。合并 article_topics.json 中新增 qsmart 规则，不覆盖后续规则。本轮路由测试为 16 图文 / 36 全文 / 2 样板 / 5 AI 研究，未来新增应更新真实预期，不删除旧文迎合测试。

所有生成完成后运行 `reports/public-site-sanitization/` 清理和审计，含嵌入HTML、base64下载与ZIP。设置正确 buildStatus/生成时间，以官方 Data separate-data 流程构建、预览和发布。保留原 Site、public访问、用户presentation与protected runtime；脚本不负责发布。

## 独立 HTML

只在单独官方 Data 导出工程执行：

```sh
python "$REPO_ROOT/reports/batch-2026-10-30/shared/prepare_article.py" qsmart "$EXPORT_PROJECT/src"
```

官方 build/export-offline 输出至该工程 `.data-app-offline/exports/report.html`，复制回主题目录；运行共用 sanitize_export.py 去可能继承的本地 thread meta，再核最终hash。HTML需JavaScript，不依赖联网或模型调用。

## 实质内容与边界

完整固定原文保留于可展开正文，不以摘要替代。图1仅串联公司披露的发现缺员、建议替补、发起电话三个动作；拨号前确认、员工接受、班表写入、到岗与成功率只置于独立证据边界，不画为已实现后续。图2明确为本院提出的任务选择与例外成本框架，不是公司实现流程或实证最优策略。

旧15故事/35原文、UI、旧蜜雪读本和脱敏样板均逐字保持，新增文章原始hash、真实firstGit、图解及路由测试已执行。真实浏览器QA单独记录，不声称门店实测、真机手机或本轮Pro新审。
