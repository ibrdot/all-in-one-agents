import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def audit():
    spec=importlib.util.spec_from_file_location('check_docs',ROOT/'scripts/check_docs.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def test_maintained_docs_links_and_assets():
    report=audit().check(ROOT)
    assert report['documents']>=23 and not report['errors'],report['errors']


def test_missing_paths_anchors_and_bad_svg_detected(tmp_path):
    docs=tmp_path/'docs';docs.mkdir()
    (tmp_path/'README.md').write_text('# Home\n[bad](missing.md)\n[anchor](docs/a.md#absent)\n![svg](docs/bad.svg)')
    (docs/'a.md').write_text('# Present')
    (docs/'bad.svg').write_text('<svg>broken')
    errors=audit().check(tmp_path)['errors']
    assert len(errors)==3 and any('missing anchor' in e for e in errors)


def test_github_duplicate_heading_anchors():
    assert audit().anchors('# Hello world\n## Hello world\n## Usage & setup')=={'hello-world','hello-world-1','usage--setup'}


def test_heading_level_skip_detected(tmp_path):
    docs=tmp_path/'docs';docs.mkdir()
    (tmp_path/'README.md').write_text('# Home\n\n## Section\n\n#### Skipped level\n')
    errors=audit().check(tmp_path)['errors']
    assert any('heading level skip' in e for e in errors)


def test_heading_decrease_is_allowed(tmp_path):
    docs=tmp_path/'docs';docs.mkdir()
    (tmp_path/'README.md').write_text('# Home\n\n## Section\n\n### Deep\n\n## Back up\n')
    assert audit().check(tmp_path)['errors']==[]
