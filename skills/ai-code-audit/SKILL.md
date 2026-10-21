---
name: ai-code-audit
description: "Use when reviewing AI-generated or AI-assisted code before merge - catches hallucinated APIs, subtle logic inversions, silent error swallowing, test-gaming, and security holes that look perfectly plausible."
---

# AI Code Audit

AI-generated code has a signature failure mode: it is fluent first and correct second. Human review calibrated for human code under-detects it. This skill is a checklist for the failure classes that only (or mostly) AI code exhibits.

## The seven tells

Check every AI-generated diff for these, in order:

1. **Hallucinated surface.** Methods, params, config keys, or package flags that do not exist. Compilers catch most; dynamically typed and config-adjacent hallucinations reach production. Verify every nonstandard call against the real signature, not the AI's memory of it.
2. **Inverted logic in plausible clothing.** Off-by-one and inverted conditions read beautifully. Re-derive boundary conditions yourself: empty, one, many, max+1, negative, unicode, concurrent.
3. **Swallowed errors.** `except: pass`, `.catch(() => {})`, defaulting-on-failure (`x = maybe_null ?? {}`) that turns data loss into silent zeros. Trace what happens when every `try` actually fires.
4. **Test gaming.** Tests that assert the mock, assert `is not None`, or were written against the implementation instead of the spec. Delete the mock and see what breaks; a test that survives deleting the tested logic is a decoration.
5. **Checklist security.** The code *names* security (sanitizes! validates!) while missing the actual hole - SQL interpolation one layer down, an unvalidated redirect, a JWT checked for existence but not signature. Audit claims, not keywords.
6. **Spec drift.** It implements a plausible requirement, not your requirement. Diff behavior against the written spec line by line; the most dangerous bug is a well-built wrong thing.
7. **Copy-paste family tree.** The same block in three places, subtly diverging. Canonicalize one.

## Process

- Audit in a separate pass from feature review. Mixing them means the feature conversation eats the audit.
- For anything touching auth, payments, or data deletion, re-read the diff as if the author were adversarial. Assume the fluent part hides the bug.
- Keep a log of which tells you keep catching in your codebase ([continuous-learning-v2](../continuous-learning-v2/SKILL.md)); models drift, and so do their failure modes.

## What this is not

This is not a reason to reject AI-assisted code. It is the review posture that lets you merge it with a straight face.
