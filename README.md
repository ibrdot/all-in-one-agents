# All-in-One Agents

![validate](https://github.com/ibrdot/all-in-one-agents/actions/workflows/validate.yml/badge.svg)

The strongest all-in-one AI agent skill pack — **72 skills, 71 agents, 97 commands** unified into a single repository.

📖 **[INDEX.md](INDEX.md)** — full categorized catalog · 🛠 **[docs/INSTALL.md](docs/INSTALL.md)** — install guide for every harness

## Structure

```
all-in-one-agents/
├── skills/     72 full-featured skills (each with SKILL.md + scripts + references + assets)
├── agents/     71 specialized agent definitions
└── commands/   97 slash commands
```

## Usage

### As a skill library
Point your agent harness at the `skills/` directory. Every skill is self-contained:

```
skills/<skill-name>/
├── SKILL.md        # instructions the agent reads
├── scripts/        # executable helpers (python, shell, node)
└── references/     # deep-dive docs loaded on demand
```

### Quick start
1. Clone this repo
2. Copy or symlink any skill from `skills/` into your agent's skills directory
3. The agent auto-discovers it via `SKILL.md`

### Categories included
- Engineering: debugging, testing, code review, architecture, CI/CD
- Documents: PDF, DOCX, XLSX, PPTX creation & editing
- Design: canvas, themes, brand, frontend, art
- Data: benchmarking, analytics, logistics, finance
- Security: hardening, scanning, OSINT
- Automation: workflows, integrations, devops

## Stats

| Collection | Count |
|------------|-------|
| Skills     | 72    |
| Agents     | 71    |
| Commands   | 97    |
| Files      | 1200+ |
