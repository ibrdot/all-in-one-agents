import os
from pathlib import Path
import subprocess
import pytest
ROOT=Path(__file__).resolve().parents[1]


def install(home,target):
    return subprocess.run(['bash',str(ROOT/'scripts/install.sh'),str(target)],env={**os.environ,'HOME':str(home)},capture_output=True,text=True)


@pytest.mark.parametrize('component',['skills','agents','commands','hooks'])
def test_install_rejects_symlink_components_before_copy(tmp_path,component):
    dest=tmp_path/'.claude';dest.mkdir();outside=tmp_path/'outside';outside.mkdir()
    (dest/component).symlink_to(outside,target_is_directory=True)
    p=install(tmp_path,'claude')
    assert p.returncode!=0
    assert list(outside.iterdir())==[]
    assert not (dest/'settings.json').exists()


def test_nested_skill_symlink_cannot_overwrite_external_file(tmp_path):
    dest=tmp_path/'custom';skill=dest/'skills'/'pack-kernel';skill.mkdir(parents=True)
    external=tmp_path/'private.txt';external.write_text('private')
    (skill/'SKILL.md').symlink_to(external)
    assert install(tmp_path,dest).returncode!=0
    assert external.read_text()=='private'


def test_modified_installed_skill_preserved_on_reinstall(tmp_path):
    dest=tmp_path/'custom'
    assert install(tmp_path,dest).returncode==0
    skill=dest/'skills'/'pack-kernel'/'SKILL.md';skill.write_text('user custom content')
    p=install(tmp_path,dest)
    assert p.returncode!=0 and skill.read_text()=='user custom content'


def test_force_flag_is_explicit_for_replacing_changes(tmp_path):
    dest=tmp_path/'custom';assert install(tmp_path,dest).returncode==0
    skill=dest/'skills'/'pack-kernel'/'SKILL.md';skill.write_text('user custom content')
    p=subprocess.run(['bash',str(ROOT/'scripts/install.sh'),str(dest),'--force'],env={**os.environ,'HOME':str(tmp_path)},capture_output=True,text=True)
    assert p.returncode==0 and skill.read_text()!='user custom content'
