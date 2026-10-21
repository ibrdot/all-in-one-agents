import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime.council import council
from runtime.evaluation import evaluate,propose_improvement


def test_debate_stages():
    calls=[]
    def provider(model,messages):
        calls.append((model,messages))
        return 'answer '+model
    r=council('solve', ['a','b'],'judge',provider)
    assert r['status']=='completed' and len(calls)==5
    assert set(r['critiques'])=={'a','b'}
    for _,messages in calls:
        assert messages[0]['role']=='system'


def test_provider_failure_is_not_consensus():
    def broken(*args):raise RuntimeError('secret should not enter report')
    r=council('x',['a','b'],'judge',broken)
    assert r['status']=='insufficient_proposals' and r['synthesis'] is None
    assert 'secret' not in str(r)


def test_critique_failure_blocks_completion():
    def provider(model,msg):
        if msg[0]['content'].startswith('Critique'):raise ValueError()
        return 'ok'
    assert council('x',['a','b'],'j',provider)['status']=='incomplete_debate'


def test_synthesis_failure():
    def provider(model,msg):
        if model=='judge':raise ValueError()
        return 'ok'
    assert council('x',['a','b'],'judge',provider)['status']=='synthesis_failed'


@pytest.mark.parametrize('models',[[],['a'],['a','a']])
def test_council_bad_models(models):
    with pytest.raises(ValueError):council('x',models,'judge',lambda *_:'ok')


def test_golden_regression_detection():
    cases=[dict(id='a',exact='yes',skill='tdd'),dict(id='b',contains=['verified'],forbidden=['guaranteed'])]
    baseline=evaluate(cases,{'a':'yes','b':'verified'})
    current=evaluate(cases,{'a':'no','b':'verified guaranteed'},baseline)
    assert current['regressions']==['a','b'] and current['passed']==0


def test_missing_answer_fails():
    assert evaluate([dict(id='a',exact='ok')],{})['passed']==0


def test_no_assertions_rejected():
    with pytest.raises(ValueError):evaluate([dict(id='a')],{})


def test_improvement_does_not_rewrite(tmp_path):
    path=tmp_path/'tdd'/'SKILL.md';path.parent.mkdir();path.write_text('original')
    r=evaluate([dict(id='a',exact='yes',skill='tdd')],{'a':'no'})
    proposal=propose_improvement(path,r,'new candidate')
    assert path.read_text()=='original' and proposal['failing_cases']==['a']
    assert proposal['status']=='needs_review_and_re_evaluation'


def test_no_failure_no_rewrite(tmp_path):
    with pytest.raises(ValueError):propose_improvement(tmp_path/'SKILL.md',{'results':[]},'candidate')


@pytest.mark.parametrize('case',[dict(id='x',contains=[]),dict(id='x',exact=2)])
def test_vacuous_assertions_rejected(case):
    with pytest.raises(ValueError):evaluate([case],{'x':'ok'})
