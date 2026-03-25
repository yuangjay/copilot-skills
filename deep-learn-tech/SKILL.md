---
name: deep-learn-tech
description: >
  Deep learning guide for a specific technology, tool, or framework.
  Triggers on: learn Kubernetes, master Docker, get good at React, understand Kafka,
  learn Terraform, study Redis, understand Prometheus, learn Ansible.
argument-hint: 'The technology to learn (e.g., "Kubernetes", "Redis", "React hooks")'
---

# Deep Learn — Technology / Framework

## Goal
Go from **zero to confidently using it in a real project** — understanding not just the
API but the mental model behind it.

---

## Phase 0 — "Why Does This Exist?" Question

Before anything else, answer:
1. What problem does this technology solve?
2. What were people using before? Why was that insufficient?
3. What is the central design philosophy? (e.g. Kubernetes: "desired state reconciliation")

**If you can't answer these, you will memorise commands without understanding them.**

---

## Phase 1 — Official Docs Orientation (30 min)

Read ONLY these sections first (skip tutorials):
- Getting Started / Overview
- Core Concepts / Architecture
- "How it works" page if it exists

Goal: build the mental model before touching the tool.

Create a concept map:
```
[Core concept 1] → [relates to] → [Core concept 2]
                                        ↓
                               [Core concept 3]
```

✅ Gate: Can you draw the architecture without the docs open?

---

## Phase 2 — Guided Hands-On (1–2 hours)

1. Follow the official quickstart — but **type every command manually** (no copy-paste).
2. After each step, stop and ask:
   - What did this command actually do?
   - What state changed?
   - What would break if I skipped this?
3. Break something deliberately — understand the error.

✅ Gate: Completed quickstart with full understanding of each step.

---

## Phase 3 — Real Project (2–8 hours, depends on complexity)

Build a project that requires at least 60% of the tool's core features:

| Technology | Suggested real project |
|------------|------------------------|
| Kubernetes | Deploy a multi-service app with config maps + ingress |
| Docker | Multi-container app with compose, health checks, volumes |
| React | Build a stateful app with hooks, context, and API calls |
| Kafka | Producer/consumer pipeline with multiple topics |
| Redis | Session store + pub/sub for a simple chat system |
| Terraform | Provision a multi-resource cloud environment |

Constraints:
- No tutorials — write everything yourself
- When stuck, read the docs (not Stack Overflow first)
- Take notes on every non-obvious decision

✅ Gate: Real project works end-to-end.

---

## Phase 4 — Go Deeper

1. **Read the source** — find one core file in the project's source code and read it.
2. **Debug mode** — run the tool with verbose/debug flags, understand every log line.
3. **Production considerations**:
   - How is this configured for production vs dev?
   - What are common production pitfalls?
   - What monitoring/alerting is needed?
4. **Compare** — what are the top 2 alternatives? When would you choose each?

✅ Gate: Feynman test — explain it to a colleague who's never used it.

---

## Active Recall Prompts

- What are the 5 most important concepts in this tool?
- Draw the architecture from memory.
- What would you tell a beginner to avoid?
- Explain the main config file line by line from memory.

---

## Examples

> `learn Kubernetes from scratch, guide me step by step`
> `I want to deeply understand how Docker networking works`
> `teach me Redis and help me build something real with it`
