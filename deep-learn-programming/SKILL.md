---
name: deep-learn-programming
description: >
  Deep learning guide for programming concepts, software engineering patterns, and code.
  Uses project-based learning and Feynman technique. Triggers on: learn to code, understand
  X pattern, how does X work in Python/JS/Go, design patterns, algorithms in code, OOP,
  functional programming, concurrency, async.
argument-hint: 'The programming concept to learn (e.g., "closures in Python", "async/await", "dependency injection")'
---

# Deep Learn — Programming & Software Engineering

## Goal
Reach **L4 mastery**: build it, break it, explain it, extend it.

---

## Phase 0 — Anchor Project

Before reading a single line of docs, pick a micro-project that **requires** the concept:

| Concept | Suggested anchor project |
|---------|--------------------------|
| Closures | Build a function factory (e.g. multiplier generator) |
| Async/await | Build a concurrent HTTP fetcher |
| Design patterns | Refactor a messy codebase using the pattern |
| Recursion | Build a tree/graph traversal from scratch |
| Decorators | Build a timing + retry decorator |

**Rule: The project must be chosen before studying. Learning happens through building.**

---

## Phase 1 — L1: Surface (15 min max)

1. Read the definition — one source only (official docs preferred).
2. Answer in your own words:
   - What problem does this concept solve?
   - What did people do BEFORE this existed?
3. Write a 1-sentence summary without looking.

✅ Gate: Can you define it without the source open?

---

## Phase 2 — L2: Mechanism (30–60 min)

1. Trace through how it works step by step:
   - For functions/algorithms: trace with a concrete example (pen and paper or whiteboard)
   - For patterns: draw the class/module diagram
   - For language features: look at the bytecode/AST if possible
2. Write down the rules:
   - When is this evaluated?
   - What happens in memory?
   - What are the edge cases?
3. Find one thing that surprises you — research why.

✅ Gate: Can you draw or write a step-by-step walkthrough from memory?

---

## Phase 3 — L3: Application (1–3 hours)

1. Build the anchor project from Phase 0 — **no copy-paste**.
2. Deliberately make it break:
   - What inputs cause unexpected behaviour?
   - What happens at the boundary conditions?
3. Read one real-world usage in an open-source project.
4. Refactor your project using what you learned.

✅ Gate: Does working code exist that you wrote from scratch?

---

## Phase 4 — L4: Mastery

1. **Compare**: How does this compare to alternatives? Why would you choose each?
2. **Extend**: Add one feature that wasn't in the original anchor project.
3. **Teach**: Write a 200-word explanation for a junior developer.
4. **Break on purpose**: Find a real bug or footgun caused by misuse of this concept.

✅ Gate: Feynman test — explain it out loud in plain English without notes.

---

## Active Recall Prompts (ask yourself after every phase)

- What is the core mechanism in one sentence?
- What problem does this solve that something simpler couldn't?
- Write the minimal working example from memory.
- Where would a beginner go wrong with this?

---

## Spaced Repetition Schedule

| Day | Prompt |
|-----|--------|
| +1  | Rebuild the anchor project from scratch without looking |
| +3  | Explain it to someone (or write a blog post outline) |
| +7  | Find a real bug in someone else's code caused by this |
| +30 | Review: what has changed in your understanding? |

---

## Examples

> `learn how Python closures work deeply, step by step`
> `I want to really understand async/await, teach me with a project`
> `explain the observer design pattern, then help me build something with it`
