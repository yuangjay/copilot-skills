---
name: tokenskill
description: "Token-saving RAG skill. Use when the user wants to reduce LLM token usage, query the local knowledge base, add documents to the vector store, check token savings stats, or use RAG-augmented chat. Triggers on: save tokens, token usage, RAG query, knowledge base, add document, token stats, rag chat, semantic search, vector search, check savings."
argument-hint: "Describe what you want to do: query knowledge base, add a document, RAG chat with a question, or check token savings stats."
---

# TokenSkill — RAG-Powered Token Saver

## What This Skill Does

This skill connects to the local **TokenSkill** service running via Docker Compose at `/ephemeral/workspace/study/tokenskill`. It reduces LLM token consumption by:

1. **RAG queries** — retrieves only the most relevant document chunks from ChromaDB instead of passing full context to the LLM
2. **Result caching** — Redis caches results for 1 hour; repeated queries cost zero tokens
3. **Context compression** — context sent to LLM is capped at 500 chars per query
4. **Cheap/local LLM routing** — can route to Ollama (local), Qwen, Kimi, Zhipu, MiniMax instead of expensive OpenAI

---

## Services

| Service     | URL                          | Purpose                     |
|-------------|------------------------------|-----------------------------|
| MCP Server  | http://localhost:18000       | MCP tool endpoint for Copilot |
| RAG API     | http://localhost:18001       | Core RAG + chat API         |
| Admin API   | http://localhost:18002       | Manage collections & docs   |
| ChromaDB    | http://localhost:18003       | Vector database             |

---

## When to Use

| User says...                                      | Action                          |
|---------------------------------------------------|---------------------------------|
| "query knowledge base about X"                    | `POST /api/v1/rag/query`        |
| "ask X using RAG" / "answer X from my knowledge" | `POST /api/v1/rag/chat`         |
| "add document / save this to knowledge base"      | `POST /api/v1/knowledge/add`    |
| "how many tokens did I save?" / "token stats"     | `GET /api/v1/stats/tokens`      |
| "list collections"                                | `GET /api/v1/knowledge/collections` |
| "is the service running?" / "health check"        | `GET /api/v1/health`            |

---

## Procedure

### Step 1 — Check Service Health
Before any operation, verify the service is up:
```bash
curl -s http://localhost:18001/api/v1/health
```
If the service is down, start it:
```bash
cd /ephemeral/workspace/study/tokenskill && docker compose up -d
```

### Step 2 — Execute the Operation

#### RAG Query (semantic search, no LLM call)
```bash
curl -s -X POST http://localhost:18001/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "<user question>", "top_k": 5, "collection": "default"}'
```
Returns the top matching document chunks and their similarity scores. **No LLM tokens used.**

#### RAG Chat (semantic search + LLM answer)
```bash
curl -s -X POST http://localhost:18001/api/v1/rag/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "<user question>", "collection": "default", "provider": "ollama"}'
```
- Prefer `provider: "ollama"` for local/free inference; fall back to `"openai"` if unavailable
- Response includes `tokens_saved` field showing how many tokens were saved vs. sending full context

#### Add Document to Knowledge Base
```bash
curl -s -X POST http://localhost:18001/api/v1/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{"content": "<document text>", "metadata": {"source": "<label>"}, "collection": "default"}'
```

#### Check Token Savings
```bash
curl -s "http://localhost:18001/api/v1/stats/tokens?period=today"
```
Available periods: `today`, `week`, `month`.

### Step 3 — Present Results
- For RAG query: show the retrieved chunks with their relevance scores
- For RAG chat: show the answer + `tokens_saved` value
- For stats: show total queries, tokens saved, estimated cost saved, cache hit rate

---

## MCP Integration

The MCP server at `http://localhost:18000` exposes these tools natively to Copilot:

| Tool name        | What it does                             |
|------------------|------------------------------------------|
| `rag_query`      | Semantic search in knowledge base        |
| `rag_chat`       | RAG-augmented LLM answer                 |
| `get_token_stats`| Token savings statistics                 |
| `health_check`   | Service health check                     |

These are called automatically when the MCP server is registered in `.vscode/settings.json`:
```json
"mcp": {
  "servers": {
    "tokenskill": {
      "url": "http://localhost:18000"
    }
  }
}
```

---

## Token Saving Tips

- **Always prefer `rag_query` over sending full documents** — retrieves only top-5 chunks
- **Use `collection` to namespace topics** — keeps retrieval precise
- **Cache is automatic** — same query within 1 hour = 0 tokens
- **Use `provider: "ollama"`** for questions that don't require GPT-4 quality
- **Build the knowledge base incrementally** — add docs once, query many times
