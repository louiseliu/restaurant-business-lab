# AI听懂“老样子”以后，谁确认下单的是哪款货：单篇图文作者源

本目录保存冻结正文、来源台账、两幅原创定性图、生成器和作者阅读界面。首次正文提交与真实时间由 frozen.json 记录；没有审校冻结、固定提交、真实时间或匹配的正文与来源哈希时，生成器拒绝继续。正文及来源中的早期研究状态保留原文，当前交付状态另记。

图一按自由叫法、商品候选、属性证据和澄清/复核四层展开；图二比较高频稳定、低频简单、频繁替换且无人维护三种采购情景。图中判断路径与条件比较均为作者分析，不冒充ShingTik的实际软件流程、合同分工或成效。实施方自报的糕点照片误配不能延伸成已错发、含真实虾类或食安事故。照片订单的事前确认不推广到所有订单；WhatsApp上线与Order Page/Portal在建保持区分。

## 兼容官方工具复建

需要Python 3、Node和兼容官方Data analytics插件。完整运行时不随作者增量源归档，不安装替代渲染器。

1. 把本目录作者文件置于生产目录的source/。从frozen.json固定提交读取research/2026-11-06-supplier-alias-mapping/note.md及sources.md，或使用本目录逐字保留的副本。运行`python source/make_article.py source/note.md source/frozen.json`。
2. 使用官方`prepare-data-app.mjs --surface report --output PROJECT --snapshot PRODUCTION/source/article-reviewed-data.json`创建新工程。阅读生成工程AGENTS.md和返回的组件文档。将准备后全部文件的相对路径与SHA256记录为PRODUCTION/standalone-prepared-sha256.json，再运行`python source/prepare_standalone.py PROJECT`。新报告使用官方生成的稳定身份，不能覆盖多篇门户或不同作者内容。
3. 运行`python source/support/test_sanitization.py`，并对PROJECT/src/content/report运行sanitize_site_content.py及其`--check`。内容完成后将PROJECT/src/data.json的buildStatus设为complete。用官方data-app.mjs执行prepare和`build --separate-data`，不修改受保护运行时。
4. 用官方`export-offline --project-dir PROJECT --output PROJECT/.data-app-offline/exports/supplier-alias.html`导出，再将产物复制到生产目录。构建环境不得注入本地线程身份；如果官方导出携带身份标签，最终副本须去除该标签并重新核验隐私，不改变受保护源代码。
5. PROJECT应对应PRODUCTION/standalone。运行`python source/test_standalone.py PRODUCTION source/note.md`，并在一次性副本用test_authoring_guard.py验证防覆盖。复建的随机报告身份或官方版本可能影响HTML哈希，必须检查新结果，不能沿用历史产物哈希。

## 验证与交付边界

build-qa.json记录实际完成的正文、来源作用范围、图与query绑定、编译数据、官方文件保护、隐私及构建清单检查。generator-reproducibility.json和authoring-guard-qa.json分别记录生成器复算和八项防覆盖场景。静态检查不能证明布局、浏览器交互、打印或真正离线行为正常。

visual-qa-status.json明确记录浏览器视觉与交互未验。现有本地HTTP连接失败与历史file协议拒绝仍为限制；本步骤不重试、不换路、不重新托管、不更改安全设置。单篇构建不意味着完整门户已更新，更不意味着原站已同步。

本任务不发布、不改权限、不上传或归档大HTML/ZIP。不保存原网页缓存、私人路径、身份、私链或凭据。manifest.json记录小型作者文件的字节和哈希；附件保存、发送和远端归档结果另记，不能把构建成功或发送请求接受说成用户已收到或打开。

## 独立审校与历史台账说明

independent-qa.json记录独立静态审校，包括三份公开原页回读和冻结正文远端核验；不代表浏览器视觉或交互验收。sources.md中未提交、未制作图文的说法是首次研究阶段历史记录，正文和台账保持冻结，后续状态见delivery-status.json。单篇附件发送请求于2026-11-06T00:13:09Z被接受，不代表已送达、打开或下载。

归档验证再次执行完整单篇静态检查、八项防覆盖测试、三项脱敏单元测试及临时目录作者JSON逐字复算。防覆盖测试参数为已完成的PROJECT，而不是其上层PRODUCTION目录。未重新执行全新官方运行时构建，不声称新增浏览器验收。
