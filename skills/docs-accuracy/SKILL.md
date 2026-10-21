---
name: docs-accuracy
description: Use when writing or updating documentation, after behavior changes, when docs and code disagree, or before publishing a README that promises commands or features.
---

# Keep documentation matching the code

## Workflow

1. Inventory what the documentation promises: commands, flags, defaults, counts, examples, and links. These are checkable claims, not vibes.
2. Run every documented command. Copy-paste examples into a fresh environment or container. A command that was never run is a bug in the docs.
3. Cross-check counts, versions, and paths against the repository at the current commit. Generated numbers come from the generator, never from hand editing.
4. Test internal links and anchors, including relative links from each file's own directory.
5. Rewrite vague claims into specific, verifiable ones. Replace "blazing fast" with the measured number or delete the claim.
6. Match the audience: READMEs for first contact, reference docs for daily use, guides for the workflow. Do not make the README everything at once.
7. Record which claims were verified and how. Claims that could not be verified get removed or marked as unverified, never quietly kept.

## Rule

Documentation that fails when followed is worse than no documentation. Ship docs like code: reviewed, tested, and versioned with the change they describe.
