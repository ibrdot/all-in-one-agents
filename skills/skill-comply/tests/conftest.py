"""Isolate this skill's ``scripts`` package from the repo-root ``scripts`` directory.

Collected from the repo root, ``from scripts import parser`` resolves to the
root-level ``scripts/`` namespace package instead of the one beside this skill.
Insert the skill root first and drop any namespace already cached.
"""
import os
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for _name in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
    del sys.modules[_name]

sys.path.insert(0, SKILL_ROOT)
