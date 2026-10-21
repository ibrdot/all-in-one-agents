"""Evaluation-led skill candidates with explicit review and stale-write guards.

Evaluators and generators are caller-selected code. Their trust/held-out quality
is not established by a score. Promotion never happens automatically.
"""
import hashlib
from pathlib import Path
import os
import tempfile


def _hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _score(report):
    passed, total = report['passed'], report['total']
    if type(passed) is not int or type(total) is not int or not 0 <= passed <= total or total < 1:
        raise ValueError('invalid evaluation counts')
    return passed, total


def improve(path, generator, failures, evaluator, heldout_evaluator=None, repeats=2):
    path = Path(path)
    if path.is_symlink(): raise ValueError('symlink skill refused')
    original = path.read_text(encoding='utf-8')
    if not isinstance(failures, list) or not failures or any(not isinstance(x, str) or not x for x in failures):
        raise ValueError('attributed failing case ids required')
    candidate = generator(original, failures)
    if not isinstance(candidate, str) or not candidate.strip() or candidate == original:
        raise ValueError('nonempty changed candidate required')
    if type(repeats) is not int or repeats < 2:
        raise ValueError('at least two repeat evaluations required')
    def stable(evaluate, text):
        reports = [evaluate(text) for _ in range(repeats)]
        signature = lambda r: (_score(r), tuple(r.get('regressions', [])))
        if any(signature(r) != signature(reports[0]) for r in reports[1:]):
            raise ValueError('unstable evaluation; candidate needs investigation')
        return reports[0]
    before, after = stable(evaluator, original), stable(evaluator, candidate)
    bp, bt = _score(before); ap, at = _score(after)
    heldout = None
    heldout_passed = True
    if heldout_evaluator:
        hb, ha = stable(heldout_evaluator, original), stable(heldout_evaluator, candidate)
        hbp, hbt = _score(hb); hap, hat = _score(ha)
        heldout_passed = hbt == hat and hap >= hbp and not ha.get('regressions')
        heldout = dict(before=hb, after=ha, passed=bool(heldout_passed))
    eligible = bt == at and ap > bp and not after.get('regressions') and heldout_passed
    return dict(path=str(path.resolve()), original=original, candidate=candidate,
                original_sha256=_hash(original), candidate_sha256=_hash(candidate),
                failures=failures, before=before, after=after, eligible=eligible,
                requires_reindex=True, heldout=heldout, repeat_count=repeats, trust='caller-supplied evaluations; not independent proof')


def _write(path, text):
    # Atomic per-file replacement. Concurrent writers must be stopped by caller;
    # hash checks are stale-write guards, not cross-process locks.
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.skill-review-')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, path.stat().st_mode & 0o777)
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)


def promote(path, proposal, approved=False):
    path = Path(path)
    if approved is not True or not proposal['eligible']:
        raise ValueError('review approval and improved evaluation required')
    if path.is_symlink() or str(path.resolve()) != proposal['path']:
        raise ValueError('proposal path mismatch')
    bp, bt = _score(proposal['before']); ap, at = _score(proposal['after'])
    if proposal.get('heldout') and not proposal['heldout']['passed']:
        raise ValueError('held-out evaluation regressed')
    if bt != at or ap <= bp or proposal['after'].get('regressions'):
        raise ValueError('candidate did not improve without regression')
    if _hash(proposal['candidate']) != proposal['candidate_sha256'] or _hash(proposal['original']) != proposal['original_sha256']:
        raise ValueError('proposal content changed after evaluation')
    if _hash(path.read_text(encoding='utf-8')) != proposal['original_sha256']:
        raise ValueError('skill changed since evaluation')
    _write(path, proposal['candidate'])
    return dict(path=str(path.resolve()), previous=proposal['original'],
                previous_sha256=proposal['original_sha256'], promoted_sha256=proposal['candidate_sha256'],
                requires_reindex=True)


def rollback(path, receipt, approved=False):
    path = Path(path)
    if approved is not True or path.is_symlink() or str(path.resolve()) != receipt['path']:
        raise ValueError('explicit approval and matching path required')
    if _hash(path.read_text(encoding='utf-8')) != receipt['promoted_sha256'] or _hash(receipt['previous']) != receipt['previous_sha256']:
        raise ValueError('rollback receipt stale or altered')
    _write(path, receipt['previous'])
