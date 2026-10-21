---
name: ast-aware-refactoring
description: Use when renaming symbols, rewriting imports, changing call signatures, or performing syntax-aware codemods where plain multi-file search and replace could alter unrelated code.
---

# Refactor symbols, not matching strings

## Workflow

1. Identify the language, parser, type checker, formatter, generated-file boundaries, and current test commands from repository configuration.
2. Establish characterization tests for the behavior that must not change. Record exported APIs and side effects.
3. Use installed language-server rename or the repository's codemod framework. Verify tool availability and version before running; never invent an AST tool or install dependencies silently.
4. Prototype against representative fixtures: alias imports, shadowed names, overloads, JSX, decorators, comments, strings, and unsupported syntax. Unsupported constructs must fail closed, not be dropped.
5. Run a dry run over an explicit file list. Inspect the diff and parser errors before applying. Exclude vendored and generated code unless the generator itself changes.
6. Apply in dependency order: definitions, imports, consumers, tests, then documentation. Keep behavior changes in a separate patch from structural changes.
7. Parse every changed source file, format with repository settings, type-check, and run targeted and regression tests. Search both old and new symbol spellings; inspect intentional compatibility aliases.

## Decision record

Record the symbol scope, tool/version, include/exclude globs, dry-run command, compatibility strategy, and verification results. Use `multi-file-editing` only for non-semantic accompanying text changes.

## Completion gate

No unexpected exports, no accidental string/comment rewrites, no parser failures, and no unreviewed generated output. A smaller diff is preferable to a broad speculative cleanup.
