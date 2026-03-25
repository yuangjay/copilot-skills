---
name: deep-learn-research
description: >
  Deep learning guide for academic papers, research publications, and model architectures.
  Triggers on: read paper, understand arxiv, study transformer, attention mechanism,
  BERT, GPT, research paper, academic publication, model architecture, explain the paper.
argument-hint: 'The paper or research topic (e.g., "Attention Is All You Need", "MapReduce paper", "RAFT consensus")'
---

# Deep Learn — Research Papers

## Goal
Move from "I skimmed the abstract" to "I can explain every design decision and implement the key idea."

---

## Phase 0 — Context First

Before reading a word of the paper:
1. Google the problem it solves — read a high-level blog post (5 min).
2. Find out: what was the state of the art BEFORE this paper?
3. Note your prediction: "I think this paper will argue that..."

**Papers are easier to understand when you already feel the pain of the problem.**

---

## Phase 1 — Three-Pass Reading

**Pass 1: Structure scan (10 min)**
Read only:
- Title, abstract
- Section headings
- First sentence of each section
- Conclusion

Answer: What is the claim? What experiment proves it?

**Pass 2: Concept read (60 min)**
Read fully, but skip:
- Math proofs
- Complex derivations (mark them for Pass 3)

For every figure: cover the caption and describe what you see first, then check.

Answer: How does the proposed method actually work?

**Pass 3: Deep dive (2–4 hours)**
- Work through the math line by line
- Verify the key equations with a small example
- Read the related work section to understand the landscape

---

## Phase 2 — Implement the Key Idea

For every paper, implement a minimal version of the core contribution:

| Paper | What to implement |
|-------|-------------------|
| Attention Is All You Need | Scaled dot-product attention from scratch |
| MapReduce | A toy word-count MapReduce in Python |
| RAFT / Paxos | Leader election simulation |
| Dropout | Manual dropout layer without a framework |
| Skip-gram (Word2Vec) | Train embeddings on a small corpus |

**Rules:**
- Do not use the framework's built-in version while implementing — understand it first
- Test with a small, inspectable example where you know the expected output

✅ Gate: Implementation runs and produces results matching the paper's description.

---

## Phase 3 — Critical Review

Answer these questions honestly:
1. What assumption does this paper make that might not hold in practice?
2. What does the ablation study show is most important?
3. What future work do the authors suggest — and has it been done?
4. What would you do differently?

Read 2 papers that **cite this paper** — did they confirm or challenge its findings?

✅ Gate: You can identify at least 2 limitations and explain why they matter.

---

## Phase 4 — Feynman Test

Write a blog post draft (or explain out loud) that covers:
1. The problem (1 paragraph)
2. The key insight (1 paragraph)
3. How it works, with a diagram (main section)
4. Why it matters / what it unlocked (1 paragraph)

**You understand it when you can write clearly about it.**

---

## Active Recall Prompts

- What is the central claim of this paper in one sentence?
- Draw the architecture from memory.
- What is the single most important equation, and what does each term mean?
- What would the authors say if you suggested [common alternative]?

---

## Examples

> `teach me the Attention Is All You Need paper deeply`
> `I want to understand the MapReduce paper, guide me step by step`
> `explain BERT architecture and help me implement the key parts`
