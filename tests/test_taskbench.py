"""Objective tasks are distinct from fixture-model contract checks."""
import json
from pathlib import Path
import pytest
from runtime.taskbench import load_tasks, grade, evaluate, compare
ROOT=Path(__file__).resolve().parents[1]


def test_fifty_distinct_tasks():
    tasks=load_tasks(ROOT/'evals/tasks/tasks.json')
    assert len(tasks)==50 and len({t['id'] for t in tasks})==50
    assert {t['kind'] for t in tasks}=={'python','json'}
    assert all('expected' not in t['prompt'] and len(t['prompt'])>40 for t in tasks)


def test_correct_json_is_graded_and_extra_prose_rejected():
    task={'id':'x','kind':'json','checks':[{'path':['replicas'],'equals':3}]}
    assert grade(task,'{"replicas":3}')['passed']
    assert not grade(task,'Here is JSON: {"replicas":3}')['passed']
    assert not grade(task,'{"replicas":1}')['passed']


def test_python_execution_requires_separate_consent():
    t={'id':'x','kind':'python','checks':[{'args':[1],'expected':2}]}
    with pytest.raises(ValueError):grade(t,'def solve(x): return x+1')


def test_python_objective_tests_detect_incorrect_solution():
    t={'id':'x','kind':'python','checks':[{'args':[1],'expected':2},{'args':[0],'expected':1}]}
    assert grade(t,'def solve(x): return x+1',allow_code_execution=True)['passed']
    assert not grade(t,'def solve(x): return 2',allow_code_execution=True)['passed']


def test_python_timeout_is_failure():
    t={'id':'x','kind':'python','checks':[{'args':[1],'expected':2}]}
    result=grade(t,'def solve(x):\n while True: pass',allow_code_execution=True,timeout=.3)
    assert not result['passed']


def test_replay_records_missing_responses_and_no_invented_scores(tmp_path):
    tasks=[{'id':'a','kind':'json','prompt':'Return object','checks':[{'path':['ok'],'equals':True}]}]
    report=evaluate(tasks,{},tmp_path/'run',source='replay')
    assert report['passed']==0 and report['results'][0]['reason']=='missing response'
    assert report['source']=='replay' and (tmp_path/'run'/'report.json').exists()


def test_baseline_requires_matching_suite():
    with pytest.raises(ValueError):compare({'suite_sha256':'a','results':[]},{'suite_sha256':'b','results':[]})


def test_regressions_are_per_task():
    old={'suite_sha256':'a','results':[{'id':'x','passed':True}]}
    new={'suite_sha256':'a','results':[{'id':'x','passed':False}]}
    assert compare(new,old)==['x']


@pytest.mark.parametrize('response',['{"ok":true,"ok":false}','{"ok":NaN}','{"ok":1}'])
def test_json_duplicate_nonfinite_and_bool_confusion_rejected(response):
    assert not grade({'id':'x','kind':'json','checks':[{'path':['ok'],'equals':True}]},response)['passed']


def test_public_prompt_and_private_grader_are_separate():
    tasks=load_tasks(ROOT/'evals/tasks/tasks.json')
    assert all('checks' not in task['prompt'] for task in tasks)
    assert len({task['prompt'] for task in tasks})==50


def test_reference_calibration_is_not_labeled_live(tmp_path):
    data=json.loads((ROOT/'evals/tasks/reference-responses.json').read_text())
    tasks=load_tasks(ROOT/'evals/tasks/tasks.json')
    r=evaluate(tasks,data['responses'],tmp_path/'calibration','reference-calibration',True)
    assert r['passed']==50 and r['source']=='reference-calibration'


def test_deep_json_is_failed_not_grader_crash():
    task={'id':'x','kind':'json','checks':[{'path':[],'equals':{}}]}
    assert not grade(task,'['*2000+'0'+']'*2000)['passed']


def test_each_python_check_gets_fresh_runner():
    task={'id':'x','kind':'python','checks':[{'args':[1],'expected':2},{'args':[2],'expected':3}]}
    source="def solve(x):\n open('runner.py','w').write('raise RuntimeError()')\n return x+1"
    assert grade(task,source,True)['passed']
