---
name: deep-learn
description: >
  Deep learning guide — teach me how to learn any topic deeply, step by step, using
  the Feynman method and project-based practice. Auto-routes to the correct domain skill.
  Triggers on: learn, study, understand deeply, teach me, how does X work, master X,
  get good at X, explain X to me.
argument-hint: 'Describe what you want to learn (e.g., "learn Kubernetes", "understand TCP/IP", "study transformer architecture")'
---

# Deep Learn — Master Routing Skill

## Purpose

Guide the user to **deeply understand** any topic using:
- **Project-based learning** (learn by building)
- **Feynman technique** (you truly understand something only when you can explain it simply)
- **Iterative depth** (start shallow, go deeper with each cycle)

---

## MANDATORY: Topic Detection Gate

Before starting, classify the topic into one of these domains:

```
User input contains...
  ├── code, algorithm, design pattern, API, library, language syntax
  │     └── DOMAIN: Programming / Software Engineering
  │           → Follow: deep-learn-programming skill
  │
  ├── OS, networking, database internals, compiler, data structures, algorithms
  │     └── DOMAIN: CS Fundamentals
  │           → Follow: deep-learn-cs skill
  │
  ├── a specific tool, framework, or platform (Docker, React, Kubernetes, etc.)
  │     └── DOMAIN: Technology / Framework
  │           → Follow: deep-learn-tech skill
  │
  ├── paper, arxiv, research, academic, study, model architecture
  │     └── DOMAIN: Research Papers
  │           → Follow: deep-learn-research skill
  │
  └── anything else (history, science, concepts, soft skills)
        └── DOMAIN: General Topic
              → Follow: deep-learn-general skill
```

**State which domain you detected before starting, so the user can correct you.**

---

## Universal Learning Principles (apply to ALL domains)

### 1. The Feynman Technique (non-negotiable)
At the end of every learning session, ask the user:
> "Explain [topic] to me as if I'm a complete beginner."

If they struggle to explain any part → that's the gap. Go back and study that part again.

### 2. Project-First Orientation
Every topic gets a **project** that forces real application:
- Choose a project before studying, not after
- Every concept learned should immediately appear in the project
- Project complexity scales with understanding depth

### 3. Depth Levels
Progress through 4 levels — never skip:

| Level | Goal | Signal you're ready to go deeper |
|-------|------|----------------------------------|
| L1: Surface | Define it. Name its parts. | Can explain what it is in 1 sentence |
| L2: Mechanism | Explain HOW it works | Can draw a diagram of the flow |
| L3: Application | Use it to build something | Working code / project exists |
| L4: Mastery | Break it, extend it, compare it | Can explain tradeoffs and edge cases |

### 4. Active Recall (not passive reading)
After every section, close the material and answer:
- What did I just learn?
- Why does it work this way?
- Where would this fail?

### 5. Spaced Repetition
Schedule revisits: after 1 day → 3 days → 1 week → 1 month.
The skill will remind you to revisit with a question prompt.

---

## Session Structure

Each learning session follows this format:

```
1. State your current level (L1–L4)
2. Set a session goal: "By the end I can ___"
3. Learn / build
4. Active recall check (3 questions minimum)
5. Feynman test: explain it back simply
6. Identify the gap (what still feels unclear)
7. Set next session goal
```

---

## Examples

**Learn a programming concept:**
> `learn how closures work in Python deeply`

**Master a framework:**
> `learn Kubernetes from scratch, guide me step by step`

**Understand CS fundamentals:**
> `I want to understand how TCP/IP really works under the hood`

**Study a research paper:**
> `teach me the Attention Is All You Need transformer paper`

**General deep learning:**
> `I want to deeply understand how Docker networking works`
