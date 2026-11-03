# AI客服暂停与恢复：第40篇完整独立图文

研究ID：research-2026-11-03-service-handoff-note。首次提交98fa4044144f56ec5d6b22bf25ea5bef5e6fee74，首次入库2026-11-03T11:10:36Z。正文SHA256：a0f7b6d072401409a1383388da56058901667426f8d71d8571a3dfd2afdb3332。

本文区分AI是否发言、人工处理责任与咨询完成。12小时仅是经营者单方自报设置，不是最佳参数。LINE事件重送和发送取消边界是平台机制，不等于该店已实现、缺失或发生事故。没有顾客资料、产品实测、成本收益推算或新增Pro咨询。

## 独立图文复建

复用已保存的官方Data作者项目，先保留原件。运行 reports/batch-2026-10-30/shared/prepare_article.py，第一个参数是本包service-handoff目录，第二个参数必须为独立项目的src目录，不能传项目根。将本包ReportContent.jsx、IllustratedArticle.jsx、HandoffDiagrams.jsx、illustrated.css、timeline.css、handoff-diagrams.css复制到项目src/content/report。

按官方Data helper执行prepare、build --separate-data和export-offline，导出只放项目.data-app-offline/exports目录。交付副本使用既有sanitize_export.py移除可选本地线程meta，不修改受保护runtime。

图1区分自动答疑、请求人工、人工处理中和确认恢复的发言与责任。图2以假设持续跟进咨询，比较定时暂停与处理进度的两条线。均为原创React/CSS机制图，绑定独立reviewed rows和固定来源；不画虚构时长、效果率或收益，也不暗示必须购买工单。正文四节论证逐段保留，另附完整冻结原文。

## 实际验收

test_article.py解码最终HTML编译JSON，验证仅本篇、完整正文逐字一致、真实首次Git时间、四节论证、两图两query和三来源。test_routes.py检查单篇默认目标、11个锚点、目录、原文自动展开与北京时间。源文件与HTML检查不含私人路径、协作定位或外部网络资产。

最终安全独立HTML：2,921,745字节。SHA256：94d6a0ef1a5638d632ae01699158f9072403acf754c6bebfe35bcc32e35e49b4。官方构建、离线导出、静态数据及路由检查通过。

许可官方静态dist预览中实际验收桌面首页、两幅机制图、目录到完整原文并自动展开、回顶部、图解来源面板的定义/两行数据/证据链以及关闭操作。手机未实测：许可浏览器无视口尺寸设置。800px与680px响应式断点仅静态检查，不能代替手机验收；打印未测。

## 门户与发布边界

门户采用增量整合，不能以本包独立ReportContent或IllustratedArticle覆盖旧门户。完整门户复建和验收见timeline/BUILD.md。保留旧正文、图文、UI/Legacy、两个样板与下载载荷，并按首次入库时间倒序。原公开站最后核验仍v19 20/40/2、AI9，本轮未复测受限原站、发布或改权限。大型HTML的GitHub归档未完成且未发起，不是等待审批；旧全站离线快照不变。完整独立附件发送请求于2026-11-03T11:15:42.016536Z被接受，不代表用户已经打开或下载；附件私人定位不纳入公开归档。
