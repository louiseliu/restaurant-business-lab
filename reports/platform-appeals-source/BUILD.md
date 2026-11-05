# 平台AI售后与门店事实记录：单篇图文作者源

本目录为第60篇研究的作者增量源。正文及来源台账按 frozen.json 指定的首次提交和SHA256冻结，两幅原创定性图分别说明责任分工和留证投入的经营取舍。

平台宣称、门店事实责任与作者建议分别标识；技术证据搜集减负不等于免除订单履约事实。评价规范中的同一评价一次、首次评价及评价产生之日起30日，不推广到退款、到店评价或其他业务。新闻、规则和后台实际操作的关系尚未核实，保留页面日期矛盾，不做任何顾客或商家的诈骗裁决。

## 本地复建

1. 从 frozen.json 的固定提交取回 research/2026-11-05-platform-appeals/note.md 和 sources.md。运行 `python make_article.py NOTE_MD frozen.json`。生成器核验两份文件哈希，完整保留正文各节、原文及来源台账，生成两项范围分别限定的定性图解查询。
2. 使用兼容官方 Data `prepare-data-app.mjs --surface report`，以 article-reviewed-data.json 准备新工程；记录准备后文件哈希至生产目录的 standalone-prepared-sha256.json。阅读新工程AGENTS及工具返回的组件文档后，运行 `python prepare_standalone.py PROJECT`。仅安装作者内容，保留官方报告身份；不覆盖不一致的既有内容或多篇门户。
3. 使用仓库 reports/public-site-sanitization 的公开内容检查；设置 buildStatus 为 complete，运行官方 `data-app.mjs prepare`、`build --separate-data` 与 `export-offline`。构建环境不注入本地线程标识。离线导出先放在 `.data-app-offline/exports/` 下，再复制为生产目录的 platform-appeals.html。
4. 运行 `python test_standalone.py PRODUCTION_DIR NOTE_MD`。核验完整正文、台账与章节，两图reviewed rows和限定来源绑定，未变更的官方非内容文件、编译JSON、构建manifest、隐私及离线静态资源。
5. 可运行 `python test_authoring_guard.py PROJECT`，在一次性副本验证完全一致时无写入，以及正文、故事、query、读本、样式、查询数量或身份改变时先拒绝再保持文件。此检查不修改正式产物。

完整官方运行时不包含在作者增量源内。复建需要兼容官方准备、构建和导出工具；新准备工程须重记保护文件指纹，不能把运行时版本变化误判为篡改。测试脚本中的PRODUCTION_DIR指同时具有source、standalone、哈希记录与离线HTML的工作目录。

本轮仅本地单篇制作，不修改完整门户、不访问受限站点、不发布、不改权限、不上传大HTML。HTML、ZIP、dist、缓存、私人路径及运行身份不得进入此小型作者源。

## 检查范围

以 build-qa.json、independent-qa.json 及 visual-qa-status.json 为准。静态检查不替代浏览器视觉和交互验收；不把成功构建写成浏览器已验。既有HTTP预览连接受限及file协议拒绝仍保留，不换路、重新托管或修改安全设置。

generator-reproducibility.json记录在空临时目录中重新生成正文条目、故事及reviewed queries的逐字一致检查，不声称以全新运行时重新构建后HTML字节相同。首次入库来源台账末段保留研究准备时的状态；此后图文构建、归档或交付状态单独记录，不回写冻结正文和来源。

## 已知非阻断标注问题

见 known-issues.json。单篇第二图的 source.metricDefinitions[0].label 复用了图一标签；图二定义、组件绑定和定性数据正确。此问题经作者JSON核对，未实看来源面板的渲染表现。已接受发送请求的单篇附件及其冻结作者数据保持不变，不重发；门户整合中的对应标签修正应单独核验，不把计划写成完成。
