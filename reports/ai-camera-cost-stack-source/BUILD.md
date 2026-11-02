# 后厨AI接口成本：独立图文与本地增量

首次正文提交2adfee7edeb9b6598c38560de8d5bedfee0364f7，首次入库2026-11-02T13:20:53Z。ai-camera-cost-stack目录保留完整冻结正文、两幅原创机制图、来源和reviewed queries。成本层次不作金额占比；取图观察时点为条件示意，不作漏检率或食品安全保证。

复用reports/batch-2026-10-30/shared/prepare_article.py、apply_batch.py、sync_illustrated_queries.py及既有受保护Data运行时。prepare_article.py的目标必须是独立PROJECT/src，不能传项目根目录。单篇新稳定report ID；时间线保留已有ID。官方separate-data构建和export-offline导出，仅移除可选本地线程meta，不改运行时。

早期本地快照42原文、22图文及所有其他UI/Legacy/sample/download文件逐字保留。第23–35篇从固定02eeb32b0702cc59381d73d6018db3e1ed4128b5恢复39篇内小文件、逐个核对Git blob SHA，再按首次入库合并。新增后本地36篇研究／56份原文／2样板，AI21；没有从旧附件覆盖基线。正式同步前仍须核对远端最新用户编辑。

```sh
python test_article.py "$OFFLINE_HTML"
node test_reader_routes.mjs "$REPORT_DIR"
```

静态通过：完整图文重建等于冻结正文；首次时间与Git；两原创图绑定2条query；最终编译HTML解码仅含第36篇，默认直接打开单篇；路由、倒序、36/56/2及AI21；73项文本载荷包含2个ZIP内文件脱敏及下载哈希校验。

CUA本地预览返回ERR_CONNECTION_REFUSED，未用其他浏览器接口绕过。桌面与移动端视觉及点击实测尚未完成，静态通过不等于视觉验证。

HTML 已经生成，2026-11-02T13:27:49Z 附件发送请求已被接受；不等于用户已打开或下载。本目录只存9小型作者源、测试及记录。大型HTML GitHub归档未完成；没有发布站点、改变权限或新建站点。原站仍为最后已核验v19的20/40/2、AI9，本地36/56/2并不等于已上站。
