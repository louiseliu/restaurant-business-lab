# 独立静态复核

从任意工作目录运行：`python audit.py PRODUCTION_DIR SITE_SOURCE SUPPLIER_SOURCE OFFICIAL_RUNTIME_JS`。前3项为必需路径；第四项为兼容官方预构建app.js，核其SHA256及在拆分/离线HTML中的原字节。目录需含baseline69、portal71、baseline69-sha256.json及timeline71-site-supplier.html。完整小型作者源归档没有完整历史基线、运行时或编译HTML，不能只靠此目录重跑全产物检查。

result.json记录完整正文、来源、旧文件、编译/离线数据、样板下载、隐私模式及818项纯JavaScript辅助函数检查。guard-result.json由另行重跑合并保护生成。runtime-and-limits.json额外记录官方作者边界验证、运行时字节、干净复建及继承的旧全项目校验失败。不是浏览器、布局、交互、远端历史或独立联网查源验收。
