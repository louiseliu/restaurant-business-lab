# 配送费要不要随忙闲变化：单篇图文作者源

本目录保留已核验正文、来源、两幅原创定性图、生成器和静态检查。首次正文提交及时间以 frozen.json 为准。正文与来源按原稿字节冻结，来源台账中的“未提交、未制作”是研究准备阶段记录，不能用来描述当前交付状态。

第一图说明价格信号、本店瓶颈、控制空间和承诺应逐步核对；第二图比较现行收费、固定低谷优惠与动态方案。均为作者经营分析，并非 Kotipizza 已实施的控制系统或三臂实验。2019官方试验、供应商不同阶段回顾与产品能力说明分别限定，不将自动定价归为已验证 AI 成效。

## 复建

1. 从 frozen.json 固定提交取回 research/2026-11-05-kotipizza-pricing/note.md 和 sources.md。运行 `python make_article.py NOTE_MD frozen.json`，核验两份源文件哈希并生成全文条目、故事和两项限定来源的查询。
2. 使用兼容官方 Data `prepare-data-app.mjs --surface report`，以 article-reviewed-data.json 准备新工程。阅读该工程 AGENTS 与组件文档，记录准备后文件指纹，然后运行 `python prepare_standalone.py PROJECT`。仅写作者内容，不覆盖已有不同内容或多篇门户。
3. 依照仓库 reports/public-site-sanitization 执行公共内容检查；设置 buildStatus 为 complete。使用官方 `data-app.mjs prepare`、`build --separate-data` 与 `export-offline`。构建环境不注入本地线程身份，离线导出放于 `.data-app-offline/exports/` 后复制到生产目录。
4. 运行 `python test_standalone.py PRODUCTION_DIR NOTE_MD`。PRODUCTION_DIR 应包含 source、standalone、初始指纹与 dynamic-delivery.html。可在一次性副本运行 `python test_authoring_guard.py PROJECT` 检查保护。

完整运行时不包含在本作者增量源内。新工程须重记保护指纹，不能把官方版本变化当成篡改。兼容准备、构建与导出工具是复建依赖。

## 检查与交付边界

静态结果见 build-qa.json 和 independent-qa.json，视觉范围见 visual-qa-status.json。静态通过不能替代桌面、窄屏、交互、打印或断网验收。仅制作单篇，未更新完整门户或原站，未重试受限来源。

本次只归档小型作者源码及真实状态，不含HTML、ZIP、原始PDF或缓存。附件保存与发送状态单独记录；入库不等于已发送或已打开。
