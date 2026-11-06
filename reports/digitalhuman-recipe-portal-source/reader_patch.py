"""Append only the two reviewed diagram/preview branches to the existing reader."""
IDS=['research-2026-11-06-digitalhuman-livestream-note','research-2026-11-06-ai-recipe-development-note']
NAMES=[['DigitalHumanDiagrams.jsx','digitalhuman-diagrams.css','digitalhuman-source-previews.json'],['AIRecipeDiagrams.jsx','ai-recipe-development-diagrams.css','ai-recipe-development-source-previews.json']]
def patch_reader(text):
 def replace(old,new):
  nonlocal text
  assert text.count(old)==1,'Reader anchor changed; preserve edits: '+old[:70]
  text=text.replace(old,new)
 replace("import React from 'react';","import React from 'react';\nimport DigitalHumanSourcePreviews from './digitalhuman-source-previews.json';\nimport {DigitalHumanDiagram} from './DigitalHumanDiagrams.jsx';\nimport AIRecipeSourcePreviews from './ai-recipe-development-source-previews.json';\nimport {AIRecipeDiagram} from './AIRecipeDiagrams.jsx';")
 replace('const diagramRows=reviewedRows(diagramId);',"const diagramRows=reviewedRows(diagramId);\n if(diagram.layout?.startsWith('digitalhuman-'))return <DigitalHumanDiagram diagram={diagram} id={id} rows={diagramRows}/>;\n if(diagram.layout?.startsWith('ai-recipe-development-'))return <AIRecipeDiagram diagram={diagram} id={id} rows={diagramRows}/>;")
 replace('sourcePreviews={',f"sourcePreviews={{id.includes('{IDS[0]}')?DigitalHumanSourcePreviews:id.includes('{IDS[1]}')?AIRecipeSourcePreviews:")
 replace("lang={item.id==='research-2026-11-06-ai-discovery-value-note'?'zh-CN':undefined}",f"lang={{['research-2026-11-06-ai-discovery-value-note','{IDS[1]}'].includes(item.id)?'zh-CN':undefined}}")
 return text
