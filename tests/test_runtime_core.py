import hashlib
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime.core import Memory,vector,route_skills,verify_evidence,select_model


@pytest.mark.parametrize('bad',[[],[0,0],[float('nan')],[float('inf')],[True],['x']])
def test_bad_vectors(bad):
    with pytest.raises(ValueError):vector(bad)


def test_persistent_retrieval_and_delete(tmp_path):
    path=tmp_path/'memory.db'; m=Memory(path)
    m.put('db','Database investigation',[1,0],'embedding-v1')
    m.put('ui','Frontend component',[0,1],'embedding-v1')
    m.close(); m=Memory(path)
    assert m.search([.9,.1],'embedding-v1')[0]['id']=='db'
    assert m.search([1,0],'other-model')==[]
    m.delete('db'); assert m.search([1,0],'embedding-v1',min_score=.5)==[]
    m.close()


def test_embedding_dimensions(tmp_path):
    m=Memory(tmp_path/'a.db');m.put('x','x',[1,0],'v1')
    with pytest.raises(ValueError):m.put('y','y',[1,0,0],'v1')
    with pytest.raises(ValueError):m.search([1,0,0],'v1')
    m.close()


def test_semantic_routing_budget_abstention(tmp_path):
    m=Memory(tmp_path/'a.db')
    m.put('db','db',[1,0],'v1',{'tokens':100})
    m.put('ui','ui',[0,1],'v1',{'tokens':100})
    assert route_skills(m,[1,0],'v1',100)['skills'][0]['id']=='db'
    assert route_skills(m,[1,0],'v1',10)['abstained']
    m.close()


def test_routing_requires_costs(tmp_path):
    m=Memory(tmp_path/'a.db');m.put('x','x',[1,0],'v1')
    with pytest.raises(ValueError):route_skills(m,[1,0],'v1')
    m.close()


def test_evidence_tampering_and_escape(tmp_path):
    p=tmp_path/'log.txt';p.write_text('pass')
    rec=[{'path':'log.txt','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]
    assert verify_evidence(tmp_path,rec)['passed']
    p.write_text('changed');assert not verify_evidence(tmp_path,rec)['passed']
    with pytest.raises(ValueError):verify_evidence(tmp_path,[{'path':'../outside','sha256':'x'}])
    assert not verify_evidence(tmp_path,[])['passed']


MODELS=[{'id':'small','input_per_million':1,'output_per_million':2,'capabilities':['json']},
        {'id':'large','input_per_million':5,'output_per_million':10,'capabilities':['json','vision']}]


def test_cost_selection():
    assert select_model(MODELS,['json'],1000000,0,10)['model']=='small'
    assert select_model(MODELS,['vision'],1000000,0,10)['model']=='large'
    assert select_model(MODELS,['vision'],1000000,0,1) is None


def test_invalid_prices():
    with pytest.raises(ValueError):select_model([dict(MODELS[0],input_per_million='NaN')],[],1,1,10)
