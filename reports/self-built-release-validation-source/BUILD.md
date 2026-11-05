# AI替餐厅改好系统，谁来决定可以上线：第47篇图文

正文冻结于 `b71e07c156aeec9fc38e2c4fb411754a9737c467`，首次入库 `2026-11-05T09:22:16Z`，正文SHA256 `5821c7ca3cc6fccc65b1617e51085abde27687170e6c2cedbc151c9b850bbef9`。文章ID为 `research-2026-11-05-self-built-release-validation-note`。独立完整HTML先构建，再整合到完整门户，没有以单篇reader替换门户。

## 内容与证据

保留五节完整论证与冻结原文。图一用四种合成身份说明允许、拒绝必须同时检查，明确示例权限约定、总部仅按实际授权范围使用，须以隔离环境专用身份与合成记录替换。图二沿已运行版本、本次源码、最终构建、实际入口四层验收，并把测试后的再次变更指回核对与重验；下方分列S2鉴权漏测与S4旧构建覆盖，不合成一次事故。

四份资料都来自同一项目的固定公开仓库提交，不构成四份独立佐证。公开蓝图自称原串技术团队，身份关联、生产部署、实际事故与经营效果未经独立核验。S4防回退当时只告警、不强制阻断；机器人页前段人工审批与后段限定免确认例外并置，首次真实触发仍在观察。矩阵、分工、验收链与扩大/收窄范围条件均为作者建议，未执行测试或门店实验。没有生成费用、停业损失、收益或效率数字。

## 46篇保护基线

本轮唯一基线是上轮46篇官方作者工程，含菜品图与排班同ID修订、盘点第三图、reader修订、样板及全部已归档旧内容。先核对完整门户HTML与固定归档 `1910e07a08bae189f908cf519d2d7f85506ab388` 的QA：13,067,318字节，SHA256 `183cf39a550a809add19de5be2efd79d0ba508207bb70e776a5faf08b58e8432` 完全一致；重跑上轮正文、源JSON/成品、旧内容、下载和隐私检查通过。

本轮将这份基线复制到隔离目录，生成295项源文件指纹。只必要地修改4个已有作者文件：articles.json、illustrated-stories.json、data.json与IllustratedArticle.jsx，并新增专用组件、样式、来源预览。其余291项文件逐字保持。旧66份全文、46篇图文、95项query逐对象不变；门户身份、标题、主题、UI、Legacy、两个样板和5项下载均保留。源码变更仅为新文追加，不重置旧图文和用户编辑。

此前46篇基线由可读工程与固定小源恢复。本轮确认的是已归档版本，不证明更早缺失历史作者工程或未归档编辑已经恢复。原站仍不可据此推定当前编辑完整或发布成功。

## 复建顺序

1. 从冻结提交取得 `research/2026-11-05-self-built-release-validation/note.md`。执行 `python make_article.py NOTE_MD frozen.json`，命令校验正文SHA256后生成完整作者JSON，不推断首次时间。
2. 使用当前官方Data准备独立报告：`node DATA_PLUGIN/scripts/prepare-data-app.mjs --surface report --output NEW_PROJECT --snapshot article-reviewed-data.json`。读取生成AGENTS与返回的组件文档；保存初始工程指纹，再执行 `python prepare_standalone.py NEW_PROJECT`。保留官方生成的新稳定身份，不复制门户身份。
3. 独立文章完成后，准备完整46篇基线副本，校验 `baseline46-sha256.json`，再运行 `python integrate47.py PORTAL_PROJECT/src ARTICLE_SOURCE`。写入前核对46/66/2、AI29、95queries、新ID/queries无冲突、全文hash和两图行。现有条目、图文、query、reader与身份不被替换。
4. 两图各绑定稳定query与componentIds；扁平中文字符串行供来源面板阅读，图中文字只读。正文、图注和作者建议通过RichNarrative绑定；实际读过的公开来源有短预览，固定链接含正文使用的锚点。
5. 在两工程所有载荷生成后，运行仓库 `reports/public-site-sanitization/test_sanitization.py` 与 `sanitize_site_content.py REPORT_DIR`、`--check`。本轮两工程无需要清理的源载荷，脱敏回归通过。不要修改受保护运行时。
6. 运行官方 `data-app.mjs prepare --project-dir PROJECT` 与 `build --project-dir PROJECT --separate-data`，使用已安装预编译runtime，不额外安装依赖或修改构建保护。完整作者内容完成时置buildStatus为complete并重构建。
7. 用官方 `export-offline` 导出到对应工程 `.data-app-offline/exports/`。该文件内含完整数据，再复制为交付HTML，仅清除可选本地thread meta。split HTML单独不是完整离线交付。两份最终HTML均为完整文件，未上传GitHub。

## 实际静态验收

- `python test_preservation.py WORK_ROOT BASELINE46 NOTE_MD`：冻结全文、全部旧对象/源文件、scope、成品解码JSON与源JSON、split manifest字节/hash、递归隐私、5下载与2ZIP通过。WORK_ROOT下需保存 `baseline-sha256.json`（本目录baseline46清单副本）与 `standalone-prepared-sha256.json`。
- `python test_merge_guard.py ARTICLE_SOURCE BASELINE46`：旧正文/摘要、图文、query中的模拟用户编辑保留；重复合并、ID或query冲突及数量异常均在写入前拒绝。
- `node test_reader_routes.mjs PORTAL_REPORT_DIR`：研究/全文/样板路由、URL往返、47/67/2数量、AI30筛选逻辑及首次时间排序通过。这不是浏览器交互测试。
- 门户为47篇研究、67份全文、2样板、AI30、97queries；单篇为1篇、1份全文、2queries。单篇241项非内容官方文件不变。门户85项文本载荷、单篇14项载荷递归隐私检查通过。
- 受保护官方runtime SHA256为 `b1771584910da746d0cf1b967a4889fee226053d841596104b457a04a2dd3d91`。最终字节/hash与范围详见 `build-qa.json`。

## 未完成或独立验收的范围

静态检查和官方构建不证明视觉或真实浏览器交互。本轮独立QA已实际重新核对四份主源、最终全文与编译数据、旧内容保护、冲突前置拒绝、路由和受保护runtime，均通过；详见 `independent-qa.json` 与 `technical-review.json`。官方split HTTP预览虽在执行器启动，云浏览器访问仍返回 `ERR_CONNECTION_REFUSED`，因此桌面视觉与交互未完成、手机未测，没有用替代浏览器或重新托管绕过。视觉、手机、来源面板操作、完整门户相邻导航、打印、真实断网和全部下载点击须以独立QA记录为准；本文件不把待测项目写成通过。此前云浏览器本地预览连接失败、本地Chromium受socket限制，不为本轮绕过限制或改权限。

本目录只包含脱敏小型作者源、测试与回执；不含HTML、dist、凭据、私人附件/消息ID或运行环境绝对路径。未访问此前403原站、未发布、未改权限、未替换旧受限附件。原站仍只能引用最后核验v19的20/40/2、AI9。本地47篇不是线上数量。第21—47篇27项新增，加第18篇视觉收银和菜品图两项同ID修订，共29项待上站；盘点、排班修订并入原篇，不另计。

完整独立HTML附件发送请求于2026-11-05 09:32 UTC被接受，不证明用户已打开或下载；详见 `delivery-receipt.json`。门户仅本地完成，未发布或作为本次附件发送。
