# 小店菜单与补货：完整图文及第56篇本地增量

正文固定于 research/2026-11-05-satellite-store/note.md，首次提交 `7abe6d06bb77b1623488288fb24529f8c62e72da`，首次UTC `2026-11-05T18:15:37Z`，SHA256 `41019aea0f0f11b62059f05a18d629079df59c11b8b2a2c836c6c51daa44f05e`。首次入库显示北京时间2026-11-06 02:15，不冒充来源发布日期。完整保留五节论证、下一步建议、研究说明与原文。

图1比较菜单、存储、补货和缺货的条件关系；图2比较缩减独立备料商品、提高补货可靠性或频率、保留库存缓冲三种取舍。均为原创机制分析，不是品牌实测流程、产品截图或量化效果。仅一条经济观察报来源，采用小吊梨汤经营者有限自述，不把同文其他品牌算作独立验证。普通商业／供应链研究，AI篇数不增加。

独立复核后，图2标题改为“菜单、补货与库存缓冲，三种取舍怎样比较”，避免把保留缓冲归入压库存；图1注改为“图中关系”，不指称并不存在的箭头。同步query并重建复测。

## 复建

1. 取得固定提交正文，运行 `python make_article.py NOTE_MD frozen.json`。生成器校验冻结哈希，从reviewed-illustration-copy.json生成完整叙事与两项reviewed queries；单一来源预览保留准确证据范围。
2. 用官方prepare-data-app.mjs，以article-reviewed-data.json准备新report，记录准备后指纹standalone-prepared-sha256.json，再运行prepare_standalone.py。保留官方身份和运行时。
3. 复制完整55篇门户为隔离基线和工作副本。基线完整HTML SHA256应为 `7999717bb8c2f798c63ae48893ffff7ab8d4182065197cabd79051cce00ce043`。保存源指纹baseline-sha256.json，运行 `python integrate56.py PORTAL/src SOURCE`。要求55研究、75全文、AI36、113queries；重复、计数和身份冲突在写入前拒绝，保留已有内容及编辑。
4. 生成内容后执行既有公共内容脱敏测试、sanitize_site_content.py及--check；设buildStatus为complete，运行官方data-app.mjs prepare、build --separate-data、export-offline。离线导出置于.data-app-offline/exports；交付副本只移除可选本地thread元数据。HTML、dist、ZIP、缓存及私人运行元数据不入Git。
5. 运行test_preservation.py（制作目录、基线、冻结正文）、test_merge_guard.py（源码、基线）和test_reader_routes.mjs（门户report目录）。后续文字修订需保持原文冻结、同步story及queries，重新构建和核验。

## 验证与边界

完整冻结原文、七节图文叙事、单一来源、两图与query一致性、官方构建和离线导出、manifest、递归隐私、旧内容保护、合并冲突拒绝及路由函数检查通过。完整门户56研究/76全文/2样板，AI36，115queries。旧75份全文、55图文、113queries和315项非必要变更文件保持，5下载载荷和2ZIP完整；单篇241项非内容官方文件保持。

单篇完成支持的管理式预览有限桌面检查：首屏及首次时间、两图与本轮修订、目录展开及图解跳转、图2来源面板/三行数据/证据链、完整原文展开和返回顶部。观察到既有阅读器把部分Markdown加粗分隔符 ** 直接显示，正文仍完整可读；未修改保护运行时或旧UI。手机或窄屏、完整门户浏览器视觉交互、逐节截图、主题与编辑持久化、全部下载点击、打印、真实断网和完整浏览器错误日志未验。不声称全部视觉交互通过或浏览器无错。

保护检查仅证明可读已归档55篇基线被保持，不证明缺失历史或未归档用户编辑已恢复。原公开站仍只能引用最后核验v19的20/40/2、AI9；本轮未访问受限原站、同步、发布或改变权限。第21—56篇36项新增加两项同ID修订，共38项待同步。既有附件替换、费用旧归档、原站可读性与用户编辑保护、旧全站离线快照待办独立保留。附件保存及发送以真实回执另行确认。
