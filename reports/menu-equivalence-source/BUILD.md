# 菜单组合与厨房信息：完整图文及第55篇本地增量

正文固定于 research/2026-11-05-menu-equivalence/note.md，首次提交 `1f2822ac58d20e678aaaa7300724a10dcd3d8c8c`，首次UTC `2026-11-05T17:08:13Z`，SHA256 `1c3eefd531526f4f3f3e8a840e0f94e393dcbc3c26801f81de64cab85d2e55ae`。首次入库显示北京时间2026-11-06 01:08，不当作来源发布日期。保留五节论证、研究说明与完整原文。

图1比较商品选项与套餐子项，图2比较全部套餐子项合计与每份套餐个别数量；均为原创机制示意，不是产品截图、当前版本修复或门店实测。图2明确厨房联须先选择相同商品显示总数，才出现子项数量设置；集中/分开排列另行设置。两份锅物与三份肉是作者模拟，无售价。六个来源入口分属经营主体与供应商，不当作六项独立效果证据。图2证据范围仅为厨房联说明与作者分析。

## 复建

1. 取得固定提交正文，运行 `python make_article.py NOTE_MD frozen.json`；校验正文哈希并生成完整叙事、六条来源预览和两项reviewed queries。
2. 用官方prepare-data-app.mjs以article-reviewed-data.json准备新的report，保存准备后指纹standalone-prepared-sha256.json，再运行prepare_standalone.py。保留官方身份与运行时。
3. 复制完整54篇门户为隔离基线与工作副本。基线完整HTML应为SHA256 `e8dc01087a3abe2bfe75dd6adc7a5cb29cc98422bafbfdee00e7a0d3d64b61e7`；保存源指纹baseline-sha256.json。运行 `python integrate55.py PORTAL/src SOURCE`。基线必须为54研究、74全文、AI36、111queries；重复、计数或身份冲突在写入前拒绝，保留已有内容和编辑。
4. 执行既有公共内容脱敏测试与sanitize_site_content.py及--check，设buildStatus为complete，运行官方data-app.mjs prepare、build --separate-data和export-offline。离线导出位于.data-app-offline/exports，交付副本只移除可选本地thread元数据。
5. 运行test_preservation.py（制作目录、基线、冻结正文）、test_merge_guard.py（源码、基线）、test_reader_routes.mjs（门户report目录）。HTML、dist、ZIP、缓存与私人运行元数据不入Git。

## 验证与边界

全文及冻结哈希、六条来源预览、两图和query一致性、官方构建、完整离线导出、manifest、递归隐私、旧内容保护、合并冲突拒绝及路由函数测试通过。门户55研究/75全文/2样板、AI36、113queries。保留旧74份全文、54篇图文、111项queries，5下载载荷与2ZIP完整；文件保留数量以build-qa.json为准。

单篇完成支持的管理式本地预览：首屏、两图、图二来源面板、两行数据与厨房联证据范围、完整原文展开、返回顶部及目录图解跳转。截图未见裁切或重叠。未检查浏览器完整日志，不声称无运行错误；手机/窄屏、完整门户视觉与交互、逐节截图、主题和编辑持久化、全部下载点击、打印及真实断网未测。静态检查不替代这些未做验收。

保留检查仅证明可读已归档54篇基线被保持，不证明缺失历史或未归档编辑已经恢复。原公开站仍只能引用最后核验v19的20/40/2、AI9；本轮未访问受限原站、同步、发布或改变权限。第21—55篇35项新增加两项同ID修订，共37项待同步。既有附件替换、费用旧归档、原站可读性与用户编辑保护、旧全站离线快照待办独立保留。附件保存及发送由后续真实回执确认。
