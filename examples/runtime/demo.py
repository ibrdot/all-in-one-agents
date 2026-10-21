#!/usr/bin/env python3
"""Offline wiring demonstration. Embeddings/provider responses are test fixtures,
not a live AI evaluation. Run from repository root: python3 examples/runtime/demo.py
"""
from pathlib import Path
import json
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from runtime.core import Memory,route_skills,select_model
from runtime.council import council
from runtime.evaluation import evaluate


def main():
    with tempfile.TemporaryDirectory() as tmp:
        memory=Memory(Path(tmp)/'demo.db')
        try:
            memory.put('systematic-debugging','Diagnose a failing service',[1,0],'fixture-only',{'tokens':500})
            memory.put('docx','Create a Word document',[0,1],'fixture-only',{'tokens':500})
            routing=route_skills(memory,[1,0],'fixture-only',1000)
        finally:
            memory.close()
    models=[dict(id='fixture-small',capabilities=['text'],input_per_million='1',output_per_million='2')]
    selected=select_model(models,['text'],1000,500,'0.01')
    def mock_provider(model,messages):
        phase=messages[0]['content'].split()[0]
        return f'{model}: {phase}. Evidence must be checked independently.'
    debate=council('Investigate a reproducible failure',['fixture-a','fixture-b'],'fixture-judge',mock_provider)
    evaluation=evaluate([dict(id='evidence',contains=['Evidence'])],{'evidence':debate['synthesis']})
    print(json.dumps(dict(mode='offline fixtures, not live models',routing=routing,selection=selected,debate=debate,evaluation=evaluation),indent=2))


if __name__=='__main__':main()
