"""Memory management is local, explicit, and usable without provider credentials."""
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]


def cli(*args):
    return subprocess.run([sys.executable,'-m','runtime.memory',*map(str,args)],cwd=ROOT,capture_output=True,text=True)


def test_memory_add_search_delete_across_processes(tmp_path):
    db=tmp_path/'memory.db';entry=tmp_path/'entry.json'
    entry.write_text(json.dumps(dict(id='lesson',text='Validate empty inputs',embedding=[1,0],embedding_model='local-v1',metadata={'source':'reviewed'})))
    p=cli('put','--database',db,'--input',entry)
    assert p.returncode==0,p.stderr
    query=tmp_path/'query.json';query.write_text(json.dumps([1,0]))
    p=cli('search','--database',db,'--embedding',query,'--embedding-model','local-v1')
    assert p.returncode==0 and json.loads(p.stdout)['results'][0]['id']=='lesson'
    assert cli('delete','--database',db,'--id','lesson').returncode==0
    assert json.loads(cli('search','--database',db,'--embedding',query,'--embedding-model','local-v1').stdout)['results']==[]


def test_read_does_not_create_missing_database(tmp_path):
    db=tmp_path/'absent.db';query=tmp_path/'q.json';query.write_text('[1,0]')
    assert cli('search','--database',db,'--embedding',query,'--embedding-model','m').returncode==2
    assert not db.exists()


def test_bad_entry_leaves_no_database(tmp_path):
    db=tmp_path/'new.db';entry=tmp_path/'bad.json';entry.write_text('{"id":"x","text":"secret","embedding":[0,0],"embedding_model":"m"}')
    p=cli('put','--database',db,'--input',entry)
    assert p.returncode==2 and 'secret' not in p.stderr and not db.exists()


def test_put_rejects_symlink_database(tmp_path):
    target=tmp_path/'private';target.write_text('sentinel');db=tmp_path/'db';db.symlink_to(target)
    entry=tmp_path/'e.json';entry.write_text('{"id":"a","text":"b","embedding":[1,0],"embedding_model":"m"}')
    assert cli('put','--database',db,'--input',entry).returncode==2
    assert target.read_text()=='sentinel'
