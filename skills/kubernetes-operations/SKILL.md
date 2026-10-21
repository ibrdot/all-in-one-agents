---
name: kubernetes-operations
description: "Use when deploying or debugging workloads on Kubernetes - manifests that survive production, probes and resources done right, and a diagnosis order for pods that will not behave."
---

# Kubernetes Operations

Kubernetes amplifies whatever you give it: good manifests run themselves; sloppy ones fail in creative distributed ways. Write manifests as if the person paged at 3am is future you.

## Manifests that survive production

- Requests AND limits set on every container (CPU limits optional, memory limits mandatory) - unbounded pods steal neighbors' memory and get OOM-killed.
- Liveness probes for deadlock, readiness for dependency状态 - never point liveness at a dependency; when the DB blinks, liveness restarts the whole fleet and turns an incident into an outage.
- PodDisruptionBudgets and topology spread so node maintenance is not downtime.
- One deployment per deliverable, config via ConfigMap/Secret, anything env-specific injected - never baked.

## Diagnosis order (when pods misbehave)

1. `kubectl get events --sort-by=.lastTimestamp` - the cluster is telling you why (OOMKilled, ImagePullBackOff, FailedScheduling...).
2. `kubectl describe pod` - read the events section, not just the spec.
3. `kubectl logs --previous` - the crashed container's last words are the diagnosis half the time.
4. `kubectl exec` in and reproduce the actual request path.
Guessing before step 4 is how 20-minute incidents become 2-hour ones.

## Operational rules

- Rollouts: `maxSurge`/`maxUnavailable` tuned so a bad image cannot take the whole service down; `kubectl rollout undo` is the rollback, know it before you need it.
- HPA on real metrics (custom, if CPU does not reflect load); do not scale on a signal that lags the pain.
- NetworkPolicies default-deny between namespaces; least-privilege service accounts; audit RBAC quarterly.
- If a manifest needed a human to fix by hand after deploy, that fix belongs in the manifest the same day.
