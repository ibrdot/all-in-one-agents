"""Explicit OpenAI-compatible HTTP boundary. No automatic retries or model aliases.

Credentials are read from an environment variable, never accepted as CLI text.
HTTPS is mandatory except explicitly enabled loopback HTTP for local servers.
Redirects are refused to avoid forwarding credentials to a different endpoint.
"""
import json
import math
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler
from runtime.core import vector


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class OpenAICompatible:
    def __init__(self, base_url, key_env='OPENAI_API_KEY', timeout=30,
                 max_output_tokens=1024, allow_local_http=False):
        parts = urlsplit(base_url)
        try:
            parts.port
        except ValueError:
            raise ValueError('invalid endpoint port') from None
        local = parts.hostname in ('localhost', '127.0.0.1', '::1')
        if (parts.scheme != 'https' and not (allow_local_http and local and parts.scheme == 'http')) or not parts.hostname:
            raise ValueError('HTTPS endpoint required; loopback HTTP requires explicit opt-in')
        if parts.username or parts.password or parts.query or parts.fragment:
            raise ValueError('endpoint must not contain credentials, query or fragment')
        if type(timeout) not in (int, float) or not math.isfinite(timeout) or not 0 < timeout <= 300:
            raise ValueError('timeout must be 0 < seconds <= 300')
        if type(max_output_tokens) is not int or max_output_tokens < 1:
            raise ValueError('positive output limit required')
        if not isinstance(key_env, str) or not key_env:
            raise ValueError('key environment variable name required')
        self.base_url = base_url.rstrip('/')
        self.key_env = key_env
        self.timeout = timeout
        self.max_output_tokens = max_output_tokens

    def _post(self, path, body):
        key = os.environ.get(self.key_env)
        if not key:
            raise ValueError(f'missing credential environment variable: {self.key_env}')
        request = Request(self.base_url + path, data=json.dumps(body).encode(),
                          headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        try:
            with build_opener(_NoRedirect(), ProxyHandler({})).open(request, timeout=self.timeout) as response:
                raw = response.read(8 * 1024 * 1024 + 1)
                if len(raw) > 8 * 1024 * 1024:
                    raise RuntimeError('provider response exceeds size limit')
                return json.loads(raw)
        except HTTPError as exc:
            raise RuntimeError(f'provider HTTP {exc.code}') from None
        except (URLError, OSError, ValueError):
            raise RuntimeError('provider transport or JSON failure') from None

    def __call__(self, model, messages):
        result = self._post('/chat/completions', dict(model=model, messages=messages,
                            max_tokens=self.max_output_tokens))
        try:
            choice = result['choices'][0]
            if choice.get('finish_reason') not in (None, 'stop'):
                raise RuntimeError('provider response incomplete or refused')
            text = choice['message']['content']
            if not isinstance(text, str) or not text.strip(): raise ValueError()
            return text
        except (KeyError, IndexError, TypeError, ValueError):
            raise RuntimeError('invalid provider chat response') from None

    def embed(self, model, text):
        result = self._post('/embeddings', dict(model=model, input=text))
        try:
            values = result['data'][0]['embedding']
            vector(values)  # Validate; Memory performs normalization itself.
            return values
        except (KeyError, IndexError, TypeError, ValueError):
            raise RuntimeError('invalid provider embedding response') from None
