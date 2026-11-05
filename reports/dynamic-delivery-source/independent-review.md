# Kotipizza 配送定价 HTML 独立静态审计

## 结论

静态核验通过；尚未进行视觉验收。没有改动 production、原稿或远端，没有上传、发布或 Git 提交。审计代码和结果仅保存在本审计目录。不能把这份报告写成已验收上线。

## 核验对象与方法

直接读取 dynamic-delivery-production/dynamic-delivery.html，独立提取其中 JSON.parse 字符串负载，再与原稿、来源台账、reviewed 文案、查询数据及构建清单核对；同时人工审读正文、图文文案和 React 阅读器代码。没有仅依赖既有 build-qa.json。没有运行会重写 build-qa.json 的既有 test_standalone.py，以保持目标只读。可重复执行本目录 audit.py；机器结果见 results.json。

- HTML：2,940,573 字节，SHA256 5b03b7cb9c609eea660e55497c7daa3dbe5c116902b2f4a36b7b1a89e126abea，与预期一致。
- 正文：SHA256 87197ed3d356b33d06d84819a221eb39b1398278afb6bfa9a65e904f752dbba1。
- 来源台账：SHA256 28d2fbc392a94e5d5c4275dd2bca2a729e0f949c195466147a973de7531cc50b。

## 逐项结果

1. **单篇及完整性：通过。** HTML 内只有一个文章目录对象和一个对应故事对象，均仅含 research-2026-11-05-kotipizza-pricing-note。正文完整字节等于 note.md；来源技术详情完整字节等于 sources.md。两者与 frozen.json 及 draft-check.json 的校核摘要一致。六个叙述章节逐节等于原文拆分结果。阅读器代码包含完整原文折叠区及来源台账折叠区，不只是摘要。
2. **固定版本及时间：通过本地一致性。** firstGit 为 a9a3137240790b5ef12abe6273adb8e0dd09505b；首次入库与更新时间均为 2026-11-05T23:17:18Z；公开源码 URL 使用该固定提交。阅读器按 Asia/Shanghai 显示，换算为北京时间 2026-11-06 07:17；不应与正文研究日期 2026-11-05 混淆。未访问远端确认该提交对象和文件内容。
3. **两幅图主张边界：通过。** 第一幅为四环节作者核对路径，明确不是 Kotipizza 已实施系统或实测因果关系，S2 仅支持供应商对全国信号错配的回顾，S3 仅支持产品能力背景；没有把加盟商独立权限当作事实。第二幅为三种方案的作者比较设计，明确不是已实施三臂实验，S1 仅提供历史限时折扣背景。没有虚构量化收益、销量、回本或新增 AI 成效主张。所有节点值为字符串，非定量坐标。React 图组件明确渲染 scope、节点来源边界、completion 与图注；实际是否无遮挡仍待视觉检查。
4. **来源可追溯：通过本地链路。** 三个正文引用 URL 与故事 sources 精确对应，均有 approvedForReport 的本地预览条目。两幅图的查询 evidenceFlow 逐项对应其 sourceIds。来源台账区分品牌公告、供应商回顾、产品说明与作者建议，并保留论文未采用及访问限制。没有将供应商宣传当作独立成效验证。本轮未重新抓取外部来源，不能担保链接实时可达或重新验证其当前页面。
5. **包装与运行时：通过本地摘要核对。** dist 中 HTML 及 snapshot 的实际字节数、摘要与 data-app-build.json 一致，snapshot 查询等于 reviewed 查询。最终离线 HTML 的摘要单独验证，不与 separate-data 模式 dist HTML 摘要混淆。241 项非内容初始基线文件全部一致；protected-runtime.json 中 240 项全部一致。此项仅证明与所给本地基线一致，不是独立认证这些基线的官方来源。未执行重新构建。
6. **隐私与可移植性静态扫描：未发现问题。** 目标 HTML 未出现工作区、个人主目录、内部会话或文件标识等指定模式，也未匹配 GitHub token、AWS key、常见 API key、私钥头模式。没有外部 src/href 资产标签。扫描不构成所有潜在凭据绝对不存在的证明；也没有检查运行时联网行为。
7. **只读保证：通过。** 审计前后对 production 目录内全部文件计算摘要，未发生变化。

## 注意事项与未验收范围

- 来源台账保留原稿阶段“未提交 GitHub、未制作图文、未发布”的历史状态，同时指明正式归档状态需另按真实记录更新。为保留 reviewed 原文，本轮未修改。交付说明应明确这是历史台账状态，不能当作目前未制作图文的事实；若需要更新台账，应另走修订与重新校核流程。
- 没有浏览器、截图、移动端或桌面端渲染检查，没有测试折叠、目录跳转、返回顶部、来源弹层、下载或离线加载。静态通过不代表排版、可访问性或交互已通过。
- 没有核验线上发布、附件交付、GitHub 远端状态或门户整合；没有访问受限论文站点。

## 补充：作者生成器重现及写入保护

追加核验通过，详见 generator-reproducibility.json、authoring-guard-qa.json；复跑入口为 check_generator.py。

- 在全新临时目录复制小型 source 文件及固定 note.md、sources.md，并先删除三个既有生成结果，随后运行 make_article.py。新生成的 article-entry.json、illustrated-story.json、article-reviewed-data.json 与 production/source 对应文件逐字节一致。
- 在一次性副本运行原有 test_authoring_guard.py：相同输入为 no-op；修改原文、故事、查询、阅读器、样式、添加他篇查询和移除报告身份共七种情况全部在写入前拒绝。八个用例均保留副本文件。
- 补测前后 production 和原稿目录文件摘要完全一致。报告未收录临时目录绝对路径或私人身份。
- 这是作者层 JSON 生成重现和保护测试，不是全新官方运行时准备、HTML 重建或视觉验收；原报告的相关限制仍然适用。
