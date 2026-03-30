---
name: agent-orchestrator
description: 'Layered Copilot skill orchestration. Use when the user asks how skills are routed, how to auto choose the right skill, how to compose multiple skills without wasting tokens, or how to scale the skill system. Triggers on: auto choose skill, layered skills, skill orchestration, query routing, scale skills, waste tokens.'
argument-hint: 'Describe the routing or orchestration problem, for example: "auto choose layered skills", "route implementation tasks", or "scale the skill registry".'
---

# Agent Orchestrator

## Purpose

Use this skill as the source of truth for layered skill selection.

## Routing Layers

1. Knowledge gate:
   - Run the RAG-first workflow first.
   - Pull in `tokenskill` only when the task is explicitly about RAG, semantic search, the knowledge base, or token savings.
2. Workflow overlays:
   - Apply `workflow-tdd` when the task is about building, fixing, or reproducing issues.
   - Apply `workflow-skill-delivery` when the task is about validating, syncing, publishing, committing, or pushing the skills repo.
3. Primary skill:
   - Choose exactly one primary skill using the highest trigger specificity.
   - Prefer exact phrase matches over broad keyword overlap.
   - Prefer meta skills for skill-system tasks and domain skills for user-facing tasks.
4. Execution:
   - Keep the stack shallow: knowledge gate, workflow overlays, then one primary skill.
   - If confidence is low, answer directly instead of forcing extra skills.

## Token Discipline

- Load at most one primary skill and at most two overlays.
- Do not read unrelated skills just because they look adjacent.
- Favor trigger precision over breadth so the routing cost stays bounded as the registry grows.

## Scalability Rules

- Every new skill must define explicit trigger phrases in frontmatter.
- Overlays should stay generic and reusable; primary skills should stay domain-specific.
- Route by layers, not by scanning every skill body in full.
- Keep validation automated so the registry, routing block, and tests evolve together.