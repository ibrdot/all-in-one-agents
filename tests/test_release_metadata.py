"""Versions and release docs must stay in sync without implicit Git writes."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1]


def tool():
    spec=importlib.util.spec_from_file_location('release_metadata',ROOT/'scripts/release_metadata.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def test_all_discovered_versions_equal_package():
    m=tool();expected=json.loads((ROOT/'package.json').read_text())['version']
    rows=m.versions(ROOT)
    assert len(rows)>=18 and all(v==expected for _,v in rows)


def test_release_heading_and_badge_match_current_version():
    version=json.loads((ROOT/'package.json').read_text())['version']
    assert (ROOT/'RELEASE-NOTES.md').read_text().startswith(f'# Release notes - v{version}\n')
    assert f'## [{version}] - ' in (ROOT/'CHANGELOG.md').read_text()
    readme=(ROOT/'README.md').read_text()
    assert '/workflows/ci.yml' not in readme and '/workflows/validate.yml' in readme


@pytest.mark.parametrize('version',['1.2','v1.2.3','1.2.3;bad','01.2.3','1.2.3\n'])
def test_invalid_version_rejected_without_writes(tmp_path,version):
    path=tmp_path/'package.json';path.write_text('{"version":"1.0.0"}')
    with pytest.raises(ValueError):tool().update(tmp_path,version)
    assert json.loads(path.read_text())['version']=='1.0.0'


def test_nested_marketplace_and_extension_versions_updated(tmp_path):
    (tmp_path/'package.json').write_text('{"version":"1.0.0"}')
    folder=tmp_path/'.claude-plugin';folder.mkdir()
    (folder/'marketplace.json').write_text('{"plugins":[{"name":"x","version":"1.0.0"}]}')
    (tmp_path/'gemini-extension.json').write_text('{"version":"1.0.0"}')
    tool().update(tmp_path,'1.5.0')
    assert all(v=='1.5.0' for _,v in tool().versions(tmp_path))


def test_wrapper_never_stages_commits_tags_or_pushes():
    text=(ROOT/'scripts/bump-version.sh').read_text()
    assert all(command not in text for command in ['git add','git commit','git tag','git push'])
