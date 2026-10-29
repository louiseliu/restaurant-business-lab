#!/usr/bin/env python3
"""零依赖，将可审查 JS 内联为单文件；不会执行网络或上传。"""
from pathlib import Path
base = Path(__file__).resolve().parent
html = (base / 'index.template.html').read_text()
for tag, filename in [('/* MODEL_SOURCE */','model.js'),('/* UI_SOURCE */','ui.js')]:
    code = (base / filename).read_text()
    assert '</script' not in code.lower(), filename
    assert html.count(tag) == 1, tag
    html = html.replace(tag, code)
(base / 'index.html').write_text(html)
(base / 'dist').mkdir(exist_ok=True)
(base / 'dist' / 'index.html').write_text(html)
print('Built index.html: self-contained, no external dependencies')
