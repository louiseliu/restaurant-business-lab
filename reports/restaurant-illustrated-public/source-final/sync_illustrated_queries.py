"""Bind authored graphics to reviewed rows; no fetching or publishing.
Usage: python sync_illustrated_queries.py path/to/project/src
"""
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);r=p/'content/report';stories=json.loads((r/'illustrated-stories.json').read_text());items={a['id']:a for a in json.loads((r/'articles.json').read_text())['articles']};data=json.loads((p/'data.json').read_text())
for key in list(data['queries']):
 if key.startswith(('diagram-research-','visual-research-')):del data['queries'][key]
for id,a in stories.items():
 if id not in items:continue
 specs=[('diagram-'+id,a['diagram'],a['diagram']['nodes'])]
 if a.get('numericChart'):specs.append(('visual-'+id,a['numericChart'],a['numericChart']['rows']))
 elif a.get('secondDiagram'):specs.append(('diagram-'+id+':second',a['secondDiagram'],a['secondDiagram']['nodes']))
 for q,c,rows in specs:
  desc=c.get('scope',c.get('subtitle',''))+' '+c.get('note',c.get('footnote',''))
  data['queries'][q]={'rows':rows,'source':{'label':c.get('title',c.get('label','图解')),'files':[items[id]['path']],'metricDefinitions':[{'label':c.get('unit','机制和口径'),'definition':desc,'componentIds':[q]}],'evidenceFlow':[{'title':'固定公开研究版本','detail':items[id]['sourceUrl']},{'title':'展示边界','detail':desc}]}}
(p/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Bound reviewed graphics for',len(stories),'articles')
