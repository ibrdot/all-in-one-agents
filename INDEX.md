# Index
## Skills (70)

### Core & Orchestration (26)
- **[brainstorming](skills/brainstorming/SKILL.md)** — Structured understanding before building — clarify intent, explore approaches, agree on a design. Use for any 
- **[commit-craft](skills/commit-craft/SKILL.md)** — Write clean conventional commits and review git history quality. Use when the user asks to commit changes, spl
- **[context-and-decisions](skills/context-and-decisions/SKILL.md)** — Govern stable domain context with a narrowly scoped CONTEXT.md when needed, and route hard-to-reverse decision
- **[delivery-gate](skills/delivery-gate/SKILL.md)** — Stop hook that blocks Claude from finishing until quality checks pass. Detects rationalization patterns (surfa
- **[desktop-electron](skills/desktop-electron/SKILL.md)** — This skill should be used when the user asks to "change the desktop app", "package Electron", "build a univers
- **[diagnosing-the-pack](skills/diagnosing-the-pack/SKILL.md)** — Debug the agent framework itself — when skills fail to trigger, hooks misfire, sessions go off the rails, or t
- **[dispatching-parallel-agents](skills/dispatching-parallel-agents/SKILL.md)** — Run independent tasks concurrently in isolated subagents with a deterministic merge strategy. Use when a plan 
- **[executing-plans](skills/executing-plans/SKILL.md)** — Execute a written plan task-by-task with evidence at each step. Use when a plan file exists and work should pr
- **[finishing-a-development-branch](skills/finishing-a-development-branch/SKILL.md)** — Close out a feature branch properly — full verification, then merge / PR / keep / discard with worktree cleanu
- **[module-regression](skills/module-regression/SKILL.md)** — Govern cross-module regression in large repositories with a REGRESSION.md ledger that records each module's do
- **[pack-kernel](skills/pack-kernel/SKILL.md)** — The orchestration core of the all-in-one pack. Always-on methodology that routes every task through understand
- **[pptx](skills/pptx/SKILL.md)** — Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This include
- **[repo-polish](skills/repo-polish/SKILL.md)** — Audit a GitHub repo for professionalism — README quality, LICENSE, CI status, docs coverage, description and t
- **[requesting-code-review](skills/requesting-code-review/SKILL.md)** — Use when completing tasks, implementing major features, or before merging to verify work meets requirements
- **[skill-pack-manager](skills/skill-pack-manager/SKILL.md)** — Manage a local skill pack — validate all skills, regenerate the index, find duplicates and stale skills. Use w
- **[skill-stocktake](skills/skill-stocktake/SKILL.md)** — Use when auditing Claude skills and commands for quality. Supports Quick Scan (changed skills only) and Full S
- **[subagent-driven-development](skills/subagent-driven-development/SKILL.md)** — Drive implementation by dispatching a fresh subagent per plan task, with review between tasks. Use for multi-t
- **[taste-application](skills/taste-application/SKILL.md)** — Generate new video against a distilled style pack and cut it into a finished piece - plan takes from the refer
- **[taste-distillation](skills/taste-distillation/SKILL.md)** — Measure a set of reference videos into a reusable style pack - colour grade as a 3D LUT, cut rhythm as a shot-
- **[terminal-opener](skills/terminal-opener/SKILL.md)** — Open an executable and its argument array in a visible terminal window through a reusable, shell-free launch p
- **[test-driven-development](skills/test-driven-development/SKILL.md)** — Use when implementing any feature or bugfix, before writing implementation code
- **[using-all-in-one-agents](skills/using-all-in-one-agents/SKILL.md)** — Bootstrap entrypoint of the all-in-one-agents framework — loaded automatically at session start and after comp
- **[using-git-worktrees](skills/using-git-worktrees/SKILL.md)** — Isolate feature work in a git worktree with a verified clean baseline. Use after design approval, before writi
- **[verification-before-completion](skills/verification-before-completion/SKILL.md)** — Hard gate before any task is claimed done — the agent must show real command output proving tests pass, build 
- **[writing-plans](skills/writing-plans/SKILL.md)** — Turn an approved design into an executable plan of atomic tasks. Use after brainstorming, before any implement
- **[writing-skills](skills/writing-skills/SKILL.md)** — Author new skills for this pack — structure, naming, trigger design, and quality bar. Use when creating a skil

### Documents & Media (22)
- **[algorithmic-art](skills/algorithmic-art/SKILL.md)** — Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this wh
- **[canvas-design](skills/canvas-design/SKILL.md)** — Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when
- **[ck](skills/ck/SKILL.md)** — Persistent per-project memory for Claude Code (Context Keeper) driven by deterministic Node.js /ck commands: i
- **[docs-governance](skills/docs-governance/SKILL.md)** — Route broad documentation-governance requests to existing ECC skills and run an opt-in, read-only audit of map
- **[docx](skills/docx/SKILL.md)** — Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Wo
- **[frontend-slides](skills/frontend-slides/SKILL.md)** — Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when th
- **[ios-icon-gen](skills/ios-icon-gen/SKILL.md)** — Generate iOS app icons as PNG imagesets for Xcode asset catalogs from SF Symbols (5000+ Apple-native) or Iconi
- **[local-stack-runtime](skills/local-stack-runtime/SKILL.md)** — This skill should be used when the user asks to "change the dev stack", "add a runtime service", "change the l
- **[manim-video](skills/manim-video/SKILL.md)** — Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs, the
- **[openhands-e2e-testing](skills/openhands-e2e-testing/SKILL.md)** — This skill should be used when the user asks to "add an E2E test", "run live E2E", "run mock-LLM tests", "debu
- **[pdf](skills/pdf/SKILL.md)** — Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text
- **[pr-design-doc](skills/pr-design-doc/SKILL.md)** — For a non-trivial pull request, write a self-contained HTML design doc under the temporary `.pr/` directory an
- **[remotion-video-creation](skills/remotion-video-creation/SKILL.md)** — Best practices for Remotion - Video creation in React. 29 domain-specific rules covering 3D, animations, audio
- **[slack-gif-creator](skills/slack-gif-creator/SKILL.md)** — Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools
- **[story-lifecycle](skills/story-lifecycle/SKILL.md)** — Manage a file-based epic → story → sprint development loop without requiring an external project management to
- **[taste](skills/taste/SKILL.md)** — Creative-direction layer for music videos and short-form edits in the angelcore / cloud-trance / hyperpop fami
- **[theme-factory](skills/theme-factory/SKILL.md)** — Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing page
- **[verify-openhands](skills/verify-openhands/SKILL.md)** — This skill should be used to "verify OpenHands features", "test the Canvas UI like a user", "drive Agent Canva
- **[video-editing](skills/video-editing/SKILL.md)** — AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pip
- **[videodb](skills/videodb/SKILL.md)** — Ingest, index, search, edit, and monitor video and audio with the VideoDB Python SDK — upload from files, URLs
- **[web-artifacts-builder](skills/web-artifacts-builder/SKILL.md)** — Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web tech
- **[xlsx](skills/xlsx/SKILL.md)** — Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user 

### Engineering & DevOps (18)
- **[agent-self-evaluation](skills/agent-self-evaluation/SKILL.md)** — Use after completing any non-trivial task. The agent self-rates its output on 5 axes — accuracy, completeness,
- **[angular-developer](skills/angular-developer/SKILL.md)** — Generates Angular code and provides architectural guidance. Trigger when creating projects, components, or ser
- **[brand-discovery](skills/brand-discovery/SKILL.md)** — Run a structured, resumable multi-session brand identity interview across 8 modules (purpose, positioning, aud
- **[brand-voice](skills/brand-voice/SKILL.md)** — Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then r
- **[claude-api](skills/claude-api/SKILL.md)** — Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, tool use, MCP, agents, c
- **[council-multi-model](skills/council-multi-model/SKILL.md)** — Add one optional external Codex critique after the existing council has produced a decision draft. Use when an
- **[frontend-api-contracts](skills/frontend-api-contracts/SKILL.md)** — This skill should be used when the user asks to "add an API call", "change a backend", "update settings persis
- **[frontend-design-direction](skills/frontend-design-direction/SKILL.md)** — Set an ECC-specific frontend design direction for production UI work. Use when building or improving websites,
- **[github-ops](skills/github-ops/SKILL.md)** — GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, relea
- **[internal-comms](skills/internal-comms/SKILL.md)** — A set of resources to help me write all kinds of internal communications, using the formats that my company li
- **[mcp-builder](skills/mcp-builder/SKILL.md)** — Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with externa
- **[rules-distill](skills/rules-distill/SKILL.md)** — Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new ru
- **[security-review](skills/security-review/SKILL.md)** — Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, 
- **[skill-creator](skills/skill-creator/SKILL.md)** — Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to c
- **[systematic-debugging](skills/systematic-debugging/SKILL.md)** — Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- **[telemetry-analytics](skills/telemetry-analytics/SKILL.md)** — This skill should be used when the user asks to "add tracking", "add a PostHog event", "change telemetry conse
- **[test-collaboration](skills/test-collaboration/SKILL.md)** — Inventory and govern a project's test assets. Connect requirements, business rules, risks, bugs, and cross-bou
- **[webapp-testing](skills/webapp-testing/SKILL.md)** — Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend 

### AI & Agents (4)
- **[continuous-learning](skills/continuous-learning/SKILL.md)** — [DEPRECATED - use continuous-learning-v2] Legacy v1 stop-hook skill extractor. v2 is a strict superset with in
- **[continuous-learning-v2](skills/continuous-learning-v2/SKILL.md)** — Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scor
- **[frontend-development](skills/frontend-development/SKILL.md)** — This skill should be used when the user asks to "add UI copy", "add a translation", "optimize the frontend bun
- **[skill-comply](skills/skill-comply/SKILL.md)** — Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 p

## Experimental (11) — opt-in, see examples/experimental/

`counterparty-channel-discipline`, `esign-field-placement`, `ito-baskets`, `ito-compute`, `lead-intelligence`, `master-agreement-generator`, `nasiko-control-plane`, `openclaw-persona-forge`, `operator-approval-loop`, `tinystruct-patterns`, `visa-doc-translate`

## Agents (73)

See [docs/AGENTS.md](docs/AGENTS.md) for full descriptions.

## Commands (97)

See [docs/COMMANDS.md](docs/COMMANDS.md) for full descriptions.
