# 盘点识别：同 ID 持续复查修订

文章 ID 保持 research-2026-11-01-inventory-capture-note，首次入库 2026-11-01T13:03:33Z，首次提交 7754605220237525f8e76c522d747b2ade7efe41。本目录归档修订源码。JSON与QA保留HTML制作时的冻结状态，其中“尚未提交”和空提交字段不代表后续归档未发生；后续归档以本目录Git历史为准。原固定链接仅指向首次版本。新版HTML已制作、原附件同身份更新已完成，2026-11-03T03:10:40Z附件发送请求已接受，不代表已打开，站点未更新，大型HTML未归档。

../../research/2026-11-01-inventory-capture/note.md 是完整冻结正文，SHA256 为 361ddd7a23696f9c32735d44e39051c225ebb8da80ab6085438d911cbb7166b2。保留原两图及四个解释段落，新增持续复查机制图与星巴克官方推出记录、路透社后续报道。新增图是研究建议，不是品牌制度；不将停用归因于单一识别错误，不作中国门店收益结论。

使用已存在的官方 Data 作者项目副本。先运行研究院 reports/batch-2026-10-30/shared/prepare_article.py，以 inventory-capture 为第一参数、作者项目的 src 目录为第二参数。随后将本包 IllustratedArticle.jsx、ReportContent.jsx、illustrated.css、timeline.css 复制到 src/content/report。不得将项目根误传给 exporter，否则会误导出旧整站。

按已安装官方 Data 工作流 prepare、build --separate-data、export-offline 生成单文件，导出路径须在项目 .data-app-offline/exports 内，再对交付副本用已有 sanitize_export.py 移除可选本地线程标签。不要改受保护运行时。此包不包含大型 HTML 或第三方图片。

静态验收：解码最终 HTML 的 JSON.parse 模块，断言只有目标一篇，正文与冻结文件逐字一致；三图与三个查询节点一致；原两图和原四段保持；首次时间不变，来源三项完整。递归检查源码、HTML、嵌入 base64 与 JSON，未发现私人会话链接或内部定位。完整 HTML 为 2919773 字节，SHA256 7ba64d0fbc18833fabe7888122482d84fc06f573815ed7a93bc2a1e6c9fb5ea3。

视觉验收未完成：许可浏览器打开本地预览返回 ERR_CONNECTION_REFUSED，未绕过或改用其他浏览器接口；桌面/手机布局、点击、全文展开和来源操作仍待可达环境实测。此限制不能由静态测试替代。

正文与来源不重复复制，分别复用 ../../research/2026-11-01-inventory-capture/note.md 和 sources.json；需要构建时将二者置入工作包根目录。旧两图及四段对照使用 ../inventory-capture-source/inventory-capture/，不重复归档original副本。QA.json是本次HTML生成时的静态检查回执，不代表视觉验收或交付成功。
