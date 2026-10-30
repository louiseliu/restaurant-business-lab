# 餐饮软件退出验收图文增量

固定正文提交 `1dd3d0510b28581dc12bc6b50cf9f4ff691b2c36`，首次入库 `2026-10-30T06:14:48Z`（北京 14:14:48）。第 15 篇正式研究，仅归商业模式，不是 AI 效果或法律结论。

## 文件与复用

`software-exit/` 下为 entry、story、reviewed-data 和自包含 HTML。HTML 可映射至 `research/2026-10-30-software-exit/report.html`；其他文件保留相对结构置于 reports 下。映射后运行本文测试时，先把已归档 HTML 复制回主题子目录。其余 UI/样式和生成器直接复用 `reports/batch-2026-10-30/shared/`，不重复保存旧源码。

对已恢复最新版本且保留用户修改的作者工程执行：

```sh
python test_article.py
python "$REPO_ROOT/reports/batch-2026-10-30/shared/apply_batch.py" . "$REPORT_DIR"
python "$REPO_ROOT/reports/batch-2026-10-30/shared/sync_illustrated_queries.py" "$PROJECT_DIR/src"
```

合并 article_topics.json 中新增 software-exit 分类，保留其它规则。当前路由测试为 15 图文 / 35 全文 / 2 样板 / 4 AI 研究；未来增文按真实情况更新测试，不删旧文迎合数量。

所有生成完成后，运行 `reports/public-site-sanitization/` 清理和审计；正确设置生成时间及 buildStatus，再用官方 Data separate-data 流程构建、真实浏览器 QA 与发布。不得覆盖 Site 身份、公开访问、用户 presentation 或 protected runtime；本包不含发布功能。

## 独立 HTML

在单独官方 Data 作者工程准备，不使用原站目录：

```sh
python "$REPO_ROOT/reports/batch-2026-10-30/shared/prepare_article.py" software-exit "$EXPORT_PROJECT/src"
```

官方 build/export-offline 输出到该工程 `.data-app-offline/exports/report.html`，复制回 `software-exit/report.html`；调用共用 `sanitize_export.py` 移除可能继承的本地 thread meta，再计算最终 hash。HTML 需 JavaScript，不依赖联网或模型调用。

## 校验与范围

正文 blob/SHA、真实 firstGit、两幅机制图及数据绑定已核。旧 14 故事 / 34 原文（包含电话篇研究院修订和机器人篇）、UI、旧读本与脱敏样板逐字保持。图中没有统一退出天数；同时显示正常导出入口和终止安排需具体确认的边界。跨日退款仅为模拟设计，不是产品字段实测或已发现缺陷。

代码测试不冒充浏览器或门店实测。真实窄屏/来源/原文/返回和独立HTML由发布 QA 另行记录；不声称真机手机、登录产品或法律效力审查。
