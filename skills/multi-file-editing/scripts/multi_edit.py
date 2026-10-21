#!/usr/bin/env python3
"""Preview hash-checked exact-text edits; opt in to per-file atomic writes."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile


def prepare(root, plan):
    root = Path(root).resolve(strict=True)
    if not isinstance(plan, list) or not plan:
        raise ValueError("plan must be a non-empty array")
    prepared, seen = [], set()
    for edit in plan:
        if not isinstance(edit, dict) or set(edit) != {"path", "sha256", "old", "new", "count"}:
            raise ValueError("each edit requires path, sha256, old, new, count only")
        if not isinstance(edit["path"], str) or not edit["path"]:
            raise ValueError("path must be a non-empty relative string")
        rel = Path(edit["path"])
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError("path must stay inside root")
        target = root
        for part in rel.parts:
            target = target / part
            if target.is_symlink():
                raise ValueError("symlinks are not supported")
        path = target.resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file() or path in seen:
            raise ValueError("invalid or duplicate path")
        seen.add(path)
        before = path.read_bytes()
        if b"\x00" in before:
            raise ValueError("binary content is not supported")
        if hashlib.sha256(before).hexdigest() != edit["sha256"]:
            raise ValueError(f"stale hash: {rel}")
        old, new, count = edit["old"], edit["new"], edit["count"]
        if not isinstance(old, str) or not old or not isinstance(new, str) or old == new:
            raise ValueError("replacement must contain non-empty old text and change it")
        if "\x00" in old or "\x00" in new:
            raise ValueError("NUL bytes are not supported")
        if type(count) is not int or count < 1:
            raise ValueError("count must be a positive integer")
        text = before.decode("utf-8")
        if text.count(old) != count:
            raise ValueError(f"unexpected match count: {rel}")
        after = text.replace(old, new).encode("utf-8")
        prepared.append((path, before, after))
    return prepared


def run(root, plan, apply=False):
    root = Path(root).resolve(strict=True)
    prepared = prepare(root, plan)
    for path, before, after in prepared:
        label = path.relative_to(root).as_posix()
        print("".join(difflib.unified_diff(before.decode().splitlines(True),
              after.decode().splitlines(True), fromfile="a/"+label, tofile="b/"+label)), end="")
    if apply:
        for path, before, after in prepared:
            if path.is_symlink() or path.read_bytes() != before:
                raise ValueError(f"file changed after validation: {path}")
            fd, temporary = tempfile.mkstemp(prefix=".multi-edit-", dir=path.parent)
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(after)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.chmod(temporary, stat.S_IMODE(path.stat().st_mode))
                os.replace(temporary, path)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
    return len(prepared)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        count = run(args.root, plan, args.apply)
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(1, f"edit failed (inspect diff for partial writes): {exc}\n")
    print(f"{count} file(s) {'applied' if args.apply else 'previewed; no files written'}")


if __name__ == "__main__":
    main()
