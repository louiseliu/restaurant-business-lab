# 呷哺门店退出现金决策：单篇图文源

本目录保留单篇图文的作者增量源。完整研究正文、来源台账和固定提交身份来自 frozen.json，两幅原创图解分别区分损益、经营现金和融资类租赁付款，以及继续经营、立即退出、到合同节点退出的同期间收付款。

图解不是上市公司已经披露的逐店流程，不将集团变化归因于关店。未来方案、现金贡献边界、解约结算不可重复计入、跨期义务与资金最低点，均为作者建议，未伪造门店数字、回本期或止损阈值。

## 本地复建

1. 从 frozen.json 指定的固定提交取回 note.md 与同目录 sources.md。运行 `python make_article.py NOTE_MD frozen.json`；生成器核验两文件 SHA256，完整保留正文六节与来源台账，并生成两项来源限定的 reviewed queries。
2. 用兼容的官方 Data `prepare-data-app.mjs --surface report`，以 article-reviewed-data.json 准备一个新的报告工程。记录初始文件 SHA256，再运行 `python prepare_standalone.py PROJECT`。只安装作者内容并保留官方报告身份，不覆盖已有不一致内容或多篇门户。
3. 运行仓库 `reports/public-site-sanitization/` 的测试与脱敏检查。设置 buildStatus 为 complete，使用官方 `data-app.mjs prepare`、`build --separate-data`、`export-offline`。构建时不传入本地线程环境标识。离线导出放在官方允许的 `.data-app-offline/exports/` 下，随后复制成所需交付文件。
4. 运行 `python test_standalone.py PRODUCTION_DIR NOTE_MD`，核验完整正文及来源台账哈希、图文叙事、两图数据和来源、官方非内容文件、编译内容、构建manifest、隐私与离线静态资产。

本目录不是完整官方运行时，复建需要兼容的官方准备、编译与导出工具。准备阶段记录的文件指纹仅证明本次工程保护范围；换运行时版本时应重新准备并记录基线，不把版本差异误报成篡改。

HTML、dist、ZIP、缓存、私人路径及运行身份不进入小型作者源或Git。本单篇流程不发布、不改访问权限、不整合既有门户，不提交HTML或触发大型blob。后续完整门户本地整合单独见 ../xiabu-exit-portal-source/PORTAL_BUILD.md。

## 检查范围

以 build-qa.json 与 visual-qa-status.json 的真实记录为准。成功构建和静态检查不替代浏览器视觉或交互检查；未执行检查不得称为通过。既有门户、站点同步、历史附件及归档任务不因本单篇完成而自动关闭。

## 同轮门户后续

已基于完整可读57篇门户在新副本整合第58篇，本地构建与静态验收完成。门户小源码及独立检查位于 [xiabu-exit-portal-source](../xiabu-exit-portal-source/PORTAL_BUILD.md)，不重复本目录单篇作者源。门户58研究/78全文/2样板、AI37、119queries；浏览器视觉与交互仍未验，原站未同步。完整门户HTML与单篇HTML均未进行Git大文件归档。
