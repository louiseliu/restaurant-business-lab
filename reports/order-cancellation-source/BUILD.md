# 订单取消图文：官方构建已恢复

研究ID：research-2026-11-03-order-cancellation-note。首次研究提交49bce5efc9fbf2d69d9fd922480f7690d07eae1f，首次入库2026-11-03T18:00:26Z；冻结正文SHA256为2ee3e6e5d9034614a32160bfa992d3186860fa2e153164af023273fbc4a7844b。普通数字化机制分析，不计AI案例。

2026-11-04，已恢复的官方Data helper通过prepare、build --separate-data及export-offline。不需要Vite依赖安装，没有源码fallback、受保护runtime修改或站点发布。单篇含完整冻结正文、四节、两幅机制图、两query和三来源，最终HTML已解码核验只包含本篇；隐私与数据绑定静态检查通过。浏览器验收与附件交付状态须看各自回执，不由构建成功推断。

## 单篇复建

保留既有完整门户，在独立官方Data作者项目的src/content/report放本包六个JSX/CSS作者文件，将article-entry.json包装为articles数组写articles.json，将illustrated-story.json按文章ID映射写illustrated-stories.json，将article-reviewed-data.json写src/data.json。不要把单篇组件覆盖完整门户。也可使用既有reports/batch-2026-10-30/shared/prepare_article.py，但其公共CSS与reader依赖必须齐全，第二参数必须是项目src目录；之后覆盖本包六个作者文件并核对最终数据。

依官方工作流prepare、build --separate-data，export-offline输出至项目.data-app-offline/exports，复制交付副本并运行既有sanitize_export.py移除可选本地线程meta。运行test_source.py与test_article.py HTML路径。后者必须通过最终HTML目标ID、全文、两图、来源、解码JSON和隐私检查，不能只核对文件名。

单篇安全HTML为2920512字节，SHA256 a83bc19af37d6aa331b115331ec62bab52f92d5a3c0a8f2330331fa6f8c711e6。完整门户整合见timeline/BUILD.md。此文件不是线上发布或GitHub大型HTML归档回执。


## 完成本轮交付与验收

单篇HTML附件发送请求已被接受。完整门户桌面验收通过，手机未测；此结果不代表原站已同步。正式研究41篇、AI25，原站22项待同步。详细验收范围另附visual-qa.json。
