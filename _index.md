# Skills Registry

Last updated: 2026-03-25

## Active Skills

| Skill name | Family | Trigger keywords | Path |
|---|---|---|---|
| `deep-learn` | deep-learn | learn, study, teach me, understand, master | `deep-learn/SKILL.md` |
| `deep-learn-programming` | deep-learn | code, pattern, language feature, algorithm in code | `deep-learn-programming/SKILL.md` |
| `deep-learn-cs` | deep-learn | TCP/IP, OS, data structure, algorithm, compiler | `deep-learn-cs/SKILL.md` |
| `deep-learn-tech` | deep-learn | Kubernetes, Docker, React, Redis, Kafka, named tool | `deep-learn-tech/SKILL.md` |
| `deep-learn-research` | deep-learn | paper, arxiv, model architecture, research | `deep-learn-research/SKILL.md` |
| `deep-learn-general` | deep-learn | general topic, science, history, concept | `deep-learn-general/SKILL.md` |
| `system-redevelopment` | dev | build system, develop, create app, iterative | `system-redevelopment/SKILL.md` |
| `software-install` | dev | install, setup, configure, add package | `software-install/SKILL.md` |
| `file` | tools | create file, move file, list, organise | `file/SKILL.md` |
| `agent-customization` | meta | create skill, update skill, SKILL.md, instructions | (built-in) |

## Skill Families

```
skills/
  ├── deep-learn*     → Learning & knowledge acquisition
  ├── system-*        → System development lifecycle
  ├── software-*      → Dev environment & tooling
  ├── file            → Filesystem operations
  └── agent-*         → Copilot self-management
```

## Naming Conventions

- `<family>` — master router for a family
- `<family>-<domain>` — domain-specific sub-skill
- No spaces, lowercase, hyphenated
- Description must include explicit trigger keywords (used for auto-routing)

## How to Add a New Skill

```bash
mkdir /root/.copilot/skills/<skill-name>
# Create SKILL.md with YAML frontmatter: name, description (with triggers), argument-hint
# Add entry to this _index.md
# Add routing rule to /root/.copilot/copilot-instructions.md
git add . && git commit -m "skill: add <skill-name>"
```

## Deprecation

When retiring a skill:
1. Move to `_deprecated/` folder (don't delete — preserve history)
2. Remove from this index
3. Remove routing rule from `copilot-instructions.md`
4. Git commit with reason: `skill: deprecate <name> — merged into <other>`

