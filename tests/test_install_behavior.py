"""Actual filesystem installs, not manifest-presence claims."""
import json
import os
from pathlib import Path
import subprocess
import pytest

ROOT = Path(__file__).resolve().parents[1]


def install(home, *args):
    return subprocess.run(['bash', str(ROOT/'scripts/install.sh'), *map(str,args)],
                          env={**os.environ, 'HOME': str(home)}, capture_output=True, text=True, timeout=60)


@pytest.mark.parametrize('target,relative', [('claude','.claude'),('opencode','.config/opencode'),('grok','.grok'),('qwen','.qwen'),('factory','.factory')])
def test_real_install_and_repeat(tmp_path, target, relative):
    dest = tmp_path/relative
    for _ in range(2):
        r = install(tmp_path,target)
        assert r.returncode == 0, r.stderr
    assert (dest/'skills/pack-kernel/SKILL.md').is_file()
    assert len(list((dest/'skills').glob('*/SKILL.md'))) == len(list((ROOT/'skills').glob('*/SKILL.md')))
    assert (dest/'agents').is_dir() and (dest/'commands').is_dir()
    assert not (tmp_path/'.claude').exists() if target != 'claude' else True
    if target == 'claude':
        data=json.loads((dest/'settings.json').read_text())
        assert len(data['hooks']['SessionStart']) == 1
        hook=subprocess.run(['bash',str(dest/'hooks/session-start.sh')],env={**os.environ,'HOME':str(tmp_path)},capture_output=True,text=True)
        assert 'UNDERSTAND' in json.loads(hook.stdout)['hookSpecificOutput']['additionalContext']


def test_custom_destination_spaces(tmp_path):
    dest=tmp_path/'custom destination'
    assert install(tmp_path,dest).returncode == 0
    assert (dest/'skills/pack-kernel/SKILL.md').is_file()


@pytest.mark.parametrize('settings', ['{', '[]', '{"hooks":[]}', '{"hooks":{"SessionStart":{}}}'])
def test_invalid_settings_no_partial_install(tmp_path, settings):
    dest=tmp_path/'.claude'; dest.mkdir()
    p=dest/'settings.json'; p.write_text(settings)
    r=install(tmp_path,'claude')
    assert r.returncode != 0
    assert p.read_text() == settings
    assert not (dest/'skills').exists()


def test_preserves_unrelated_configuration(tmp_path):
    dest=tmp_path/'.claude'; dest.mkdir()
    p=dest/'settings.json'
    p.write_text(json.dumps({'theme':'dark','hooks':{'Stop':[{'custom':True}],'SessionStart':[{'hooks':[{'command':'echo existing'}]}]}}))
    assert install(tmp_path,'claude').returncode == 0
    data=json.loads(p.read_text())
    assert data['theme']=='dark' and data['hooks']['Stop']==[{'custom':True}]
    assert len(data['hooks']['SessionStart'])==2


@pytest.mark.parametrize('args',[['--nonsense'],['claude','opencode']])
def test_invalid_arguments_fail_before_write(tmp_path,args):
    assert install(tmp_path,*args).returncode != 0
    assert not (tmp_path/'.claude').exists()
