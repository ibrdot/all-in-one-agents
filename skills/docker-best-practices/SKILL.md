---
name: docker-best-practices
description: "Use when writing or fixing Dockerfiles - small, fast-building, secure images with sane layer caching, and the runtime settings that matter in production."
---

# Docker Best Practices

A Dockerfile is a build contract. Make images small, builds cache-friendly, and runtimes boring.

## Layer caching (the 10x build win)

- Copy lockfiles and install dependencies BEFORE copying source: `COPY package*.json ./` then `npm ci`, then `COPY . .`. Code changes rebuild one fast layer; lockfile changes rebuild the install.
- One concern per layer; order layers from least to most frequently changing.

## Image hygiene

- Use slim/distroless base images; pin digests, not `:latest`.
- Multi-stage builds: compiler and dev dependencies stay in the builder stage; the final image has runtime only. Node app images under 200MB are normal, not heroic.
- `.dockerignore` as seriously as `.gitignore` - `.git`, `node_modules`, and test fixtures in the context slow every build and leak secrets.
- Run as a non-root user; drop Linux capabilities in prod (`--cap-drop=ALL`).

## Runtime settings that matter

- Healthcheck that checks the real dependency path, not "port is open."
- Resource limits (memory/CPU) set in compose/k8s - an unbounded container takes its neighbors down OOM-killing first.
- One process per container; logs to stdout/stderr, PID 1 handled (exec form or a tiny init).

## The review checklist

- [ ] Rebuild from clean checkout is fast and works
- [ ] No secrets baked into any layer (they survive `rm` in earlier layers!)
- [ ] Image runs read-only filesystem where possible
- [ ] Same image artifact promoted dev -> staging -> prod, config injected at runtime only
