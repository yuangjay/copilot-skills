# Skills Registry

Last updated: 2026-03-30

## Active Skills

| Skill name | Family | Trigger keywords | Path |
|---|---|---|---|
| `deep-learn` | deep-learn | learn, study, understand deeply, teach me, how does x work, master x, get good at x, explain x to me | `deep-learn/SKILL.md` |
| `deep-learn-cs` | deep-learn | how does x work internally, tcp/ip, memory management, cpu scheduling, b-tree, hash table, consensus algorithm, cap theorem | `deep-learn-cs/SKILL.md` |
| `deep-learn-general` | deep-learn | understand x, explain x to me, learn about x, study x deeply, how does x really work (non-coding topics) | `deep-learn-general/SKILL.md` |
| `deep-learn-programming` | deep-learn | learn to code, understand x pattern, how does x work in python/js/go, design patterns, algorithms in code, oop, functional programming, concurrency, async | `deep-learn-programming/SKILL.md` |
| `deep-learn-research` | deep-learn | read paper, understand arxiv, study transformer, attention mechanism, bert, gpt, research paper, academic publication, model architecture, explain the paper | `deep-learn-research/SKILL.md` |
| `deep-learn-tech` | deep-learn | learn kubernetes, master docker, get good at react, understand kafka, learn terraform, study redis, understand prometheus, learn ansible | `deep-learn-tech/SKILL.md` |
| `software-install` | dev | install, setup, configure dependencies, add package, get x working, install and test, make sure x runs, check if x is installed | `software-install/SKILL.md` |
| `system-redevelopment` | dev | iterative development, system refinement, re-development, continuous improvement, openclaw-like workflows | `system-redevelopment/SKILL.md` |
| `agent-customization` | meta | create skill, update skill, fix skill, skill.md, instructions, skills repo, skill system | `(built-in)` |
| `agent-orchestrator` | meta | auto choose skill, layered skills, skill orchestration, query routing, scale skills, waste tokens | `agent-orchestrator/SKILL.md` |
| `file` | tools | create file, write file, update file, delete file, rename file, move file, copy file, find file, list files, organize directory, file structure, read file contents, overwrite file, append to file, batch file operations | `file/SKILL.md` |
| `tokenskill` | tools | save tokens, token usage, rag query, knowledge base, add document, token stats, rag chat, semantic search, vector search, check savings | `tokenskill/SKILL.md` |
| `workflow-skill-delivery` | workflow | validate skill repo, sync instructions, publish skills, commit skills, push skill repo, verify all tests, ci/cd | `workflow-skill-delivery/SKILL.md` |
| `workflow-tdd` | workflow | implement, build feature, issue, bug fix, regression, failing test, test first, tdd | `workflow-tdd/SKILL.md` |

## Skill Families

```
skills/
  ├── deep-learn*     → Learning & knowledge acquisition
  ├── workflow-*      → TDD, validation, publishing, CI gates
  ├── system-*        → System development lifecycle
  ├── software-*      → Dev environment & tooling
  ├── file            → Filesystem operations
  ├── token*          → Token, RAG, and knowledge retrieval
  └── agent-*         → Copilot self-management
```

## Naming Conventions

- `<family>` — master router for a family
- `<family>-<domain>` — domain-specific or workflow-specific sub-skill
- No spaces, lowercase, hyphenated
- Description must include explicit trigger keywords (used for auto-routing)

## How to Add a New Skill

```bash
mkdir /root/.copilot/skills/<skill-name>
# Create SKILL.md with YAML frontmatter: name, description (with triggers), argument-hint
# Run: python scripts/skill_repo.py build-index
# Run: python scripts/skill_repo.py sync
git add . && git commit -m "skill: add <skill-name>"
```

## Deprecation

When retiring a skill:
1. Move to `_deprecated/` folder (don't delete — preserve history)
2. Remove from this index
3. Remove routing rule from `copilot-instructions.md` managed block
4. Git commit with reason: `skill: deprecate <name> — merged into <other>`
