# 炒菜机器人研究图文增量

固定正文提交 `6becd8035a336f37598f918a0089893dacd66337`，首次入库 `2026-10-30T05:06:54Z`（北京 13:06:54）。这是新增正式研究，第 14 篇；仅归商业模式，不把机械自动化写成已验证 AI 效果。

## 归档布局

本目录包含 `robot-kitchen/` 下的 entry、story、reviewed-data 与独立 report.html，以及小量分类规则、路由测试、本文测试。独立 HTML 可归档至 `research/2026-10-30-robot-kitchen/report.html`，其他文件保持相对结构置于 reports 下。若移走 HTML，运行本文测试前把该文件复制回 `robot-kitchen/report.html` 即可。

UI、样式和生成器复用仓库 `reports/batch-2026-10-30/shared/`，不再保存重复整套作者源码。以已恢复到当前版本、保留用户编辑的作者工程为目标：

```sh
python test_robot.py
python "$REPO_ROOT/reports/batch-2026-10-30/shared/apply_batch.py" . "$REPORT_DIR"
python "$REPO_ROOT/reports/batch-2026-10-30/shared/sync_illustrated_queries.py" "$PROJECT_DIR/src"
```

以上 shared 脚本位置应按实际工作目录解析为仓库根下的 `reports/batch-2026-10-30/shared/`；不依赖任何固定工作机路径。合并本目录 article_topics.json 中新增 robot 条目，保留旧规则。路由测试对应本轮 14 篇图文 / 34 篇全文 / 2 样板 / 4 AI 研究；后续增文应按真实数目更新，而非删旧文满足测试。

运行已有 `reports/public-site-sanitization/` 清理与审计后，设置正确 buildStatus/生成时间，使用官方 Data separate-data 构建。保留原 Site、公开范围、用户 presentation 和已完成的电话篇编辑升级。

## 单篇复建

先准备独立官方 Data 导出工程，不要使用原站工程：

```sh
python "$REPO_ROOT/reports/batch-2026-10-30/shared/prepare_article.py" robot-kitchen "$EXPORT_PROJECT/src"
```

通过官方 build/export-offline 导出至该工程 `.data-app-offline/exports/report.html`，复制到 `robot-kitchen/report.html`；运行 shared/sanitize_export.py 移除可能继承的 local-thread meta，再计算最终 SHA。导出副本清理不修改 protected runtime。

## 检查范围

原始正文 Git blob 和 SHA 已核，索引使用真实首次时间。两图分别解释三个覆盖分母与整条出餐线的瓶颈，不绘制虚构数值、不把菜单百分比移到销量或工时。已有 13 故事 / 33 原文对象、UI、旧蜜雪读本与脱敏样板 JSON 均逐字保持。本文测试与原站路由/内容测试已执行；真实浏览器 QA 由发布流程另记，不声称现场经营测量或手机真机测试。
