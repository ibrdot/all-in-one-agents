"""Offline integration contracts; local HTTP is real, model replies are fixtures."""
import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import pytest
from runtime.providers import OpenAICompatible
from runtime.orchestrator import Agent, index_skills, Budget
from runtime.core import Memory
from runtime.improvement import improve, promote, rollback


@pytest.fixture
def endpoint(monkeypatch):
    requests = []
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            requests.append((self.path, data, self.headers.get('Authorization')))
            if data['model'] == 'broken':
                self.send_response(401); self.end_headers(); self.wfile.write(b'SUPERSECRET'); return
            body = {'data': [{'index': 0, 'embedding': [1., 0.]}]} if self.path.endswith('embeddings') else {'choices': [{'message': {'content': 'fixture response'}}]}
            self.send_response(200); self.end_headers(); self.wfile.write(json.dumps(body).encode())
        def log_message(self, *args): pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    monkeypatch.setenv('TEST_AGENT_KEY', 'fixture-secret')
    yield f'http://127.0.0.1:{server.server_port}/v1', requests
    server.shutdown(); server.server_close(); thread.join()


def test_http_adapter(endpoint):
    url, calls = endpoint
    p = OpenAICompatible(url, 'TEST_AGENT_KEY', allow_local_http=True)
    assert p.embed('emb', 'task') == [1., 0.]
    assert p('chat', [{'role': 'user', 'content': 'task'}]) == 'fixture response'
    assert calls[0][0] == '/v1/embeddings'
    assert calls[1][2] == 'Bearer fixture-secret'


def test_http_errors_redacted(endpoint):
    p = OpenAICompatible(endpoint[0], 'TEST_AGENT_KEY', allow_local_http=True)
    with pytest.raises(RuntimeError) as exc: p('broken', [])
    assert 'SUPERSECRET' not in str(exc.value) and '401' in str(exc.value)


@pytest.mark.parametrize('url', ['http://example.com', 'https://user:pass@example.com', 'https://example.com/?key=secret'])
def test_provider_url_guards(url):
    with pytest.raises(ValueError): OpenAICompatible(url, 'KEY')


def test_provider_missing_key(monkeypatch):
    monkeypatch.delenv('MISSING_TEST_KEY', raising=False)
    p = OpenAICompatible('https://example.com/v1', 'MISSING_TEST_KEY')
    with pytest.raises(ValueError): p('chat', [])


def test_budget_reserves_before_call():
    b = Budget('0.01')
    b.reserve('0.006')
    with pytest.raises(ValueError): b.reserve('0.005')
    assert str(b.remaining) == '0.004'


@pytest.mark.parametrize('amount', ['-1', 'NaN', 'Infinity'])
def test_budget_invalid(amount):
    with pytest.raises(ValueError): Budget(amount)


MODELS = [{'id': 'small', 'capabilities': ['text'], 'input_per_million': 1, 'output_per_million': 2}]


def test_connected_routing_memory_and_evidence(tmp_path):
    skill = tmp_path / 'skills' / 'testing'; skill.mkdir(parents=True)
    (skill / 'SKILL.md').write_text('---\nname: testing\ndescription: Write failing tests before fixing code.\n---\nTest first.')
    db = tmp_path / 'skills.db'
    store = Memory(db)
    assert index_skills(tmp_path / 'skills', store, lambda _: [1., 0.], 'embed') == 1
    store.close(); store = Memory(db)
    memory = Memory(tmp_path / 'memory.db')
    memory.put('lesson', 'Previous bug: reject empty input.', [1., 0.], 'embed')
    calls = []
    def provider(model, messages): calls.append(messages); return 'fixture answer'
    agent = Agent(store, memory, lambda _: [1., 0.], 'embed', provider, MODELS)
    result = agent.run('fix validation', tmp_path / 'run', budget='0.1')
    assert result['status'] == 'completed'
    assert result['skills'] == ['testing']
    assert 'Previous bug' in calls[0][-1]['content']
    assert 'Test first.' in calls[0][-1]['content']
    manifest = json.loads((tmp_path / 'run' / 'manifest.json').read_text())
    assert manifest['passed'] and result['evidence']['passed']
    from runtime.core import verify_evidence
    assert verify_evidence(tmp_path / 'run', manifest['records'])['passed']
    assert not (tmp_path / 'run' / 'secret').exists()
    store.close(); memory.close()


def test_agent_insufficient_budget_no_provider(tmp_path):
    store = Memory(':memory:'); calls = []
    agent = Agent(store, None, lambda _: [1., 0.], 'emb', lambda *a: calls.append(a), MODELS)
    with pytest.raises(ValueError): agent.run('task', tmp_path / 'run', budget='0')
    assert calls == []
    store.close()


def test_improvement_evaluated_then_explicit_promotion(tmp_path):
    path = tmp_path / 'SKILL.md'; path.write_text('old')
    def evaluator(text): return {'passed': 2 if text == 'better' else 1, 'total': 2, 'regressions': []}
    p = improve(path, lambda old, failures: 'better', ['case-1'], evaluator)
    assert p['eligible'] and path.read_text() == 'old'
    with pytest.raises(ValueError): promote(path, p, approved=False)
    receipt = promote(path, p, approved=True)
    assert path.read_text() == 'better'
    rollback(path, receipt, approved=True)
    assert path.read_text() == 'old'


def test_improvement_blocks_regression_and_stale_write(tmp_path):
    path = tmp_path / 'SKILL.md'; path.write_text('old')
    p = improve(path, lambda *_: 'new', ['x'], lambda text: {'passed': 2, 'total': 2, 'regressions': ['x']})
    assert not p['eligible']
    with pytest.raises(ValueError): promote(path, p, approved=True)
    p = improve(path, lambda *_: 'new', ['x'], lambda text: {'passed': 1 if text == 'old' else 2, 'total': 2, 'regressions': []})
    path.write_text('concurrent update')
    with pytest.raises(ValueError): promote(path, p, approved=True)
    assert path.read_text() == 'concurrent update'


def test_http_rejects_truncated_and_redirected_responses(monkeypatch):
    seen=[]
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            data=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            seen.append(self.path)
            if data['model']=='redirect':
                self.send_response(307);self.send_header('Location','/leaked');self.end_headers();return
            self.send_response(200);self.end_headers()
            self.wfile.write(json.dumps({'choices':[{'finish_reason':'length','message':{'content':'partial'}}]}).encode())
        def log_message(self,*_):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    monkeypatch.setenv('TEST_AGENT_KEY','fixture-key')
    monkeypatch.setenv('http_proxy','http://127.0.0.1:1')
    try:
        p=OpenAICompatible(f'http://127.0.0.1:{server.server_port}/v1','TEST_AGENT_KEY',allow_local_http=True)
        with pytest.raises(RuntimeError,match='incomplete'):p('truncate',[])
        with pytest.raises(RuntimeError,match='307'):p('redirect',[])
        assert '/leaked' not in seen
    finally:
        server.shutdown();server.server_close();thread.join()


def test_every_repository_skill_can_be_semantically_indexed(tmp_path):
    root=Path(__file__).resolve().parents[1]/'skills'
    store=Memory(tmp_path/'all.db');calls=[]
    count=index_skills(root,store,lambda text:calls.append(text) or [1.,0.],'fixture-space')
    assert count==len(list(root.glob('*/SKILL.md'))) and count>=140
    assert len(calls)==count and all(c.strip() for c in calls)
    store.close()
