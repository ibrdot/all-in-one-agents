"""Persistent vector retrieval, evidence checks and explicit cost routing.
Embeddings must come from one caller-selected embedding model; none are faked.
"""
import hashlib
import json
import math
from pathlib import Path
import sqlite3
from decimal import Decimal


def vector(values):
    if not isinstance(values, list) or not values:
        raise ValueError('embedding must be a nonempty list')
    if any(type(x) not in (int,float) or not math.isfinite(x) for x in values):
        raise ValueError('embedding must contain finite numbers')
    norm=math.hypot(*values)
    if not math.isfinite(norm) or norm==0:
        raise ValueError('embedding norm must be finite and nonzero')
    return [x/norm for x in values]


class Memory:
    """Local SQLite store. Explicit saves only; no automatic private-data capture.

    model is an embedding-space identifier, not a chat-model name. Matching
    dimensions alone do not make different embedding models compatible.
    """
    def __init__(self,path):
        self.db=sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS memory (id TEXT PRIMARY KEY, text TEXT NOT NULL, model TEXT NOT NULL, embedding TEXT NOT NULL, metadata TEXT NOT NULL)')

    def close(self):
        self.db.close()

    def put(self,key,text,embedding,model,metadata=None):
        if not all(isinstance(x,str) and x for x in (key,text,model)):
            raise ValueError('key, text and model must be nonempty strings')
        v=vector(embedding)
        dimensions={len(json.loads(r[0])) for r in self.db.execute('SELECT embedding FROM memory WHERE model=? AND id<>?',(model,key))}
        if dimensions and dimensions!={len(v)}:
            raise ValueError('dimension mismatch within embedding model')
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO memory VALUES(?,?,?,?,?)',(key,text,model,json.dumps(v),json.dumps(metadata or {})))

    def delete(self,key):
        with self.db:
            self.db.execute('DELETE FROM memory WHERE id=?',(key,))

    def search(self,embedding,model,limit=5,min_score=0):
        q=vector(embedding)
        if type(limit) is not int or limit<1:
            raise ValueError('limit must be positive integer')
        if not isinstance(min_score,(int,float)) or not math.isfinite(min_score) or not -1<=min_score<=1:
            raise ValueError('invalid cosine threshold')
        hits=[]
        for key,text,raw,metadata in self.db.execute('SELECT id,text,embedding,metadata FROM memory WHERE model=?',(model,)):
            v=json.loads(raw)
            if len(v)!=len(q):
                raise ValueError('query embedding dimension mismatch')
            score=sum(a*b for a,b in zip(q,v))
            if score>=min_score:
                hits.append(dict(id=key,text=text,score=score,metadata=json.loads(metadata)))
        return sorted(hits,key=lambda x:(-x['score'],x['id']))[:limit]


def route_skills(store,embedding,model,token_budget=4000,limit=4):
    """Select by cosine similarity with a caller-supplied token estimate.

    Index only skill descriptions here, not unrelated personal memory. No LLM
    call or keyword matching is performed. Missing token costs fail closed.
    """
    if type(token_budget) is not int or token_budget<=0 or type(limit) is not int or limit<=0:
        raise ValueError('budget and limit must be positive integers')
    selected=[]; used=0
    for hit in store.search(embedding,model,limit=100000,min_score=0.1):
        tokens=hit['metadata'].get('tokens')
        if type(tokens) is not int or tokens<=0:
            raise ValueError(f"missing positive token estimate: {hit['id']}")
        if used+tokens<=token_budget:
            selected.append(hit); used+=tokens
        if len(selected)==limit: break
    return dict(skills=selected,estimated_tokens=used,abstained=not selected)


def verify_evidence(root,records):
    """Verify bounded local artifacts by SHA256; never follow outside-root paths.
    Matching a digest proves bytes, not truth of a screenshot or claim.
    """
    root=Path(root).resolve(); results=[]
    for record in records:
        path=(root/record['path']).resolve()
        if not path.is_relative_to(root): raise ValueError('evidence escapes root')
        digest=hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda:stream.read(65536),b''): digest.update(chunk)
        results.append(dict(path=record['path'],valid=digest.hexdigest()==record['sha256']))
    return dict(passed=all(r['valid'] for r in results) and bool(results),artifacts=results)


def select_model(models,required_capabilities,input_tokens,output_tokens,budget):
    """Cheapest eligible explicitly priced model; no subjective difficulty guess."""
    if any(type(x) is not int or x<0 for x in (input_tokens,output_tokens)):
        raise ValueError('token estimates must be nonnegative integers')
    ceiling=Decimal(str(budget))
    if not ceiling.is_finite() or ceiling<0: raise ValueError('invalid budget')
    choices=[]
    for item in models:
        pin,pout=Decimal(str(item['input_per_million'])),Decimal(str(item['output_per_million']))
        if not all(x.is_finite() and x>=0 for x in (pin,pout)): raise ValueError('invalid price')
        if not set(required_capabilities)<=set(item['capabilities']):continue
        cost=(input_tokens*pin+output_tokens*pout)/Decimal(1000000)
        if cost<=ceiling: choices.append((cost,item['id']))
    if not choices: return None
    cost,model=min(choices)
    return dict(model=model,estimated_usd=str(cost))
