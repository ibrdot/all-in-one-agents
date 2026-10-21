"""Live generation test doubles are labeled; no billed API calls in this suite."""
import pytest
from runtime.taskbench import generate


def test_generation_never_sends_hidden_checks_to_provider():
    calls=[]
    def provider(model,messages):calls.append(messages);return '{"ok":true}'
    task={'id':'a','kind':'json','prompt':'Return ok true','checks':[{'path':[],'equals':{'hidden-secret-grader':True}}]}
    report=generate([task],provider,'model-a',max_calls=1)
    assert 'hidden-secret-grader' not in str(calls)
    assert report['responses']['a']=='{"ok":true}' and report['model']=='model-a'


def test_generation_cap_checked_before_any_call():
    calls=[]
    with pytest.raises(ValueError):generate([{'id':'a','prompt':'one'},{'id':'b','prompt':'two'}],lambda *x:calls.append(x),'model-a',max_calls=1)
    assert calls==[]


def test_generation_retains_per_task_errors_without_secret_text():
    def provider(*_):raise RuntimeError('PRIVATE_API_KEY')
    r=generate([{'id':'a','prompt':'one'}],provider,'m',max_calls=1)
    assert r['errors']=={'a':'RuntimeError'} and 'PRIVATE_API_KEY' not in str(r)
