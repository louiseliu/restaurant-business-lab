# 第57篇完整门户的本地增量复建

## 固定输入与基线

- 正文/来源固定提交：7d24196f2e5ab9868d4a3fd024618cc1d7eccc7f；已有小作者源：ac143694258318dcff51e9a357e21b8aaf126311。
- 正文和sources哈希见 frozen.json，时间使用首次入库2026-11-05T19:11:27Z，不冒充来源发布日期。
- 已核验56篇门户离线HTML SHA256：8cf61555433c92e8328f4e695c5f122f1b5b9f1e0b048d925f4b0db24fca6a32。基线为56研究/76全文/2样板/AI36/115queries；源文件指纹见 baseline56-sha256.json。
- integrate57.py复用仓库当前satellite-store增量流程；构建仍使用当前安装的官方Data工具，不改受保护运行时，不覆盖旧文或用户UI。

## 本地步骤

1. 准备制作目录PRODUCTION_DIR，其中source含本目录小作者源、standalone保留已验证单篇；正文NOTE_MD旁为sources.md。取可读且完整的56篇门户源，保留原件，将其复制为baseline56与portal57。复制时排除dist、.data-app-offline、node_modules、缓存；不要在既有用户工作副本上直接覆盖。核对baseline56-sha256.json并在制作目录保存同一份。该指纹是本次固定基线，不代表缺失历史编辑被恢复。
2. 运行 python source/build_portal.py PRODUCTION_DIR NOTE_MD NODE DATA_APP_MJS SANITIZATION_DIR。后三项为环境中官方Node绝对路径、官方data-app.mjs及仓库reports/public-site-sanitization目录。脚本无网络、上传或发布调用。
3. 脚本先测试冲突拒绝，再增量整合；要求76原文/56图文/115queries及AI36，校验新身份、冻结正文、时间、两图query一致性，在任何写入之前拒绝重复或新文件同名冲突（包括符号链接）。原有body、excerpt、story、query编辑应保留。
4. 运行既有脱敏测试、sanitize_site_content.py及--check；将buildStatus置complete，再用官方prepare、build --separate-data、export-offline。为公开候选去除构建子进程的可选会话环境；必须使用无旧dist的新工作副本，避免工具继承旧构建的本地线程元数据。保留生成的原始manifest，不手写或放宽校验。离线文件在.data-app-offline/exports生成，复制为timeline57-kitchen-label.html。
5. test_portal_preservation.py检验完整冻结叙事及来源、query范围、旧内容/文件/身份、排序、legacy、嵌入样板、5下载、递归ZIP/CRC与内部manifest、编译JSON和dist清单/脱敏。test_reader_routes.mjs运行真实路由辅助函数及计数/排序检查。test_portal_merge_guard.py在临时副本验证用户编辑保留及冲突零写入。

## 当前产物与未验范围

本地门户：57研究/77全文/2样板/AI37/117queries。旧76原文、56图文、115queries保持；318项非必要变更基线文件保持。HTML为13,510,333字节，SHA256为9cdafd346a247ea3f0cbe1ae2a107fd4580b4b84c4bdecac2a36637944f2d0dd。

本地静态与官方构建检查通过；完整门户的浏览器渲染、导航历史/滚动、窄屏、主题/编辑持久化、所有下载点击、打印、真实断网与完整浏览器错误日志未验。单篇原有视觉记录仅覆盖单篇，不等于门户验收。

原站同步此前受限，本轮没有访问或重试、没有换站发布、没有改变权限；最后核验原站仍为v19的20/40/2、AI9，当前可读性未复核。39项待同步及历史归档/附件待办仍独立存在。小作者源只含公开内容、方法和QA，不含HTML、ZIP、dist、缓存、私人元数据。此目录不是完整56篇运行时仓库的替代品；完整复建仍需要上述可读基线与兼容官方工具。
