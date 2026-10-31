import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'vision-checkout';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-30-vision-checkout-note'
assert a['publishedAt']=='2026-10-30T15:02:15Z' and a['updatedAt']=='2026-10-31T06:01:35Z'
assert a['firstGit']=='98b377faa73538f6fd0168ceba7e7ec2f53faf8d'
assert a['revisionGit']=='ffb0f400d7b4adae112e4a84b99e8d2eddca70ed' and a['revisionGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='f29d310c7337d631a9e80d7df25a8bbedd9ea6d140b2b231bfe6955fa0b4bbc6'
assert a['topics']==['ai','business-model']
assert '二选一' in s['diagram']['scope'] and '银豹餐饮PC版' in s['secondDiagram']['scope']
assert '不证明后续识别必然变差' in s['secondDiagram']['note']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed same-ID/first-time preservation, revised commit/time, full-body hash, mechanism/source boundaries and privacy')
