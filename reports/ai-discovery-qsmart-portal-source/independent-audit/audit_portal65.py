"""Read-only static audit of one 65-study portal; no browser or network actions.

Pass existing directories as arguments. Outputs contain public artifact names and
hashes, never the supplied directory locations. This is a new audit, not a copy
of any historical audit whose archival state remains unresolved.
"""
import argparse
import base64
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

GEO = 'research-2026-11-06-ai-discovery-value-note'
QSMART = 'research-2026-10-30-qsmart-note'
EXPECTED_HTML = 'f033d638d659037cb96f0e062784c55c5451622c90a8793ed4c3244b97b97305'
BASELINE_MANIFEST_GIT = 'b3f6a0597b57e24b234ea70b521e050ec5e8df4b'
QSMART_BODY_GIT = 'e4227d30b125a17972f3985b64b111edc776a3ce'
QSMART_SOURCES_GIT = 'be0384643892c4a08d557ae7d03e402f6a65948c'

def read(path):
    return json.loads(path.read_text())

def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()

def git_blob(value):
    value = value.encode() if isinstance(value, str) else value
    return hashlib.sha1(b'blob ' + str(len(value)).encode() + b'\0' + value).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['production', 'original-baseline', 'geo', 'qsmart', 'output']:
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    root, original, geo, qs = args.production, args.original_baseline, args.geo, args.qsmart
    baseline, project = root / 'baseline64', root / 'portal65'
    br, nr = baseline / 'src/content/report', project / 'src/content/report'
    failures = []
    checks = []
    def check(value, message):
        checks.append(message)
        if not value:
            failures.append(message)

    # Bind the audit to exactly one completed HTML, not a mutable later revision.
    html_path = root / 'timeline65-discovery-qsmart.html'
    html_bytes = html_path.read_bytes()
    html = html_bytes.decode()
    check(sha(html_bytes) == EXPECTED_HTML and len(html_bytes) == 13892324, 'Exact target HTML identity')
    check(html_bytes == (project / '.data-app-offline/exports/timeline65-discovery-qsmart.html').read_bytes(), 'Portable output equals official offline export')

    # The remote manifest blob was independently read at the recorded commit.
    # Its contents authenticate the 18 remaining saved, readable source receipts.
    receipts = read(root / 'baseline-remote-files.json')
    prefix = 'reports/camera-reuse-portal-source/'
    records = {r['path'].removeprefix(prefix): r for r in receipts}
    check(len(records) == 19, 'Nineteen readable baseline archive receipts')
    manifest_record = records['manifest.json']
    check(git_blob(manifest_record['content']) == BASELINE_MANIFEST_GIT == manifest_record['sha'], 'Baseline archive manifest matches independently fetched Git blob')
    remote_manifest = json.loads(manifest_record['content'])
    check(set(remote_manifest['files']) == set(records) - {'manifest.json'}, 'Remote manifest covers all other readable archive receipts')
    for name, record in records.items():
        check(git_blob(record['content']) == record['sha'], 'Archived Git blob verified: ' + name)
        if name != 'manifest.json':
            declared = remote_manifest['files'][name]
            check(sha(record['content']) == declared['sha256'] and len(record['content'].encode()) == declared['bytes'], 'Archived manifest entry verified: ' + name)

    frozen_files = read(root / 'baseline64-sha256.json')
    changed = []
    for name, digest in frozen_files.items():
        check(sha((baseline / name).read_bytes()) == digest, 'Frozen baseline bytes: ' + name)
        check((baseline / name).read_bytes() == (original / name).read_bytes(), 'Original readable baseline preserved: ' + name)
        if (project / name).read_bytes() != (baseline / name).read_bytes():
            changed.append(name)
    allowed_changes = {'src/data.json', 'src/content/report/articles.json', 'src/content/report/illustrated-stories.json', 'src/content/report/IllustratedArticle.jsx'}
    check(set(changed) == allowed_changes, 'Only four intended existing source files changed')
    baseline_content = {str(p.relative_to(br)) for p in br.rglob('*') if p.is_file()}
    new_content = {str(p.relative_to(nr)) for p in nr.rglob('*') if p.is_file()}
    additions = {'AIDiscoveryDiagrams.jsx', 'ai-discovery-value-diagrams.css', 'ai-discovery-value-source-previews.json', 'QSmartRevision.jsx', 'qsmart-revision.css'}
    check(new_content - baseline_content == additions and not baseline_content - new_content, 'Exactly five scoped content files added; no content files removed')
    for name in additions:
        source = geo if name.startswith(('AI', 'ai-')) else qs
        check((nr / name).read_bytes() == (source / name).read_bytes(), 'Frozen new component preserved: ' + name)

    old_catalog, catalog = read(br / 'articles.json'), read(nr / 'articles.json')
    old_stories, stories = read(br / 'illustrated-stories.json'), read(nr / 'illustrated-stories.json')
    old_data, data = read(baseline / 'src/data.json'), read(project / 'src/data.json')
    old_articles = {a['id']: a for a in old_catalog['articles']}
    articles = {a['id']: a for a in catalog['articles']}
    samples, old_samples = read(nr / 'samples.json'), read(br / 'samples.json')
    research = [a for a in catalog['articles'] if a['section'] == 'research']
    counts = {'research': len(research), 'fullOriginals': len(catalog['articles']), 'stories': len(stories), 'samples': len(samples), 'aiResearch': sum('ai' in a['topics'] for a in research), 'queries': len(data['queries'])}
    check(counts == {'research': 65, 'fullOriginals': 85, 'stories': 65, 'samples': 2, 'aiResearch': 43, 'queries': 134}, 'Complete 65/85/65/2/43/134 counts')
    check(len(articles) == len(catalog['articles']) and set(articles) - set(old_articles) == {GEO} and not set(old_articles) - set(articles), 'Unique article IDs with one addition and no deletions')
    check(set(stories) == {a['id'] for a in research}, 'Each research article has exactly one story')
    check(catalog['articles'] == sorted(catalog['articles'], key=lambda a: (a['publishedAt'], a['id']), reverse=True), 'Chronological order uses first-entry time')
    for key, article in old_articles.items():
        if key != QSMART:
            check(articles[key] == article, 'Unrelated original preserved: ' + key)
    for key, story in old_stories.items():
        if key != QSMART:
            check(stories[key] == story, 'Unrelated story preserved: ' + key)
    check({k:v for k,v in data.items() if k not in ['queries', 'generatedAt', 'buildStatus']} == {k:v for k,v in old_data.items() if k not in ['queries', 'generatedAt', 'buildStatus']}, 'Report identity, preferences, filters and settings unchanged')
    check(data['buildStatus'] == 'complete', 'Build lifecycle completed')
    check(samples == old_samples, 'Two embedded samples and five downloadable payloads unchanged')

    # Article identity and complete original text are separate from visual summaries.
    ga, gs = read(geo / 'article-entry.json'), read(geo / 'illustrated-story.json')
    check(articles[GEO] == ga and stories[GEO] == gs, 'GEO article and illustrated story match frozen input exactly')
    check(ga['publishedAt'] == ga['updatedAt'] == '2026-11-06T02:15:50Z' and ga['firstGit'] == '40e158a2766f7edd8e3d684b66436dd197624ecb', 'GEO first identity and timestamp retained')
    check(sha(ga['body']) == ga['originalBodySha256'] == 'f1d0bc9dd94245f28191c1800f9a9ec583daee5bab1e27b90cda10e1de0f47b3', 'GEO original matches first-commit SHA-256')
    sections = re.split(r'^## ', ga['body'], flags=re.M)
    expected_sections = [{'title': part.split('\n',1)[0], 'body': part.split('\n',1)[1].strip().split('\n\n')} for part in sections[1:]]
    check(gs['sections'] == expected_sections and len(expected_sections) == 6, 'All six GEO narrative sections complete')
    qa, qstory = read(qs / 'article-entry.json'), read(qs / 'illustrated-story.json')
    check(articles[QSMART] == qa and stories[QSMART] == qstory, 'Q-Smart same-ID revised input retained exactly')
    check(qa['body'].startswith(old_articles[QSMART]['body']) and {k:v for k,v in qstory.items() if k != 'revision'} == old_stories[QSMART], 'Q-Smart full original prefix and all original story fields unchanged')
    check(qa['publishedAt'] == old_articles[QSMART]['publishedAt'] == '2026-10-30T07:29:17Z', 'Q-Smart first-entry time unchanged')
    check(qa['updatedAt'] == '2026-11-06T02:12:43Z' and qa['revisionGit'] == '8770ddeefaa8ace5dd3fe1f9e4f68d7abbc4e760', 'Q-Smart revision identity retained')
    check(git_blob(qa['body']) == QSMART_BODY_GIT and git_blob(qstory['revision']['sourceLedger']) == QSMART_SOURCES_GIT, 'Q-Smart body and source ledger equal independently fetched Git blobs')
    check(qa['firstSourceUrl'] == old_articles[QSMART]['sourceUrl'] and qa['originalBodySha256'] == old_articles[QSMART]['originalBodySha256'], 'Q-Smart original link and digest preserved')

    old_queries, queries = old_data['queries'], data['queries']
    for key, value in old_queries.items():
        check(queries[key] == value, 'Original reviewed query preserved: ' + key)
    new_queries = {**read(geo / 'article-reviewed-data.json')['queries'], **{k:v for k,v in read(qs / 'article-reviewed-data.json')['queries'].items() if k not in old_queries}}
    check(set(queries) - set(old_queries) == set(new_queries) and len(new_queries) == 3, 'Exactly three reviewed queries added')
    for key, value in new_queries.items():
        check(queries[key] == value, 'Frozen added query retained: ' + key)
    revision_query = 'diagram-' + QSMART + ':revision-2026-11-06'
    for source in qstory['revision']['sources']:
        check([key for key, value in queries.items() if source['url'] in json.dumps(value, ensure_ascii=False)] == [revision_query], 'Q-Smart added source binds only to its revision query: ' + source['url'])
    bound_queries = {'network', 'comparison'}
    for key, story in stories.items():
        visual_keys = [('diagram', '')]
        if story.get('secondDiagram') and not story.get('numericChart'):
            visual_keys.append(('secondDiagram', ':second'))
        if story.get('thirdDiagram'):
            visual_keys.append(('thirdDiagram', ':third'))
        for field, suffix in visual_keys:
            qid = 'diagram-' + key + suffix
            bound_queries.add(qid)
            check(queries[qid]['rows'] == story[field]['nodes'], 'Rendered diagram uses reviewed rows: ' + qid)
        if story.get('numericChart'):
            bound_queries.add('visual-' + key)
        if story.get('revision'):
            qid = 'diagram-' + key + ':revision-2026-11-06'
            bound_queries.add(qid)
            check(queries[qid]['rows'] == story['revision']['diagram']['nodes'], 'Revision diagram uses reviewed rows: ' + qid)
    check(bound_queries == set(queries), 'All 134 queries accounted for by story visuals and legacy components')
    for key, value in queries.items():
        definitions = value['source']['metricDefinitions']
        expected = 'methods' if key == 'network' else 'network-comparison' if key == 'comparison' else key
        check(any(expected in definition.get('componentIds', []) for definition in definitions), 'Component provenance binding: ' + key)
    for field, suffix, sources in [('diagram', '', ['S1', 'S1扩展']), ('secondDiagram', ':second', ['S2', 'S3'])]:
        q = queries['diagram-' + GEO + suffix]
        check(gs[field]['sourceIds'] == sources == [v['title'].split(' · ')[0] for v in q['source']['evidenceFlow'][1:]], 'GEO diagram scoped source identities: ' + field)
    check(round(3 / 34 * 100, 1) == 8.8 and 96 * (5 + 3 + 5 + 10) == 2208, 'GEO independent count arithmetic')

    # Source-level inspection, not a claim that browser behavior has been exercised.
    reader, old_reader = (nr / 'IllustratedArticle.jsx').read_text(), (br / 'IllustratedArticle.jsx').read_text()
    check(f"lang={{item.id==='{GEO}'?'zh-CN':undefined}}" in reader, 'Chinese language attribute limited to GEO article')
    check('reader-adjacent' in reader and 'story.thirdDiagram' in reader and 'key={item.id}' in reader, 'Existing adjacent navigation, third diagram and keyed identity retained')
    check((nr / 'ReportContent.jsx').read_bytes() == (br / 'ReportContent.jsx').read_bytes(), 'Main reader routing and filters unchanged')
    check((nr / 'LegacyReport.jsx').read_bytes() == (br / 'LegacyReport.jsx').read_bytes(), 'Legacy report unchanged')
    check('story.revision&&<QSmartRevision' in reader and 'resolveQSmartLinks(item.body)' in reader and 'item.firstSourceUrl&&' in reader, 'Revision section, complete-body links and original-source link retained')
    old_routes = re.findall(r"if\(diagram\.layout\?\.startsWith\('([^']+)'\)\)", old_reader)
    check(all(route in reader for route in old_routes), 'All existing specialized diagram routes remain')

    # Parse serialized content rather than treating a successful build log as proof.
    objects = []
    for literal in re.findall(r'JSON\.parse\(("(?:[^"\\]|\\.)*")\)', html):
        try:
            objects.append(json.loads(json.loads(literal)))
        except (ValueError, TypeError):
            pass
    for label, expected in [('catalog', catalog), ('stories', stories), ('samples', samples)]:
        check(sum(value == expected for value in objects) == 1, 'Compiled JSON equals complete source: ' + label)
    build = read(project / 'dist/data-app-build.json')
    for field in ['html', 'snapshot']:
        record = build[field]
        raw = (project / 'dist' / record['path']).read_bytes()
        check(sha(raw) == record['sha256'] and len(raw) == record['bytes'], 'Build manifest exact bytes: ' + field)
    check(read(project / 'dist' / build['snapshot']['path']) == data, 'Complete built snapshot equals reviewed source')
    chunks = re.findall(r'<script type="application/json"(?: id="data-app-reviewed-snapshot"| data-app-snapshot-chunk)>(.*?)</script>', html, re.S)
    offline_snapshot = ''.join(chunks).encode()
    check(len(chunks) == 6 and offline_snapshot == (project / 'src/data.json').read_bytes(), 'All six offline snapshot chunks concatenate to exact reviewed source bytes')
    check(sha(offline_snapshot) == build['snapshot']['sha256'], 'Offline snapshot matches split-build snapshot hash')
    check(not re.search(r'(?:src|href)=["\x27]https?://', html), 'No statically declared remote asset dependencies')

    # Recursively decode every download ZIP in memory; do not execute embedded code.
    patterns = {
        'private-chat-link': r'https?://(?:www\.)?chatgpt\.com/(?:g|c|share)/',
        'private-local-path': r'/(?:workspace|home/agent|Users)/[A-Za-z0-9]',
        'private-project-reference': r'(?:appgprj_|libfile_|Sentinel_|rtc_u\d+_)[A-Za-z0-9_-]{6,}',
        'private-thread-link': r'codex://threads/',
        'internal-repository': r'https?://git\.chatgpt-team\.site',
        'local-thread-metadata': r'data-app-local-thread["\x27]\s+content=',
        'private-key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        'credential-format': r'(?<![A-Za-z0-9_-])(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})',
    }
    payload_count, zip_count, zip_members, manifests = 0, 0, 0, 0
    privacy_hits = []
    def scan(raw, label):
        nonlocal payload_count
        payload_count += 1
        text = raw.decode('utf-8', errors='replace')
        for kind, pattern in patterns.items():
            if re.search(pattern, text):
                privacy_hits.append({'payload': label, 'kind': kind})
    def archive_scan(raw, label):
        nonlocal zip_count, zip_members, manifests
        if not zipfile.is_zipfile(io.BytesIO(raw)):
            scan(raw, label)
            return
        zip_count += 1
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            names = archive.namelist()
            check(len(names) == len(set(names)), 'ZIP has unique member names: ' + label)
            contents = {name: archive.read(name) for name in names if not name.endswith('/')}
            for name, content in contents.items():
                zip_members += 1
                check(not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts, 'ZIP member path is bounded: ' + name)
                archive_scan(content, label + '/' + name)
                if name.endswith('release-manifest.json'):
                    manifests += 1
                    m = json.loads(content)
                    parent = str(PurePosixPath(name).parent)
                    for entry in m['files']:
                        target = (parent + '/' if parent != '.' else '') + entry['path']
                        check(target in contents and len(contents[target]) == entry['bytes'] and sha(contents[target]) == entry['sha256'], 'Nested release manifest entry: ' + entry['path'])
    for path in nr.rglob('*'):
        if path.is_file():
            scan(path.read_bytes(), 'content/' + str(path.relative_to(nr)))
    scan((project / 'src/data.json').read_bytes(), 'reviewed-data.json')
    scan(html_bytes, 'portable.html')
    scan(offline_snapshot, 'offline-reviewed-snapshot.json')
    for index, value in enumerate(objects):
        scan(json.dumps(value, ensure_ascii=False).encode(), 'compiled-json-' + str(index))
    downloads = 0
    for key, sample in samples.items():
        raw = sample['html'].encode()
        check(sha(raw) == sample['sha256'], 'Embedded HTML digest: ' + key)
        scan(raw, key + '/embedded.html')
        for file in sample['files']:
            downloads += 1
            raw = base64.b64decode(file['body'], validate=True) if file.get('encoding') == 'base64' else file['body'].encode()
            check(sha(raw) == file['sha256'], 'Download digest: ' + key + '/' + file['name'])
            archive_scan(raw, key + '/' + file['name'])
    check(downloads == 5 and zip_count == 2 and manifests == 1, 'All downloads and nested manifests inspected')
    check(not privacy_hits, 'No privacy patterns in authored, compiled, embedded or recursively decoded payloads')

    fingerprints = read(root / 'portal-archive-source/input-fingerprints.json')
    input_count = 0
    for label, folder in [('aiDiscovery', geo), ('qsmartRevision', qs)]:
        for name, expected in fingerprints[label].items():
            input_count += 1
            raw = (folder / name).read_bytes()
            check(len(raw) == expected['bytes'] and sha(raw) == expected['sha256'], 'Frozen integration input: ' + label + '/' + name)
    check(input_count == 20, 'Twenty integration inputs frozen by byte length and hash')
    # Execute current guard tests only in disposable copies. Their QA outputs
    # remain there; no production QA or historical audit file is overwritten.
    guard_results = {}
    with tempfile.TemporaryDirectory(prefix='portal65-audit-') as temporary:
        temp = Path(temporary)
        for name in ['integrate65.py', 'reader_patch.py', 'input-fingerprints.json', 'test_portal_merge_guard.py', 'test_frozen_input_guards.py']:
            shutil.copyfile(root / 'portal-archive-source' / name, temp / name)
        for script in ['test_portal_merge_guard.py', 'test_frozen_input_guards.py']:
            result = subprocess.run([sys.executable, str(temp / script), str(geo.resolve()), str(qs.resolve()), str(baseline.resolve())], capture_output=True, text=True)
            check(result.returncode == 0, 'Disposable guard execution: ' + script)
            if result.returncode == 0:
                guard_results[script] = json.loads(result.stdout)['checksPassed']
    route_test = subprocess.run([shutil.which('node') or 'node', str(root / 'portal-archive-source/test_reader_routes.mjs'), str(nr)], capture_output=True, text=True)
    check(route_test.returncode == 0, 'Read-only route helper and chronological filtering tests')

    report = {
        'schemaVersion': 1,
        'scope': 'Independent static preservation and privacy audit of the exact 65-study portal HTML; no publication or browser acceptance claim.',
        'artifact': {'filename': html_path.name, 'bytes': len(html_bytes), 'sha256': sha(html_bytes)},
        'result': 'passed-with-explicit-unverified-scope' if not failures else 'needs-revision',
        'counts': counts,
        'preservation': {'baselineFiles': len(frozen_files), 'unchangedBaselineFiles': len(frozen_files)-len(changed), 'changedExistingFiles': sorted(changed), 'addedScopedFiles': sorted(additions), 'unrelatedOriginalsUnchanged': 83, 'unrelatedStoriesUnchanged': 63, 'originalQueriesUnchanged': len(old_queries), 'qsmartOriginalBodyPrefixAndStoryFields': 'verified', 'qsmartFirstEntry': qa['publishedAt'], 'reportIdentityUnchanged': True, 'mainReaderAndLegacyUnchanged': True},
        'archiveEvidence': {'baselineCommitRead': 'd7c47b97d6f63175fa7498c464b5e3d5a01aa8d8', 'baselineArchiveCommit': '42da422322ff0e6332161fb079fb1090eb50e320', 'readableReceiptsVerifiedAgainstRemoteManifest': 19, 'manifestGitBlob': BASELINE_MANIFEST_GIT, 'qsmartRevisionCommit': qa['revisionGit'], 'independentlyFetchedQsmartBodyGitBlob': QSMART_BODY_GIT, 'independentlyFetchedQsmartSourcesGitBlob': QSMART_SOURCES_GIT},
        'staticCoverage': {'assertionsEvaluated': len(checks), 'reviewedQueryBindings': len(bound_queries), 'compiledJsonObjectsParsed': len(objects), 'offlineSnapshotChunks': len(chunks), 'offlineSnapshotBytes': len(offline_snapshot), 'offlineSnapshotSha256': sha(offline_snapshot), 'offlineSnapshotEqualsSourceBytes': offline_snapshot == (project / 'src/data.json').read_bytes(), 'qsmartAddedSourcesOnlyBindToRevisionQuery': True, 'privacyPayloadsScanned': payload_count, 'embeddedHtmlFiles': len(samples), 'downloadFiles': downloads, 'recursiveZipContainers': zip_count, 'zipMembers': zip_members, 'releaseManifests': manifests, 'privacyPatternHits': privacy_hits, 'buildManifestVerified': True, 'runtimeSha256': build['runtimeSha256'], 'frozenInputFiles': input_count, 'disposableGuardTests': guard_results, 'routeHelperTestsPassed': route_test.returncode == 0},
        'materialIssues': failures,
        'retainedLimitations': ['The fourth shared S2 source title still omits page 19. This existing display issue was not changed or considered resolved.', 'Historical uncertain audit archival items remain unresolved and were neither retried nor copied into this new audit.', 'Baseline preservation means the readable local 64-story baseline, not unavailable original-site edits or historical files.'],
        'notVerified': ['Browser rendering, mobile layout, dark mode, accessibility behavior, source popups, navigation history and scroll restoration, editing, print and export interactions.', 'Fresh compilation or independent replay of embedded calculator and weekly-report calculations; this audit inspected existing build bytes, manifests, source and serialized payloads.', 'Primary external webpages, restricted PDFs, restaurant records, original study datasets or causal business effects.', 'Original-site access, upload, publication, sharing settings or subsequent changes to the audited HTML.'],
        'privacyMethodLimit': 'Pattern-based inspection is not a formal guarantee that every possible sensitive datum is absent.',
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'portal65-static-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'result': report['result'], 'counts': counts, 'assertions': len(checks), 'privacyPayloads': payload_count, 'issues': failures, 'auditSha256': sha((args.output / 'portal65-static-audit.json').read_bytes())}, ensure_ascii=False, indent=2))
    return 1 if failures else 0

if __name__ == '__main__':
    raise SystemExit(main())
