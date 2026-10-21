---
name: repo-polish
description: Audit a GitHub repo for professionalism — README quality, LICENSE, CI status, docs coverage, description and topics. Use when the user wants their repository to look maintained and trustworthy, before sharing a repo link, or when an outside review called the repo unmaintained.
---

# Repo Polish

First impressions on GitHub happen in 5 seconds. This audit makes a repo pass them.

## Checklist

### Identity
- [ ] Description filled (no placeholder, no third-party names)
- [ ] Topics set (5–10 relevant tags)
- [ ] LICENSE present

### README
- [ ] One-line pitch at the top
- [ ] Structure diagram or quick start within the first screen
- [ ] Badges that actually work (CI green)
- [ ] Links to docs/index — no dead links

### Maintenance signals
- [ ] CI workflow present and passing
- [ ] Recent commits with conventional messages
- [ ] No dead folders or empty files
- [ ] Docs folder for anything beyond the README

## Fix order
1. CI green first — a red badge is worse than no badge
2. README accuracy — counts and links must be true
3. Description/topics — this is what search engines read
4. Then cosmetic polish

## Verify
Open the repo in an incognito tab: can a stranger understand what it is in 5 seconds? If not, keep polishing.

## Done when

- The procedure's stated outcome is observable and checked
- The user can verify the result without trusting the agent's word
