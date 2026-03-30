# GitHub Copilot — Global Instructions

## MANDATORY: RAG-First Universal Workflow (applies to EVERY message)

Before composing any answer, **always** run this silent 4-step loop:

```
STEP 1 — RAG QUERY
  Call: POST http://localhost:18001/api/v1/rag/query
        body: {"query": "<user question>", "top_k": 5, "collection": "default"}
  If service is unreachable → skip to STEP 3, note "(RAG offline)" at end of answer
  If similarity score of top result < 0.4 → treat as "no relevant knowledge found"

STEP 2 — DECIDE ANSWER SOURCE
  If RAG returned results (score ≥ 0.4):
    → Build answer FROM the RAG chunks (cite them)
    → Summarise: "📚 Answer from knowledge base"
  Else:
    → Answer from LLM knowledge directly
    → Summarise: "🧠 Answer from model (not in knowledge base)"

STEP 3 — ANSWER
  Compose and deliver the answer as normal.

STEP 4 — AUTO-SAVE (only if BOTH conditions are met)
  Condition A — Answer is verified:
    • The answer is factual and non-speculative (no "I think", "maybe", "not sure")
    • Confidence level is HIGH (you would stake the answer on docs/known facts)
  Condition B — Not already stored:
    • RAG query in STEP 1 returned score < 0.85 for this exact content
    (high similarity means it's already there — skip to avoid duplicates)
  If A AND B → silently call:
    POST http://localhost:18001/api/v1/knowledge/add
    body: {"content": "Q: <question>\nA: <answer>", "metadata": {"source": "copilot-auto", "date": "<today>"}, "collection": "default"}
  Append a tiny footnote to your response: "💾 Saved to knowledge base"
  If save fails → append: "⚠️ Auto-save failed (RAG API unavailable)"
```

### RAG Failover Policy

| Situation | Behaviour |
|---|---|
| `rag-api` (18001) is down | Skip RAG, answer from LLM, append "(RAG offline)" |
| `chromadb` (18003) is down | Same as above — RAG API will error, treat as offline |
| `redis` (16379) is down | RAG still works (just no cache), continue normally |
| `mcp-server` (18000) is down | Copilot MCP tools unavailable, fall back to direct curl calls above |
| All services down | Answer 100% from LLM, auto-save skipped, no footnote shown |

---

{{MANAGED_ROUTING_BLOCK}}

---

## Behaviour Defaults

- **Always take action** — infer intent and act rather than asking for clarification when context is clear
- **Always use Docker first** for any deployment (check `docker --version` first if unsure)
- **Always use `.venv`** for Python if Docker is not applicable
- **Never commit code unless all tests pass**
- **Always follow TDD** when building new systems: tests first, then implementation
- **Git commits must include verification steps** so any admin can trace and reproduce the state
- **Code output** must be free of OWASP Top 10 security issues

---

## Tone & Format

- Be concise — match depth to complexity of question
- Use tables, diagrams (ASCII/Mermaid), and code blocks liberally
- For multi-step tasks, use a todo list to show progress
- For complex implementations, explain the "why" not just the "what"