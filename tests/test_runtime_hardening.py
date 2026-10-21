import json
import subprocess
import sys
import pytest
from runtime.core import Memory
from runtime.orchestrator import Agent, index_skills
from runtime.improvement import improve, promote, rollback
from runtime.providers import OpenAICompatible


def test_index_rejects_symlink(tmp_path):
    root=tmp_path/'skills'; skill=root/'x'; skill.mkdir(parents=True)
    outside=tmp_path/'outside'; outside.write_text('private')
    (skill/'SKILL.md').symlink_to(outside)
    store=Memory(':memory:')
    with pytest.raises(ValueError):index_skills(root,store,lambda _:[1,0],'e')
    store.close()


def test_index_rejects_missing_description(tmp_path):
    skill=tmp_path/'x';skill.mkdir();(skill/'SKILL.md').write_text('no description')
    store=Memory(':memory:')
    with pytest.raises(ValueError):index_skills(tmp_path,store,lambda _:[1,0],'e')
    store.close()


def test_candidate_tampering_rejected(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old')
    proposal=improve(p,lambda *_:'new',['x'],lambda text:dict(total=2,passed=1 if text=='old' else 2))
    proposal['candidate']='tampered'
    with pytest.raises(ValueError):promote(p,proposal,True)
    assert p.read_text()=='old'


def test_rollback_does_not_overwrite_later_work(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old')
    proposal=improve(p,lambda *_:'new',['x'],lambda text:dict(total=2,passed=1 if text=='old' else 2))
    receipt=promote(p,proposal,True);p.write_text('later edit')
    with pytest.raises(ValueError):rollback(p,receipt,True)
    assert p.read_text()=='later edit'


def test_candidate_needs_comparable_evaluations(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old')
    proposal=improve(p,lambda *_:'new',['x'],lambda text:dict(total=2 if text=='old' else 3,passed=1 if text=='old' else 3))
    assert not proposal['eligible']


def test_cli_requires_explicit_network_consent():
    proc=subprocess.run([sys.executable,'-m','runtime','--base-url','https://example.com/v1','--embedding-model','e','index','--database','unused.db'],capture_output=True,text=True)
    assert proc.returncode==2 and '--allow-network is required' in proc.stderr



def test_agent_council_is_connected(tmp_path):
    store=Memory(':memory:')
    models=[dict(id=m,capabilities=['text'],input_per_million=1,output_per_million=2) for m in ('a','b','j')]
    calls=[]
    def provider(model,messages):calls.append((model,messages));return 'fixture reply'
    agent=Agent(store,None,lambda _:[1,0],'e',provider,models)
    result=agent.run('task',tmp_path/'run','1',debate_models=['a','b'],judge='j')
    assert result['status']=='completed' and len(calls)==5
    assert len(result['model_calls'])==5 and len(result['debate']['critiques'])==2
    store.close()


def test_empty_model_reply_never_completes(tmp_path):
    store=Memory(':memory:')
    models=[dict(id='a',capabilities=['text'],input_per_million=1,output_per_million=2)]
    agent=Agent(store,None,lambda _:[1,0],'e',lambda *_:'',models)
    with pytest.raises(ValueError):agent.run('task',tmp_path/'run','1')
    assert not (tmp_path/'run').exists()
    store.close()


def test_index_embedding_space_is_preserved(tmp_path):
    skill=tmp_path/'x';skill.mkdir();(skill/'SKILL.md').write_text('---\ndescription: Testing semantic routing.\n---\ncontent')
    store=Memory(':memory:')
    index_skills(tmp_path,store,lambda _:[1,0],'space-a')
    assert store.search([1,0],'space-b')==[]
    assert store.search([1,0],'space-a')[0]['metadata']['content'].endswith('content')
    store.close()


def test_provider_rejects_unbounded_timeout():
    with pytest.raises(ValueError):OpenAICompatible('https://example.com',timeout=float('inf'))


def test_provider_rejects_zero_output_cap():
    with pytest.raises(ValueError):OpenAICompatible('https://example.com',max_output_tokens=0)


def test_invalid_evaluator_scores_block_promotion(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old')
    with pytest.raises(ValueError):improve(p,lambda *_:'new',['x'],lambda _:dict(passed=3,total=2))


def test_unchanged_candidate_is_not_improvement(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old')
    with pytest.raises(ValueError):improve(p,lambda *_:'old',['x'],lambda _:dict(passed=1,total=2))


def test_improvement_requires_attributed_failures(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old')
    with pytest.raises(ValueError):improve(p,lambda *_:'new',[],lambda _:dict(passed=1,total=2))


def test_rollback_requires_approval(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old')
    proposal=improve(p,lambda *_:'new',['x'],lambda text:dict(total=2,passed=1 if text=='old' else 2))
    receipt=promote(p,proposal,True)
    with pytest.raises(ValueError):rollback(p,receipt)
    assert p.read_text()=='new'


def test_cross_path_promotion_is_refused(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old');other=tmp_path/'OTHER.md';other.write_text('old')
    proposal=improve(p,lambda *_:'new',['x'],lambda text:dict(total=2,passed=1 if text=='old' else 2))
    with pytest.raises(ValueError):promote(other,proposal,True)
    assert other.read_text()=='old'


def test_candidate_requires_strict_improvement(tmp_path):
    p=tmp_path/'SKILL.md';p.write_text('old')
    proposal=improve(p,lambda *_:'new',['x'],lambda _:dict(total=2,passed=1))
    assert not proposal['eligible']


def test_budget_rejects_invalid_reservation():
    from runtime.orchestrator import Budget
    b=Budget('1')
    with pytest.raises(ValueError):b.reserve('-0.1')
    assert b.remaining==1


def test_memory_metadata_survives_restart(tmp_path):
    p=tmp_path/'m.db';m=Memory(p);m.put('a','lesson',[1,0],'e',{'source':'approved note'});m.close()
    m=Memory(p);assert m.search([1,0],'e')[0]['metadata']['source']=='approved note';m.close()


def test_no_memory_capture_without_explicit_save(tmp_path):
    m=Memory(tmp_path/'m.db');s=Memory(':memory:')
    agent=Agent(s,m,lambda _:[1,0],'e',lambda *_:'fixture', [dict(id='a',capabilities=['text'],input_per_million=1,output_per_million=2)])
    agent.run('private task',tmp_path/'run','1')
    assert m.search([1,0],'e')==[]
    m.close();s.close()


def test_index_accepts_folded_frontmatter_only(tmp_path):
    skill=tmp_path/'x';skill.mkdir();(skill/'SKILL.md').write_text('---\nname: x\ndescription: >-\n  Semantic routing with real\n  embedding context.\n---\nbody\ndescription: not metadata')
    store=Memory(':memory:');embedded=[]
    index_skills(tmp_path,store,lambda text:embedded.append(text) or [1,0],'e')
    assert embedded==['Semantic routing with real embedding context.']
    store.close()


def test_body_description_cannot_impersonate_frontmatter(tmp_path):
    skill=tmp_path/'x';skill.mkdir();(skill/'SKILL.md').write_text('---\nname: x\n---\ndescription: fake')
    store=Memory(':memory:')
    with pytest.raises(ValueError):index_skills(tmp_path,store,lambda _:[1,0],'e')
    store.close()


def test_output_cap_mismatch_blocks_before_embedding(tmp_path):
    store=Memory(':memory:');embedded=[]
    provider=OpenAICompatible('https://example.com',max_output_tokens=4096)
    a=Agent(store,None,lambda _:embedded.append('called') or [1,0],'e',provider,[])
    with pytest.raises(ValueError):a.run('task',tmp_path/'run','1',output_tokens=1024)
    assert not embedded
    store.close()


def test_improvement_rejects_flaky_evaluation(tmp_path):
    path=tmp_path/'SKILL.md';path.write_text('old');calls={'old':0,'new':0}
    def flaky(text):
        calls[text]+=1
        return dict(total=3,passed=calls[text])
    with pytest.raises(ValueError):improve(path,lambda *_:'new',['case'],flaky)


def test_heldout_regression_blocks_candidate(tmp_path):
    path=tmp_path/'SKILL.md';path.write_text('old')
    score=lambda text:dict(total=2,passed=1 if text=='old' else 2)
    heldout=lambda text:dict(total=2,passed=2 if text=='old' else 1)
    p=improve(path,lambda *_:'new',['case'],score,heldout_evaluator=heldout)
    assert not p['eligible']
