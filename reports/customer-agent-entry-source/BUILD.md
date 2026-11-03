# 顾客自有AI入口：第39篇独立完整图文

研究ID：research-2026-11-03-customer-agent-entry-note。正文首次提交90a3b9b65e399b3df0169092f1685adb857658f9，首次入库2026-11-03T07:05:31Z。正文SHA256：4096e9ea61b55452e68d4d79a07201324ac4ce83963c05f8f4531b39c5d66c91。

本文只讨论2026年4月金谷园早期AI取号实践，不代表当前版本或持续运行。三篇不同记者采访不是三个独立效果验证；一次记者体验与参与方自述分别记录，未使用经营效果数字、未知身份仓库或业务调用。图文保留四节完整论证、完整冻结原文、三条来源与首次Git时间。

## 独立图文复建

复用现有官方Data作者项目，先保留原件。运行仓库 reports/batch-2026-10-30/shared/prepare_article.py：第一个参数为本包 customer-agent-entry 目录，第二个参数必须为独立项目的src目录，不得传项目根目录。将本包ReportContent.jsx、IllustratedArticle.jsx、AgentEntryDiagrams.jsx、illustrated.css、timeline.css、agent-entry-diagrams.css复制到该项目src/content/report。

按官方Data helper执行prepare、build --separate-data、export-offline，导出到项目.data-app-offline/exports内。对交付副本使用仓库现有sanitize_export.py移除可选本地线程meta，不修改受保护运行时。

图1比较首次与再次使用的准备、当次需求、确认结果，并保留原入口退路；节点宽度不表示时长。图2并列探索学习、服务改善和新增贡献各自所需证据与投入，不画自动升级或虚构收益。两图均为原创React/CSS，绑定独立reviewed rows及固定研究来源。标题在语义逗号处换行，保持原题内容。

## 实际验收

test_article.py解码最终HTML中的编译JSON，断言仅含本篇、完整正文逐字一致、两图两query、四论证章节、三来源、首次Git和真实入库时间；检查源文件及HTML无私人定位或外部网络资产。test_routes.py检查单篇默认目标、11个锚点、目录、原文展开和北京时间显示。

最终单篇HTML为2,922,823字节，SHA256：b95a6b2ead7651f9c70b1298dccf71033f2d9347ef53eac9339633c4039283d2。官方构建与导出完成，不是旧22篇门户，也没有以摘要替代正文。

本轮采用第38篇BUILD说明的官方静态dist预览方法，实际检查桌面标题、两幅机制图、目录跳到完整原文并自动展开、图解来源面板，均正常。手机未实测：当前许可浏览器接口没有视口尺寸设置；响应式680px断点已静态检查，不冒充手机验收。未做打印或真机测试。

## 门户集成边界

本包是独立第39篇，不覆盖完整门户ReportContent或旧图解组件。本轮未恢复和测试39/59/2完整门户，门户整合明确待完成。后续应先按 reports/food-waste-measurement-source/timeline/BUILD.md 恢复38/58/2全量基线（包括第30篇同ID修订第三图），再合并本篇三JSON到articles、stories和queries；排序保留首次入库时间。门户IllustratedArticle只增加AgentEntryDiagram导入和agent-entry布局分支，不替换旧分支。保留所有旧文章、下载载荷、Legacy与两个样板，并重做旧内容保护、查询、路由、隐私及浏览器检查。

原公开站最近核实仍为v19的20篇研究、40份全文与2个样板。本轮未读取、发布或变更原站权限，本地预览成功不代表其访问限制解除。大型HTML的GitHub归档未完成且未发起；完整独立附件的发送请求于2026-11-03T07:12:58.969750Z被接受，不代表用户已经打开或下载；附件定位不进入公开仓库。


## 2026-11-03 08:04 UTC：完整门户整合续记

上节所述未整合为07:17归档时状态，后续本地完整门户已达到39/59/2、AI24，并通过官方构建、全文与旧内容保护、递归隐私及桌面重点交互验收。详见[timeline/BUILD.md](timeline/BUILD.md)。仅本地整合待办关闭，不代表上线；既有独立图文和已发送附件不变。
