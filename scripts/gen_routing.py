#!/usr/bin/env python3
"""Regenerate the routing table section of MASTER-PROMPT.md from skills/.

Keeps the hand-curated category mapping at the top of this file; regenerates
the table rows so new skills never go unrouted. Run after adding/removing skills.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT = os.path.join(ROOT, "MASTER-PROMPT.md")

# Hand-curated: skill -> (category, trigger phrase)
CATS = {
    "Core & Orchestration": [
        ("brainstorming", "Vague / brief-less request"),
        ("writing-plans", "Multi-step build"),
        ("executing-plans", "Plan exists, work to proceed"),
        ("subagent-driven-development", "Multi-task plan with subagents"),
        ("dispatching-parallel-agents", "Independent parallel tasks"),
        ("using-git-worktrees", "Approved design, code next"),
        ("test-driven-development", "Any behavior change"),
        ("systematic-debugging", "Bug, cause unknown"),
        ("verification-before-completion", "About to claim \"done\""),
        ("finishing-a-development-branch", "Ready to merge / PR / discard"),
        ("requesting-code-review", "Diff needs independent eyes"),
        ("delivery-gate", "\"Quick fix\" temptation"),
        ("using-all-in-one-agents", "Long session / compaction"),
        ("diagnosing-the-pack", "Framework itself misbehaves"),
        ("pack-kernel", "Deep phase-loop guidance"),
        ("the-oath", "Identity re-anchor needed"),
        ("ck", "Session state must survive"),
    ],
    "Engineering & DevOps": [
        ("multi-file-editing", "Coordinated edits without collateral damage"),
        ("ast-aware-refactoring", "Refactor symbols, not matching strings"),
        ("api-migration", "Migrate contracts without breaking consumers"),
        ("dependency-upgrades", "Upgrade dependencies with controlled risk"),
        ("codebase-context", "Build a precise working map before editing"),
        ("agent-evaluation", "Measure agent changes against reproducible tasks"),
        ("checkpoint-recovery", "Resume work from evidence, not stale memory"),
        ("receiving-code-review", "Evaluate reviewer feedback before changing code"),
        ("mcp-builder", "Build an MCP server"),
        ("github-ops", "GitHub ops (issues, PRs, CI)"),
        ("security-review", "Auth / secrets / API endpoints"),
        ("telemetry-analytics", "Tracking / analytics events"),
        ("angular-developer", "Angular project"),
        ("frontend-development", "Frontend UI/UX work"),
        ("frontend-design-direction", "Frontend direction unclear"),
        ("frontend-api-contracts", "Frontend-backend contract"),
        ("desktop-electron", "Electron desktop app"),
        ("local-stack-runtime", "Local dev stack / services"),
        ("openhands-e2e-testing", "E2E testing (desktop app)"),
        ("verify-openhands", "Feature verification passes"),
        ("webapp-testing", "Playwright webapp testing"),
        ("web-artifacts-builder", "HTML artifacts"),
        ("story-lifecycle", "Story / epic / sprint lifecycle"),
        ("claude-api", "LLM API question"),
        ("module-regression", "Regression fear in large repo"),
        ("repo-polish", "Repo looks unmaintained"),
        ("commit-craft", "Commit hygiene"),
        ("terminal-opener", "Terminal / session chores"),
    ],
    "Meta & Learning": [
        ("writing-skills", "Author a new skill"),
        ("skill-creator", "Scaffold a new skill"),
        ("skill-pack-manager", "Validate pack integrity"),
        ("skill-stocktake", "Inventory the pack"),
        ("rules-distill", "Extract cross-cutting rules"),
        ("skill-comply", "Skill compliance check"),
        ("continuous-learning", "Same mistake repeating"),
        ("continuous-learning-v2", "Process improvement"),
        ("council-multi-model", "Multi-model critique needed"),
        ("context-and-decisions", "Repeated domain terms"),
        ("agent-self-evaluation", "Agent grading itself"),
        ("test-collaboration", "Test strategy with humans"),
        ("taste", "Taste / quality bar question"),
    ],
    "Documents & Media": [
        ("docx", "Word document"),
        ("pdf", "PDF file"),
        ("xlsx", "Spreadsheet"),
        ("pptx", "PowerPoint deck"),
        ("frontend-slides", "Animation-rich HTML slides"),
        ("algorithmic-art", "Generative art"),
        ("canvas-design", "Visual design"),
        ("theme-factory", "Theme / style artifacts"),
        ("ios-icon-gen", "iOS app icons"),
        ("manim-video", "Manim explainer video"),
        ("remotion-video-creation", "Remotion React video"),
        ("video-editing", "Video editing pipeline"),
        ("videodb", "Video library / search"),
        ("taste-distillation", "Style pack from reference"),
        ("taste-application", "Apply a distilled style pack"),
        ("slack-gif-creator", "Slack-optimized GIF"),
        ("brand-discovery", "Brand identity discovery"),
        ("brand-voice", "Brand voice work"),
    ],
    "Comms & Governance": [
        ("internal-comms", "Internal announcement / memo"),
        ("docs-governance", "Docs governance / freshness"),
        ("pr-design-doc", "PR needs a design doc"),
    ],
}

def main():
    text = open(PROMPT, encoding="utf-8").read()
    m = re.search(r"(#\s*FULL SKILL ROUTING TABLE[^\n]*\n#\s*\u2550+\n)(.*?)(#\s*\u2550+\n#\s*ANTI-PATTERNS)", text, re.S)
    if not m:
        print("routing section markers not found — is this the v2 prompt?")
        sys.exit(1)

    out = []
    listed = set()
    for cat, rows in CATS.items():
        out.append(f"### {cat}\n")
        out.append("| You notice... | Load |")
        out.append("|---|---|")
        for skill, trigger in rows:
            out.append(f"| {trigger} | `{skill}` |")
            listed.add(skill)
        out.append("")

    real = {d for d in os.listdir(os.path.join(ROOT, "skills")) if os.path.isdir(os.path.join(ROOT, "skills", d))}
    missing = real - listed
    if missing:
        print("WARNING: skills not in curated map:", sorted(missing))

    new = text[:m.start(2)] + "\n" + "\n".join(out) + "\n" + text[m.start(3):]
    open(PROMPT, "w").write(new)
    print(f"routing table regenerated: {len(listed)} skills routed")

if __name__ == "__main__":
    main()
