# Copilot Skills System

This repository is the canonical source for the layered Copilot skill system.

## What is versioned here

- Skill definitions under each skill folder
- The canonical global instructions template at `templates/copilot-instructions.base.md`
- Benchmark cases at `benchmarks/routing.json`
- Validation, telemetry, and routing logic under `skilllib/` and `scripts/`

## What is generated locally

- The installed global instructions file at `/root/.copilot/copilot-instructions.md`
- Routing telemetry at `/root/.copilot/logs/skill-routing.jsonl`

## What stays local-only

- `/root/.copilot/copilot-instructions.local.md`

## Install or refresh

```bash
bash /root/.copilot/skills/scripts/install-skill-system.sh
```

## Validate the system

```bash
cd /root/.copilot/skills
/ephemeral/workspace/study/integration/tests/.venv/bin/python scripts/skill_repo.py ci
```

## Trace routing decisions

```bash
cd /root/.copilot/skills
/ephemeral/workspace/study/integration/tests/.venv/bin/python scripts/skill_repo.py classify "fix an issue in the skill system, update tests first, then commit and push the skills repo"
/ephemeral/workspace/study/integration/tests/.venv/bin/python scripts/skill_repo.py trace --limit 10
/ephemeral/workspace/study/integration/tests/.venv/bin/python scripts/skill_repo.py metrics
```

## Benchmark routing quality

```bash
cd /root/.copilot/skills
/ephemeral/workspace/study/integration/tests/.venv/bin/python scripts/skill_repo.py benchmark
```

## Publishing policy

- Generated artifacts can be auto-synced.
- Semantic changes to routing logic, skill triggers, or workflow rules should be reviewed by a human before publish.
- CI must pass before commit and push.