import base64, io, json, tempfile, unittest, zipfile
from pathlib import Path
import sanitize_site_content as s

# Deliberately fake fixtures, never actual project, conversation or task identifiers.
PRIVATE='https://'+'chatgpt.com/c/'+'EXAMPLE-NOT-A-REAL-CONVERSATION'
HTML='<html><head><meta name="data-app-local-thread" content="EXAMPLE-ONLY"></head><body>模拟数据 42</body></html>'
class SanitizationTests(unittest.TestCase):
    def test_link_formats(self):
        for text in [PRIVATE,'[协作]('+PRIVATE+')','<a href="'+PRIVATE+'">协作</a>']:
            self.assertEqual(s.clean_text(text),s.NOTICE)
        self.assertEqual(s.clean_text('https://example.org/research'), 'https://example.org/research')
    def test_meta_only(self):
        text=s.clean_text(HTML);self.assertNotIn('EXAMPLE-ONLY',text);self.assertIn('模拟数据 42',text)
    def test_nested_download_manifest_and_idempotence(self):
        raw=HTML.encode();manifest={'files':[{'path':'case-demo.html','bytes':len(raw),'sha256':s.sha(raw)}]}
        z=io.BytesIO()
        with zipfile.ZipFile(z,'w') as a:
            a.writestr('demo/case-demo.html',raw);a.writestr('demo/release-manifest.json',s.dump(manifest));a.writestr('demo/values.csv','amount\n42\n')
        def file(name,b):return {'name':name,'encoding':'base64','body':base64.b64encode(b).decode(),'sha256':s.sha(b)}
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);body='Original '+PRIVATE
            (p/'LegacyReport.jsx').write_text('const note = "'+PRIVATE+'";')
            (p/'articles.json').write_bytes(s.dump({'articles':[{'body':body,'originalBodySha256':s.sha(body.encode())}]}))
            (p/'samples.json').write_bytes(s.dump({'demo':{'html':HTML,'sha256':s.sha(raw),'version':'1.0.0','files':[file('case-demo.html',raw),file('pack.zip',z.getvalue())]}}))
            self.assertEqual(len(s.sanitize(p)),3);self.assertEqual(s.sanitize(p),[])
            a=json.loads((p/'articles.json').read_text())['articles'][0]
            self.assertEqual(a['originalBodySha256'],s.sha(body.encode()));self.assertEqual(a['renderedBodySha256'],s.sha(a['body'].encode()))
            sample=json.loads((p/'samples.json').read_text())['demo']
            with zipfile.ZipFile(io.BytesIO(base64.b64decode(sample['files'][1]['body']))) as zz:
                clean=zz.read('demo/case-demo.html');m=json.loads(zz.read('demo/release-manifest.json'))
                self.assertEqual(m['files'][0]['sha256'],s.sha(clean));self.assertEqual(m['files'][0]['bytes'],len(clean));self.assertEqual(zz.read('demo/values.csv'),b'amount\n42\n')
            self.assertGreater(s.audit(p),3)
if __name__=='__main__':unittest.main()
