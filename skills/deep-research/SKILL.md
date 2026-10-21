---
name: deep-research
description: "Multi-source technical research that ends in a decision, not a link dump: question decomposition, source triangulation, version-aware documentation digging, and a written synthesis with receipts. Use when choosing between technologies, investigating an unfamiliar domain, or answering a question where being wrong is expensive."
---

# Deep Research

Research without a decision-maker is procrastination with citations. Start from the decision the user must make.

## Method

1. **Decompose the question** into sub-questions that can each be answered by an observable fact. State explicitly what evidence would change the conclusion.
2. **Go primary.** Official docs, RFCs, changelogs, issue threads, benchmarks with published methodology. Aggregator posts are leads, not evidence; follow them to the source or do not cite them.
3. **Triangulate.** No conclusion from a single source. When sources disagree, resolve by version and date first ("that was true for v2; v3 changed it"), then by methodology. Record what each source actually claims - misquoting a source is worse than not having it.
4. **Version and time-stamp everything.** Most technical claims have a half-life. "As of X, version Y" is the minimum unit of honesty.
5. **Write the synthesis for the decision:** recommendation, confidence, what would change it, and the receipts as inline links.

## Depth ladder

Match effort to stakes. Announce which rung you are on.

1. **Quick fact:** one authoritative source
2. **Comparison:** two to four primary sources, tradeoff table
3. **Full research:** decomposition, primary sources for every sub-question, triangulation, written synthesis with a recommendation

## Synthesis format

- Answer in the first paragraph; evidence after.
- Tradeoffs as a table with the user's actual criteria as columns.
- Open questions separated from findings. Unknowns stated as unknowns, never smoothed over.

## Anti-patterns

- Ten links and no recommendation
- Citing a benchmark without reading how it was run
- Confidently reporting the SEO winner of a keyword as "the community consensus"
