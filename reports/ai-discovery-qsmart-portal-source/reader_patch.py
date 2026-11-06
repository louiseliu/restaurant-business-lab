"""Narrow authored-reader additions; never replace the portal reader or runtime."""
ID='research-2026-11-06-ai-discovery-value-note'
QID='research-2026-10-30-qsmart-note'
def patch_reader(text):
    def replace(old,new):
        nonlocal text
        assert text.count(old)==1,'Reader changed: '+old[:80]
        text=text.replace(old,new)
    replace("import React from 'react';", "import React from 'react';\nimport AIDiscoverySourcePreviews from './ai-discovery-value-source-previews.json';\nimport {AIDiscoveryDiagram} from './AIDiscoveryDiagrams.jsx';\nimport {QSmartRevision} from './QSmartRevision.jsx';")
    replace('const diagramRows=reviewedRows(diagramId);',"const diagramRows=reviewedRows(diagramId);\n if(diagram.layout?.startsWith('ai-discovery-value-'))return <AIDiscoveryDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
    replace('sourcePreviews={',f"sourcePreviews={{id.includes('{ID}')?AIDiscoverySourcePreviews:")
    replace(' const anchor=name=>',f" const resolveQSmartLinks=text=>text.replaceAll('(sources.md)',`(${{item.sourceUrl.replace(/note\\.md$/,'sources.md')}})`).replaceAll('(sources-update-2026-11-06.md)',`(${{item.sourceUrl.replace(/note\\.md$/,'sources-update-2026-11-06.md')}})`);\n const anchor=name=>")
    replace("['limits','未知与核查'],['sources','来源']","['limits','未知与核查'],...(story.revision?[['revision-2026-11-06','2026年11月6日同篇补充']]:[]),['sources','来源']")
    replace(' const refs=story.sources', ' const oldRefs=story.sources')
    replace(' return <article key={item.id}',f" const refs=story.revision?[...oldRefs,...story.revision.sources.map(s=>({{label:s.title,href:s.url}}))]:oldRefs;\n return <article lang={{item.id==='{ID}'?'zh-CN':undefined}} key={{item.id}}")
    replace(' <section className="study-sources"',' {story.revision&&<QSmartRevision item={item} revision={story.revision}/>}\n <section className="study-sources"')
    replace("item.id==='research-2026-11-01-shift-constraints-note'?",f"(item.id==='research-2026-11-01-shift-constraints-note'||item.id==='{QID}')?")
    replace(" ↗</a>{item.id==='research-2026-11-01-inventory-capture-note'", " ↗</a>{item.firstSourceUrl&&<p><a href={item.firstSourceUrl} target=\"_blank\" rel=\"noreferrer\">查看首次固定版本研究原文 ↗</a>；保留首次入库时间，本次补充不另计一篇研究。</p>}{item.id==='research-2026-11-01-inventory-capture-note'")
    replace("{['research-2026-11-05-monthly-meal-customization-note'",f"{{item.id==='{QID}'?resolveQSmartLinks(item.body):['research-2026-11-05-monthly-meal-customization-note'")
    return text
