# 2026-10-30 三篇研究图文增量

本包不是全站快照；在已有公开阅读门户上增量加入三篇，保留旧 UI、研究、原文、样板与已完成的公开脱敏。

## 来源与时间

三篇正文固定提交 `e7575c5632a6bd4e1fd1752ff4e954fee29f615c`，真实首次入库 `2026-10-30T04:06:26Z`（北京时间 12:06:26）。三篇同一提交，时间相同，按现有 ID 倒序稳定排列，不暗示写作或验证先后。entry 中原始正文 hash 已核对提交 blob。电话与菜图归 AI/商业模式，订货篇仅归商业模式，不把规则流程当 AI 成功。

## 文件布局

- 每个主题目录：`article-entry.json`、`illustrated-story.json`、`article-reviewed-data.json`、`report.html`。
- `shared/`：共用独立阅读组件、样式、增量与导出准备脚本、查询同步及验证脚本；避免逐篇重复保存整套作者源码。
- 独立 HTML 为官方 Data 自包含导出，需要 JavaScript，不需网络、模型调用或登录。图示是有标签的事实/验收机制，不是新实测结果。

## 原站增量（保留用户修改）

在已经恢复到当前版本的作者工程中运行；不要覆盖 protected runtime、站点配置或 presentation：

```sh
python shared/test_batch.py
python shared/apply_batch.py . "$REPORT_DIR"
python shared/sync_illustrated_queries.py "$PROJECT_DIR/src"
```

将 `shared/article_topics.json` 中新增的三个主题规则合入原有规则，保留后续用户修改。`shared/test_reader_routes.mjs` 对应本轮 13 图文 / 33 全文 / 2 样板 / 4 AI 研究基线，后续增文应按真实内容更新测试，不可删文迎合旧数目。

**所有生成完成后**执行仓库 `reports/public-site-sanitization/` 的脱敏及 `--check`，防止历史链接或样板本地 metadata 重新进入公开载荷。同步后设置 `src/data.json` 正确的生成时间与 buildStatus，经 QA 完成后置 complete。按当前安装官方 Data 工作流 separate-data 构建、预览、检查所有下载的解码载荷，再由原站发布负责人发布；本包脚本不发布、不修改权限。

## 单篇独立复建

每篇使用一个单独的官方 Data 作者工程；绝不可把这一步用于原站工程，否则会把列表临时替换为单篇。

```sh
python shared/prepare_article.py food-images "$EXPORT_PROJECT/src"
```

另两篇将参数替换为 `voice-receptionist` 或 `restocking-controls`。使用当前官方 Data build `--separate-data`，再 export-offline 到该工程 `.data-app-offline/exports/report.html`；复制最终产物回对应主题目录。随后对每份交付 HTML 执行 `python shared/sanitize_export.py 主题目录/report.html`，移除导出器可能继承的本地线程 meta（仅导出副本，不修改 protected runtime），再重新计算 hash。无需另建 Site，也不包含站点 ID、账号或发布凭据。

## 校验

已执行 entry/hash/首次提交、6 幅图、独立数据快照、幂等增量脚本测试，以及原站图文完整性/路由/排序检查。旧 30 篇原文对象与 10 篇图文故事保持不变；Legacy、UI/CSS 和脱敏样板 HTML/ZIP 均逐字保留。实际浏览器检查由联合发布 QA 单独记录，不用源码测试冒充真机验证。

## Git 归档路径

本目录只归档作者增量。三个独立 HTML 位于仓库 `research/2026-10-30-<主题>/report.html`，主题为 food-images、restocking-controls、voice-receptionist，不在本目录重复保存。复建时仍生成到主题目录，清理元数据并核验后再复制至对应研究路径。manifest 的 path 是原冻结包相对路径，repositoryPath 是实际仓库路径；HTML 哈希不因移动改变。

## 后续同篇修订

电话篇已有研究院风格修订，来源固定为 `e6f524b36e3efd43e7c7d43ee43439852030412c`，首次入库时间不变。当前条目以 manifest 及[同篇更新说明](EDITORIAL-UPDATE.md)为准；已有旧版时使用带旧内容哈希保护的更新脚本，不用追加脚本强行覆盖。其余两篇来源及离线 HTML 未变。
