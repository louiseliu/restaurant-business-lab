# 第63篇ShingTik别名研究并入完整门户：本地可复建增量

## 远端归档范围：部分完成

本地完整63篇门户与独立审计已完成。远端本目录仅包含正常获准的小源码与部分QA。四项文件写入未获可核验成功：ai-weekly-calculations.log、ai-weekly-snapshot.log、audit-run.log、audit_portal.py；与audit-run.log字节相同的independent-portal-qa.json也未另行上传。原始失败详情不可用，只读回查未发现对应blob，未重试或改用其他接口。完整本地审计文件和哈希保留，不称为完整远端归档。缺件清单及哈希见archive-status.json；independent-audit/manifest.json是完整本地审计清单，不表示其所有成员已远端归档。

本轮仅将已冻结的供应商商品别名研究并入完整62篇本地门户，没有新增或改写研究。正文首次入库为2b9bb2518e851397a67f4b4ba35456b8436813f8，真实时间2026-11-06T00:08:21Z；该时间不是公开来源的发布日期。

## 输入和复建

本目录只存增量脚本、冻结基线指纹、测试与真实QA，不含HTML、ZIP、dist、完整运行时、缓存或私人绝对路径。需要可读的完整62篇门户基线及兼容的官方Data构建工具。本目录不是全部历史源码的独立镜像，也不恢复不可读的旧版本或未归档编辑。

1. 使用reports/supplier-alias-source目录作为SUPPLIER_ALIAS_SOURCE，具体归档提交见manifest.json的inputCommit。其article-entry.json、illustrated-story.json及article-reviewed-data.json作为只读冻结输入。正文和来源可在首次提交的research/2026-11-06-supplier-alias-mapping/目录核验。
2. 在新的PRODUCTION_DIR中放置本目录为portal-archive-source，运行python portal-archive-source/prepare_portal.py PRODUCTION_DIR EXISTING_PORTAL62。先验证全部340项基线文件指纹；基线存在新编辑或目标已经存在则拒绝，不覆盖。先保存、审查新编辑再另行合并。
3. 运行python portal-archive-source/build_portal.py PRODUCTION_DIR SUPPLIER_ALIAS_SOURCE NODE DATA_APP_MJS SANITIZATION_DIR。NODE为官方Node，DATA_APP_MJS为官方scripts/data-app.mjs，SANITIZATION_DIR可使用SUPPLIER_ALIAS_SOURCE/support。
4. 合并先检查所有身份、query、组件、CSS及预览文件冲突，通过后追加一篇、两项query及三个图文源码文件。只在作者图文reader中增加该篇分支，主门户reader、主题、时间线、导出偏好、稳定身份、受保护运行时与旧内容不变。
5. 脱敏检查只读执行。buildStatus设为complete后运行官方prepare、build --separate-data、export-offline。子进程移除可选会话标记环境变量；输出PRODUCTION_DIR/timeline63-supplier-alias.html仅本地保存。
6. test_portal_preservation.py验证旧对象、冻结正文和来源、两图行与组件绑定、编译JSON、两项样板及五项下载、递归ZIP CRC和内部release manifest、数据载荷和隐私模式；test_reader_routes.mjs实际运行路由辅助函数及URL往返、目录数量、AI分类与新旧时间排序。它们不代表浏览器交互或视觉验收。

## 已完成的验证

63篇研究、83份完整原文、63篇图文、2个样板、AI41、129项queries。原82份原文、62篇图文、127项queries及336项无需变更的基线文件逐项不变。legacy、主门户reader、两份内嵌HTML及五项下载全部保持。主构建测试扫描165项文本载荷，检查两个递归ZIP和一份内部release manifest。独立审计另扫描167项载荷，包括22个解码JSON与文本data-URI；两个ZIP共45个成员、两份清单的43个条目全部核验。

完整HTML为13,779,964字节，SHA256：0476bca422a967990ff2a3da045be667852c150c33562ff0c05bc52102d39c34。新的无dist、缓存或node_modules目录通过同一脚本完成官方prepare→build→export以及全部测试，HTML逐字相同，见portal-reproducibility.json。

防覆盖测试模拟既有正文、摘要、图文lead、query来源标签及导出偏好编辑，均被保留；重复合并及身份、query、计数、组件、样式、来源预览与符号链接冲突均在写入前拒绝。初始远端基线归档的15个文件逐项Git blob核验；前一轮62篇历史保留检查重新通过。见baseline-verification.json。

旧Fourth图文共享S2标题遗漏第19页，第二图注释和定义含正确页码。为保持旧内容与已发送单篇一致，本轮不改写该非阻塞显示缺项。

独立审计还实际复跑外卖样板45项测试并重建相同HTML；AI周报16项测试、107数值预期及78项勾稽通过，13份输入/结果/SQL复算字节一致。AI样板HTML没有重新编译；重生成snapshot仅生命周期buildStatus和id不同，内容字段相同。见independent-audit/README.md和原始小型日志。

## 未验证或未执行

浏览器视觉、窄屏、深浅主题、来源面板、点击导航/历史/滚动、编辑持久化、下载点击、打印、真实断网与浏览器日志未验。既有HTTP ERR_CONNECTION_REFUSED及file协议拒绝继续保留；未重试、换路、重新托管、修改安全设置或访问受限原站。

未上传、发送或归档本完整门户HTML/ZIP，未发布站点或改权限。原站最后验收记录仍v19，20研究/40全文/2样板、AI9；当前可读性未复核，45项待同步。本地63篇完成不能称为线上已更新。历史附件替换、旧全站离线快照、原站用户编辑和既有待办继续保留。
