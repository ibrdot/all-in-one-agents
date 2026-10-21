"""Catalog freshness, provenance integrity, and refreshed documentation links."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def test_generated_catalog_is_current():
    subprocess.run([sys.executable, str(ROOT/'scripts/sync_catalog.py'), '--check'], check=True)


def test_imported_files_match_pinned_manifest():
    data = json.loads((ROOT/'docs/import-manifest.json').read_text())
    for item in data['imports']:
        assert re.fullmatch('[0-9a-f]{40}', item['commit'])
        assert item['license'] == 'MIT'
        destination = ROOT/item['destination']
        assert (destination/'LICENSE').is_file()
        assert item['files']
        for path, expected in item['files'].items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected


def test_updated_documentation_relative_links():
    files = ['README.md', 'CONTRIBUTING.md', 'docs/GETTING-STARTED.md',
             'docs/CODING-WORKFLOWS.md', 'docs/INSTALL.md']
    for name in files:
        path = ROOT/name
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if target.startswith(('https://', 'http://', '#')):
                continue
            assert (path.parent/target.split('#')[0]).exists(), (name, target)
