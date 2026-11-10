"""Bounded static checks. No claim of browser, safety, or device validation."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, re, subprocess, sys, xml.etree.ElementTree as ET

R=Path(__file__).resolve().parent
class Parse(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.figures=0; self.svgs=0; self.scripts=0; self.lang=None; self.remote_assets=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='figure':self.figures+=1
        if tag=='svg':self.svgs+=1
        if tag=='script':self.scripts+=1
        if tag=='html':self.lang=a.get('lang')
        if tag in ['script','img','link','iframe','object','audio','video'] and any(a.get(x,'').startswith(('https:','http:','//')) for x in ['href','src','data']):self.remote_assets.append(tag)

subprocess.run([sys.executable,str(R/'build.py')],check=True,capture_output=True)
b=(R/'xray-acceptance.html').read_bytes(); h=hashlib.sha256(b).hexdigest()
subprocess.run([sys.executable,str(R/'build.py')],check=True,capture_output=True)
assert b==(R/'xray-acceptance.html').read_bytes(), 'nondeterministic build'
s=b.decode(); p=Parse(); p.feed(s)
assert p.lang=='zh-CN' and p.figures==2 and p.svgs==2
assert len(p.ids)==len(set(p.ids)), 'duplicate IDs'
assert not p.scripts and not p.remote_assets
assert all(x[1:] in p.ids for x in p.links if x.startswith('#'))
allowed={'https://www.airchina.com.cn/airchinacms/4/upload/resources/file/7142.pdf','https://www.meyerop.com/cn/news/company-news/2024/06/1763','https://foodsafety.meyerop.com/upload/image/20240611/20240611162530_43570.jpg'}
assert {x for x in p.links if not x.startswith('#')} <= allowed
assert len(re.findall(r'<h2 id="article-',s))==6
for text in ['不锈钢≥1.0mm','直径0.3毫米','未核定它与上述2024年验收','测试餐食不得进入销售或供餐','浏览器视觉、交互和打印未验']:
    assert text in s,text
for bad in ['/workspace/','/home/','chatgpt.com/c/','codex://','Bearer ','ghp_','sk-proj-']:
    assert bad not in s,bad
svg_checks=[]
for f in ['test-conditions.svg','inspection-workflow.svg']:
    root=ET.fromstring((R/f).read_text()); vb=list(map(float,root.attrib['viewBox'].split()))
    assert root.find('{http://www.w3.org/2000/svg}title') is not None
    assert root.find('{http://www.w3.org/2000/svg}desc') is not None
    for t in root.iter('{http://www.w3.org/2000/svg}text'):
        assert 0 <= float(t.attrib['x']) < vb[2] and 0 <= float(t.attrib['y']) < vb[3]
    svg_checks.append({'file':f,'xml_valid':True,'text_anchor_bounds':True,'visual_rendering':'not verified'})
result={'checks':'passed','scope':'deterministic build, HTML structure, links, privacy patterns, SVG XML and text-anchor bounds; not browser rendering or device testing','html':{'bytes':len(b),'sha256':h},'figure_count':p.figures,'unique_ids':len(p.ids),'external_source_urls':sorted(allowed),'remote_assets':0,'scripts':0,'svg':svg_checks,'visual_status':'Browser, SVG raster rendering, interaction, print, screen reader and real offline operation unverified. Installed ImageMagick SVG rendering failed because rsvg-convert is absent. No browser permission or preview restriction was retried or bypassed.'}
(R/'qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
