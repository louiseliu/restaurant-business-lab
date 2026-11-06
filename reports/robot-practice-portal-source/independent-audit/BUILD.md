# Independent local audit

Python 3 and Node are required. No external packages or network access are used.

From the repository root, run with explicit paths (replace the example source locations with their archived equivalents):

```sh
python path/to/independent-audit/check_inputs.py ROBOT_SOURCE AI_SOURCE BASELINE67
python path/to/independent-audit/audit_portal69.py PRODUCTION_DIR ROBOT_SOURCE AI_SOURCE
node path/to/independent-audit/test_scoped_fixes.mjs PRODUCTION_DIR
```

ROBOT_SOURCE and AI_SOURCE must be the frozen author-source directories containing manifest.json, article-entry.json and related inputs. BASELINE67 must contain the baseline src directory. PRODUCTION_DIR must contain baseline67, baseline67-sha256.json, portal69 (including dist and the official offline export), timeline69-robot-practice.html, and portal-archive-source/input-fingerprints.json. Keep test_scoped_fixes.mjs beside audit_portal69.py. Results are written beside the audit scripts. The scripts retain defaults for the original local production layout, but archived source names need explicit arguments.

An author-only Git archive intentionally omits compiled HTML, complete baseline/runtime, and ZIP payloads. The full artifact audit cannot run on that archive alone: reconstruct the local production directory through its build workflow and restore the exact baseline and generated outputs first. Do not substitute missing inputs or interpret an unavailable full audit as a pass. If the older sibling original portal is present, it is also compared with the baseline; otherwise baseline checks use the preserved fingerprint manifest.

## Findings and repair record

portal69-before-fixes.json records two integration failures in the initial artifact: the robot study was excluded by the commercial-topic filter, and relative Markdown source links were not resolved against frozen source URLs.

The final audit verifies the scoped topic and link adapters and preserves the frozen entry, story and query payloads. Actual extracted JavaScript helpers are executed using Node: 717 checks compare all 87 old entries and validate six new relative-link occurrences. The remaining ReportContent and IllustratedArticle source is compared with the baseline after removing only the reviewed additions. portal69-static-audit.json records the repaired artifact identity and final checks.

## Boundaries

This is local static and pure-helper testing, not browser acceptance. It does not establish layout, mobile/dark-mode rendering, editing, source-panel interaction, print/export interaction, real offline opening, or calculator behavior. It does not repeat remote Git readback or external fact research. The parent's separately recorded remote readback is not represented as this auditor's independent network verification. Privacy checks use explicit patterns and recursive archive inspection, not a guarantee that every possible sensitive value is absent. Existing language inheritance, Fourth source-title limitation, and historical audit gaps remain disclosed.
