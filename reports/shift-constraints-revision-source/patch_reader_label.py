"""Correct the shift article link label only; preserve every other reader byte.
Usage: python patch_reader_label.py PORTAL_REPORT_DIRECTORY
"""
from pathlib import Path
import sys
OLD='查看首次固定版本研究原文与计算附件 ↗'
NEW="{item.id==='research-2026-11-01-shift-constraints-note'?'查看固定版本研究原文与计算附件':'查看首次固定版本研究原文与计算附件'} ↗"
def patch(root):
    p=Path(root)/'IllustratedArticle.jsx';text=p.read_text()
    if NEW in text:
        assert text.count(NEW)==1 and OLD not in text
        print('Scoped label already corrected; no mutation');return
    assert text.count(OLD)==1,'Unexpected source label; preserve user edits'
    p.write_text(text.replace(OLD,NEW))
    print('Corrected shift article label only; all other articles retain their existing label and URL.')
if __name__=='__main__':patch(sys.argv[1])
