# 低销量与可售记录：第37篇完整图文

正文首次提交7e152c427d672618f8fab223a6ddf6e0111d356a，首次入库2026-11-02T14:16:18Z。stockout-demand目录包含冻结全文、两幅原创机制图、来源及reviewed queries。图1区分缺料停售、正常可售至收档、主动限量/关闭渠道；图2按可售记录状态分流后续决定。均为研究者示意，无虚构丢失订单、销量、利润或餐饮产品故障判断。

直接保留上轮第36篇完整作者源码与全部既有内容；不需恢复早期快照。逐项比较确认旧56份原文、36图文及其他UI/Legacy/嵌入样板/下载载荷未变。新增后本地37研究／57原文／2样板，AI22；排序依首次入库时间。正式同步前仍须核对远端用户编辑。

复用reports/batch-2026-10-30/shared/prepare_article.py与sync_illustrated_queries.py。prepare_article.py参数为独立PROJECT/src；单篇新稳定report ID，不改变旧时间线身份。官方separate-data编译与export-offline导出，导出后仅移除可选本地线程meta，不改运行时。新HTML为独立完整文章，不是全部门户或摘要。

```sh
python test_article.py "$OFFLINE_HTML"
node test_reader_routes.mjs "$REPORT_DIR"
```

验证：冻结正文SHA及首次Git/时间、连贯图文可重建全部原文；两图绑定两条query；最终HTML编译数据解码只含第37篇，默认直接单篇；本地37/57/2及AI22、倒序与路由通过。73项文本载荷和2个ZIP内文件脱敏检查通过；嵌入样板及下载文件哈希复核通过。

CUA本次访问localhost4187返回ERR_CONNECTION_REFUSED；未通过其他浏览器接口绕过。桌面/移动视觉与点击实测未完成，静态通过不等于视觉完成。

大型HTML GitHub归档未完成，未发起上传。未更新线上站点或访问权限；最后已核验线上v19为20/40/2、AI9，本地增量不等于已上站。附件交付状态见publication-receipt.json。
