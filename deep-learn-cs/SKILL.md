---
name: deep-learn-cs
description: >
  Deep learning guide for computer science fundamentals: algorithms, data structures,
  operating systems, networking, compilers, databases, distributed systems.
  Triggers on: how does X work internally, TCP/IP, memory management, CPU scheduling,
  B-tree, hash table, consensus algorithm, CAP theorem.
argument-hint: 'The CS fundamental to learn (e.g., "TCP/IP networking", "B-tree internals", "OS scheduling")'
---

# Deep Learn — CS Fundamentals

## Goal
Build correct **mental models** — understand the WHY behind every design decision.

---

## Phase 0 — Anchor Implementation

For every CS fundamental, you will **implement a simplified version from scratch**.
This is non-negotiable.

| Topic | Anchor implementation |
|-------|-----------------------|
| Hash table | Build one in Python: handle collisions with chaining |
| TCP/IP | Build a simple TCP-like protocol over UDP |
| B-tree | Implement insert + search from scratch |
| OS scheduling | Simulate round-robin and priority scheduling |
| Consensus | Implement a simplified Raft leader election |
| Compiler basics | Build a calculator with tokeniser + parser |

---

## Phase 1 — Historical Context (10 min)

Before studying HOW it works, study WHY it was invented:
1. What problem existed before this?
2. What was the previous solution, and why was it inadequate?
3. What constraints shaped the design? (hardware limits, network conditions, etc.)

**Understanding constraints is 80% of understanding the design.**

---

## Phase 2 — Mental Model Construction

1. Draw a diagram **before** reading. Sketch your guess of how it works.
2. Read the actual mechanism. Compare with your diagram.
3. Redraw the corrected version from memory.

Key questions to answer:
- What are the components and their responsibilities?
- How do they communicate / coordinate?
- What invariants must always hold?
- What happens when something fails?

✅ Gate: Can you redraw the architecture from memory?

---

## Phase 3 — Implement the Simplified Version

1. Build the anchor implementation from Phase 0.
2. Start with the happy path — get it working for basic cases.
3. Add failure modes one by one:
   - What happens under load?
   - What happens on network partition / disk failure / race condition?
4. Compare your implementation decisions with the real one.

✅ Gate: Working implementation exists, failure modes are understood.

---

## Phase 4 — Tradeoffs & Alternatives

1. Study 2 alternative approaches to the same problem.
2. Fill in this table:

| Approach | Strength | Weakness | When to use |
|----------|----------|----------|-------------|
| This    | ...      | ...      | ...         |
| Alt 1   | ...      | ...      | ...         |
| Alt 2   | ...      | ...      | ...         |

3. Find a real-world system (Linux kernel, PostgreSQL, nginx) that uses this concept.
4. Read the relevant section of its source code or docs.

✅ Gate: Feynman test — explain to a non-CS friend in plain English.

---

## Active Recall Prompts

- Draw the architecture from memory right now.
- What are the 3 hardest problems this design has to solve?
- What would break first under high load?
- Why didn't they just use [simpler solution]?

---

## Examples

> `teach me how TCP/IP really works under the hood`
> `I want to deeply understand how a hash table works, help me implement one`
> `explain B-trees deeply and why databases use them over other structures`
