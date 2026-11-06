# 65篇门户独立静态审计

结论：在下列静态核验范围内通过，未发现新增内容阻断项。此结论不代表浏览器视觉或交互验收通过。

## 唯一受审版本

- 文件：`timeline65-discovery-qsmart.html`
- 大小：13,892,324字节
- SHA-256：`f033d638d659037cb96f0e062784c55c5451622c90a8793ed4c3244b97b97305`

后续修改须另行核验，不得沿用本报告为其他HTML版本背书。

## 实际完成的核验

- 65篇研究、85篇全文、65篇图文故事、2个样板、43篇AI研究和134条查询，身份唯一，按首次入库时间排序。
- 83篇其他全文、63篇其他故事、131条原查询未变。346份冻结基线文件中342份未变，原有文件仅有4处预定修改，新增5份限定用途组件文件。主阅读器及历史读本逐字保留。
- GEO全文及6节正文对应首次提交 `40e158a2766f7edd8e3d684b66436dd197624ecb`，两图与各自来源和查询一致。`3÷34×100`复算为约8.8%；未把服务商自报写成净增量、因果或利润验证。
- Q-Smart同ID补充保留原文前缀、原图文全部字段、原两图和首次入库时间。修订正文与来源台账的Git blob与本次独立读取的固定提交一致。两项补充来源只绑定新增补充图查询，不进入原查询。
- 134条查询均有对应图文或历史组件。HTML编译后的目录、故事和样板与源数据一致。离线6段数据拼接为351,068字节，与完整源数据逐字一致；现有构建清单及离线导出字节校验通过。
- 检查174份内容载荷、2份内嵌HTML和5个下载文件；递归检查2个ZIP中的45个成员，核验1份release manifest。未检出实际私人路径、私人会话或常见凭据格式。模式扫描不构成对所有可能敏感信息的形式化保证。
- 对20项冻结输入检查字节数与哈希；在临时副本独立重跑17项合并保护和20项冻结输入篡改测试，均通过。只读路由解析、筛选与排序测试通过，不等于浏览器导航行为已验。
- 独立读取远端基线清单，核对19份可读归档回执的Git blob及清单哈希。未将尚不可核验的历史归档补写为成功。

审计脚本共执行1,432项检查。详见 `portal65-static-audit.json`；`manifest.json`记录本套审计文件的字节数和SHA-256。

## 保留的问题与未验范围

- 第四处共用S2来源标题仍未列第19页，属于本轮未修改的既有展示问题，不声称已经解决。
- 基线保留仅覆盖可读的本地64篇版本，不代表取回或保留了无法读取的原站编辑及历史文件。历史不确定审计归档仍待解决，本次未重试或复制其内容。
- 未打开浏览器或原站；未验桌面与手机渲染、暗色主题、实际无障碍表现、来源弹窗、导航回退与滚动、编辑、打印或导出交互。
- 未重新编译，未重新执行内嵌经营计算器或周报运算；只检查现有输出、数据、哈希、清单及保留关系。
- 未重新读取外部原始网页、受限PDF、商家后台或论文原始数据，未验证经营成效或因果关系。
- 未上传、发布或核验在线分享权限。

## 复核方式

本目录不是自包含的门户或复建包。复跑需要完整的受审版本、可读冻结基线、两组文章输入及以下外部依赖；本次小文件归档不包含这些大文件，也不补齐历史不可读文件。

使用Python标准库，且需在PATH中提供可用的Node。将占位符替换为对应的已存在目录，使用单独的审计输出目录：

```sh
python audit_portal65.py \
  --production <production> \
  --original-baseline <original-baseline> \
  --geo <geo-source> \
  --qsmart <qsmart-source> \
  --output <audit-output>
```

所需文件关系：

- `<production>`包含本报告指定哈希的`timeline65-discovery-qsmart.html`、完整`portal65/`、完整`baseline64/`、`baseline64-sha256.json`、`baseline-remote-files.json`和`portal-archive-source/`。`portal65/`须保留`src/`、`dist/`及`.data-app-offline/exports/timeline65-discovery-qsmart.html`。
- `portal-archive-source/`须包含本轮的`integrate65.py`、`reader_patch.py`、`input-fingerprints.json`、`test_portal_merge_guard.py`、`test_frozen_input_guards.py`和`test_reader_routes.mjs`。前两类保护测试会复制到临时目录后运行。
- `<original-baseline>`为原始可读64篇完整项目，用于核对冻结副本未被改写；不能用任意新建同名目录替代。
- `<geo-source>`和`<qsmart-source>`分别为冻结的GEO小源码与Q-Smart同ID修订小源码，须包含正文、来源、文章与图文JSON、查询JSON及对应组件。20项输入应符合`input-fingerprints.json`。

### 19份基线远端读取回执

`<production>/baseline-remote-files.json`是外部输入，未随本审计小目录归档。其来源固定为仓库`louiseliu/restaurant-business-lab`的提交`d7c47b97d6f63175fa7498c464b5e3d5a01aa8d8`，目录为`reports/camera-reuse-portal-source/`。不要改用浮动分支或后来版本。

需要构造UTF-8 JSON数组：先读取该目录的`manifest.json`，再读取其`files`字段列出的18项文件，共19项。每项至少保留以下字段，其他读取工具返回字段可以保留：

```json
[
  {
    "path": "reports/camera-reuse-portal-source/PORTAL_BUILD.md",
    "content": "该固定提交中此文件的完整UTF-8文本，保持原始换行与尾部换行",
    "sha": "GitHub返回的该文件Git blob SHA-1"
  }
]
```

`sha`不是提交号或SHA-256。脚本重算每项Git blob SHA-1，并用远端清单核验其余18项的字节数和SHA-256。`manifest.json`本身的预期Git blob为`b3f6a0597b57e24b234ea70b521e050ec5e8df4b`，已在本次审计中独立读取核对。这里只说明如何准备已有审计的输入，不表示本轮又重新请求了所有19项，更不授权重试其他历史不确定写入。

脚本不访问网络或浏览器，只写入指定审计输出目录及自动清理的临时测试副本，不修改生产内容。缺少上述完整依赖时，不能声称已经复跑或验证通过。
