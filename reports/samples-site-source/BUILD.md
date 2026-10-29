# 同站实战样板：可复建作者组件

这是站内新增样板承载的作者源码，不是完整 Data runtime，不会自动部署，也不是新的研究实测文章。既有8篇研究与原图文保持不变。旧归档的全站 HTML 是当时快照，不含本次样板入口。

## 复建
1. 公共仓库必须包含 `tools/delivery-campaign/` 与 `examples/ai-weekly-report/` 的已核验原件及ZIP；文件名和SHA由 samples-metadata.json固定。
2. 执行 `python generate_samples.py --repo <仓库检出目录> --output <既有项目>/src/content/report/samples.json`。脚本只读仓库相对文件，检查全部原件SHA，生成内联HTML和下载载荷。不需要未归档JSON或私人目录。
3. 将 Samples.jsx、samples.css 放到同一report作者目录。在既有 ReportContent.jsx 导入 `SampleCards, SampleReader, sampleIds`；读取路由后，`selected==='samples'` 时显示返回入口和 SampleCards；`sampleIds.includes(selected)` 时显示 `<SampleReader id={selected}/>`。首页增加 `#read/samples` 入口，可在页尾显示 SampleCards。
4. 兼容官方 Data app API 1 的既有项目内用标准 build；保留保护runtime、访问权限、已保存编辑。源代码单独不能取代完整 Data runtime。
5. 浏览器核查桌面和窄屏：两样板可读可用、返回清楚、父页下载哈希一致、原8篇仍在。iframe只授予allow-scripts、不授予same-origin，下载不放沙盒里。不要增加模型API、真实资料上传或账号权限。
6. 样板版本变化时必须重新审核原件、数据与边界测试，再更新metadata的SHA。没有自动实时同步或自动发布。

条件计算器输出不是实测净利润；AI周报全部模拟数据，仅展示预计算Python结果和AI辅助叙事，不声称站内调用AI或测得效率收益。文件下载原件保持字节一致。
