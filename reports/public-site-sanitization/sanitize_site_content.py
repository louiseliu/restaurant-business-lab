#!/usr/bin/env python3
"""Remove private collaboration links and local authoring metadata from authored payloads.
No network, Git, runtime edits, publication or access changes. Python standard library.
"""
import argparse, base64, hashlib, io, json, re, zipfile
from pathlib import Path

NOTICE = '私人协作会话，未公开'
URL = r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/[^\s<>"\x27)\\]+'
MARKDOWN = re.compile(r'\[[^\]]*\]\(' + URL + r'\)')
BARE = re.compile(URL)
ANCHOR = re.compile(r'<a\b[^>]*href=["\x27]' + URL + r'["\x27][^>]*>.*?</a>', re.I | re.S)
META = re.compile(r'<meta\b(?=[^>]*\bname\s*=\s*["\x27]data-app-local-thread["\x27])[^>]*>\n?', re.I)

def sha(b): return hashlib.sha256(b).hexdigest()
def clean_text(text):
    return META.sub('', BARE.sub(NOTICE, MARKDOWN.sub(NOTICE, ANCHOR.sub(NOTICE, text))))
def dump(obj): return (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode()

def clean_zip(raw):
    source = zipfile.ZipFile(io.BytesIO(raw)); infos = source.infolist()
    values = {i.filename: source.read(i.filename) for i in infos}
    changed = set()
    for name, value in list(values.items()):
        if name.lower().endswith(('.html', '.htm', '.md', '.txt')):
            updated = clean_text(value.decode('utf-8')).encode()
            if updated != value: values[name] = updated; changed.add(name)
    # Recompute declared file checksums, not business/result values.
    for name, value in list(values.items()):
        if not name.endswith('release-manifest.json'): continue
        manifest = json.loads(value); prefix = name.rsplit('/', 1)[0]+'/' if '/' in name else ''
        touched = False
        for row in manifest.get('files', []):
            target = prefix+row.get('path', '')
            if target in changed:
                row.update(bytes=len(values[target]), sha256=sha(values[target])); touched=True
        if touched:
            manifest['public_metadata_cleanup'] = 'Removed private collaboration links or local authoring metadata only; business data and calculations unchanged.'
            values[name] = dump(manifest)
    if not changed: return raw
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as target:
        for info in infos: target.writestr(info, values[info.filename])
    return output.getvalue()

def sanitize(report_dir):
    root = Path(report_dir); changed=[]
    def write(name, content):
        path=root/name
        if path.read_bytes()!=content: path.write_bytes(content); changed.append(name)
    legacy=root/'LegacyReport.jsx'
    if legacy.exists(): write(legacy.name, clean_text(legacy.read_text()).encode())
    catalog=json.loads((root/'articles.json').read_text())
    for article in catalog['articles']:
        body=article['body']; cleaned=clean_text(body)
        if body!=cleaned:
            article.setdefault('originalBodySha256',sha(body.encode()))
            article['body']=cleaned; article['renderedBodySha256']=sha(cleaned.encode())
            article['redactionNote']='公开阅读版移除私人协作会话链接；originalBodySha256 保留原始公开仓库正文校验值，renderedBodySha256 对应本站脱敏正文。'
    write('articles.json', dump(catalog))
    samples=json.loads((root/'samples.json').read_text())
    for sample in samples.values():
        old=sample['html']; sample['html']=clean_text(old)
        if old!=sample['html']:
            sample['sha256']=sha(sample['html'].encode())
            sample['version']='1.0.1-public-metadata-cleanup'
        for file in sample['files']:
            raw=base64.b64decode(file['body']) if file.get('encoding')=='base64' else file['body'].encode()
            updated=clean_zip(raw) if zipfile.is_zipfile(io.BytesIO(raw)) else clean_text(raw.decode('utf-8')).encode()
            if updated!=raw:
                file['body']=base64.b64encode(updated).decode() if file.get('encoding')=='base64' else updated.decode()
                file['sha256']=sha(updated)
    write('samples.json', dump(samples))
    audit(root)
    return changed

def audit(root):
    root=Path(root); payloads=[]
    for name in ['LegacyReport.jsx','articles.json','illustrated-stories.json']:
        if (root/name).exists(): payloads.append((name,(root/name).read_bytes()))
    samples=json.loads((root/'samples.json').read_text())
    for sample in samples.values():
        html=sample['html'].encode(); assert sha(html)==sample['sha256']
        payloads.append(('embedded HTML',html))
        for file in sample['files']:
            raw=base64.b64decode(file['body']) if file.get('encoding')=='base64' else file['body'].encode()
            assert sha(raw)==file['sha256'],file['name']
            if zipfile.is_zipfile(io.BytesIO(raw)):
                with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                    for name in archive.namelist(): payloads.append((name,archive.read(name)))
            else: payloads.append((file['name'],raw))
    for name,raw in payloads:
        text=raw.decode('utf-8',errors='replace')
        assert not BARE.search(text),f'Private link remains in {name}'
        assert not META.search(text),f'Local thread metadata remains in {name}'
    return len(payloads)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('report_dir',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    print(json.dumps({'checkedPayloads':audit(args.report_dir)} if args.check else {'changedFiles':sanitize(args.report_dir)},ensure_ascii=False))
