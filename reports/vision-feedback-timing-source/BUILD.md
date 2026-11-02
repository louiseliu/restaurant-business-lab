# AI品控反馈时间：独立图文与本地增量

首次正文提交 cb1d36b11f6d6166cf6e0cbff81bca3fc96da65b，首次入库 2026-11-02T09:29:26Z。完整冻结正文、两幅原创机制图和来源绑定于 vision-feedback-timing 目录。图一为同步与异步路径的研究示意，图二为验收建议；品牌按日反馈是2025年自述，非独立收益验证。

复用 reports/batch-2026-10-30/shared/prepare_article.py、apply_batch.py、sync_illustrated_queries.py及既有受保护Data运行时。独立官方report使用新稳定ID，时间线保留既有ID。按官方separate-data构建及export-offline导出；仅移除可选本地线程meta，不改运行时。

早期本地快照保留42份原文、22篇图文、46查询和所有其他UI/Legacy/sample/download文件；第23–34篇从固定 d310d5ad0bbb84fc062610fdd2dbad800ab911f6 的各reports/<slug>-source恢复36小文件并逐一核对Git blob SHA，再按首次入库合并；没有从旧附件覆盖基线。新增后本地35篇研究／55份原文／2样板、AI20。正式同步前仍须核对远端最新用户改动。

```sh
python test_article.py "$OFFLINE_HTML"
node test_reader_routes.mjs "$REPORT_DIR"
```

静态检查：完整图文正文逐字重建等于冻结原文；两图绑定2条reviewed queries；路由、计数、首次时间倒序、文章跳转、35篇完整图文覆盖通过；53个正文、Legacy、样板与解码ZIP等载荷脱敏和校验通过；独立HTML检查2个base64文本载荷。

本轮视觉预览未完成：CUA访问本地预览返回ERR_CONNECTION_REFUSED，未用其他浏览器接口绕过。不将静态检查称为桌面/移动端视觉或点击实测。

独立HTML已修正为默认直接打开第35篇：编译产物中仅有该篇冻结正文，2条图解查询；最终单篇身份已核，附件发送于2026-11-02T09:38:49Z被接受；本目录只含9个小型作者源、测试及记录。不提交大型HTML，不改变站点权限、不新建站点。原站仍为最后已核验v19的20/40/2、AI9；本篇尚未上站，HTML GitHub归档未完成。
