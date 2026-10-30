# 公开站点脱敏复建补丁

此补丁处理历史作者源中的私人 ChatGPT 协作链接与样板 HTML 的 `data-app-local-thread` 元数据。它不抓取资料、不改变事实、不调用模型、不发布站点、不改变访问权限。Python 3 标准库即可运行。不得将整站私有配置或作者工作目录一起归档。

## 放置与执行顺序

1. 依照仓库已有的阅读门户/图文文章/样板生成说明，在独立作者工程恢复最新内容与 UI。保留用户编辑，不能用旧快照覆盖当前版本。
2. **所有文章及样板嵌入/下载载荷生成后、官方 Data 构建之前**，运行本补丁。`REPORT_DIR` 是该工程的 `src/content/report` 路径，由执行者传入；本补丁不依赖任何固定工作机目录。

```sh
python reports/public-site-sanitization/test_sanitization.py
python reports/public-site-sanitization/sanitize_site_content.py "$REPORT_DIR"
python reports/public-site-sanitization/sanitize_site_content.py "$REPORT_DIR" --check
```

3. 再运行既有图文完整性、路由与样板测试，确认当前数量、首次入库倒序和旧内容保留。本次基线为 10 篇图文研究、30 篇 Markdown 全文、2 个实战样板；未来新增文章不能被固定数量测试误删。
4. 通过当前官方 Data 构建流程重新生成 split HTML/数据侧文件，并检查构建后载荷，包括所有 base64 下载、ZIP 内 HTML 和清单。旧构建产物不能直接发布。嵌入沙盒仍只允许脚本，不能为了清理元数据增加权限。
5. 由既有发布负责人沿原站发布，并重新核实用户保存的 presentation、访问范围及实际部署产物。此脚本不具备发布或共享能力。

## 精确修改范围

- `LegacyReport.jsx` 与 `articles.json`：把私人 ChatGPT `/g/`、`/c/`、`/share/` 链接替换为“私人协作会话，未公开”，不保留可点击 href。支持 Markdown、HTML anchor 和裸链接。
- 原文章 `originalBodySha256` 保留；变动正文另加 `renderedBodySha256` 和脱敏说明。两种 hash 不可混称。
- `samples.json`：清理嵌入 HTML、可下载 HTML，以及 ZIP 内 HTML/Markdown/文本；移除本地 thread meta，不更改计算代码与数值。更新下载校验值和 ZIP 内 `release-manifest.json` 对应文件的字节数/hash。
- 不修改研究故事、reviewed 数据、UI、runtime、站点身份、账号或访问配置。

脚本可重复执行：已清理的输入不会再次改动。ZIP 封装与清单说明可能随生成器版本产生不同字节，因此复建后应使用本次输出的新 hash，不能声称与历史 ZIP 逐字相同；HTML 计算与数据必须保持一致。

## 验证与范围限制

已实跑 3 个测试方法：三种链接形式、仅移除 meta、嵌套 ZIP/清单校验、原文/rendered hash 区分、非敏感 CSV 保持、二次执行无改动。另在原有作者源的临时副本上执行，只有 Legacy、文章索引和样板载荷 3 个文件变动；30 篇中仅 1 篇协作记录正文脱敏，10 篇图文故事字节不变，2 样板校验通过。当前冻结版本 `--check` 检查 53 个内容/下载解码载荷通过。

这是针对已知泄漏面的最小补丁，不是通用秘密检测器。新增未知凭据、账号、内部路径、压缩/编码载荷或非标准清单需要独立审计；不要以测试通过代替完整公开前审查。测试只使用明确虚构的占位链接及标识，没有真实私人 URL、项目 ID 或线程 ID。运行脚本后仍需核对实际页面与离线下载可读、可操作。
