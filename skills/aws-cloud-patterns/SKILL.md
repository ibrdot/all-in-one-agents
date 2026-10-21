---
name: aws-cloud-patterns
description: "Use when designing or reviewing AWS architecture - service selection, IAM and VPC defaults that scale, cost-aware patterns, and the failure modes that page people at 3am."
---

# AWS Cloud Patterns

AWS gives you a hundred ways to build each thing; only a few of them survive contact with scale, cost reviews, and audits.

## Service selection defaults

- Queue + worker (SQS + Lambda/containers) over synchronous chains: one slow dependency should not 500 your user request.
- RDS Postgres by default; DynamoDB only when access patterns are known up front and single-digit-millisecond latency is a requirement, not a wish.
- S3 for anything file-shaped, with lifecycle rules from day one - unmanaged buckets become unmanaged bills.
- ElastiCache for read-heavy hot paths, only after measuring, and only with an explicit invalidation story.

## IAM and VPC: the boring survival kit

- Roles per service, least privilege, no wildcard actions. Wildcards in prod IAM are audit findings waiting to happen.
- Secrets in Secrets Manager/SSM, rotated; never in env-committed files or AMIs.
- Private subnets for workloads, NAT gated and logged; VPC endpoints for S3/DynamoDB (cheaper and safer than NAT egress).

## Patterns that pay for themselves

- **Idempotent consumers:** SQS delivers at-least-once; dedupe on message ID or business key or you will double-charge someone.
- **Dead-letter queues with alarms:** a DLQ nobody alerts on is a slow data-loss incident.
- **Aurora/RDS Proxy** under Lambda to survive connection storms.
- **Infrastructure as code everything** (Terraform/CDK); console changes are drift and drift is downtime.

## Cost and failure reviews

Before ship: what does this cost at 10x traffic, what happens when each dependency is down, and what is the rollback? Unanswered questions are the roadmap for the 3am page.
