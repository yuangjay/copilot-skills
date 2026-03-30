from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import UTC
import json
from pathlib import Path
import re
from textwrap import dedent


REPO_ROOT = Path("/root/.copilot/skills")
GLOBAL_INSTRUCTIONS = Path("/root/.copilot/copilot-instructions.md")
GLOBAL_INSTRUCTIONS_TEMPLATE = REPO_ROOT / "templates" / "copilot-instructions.base.md"
LOCAL_OVERRIDE_PATH = Path("/root/.copilot/copilot-instructions.local.md")
LOCAL_OVERRIDE_TEMPLATE = REPO_ROOT / "templates" / "copilot-instructions.local.example.md"
ROUTING_BENCHMARKS_PATH = REPO_ROOT / "benchmarks" / "routing.json"
ROUTING_LOG_PATH = Path("/root/.copilot/logs/skill-routing.jsonl")
MANAGED_START = "<!-- BEGIN MANAGED: layered-skill-routing -->"
MANAGED_END = "<!-- END MANAGED: layered-skill-routing -->"
MANAGED_ROUTING_PLACEHOLDER = "{{MANAGED_ROUTING_BLOCK}}"


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    argument_hint: str
    path: str
    family: str
    triggers: tuple[str, ...]
    built_in: bool = False


@dataclass(frozen=True)
class RoutingDecision:
    primary_skill: str | None
    overlay_skills: tuple[str, ...]
    knowledge_skills: tuple[str, ...]
    primary_score: int = 0
    secondary_score: int = 0
    confidence: float = 0.0
    fallback_reason: str | None = None

    @property
    def selected_skills(self) -> tuple[str, ...]:
        ordered = list(self.knowledge_skills) + list(self.overlay_skills)
        if self.primary_skill:
            ordered.append(self.primary_skill)
        return tuple(ordered)


@dataclass(frozen=True)
class RoutingBenchmarkCase:
    name: str
    query: str
    primary_skill: str | None
    overlay_skills: tuple[str, ...]
    knowledge_skills: tuple[str, ...]
    fallback_reason: str | None = None


@dataclass(frozen=True)
class RoutingBenchmarkResult:
    cases: tuple[RoutingBenchmarkCase, ...]
    failures: tuple[dict[str, object], ...]


BUILTIN_SKILLS = (
    Skill(
        name="agent-customization",
        description=(
            "Workflow skill for creating, updating, fixing, or reviewing Copilot "
            "skills and instruction files. Triggers on: create skill, update skill, "
            "fix skill, SKILL.md, instructions, skills repo, skill system."
        ),
        argument_hint="Describe the skill or instruction change you want to make.",
        path="(built-in)",
        family="meta",
        triggers=(
            "create skill",
            "update skill",
            "fix skill",
            "skill.md",
            "instructions",
            "skills repo",
            "skill system",
        ),
        built_in=True,
    ),
)


PROCESS_OVERLAYS = ("workflow-tdd", "workflow-skill-delivery")


def _normalize_space(value: str) -> str:
    return " ".join(value.split())


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _extract_frontmatter(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md is missing YAML frontmatter")

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index]

    raise ValueError("SKILL.md has an unterminated YAML frontmatter block")


def _parse_frontmatter(path: Path) -> dict[str, str]:
    frontmatter = _extract_frontmatter(path.read_text())
    parsed: dict[str, str] = {}
    index = 0

    while index < len(frontmatter):
        line = frontmatter[index]
        if not line.strip():
            index += 1
            continue

        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line in {path}: {line}")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if raw_value in {">", "|"}:
            index += 1
            block: list[str] = []
            while index < len(frontmatter):
                candidate = frontmatter[index]
                if candidate.strip() and not candidate.startswith((" ", "\t")) and ":" in candidate:
                    break
                if candidate.startswith("  "):
                    block.append(candidate[2:])
                elif candidate.startswith("\t"):
                    block.append(candidate[1:])
                else:
                    block.append(candidate.strip())
                index += 1

            if raw_value == ">":
                parsed[key] = _normalize_space(" ".join(part for part in block if part.strip()))
            else:
                parsed[key] = "\n".join(block).strip()
            continue

        parsed[key] = _strip_quotes(raw_value)
        index += 1

    return parsed


def _extract_triggers(description: str) -> tuple[str, ...]:
    normalized = _normalize_space(description)
    match = re.search(r"Triggers on:\s*(.+?)(?:\.$|$)", normalized, flags=re.IGNORECASE)
    if not match:
        return ()

    triggers = []
    for item in match.group(1).split(","):
        trigger = item.strip().strip(".").lower()
        if trigger:
            triggers.append(trigger)
    return tuple(dict.fromkeys(triggers))


def _family_for_skill(name: str) -> str:
    if name.startswith("deep-learn"):
        return "deep-learn"
    if name.startswith("agent-"):
        return "meta"
    if name.startswith("workflow-"):
        return "workflow"
    if name in {"file", "tokenskill"}:
        return "tools"
    if name.startswith("software-") or name.startswith("system-"):
        return "dev"
    return name.split("-", 1)[0]


def discover_skills(repo_root: Path = REPO_ROOT) -> list[Skill]:
    skills: list[Skill] = []

    for skill_file in sorted(repo_root.glob("*/SKILL.md")):
        metadata = _parse_frontmatter(skill_file)
        name = metadata.get("name") or skill_file.parent.name
        description = metadata.get("description", "")
        argument_hint = metadata.get("argument-hint", "")
        triggers = _extract_triggers(description)

        skills.append(
            Skill(
                name=name,
                description=description,
                argument_hint=argument_hint,
                path=skill_file.relative_to(repo_root).as_posix(),
                family=_family_for_skill(name),
                triggers=triggers,
            )
        )

    skills.extend(BUILTIN_SKILLS)
    return skills


def _tokenize(text: str) -> set[str]:
    raw_tokens = re.findall(r"[a-z0-9]+", text.lower())
    tokens = set()
    for token in raw_tokens:
        if token.endswith("s") and len(token) > 3:
            tokens.add(token[:-1])
        else:
            tokens.add(token)
    return tokens


def _score_trigger(query: str, query_tokens: set[str], trigger: str) -> int:
    trigger = trigger.lower().strip()
    if not trigger:
        return 0

    if trigger in query:
        return 5 + trigger.count(" ")

    trigger_tokens = _tokenize(trigger)
    overlap = len(query_tokens & trigger_tokens)

    if overlap == len(trigger_tokens) and overlap > 0:
        return 4 + max(0, overlap - 1)
    if overlap >= 2:
        return 2
    if overlap == 1:
        return 1
    return 0


def _score_skill(query: str, skill: Skill) -> int:
    query = _normalize_space(query.lower())
    query_tokens = _tokenize(query)
    score = 0

    for trigger in skill.triggers:
        score = max(score, _score_trigger(query, query_tokens, trigger))

    for token in _tokenize(skill.name.replace("-", " ")):
        if token in query_tokens:
            score += 1

    return score


def _confidence_from_scores(best_score: int, second_score: int) -> float:
    if best_score <= 0:
        return 0.0

    score_signal = min(best_score / 8.0, 1.0)
    if second_score <= 0:
        margin_signal = 1.0
    else:
        margin_signal = min(max(best_score - second_score, 0) / best_score, 1.0)

    return round((0.65 * score_signal) + (0.35 * margin_signal), 3)


def _match_score_with_bias(skill: Skill, normalized_query: str) -> int:
    score = _score_skill(normalized_query, skill)
    query_tokens = _tokenize(normalized_query)

    if skill.name == "agent-customization" and ({"skill", "instruction", "repo"} & query_tokens):
        score += 2

    if skill.name == "agent-orchestrator" and (
        {"route", "routing", "layered", "orchestration", "orchestrator", "token", "auto", "choose"}
        & query_tokens
    ):
        score += 3

    if skill.name == "tokenskill" and (
        {"token", "rag", "knowledge", "semantic", "vector", "cache"} & query_tokens
    ):
        score += 2

    return score


def classify_query(query: str, repo_root: Path = REPO_ROOT) -> RoutingDecision:
    skills = {skill.name: skill for skill in discover_skills(repo_root)}
    normalized_query = _normalize_space(query.lower())
    query_tokens = _tokenize(normalized_query)

    knowledge_skills: list[str] = []
    if "tokenskill" in skills and _match_score_with_bias(skills["tokenskill"], normalized_query) >= 2:
        knowledge_skills.append("tokenskill")

    overlay_skills: list[str] = []
    for overlay_name in PROCESS_OVERLAYS:
        overlay = skills.get(overlay_name)
        if overlay and _match_score_with_bias(overlay, normalized_query) >= 3:
            overlay_skills.append(overlay_name)

    best_name: str | None = None
    best_score = 0
    second_score = 0
    ignored = set(knowledge_skills) | set(overlay_skills)

    for skill in skills.values():
        if skill.name in ignored:
            continue

        score = _match_score_with_bias(skill, normalized_query)

        if score > best_score:
            second_score = best_score
            best_name = skill.name
            best_score = score
        elif score > second_score:
            second_score = score

    confidence = _confidence_from_scores(best_score, second_score)
    fallback_reason: str | None = None

    if best_score < 3:
        best_name = None
        fallback_reason = "low_score"
    elif second_score >= best_score and best_score < 6:
        best_name = None
        fallback_reason = "ambiguous_match"
    elif confidence < 0.45:
        best_name = None
        fallback_reason = "low_confidence"

    if best_name is None and best_score >= 3 and fallback_reason is None:
        fallback_reason = "no_primary"

    return RoutingDecision(
        primary_skill=best_name,
        overlay_skills=tuple(overlay_skills[:2]),
        knowledge_skills=tuple(knowledge_skills[:1]),
        primary_score=best_score,
        secondary_score=second_score,
        confidence=confidence if best_name else 0.0,
        fallback_reason=fallback_reason,
    )


def generate_index(skills: list[Skill], today: date | None = None) -> str:
    today = today or date.today()
    ordered = sorted(skills, key=lambda skill: (skill.family, skill.name))

    lines = [
        "# Skills Registry",
        "",
        f"Last updated: {today.isoformat()}",
        "",
        "## Active Skills",
        "",
        "| Skill name | Family | Trigger keywords | Path |",
        "|---|---|---|---|",
    ]

    for skill in ordered:
        trigger_text = ", ".join(skill.triggers) if skill.triggers else "-"
        lines.append(
            f"| `{skill.name}` | {skill.family} | {trigger_text} | `{skill.path}` |"
        )

    lines.extend(
        [
            "",
            "## Skill Families",
            "",
            "```",
            "skills/",
            "  ├── deep-learn*     → Learning & knowledge acquisition",
            "  ├── workflow-*      → TDD, validation, publishing, CI gates",
            "  ├── system-*        → System development lifecycle",
            "  ├── software-*      → Dev environment & tooling",
            "  ├── file            → Filesystem operations",
            "  ├── token*          → Token, RAG, and knowledge retrieval",
            "  └── agent-*         → Copilot self-management",
            "```",
            "",
            "## Naming Conventions",
            "",
            "- `<family>` — master router for a family",
            "- `<family>-<domain>` — domain-specific or workflow-specific sub-skill",
            "- No spaces, lowercase, hyphenated",
            "- Description must include explicit trigger keywords (used for auto-routing)",
            "",
            "## How to Add a New Skill",
            "",
            "```bash",
            "mkdir /root/.copilot/skills/<skill-name>",
            "# Create SKILL.md with YAML frontmatter: name, description (with triggers), argument-hint",
            "# Run: python scripts/skill_repo.py build-index",
            "# Run: python scripts/skill_repo.py sync",
            "git add . && git commit -m \"skill: add <skill-name>\"",
            "```",
            "",
            "## Deprecation",
            "",
            "When retiring a skill:",
            "1. Move to `_deprecated/` folder (don't delete — preserve history)",
            "2. Remove from this index",
            "3. Remove routing rule from `copilot-instructions.md` managed block",
            "4. Git commit with reason: `skill: deprecate <name> — merged into <other>`",
        ]
    )
    return "\n".join(lines) + "\n"


def write_index(repo_root: Path = REPO_ROOT, today: date | None = None) -> Path:
    index_path = repo_root / "_index.md"
    index_path.write_text(generate_index(discover_skills(repo_root), today=today))
    return index_path


def build_managed_routing_block(repo_root: Path = REPO_ROOT) -> str:
    skills = {skill.name: skill for skill in discover_skills(repo_root)}
    known_primary = [
        name
        for name in (
            "deep-learn",
            "deep-learn-programming",
            "deep-learn-cs",
            "deep-learn-tech",
            "deep-learn-research",
            "deep-learn-general",
            "system-redevelopment",
            "software-install",
            "file",
            "agent-customization",
            "agent-orchestrator",
        )
        if name in skills
    ]

    primary_list = "\n".join(f"- `{name}`" for name in known_primary)

    return dedent(
        f"""
## MANDATORY: Multi-Layer Skill Orchestration (managed from /root/.copilot/skills)

Before responding to any user message, silently run this layered selector:

STEP 0 — Knowledge Gate
  - Run the RAG-first workflow already defined above.
  - Load `tokenskill` only when the query is about RAG, the knowledge base, semantic search, or token savings.

STEP 1 — Workflow Overlays
  - If the query implies implementation, bug fixing, issue reproduction, regression handling, or test-first delivery, apply `workflow-tdd`.
  - If the query implies validating, syncing, committing, publishing, or pushing the skills repo, also apply `workflow-skill-delivery`.

STEP 2 — Primary Skill Selection
  - Choose exactly one primary skill using the highest trigger specificity.
  - Prefer exact trigger phrase matches over loose keyword overlap.
  - Prefer meta skills for skill-system work and domain skills for end-user tasks.
  - If no skill has a confident match, answer directly instead of forcing a skill.

STEP 3 — Token Discipline
  - Load at most 1 primary skill and at most 2 overlays.
  - Do not load unrelated skills just because they are broadly adjacent.
  - Keep routing shallow: knowledge gate, workflow overlay(s), then one primary skill.

### Overlay Routing Table

| Query signal | Overlay skill |
|---|---|
| implement / build / change / issue / bug / fix / regression / failing test / tdd | `workflow-tdd` |
| validate / verify / sync / commit / push / publish / skills repo / ci/cd | `workflow-skill-delivery` |

### Primary Skill Candidates

{primary_list}
        """
    ).strip()


def render_global_instructions(
    repo_root: Path = REPO_ROOT,
    template_path: Path = GLOBAL_INSTRUCTIONS_TEMPLATE,
    override_path: Path = LOCAL_OVERRIDE_PATH,
) -> str:
    if not template_path.exists():
        raise ValueError(f"Global instructions template is missing: {template_path}")

    template = template_path.read_text()
    if MANAGED_ROUTING_PLACEHOLDER not in template:
        raise ValueError("Global instructions template is missing the managed routing placeholder")

    managed_block = build_managed_routing_block(repo_root)
    managed_section = f"{MANAGED_START}\n{managed_block}\n{MANAGED_END}"
    rendered = template.replace(MANAGED_ROUTING_PLACEHOLDER, managed_section)

    if override_path.exists():
        override = override_path.read_text().strip()
        if override:
            rendered = (
                rendered.rstrip()
                + "\n\n---\n\n## Local Overrides\n\n"
                + override
                + "\n"
            )

    return rendered.rstrip() + "\n"


def sync_global_instructions(
    repo_root: Path = REPO_ROOT,
    instructions_path: Path = GLOBAL_INSTRUCTIONS,
    template_path: Path = GLOBAL_INSTRUCTIONS_TEMPLATE,
    override_path: Path = LOCAL_OVERRIDE_PATH,
) -> bool:
    updated = render_global_instructions(
        repo_root,
        template_path=template_path,
        override_path=override_path,
    )
    existing = instructions_path.read_text() if instructions_path.exists() else None
    if existing == updated:
        return False

    instructions_path.write_text(updated)
    return True


def record_routing_event(
    query: str,
    decision: RoutingDecision,
    *,
    log_path: Path = ROUTING_LOG_PATH,
    source: str = "cli",
    metadata: dict[str, object] | None = None,
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": source,
        "query": query,
        "query_length": len(query),
        "primary_skill": decision.primary_skill,
        "overlay_skills": list(decision.overlay_skills),
        "knowledge_skills": list(decision.knowledge_skills),
        "selected_skills": list(decision.selected_skills),
        "primary_score": decision.primary_score,
        "secondary_score": decision.secondary_score,
        "confidence": decision.confidence,
        "fallback_reason": decision.fallback_reason,
        "matched": decision.primary_skill is not None,
    }
    if metadata:
        event["metadata"] = metadata

    with log_path.open("a") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def read_routing_events(log_path: Path = ROUTING_LOG_PATH, limit: int | None = None) -> list[dict[str, object]]:
    if not log_path.exists():
        return []

    events = [json.loads(line) for line in log_path.read_text().splitlines() if line.strip()]
    if limit is not None:
        return events[-limit:]
    return events


def summarize_routing_metrics(log_path: Path = ROUTING_LOG_PATH) -> dict[str, object]:
    events = read_routing_events(log_path)
    total = len(events)
    matched = sum(1 for event in events if event.get("matched"))
    fallback = total - matched
    selected_counts = [len(event.get("selected_skills", [])) for event in events]
    low_confidence = sum(1 for event in events if 0 < float(event.get("confidence", 0.0)) < 0.6)
    knowledge_activated = sum(1 for event in events if event.get("knowledge_skills"))

    primary_counts = Counter(
        str(event["primary_skill"]) for event in events if event.get("primary_skill")
    )
    overlay_counts = Counter(
        overlay
        for event in events
        for overlay in event.get("overlay_skills", [])
    )
    fallback_reasons = Counter(
        str(event["fallback_reason"]) for event in events if event.get("fallback_reason")
    )

    recent_fallback_queries = [
        str(event["query"])
        for event in events
        if not event.get("matched")
    ][-5:]

    return {
        "total_queries": total,
        "matched_queries": matched,
        "fallback_queries": fallback,
        "match_rate": round(matched / total, 3) if total else 0.0,
        "fallback_rate": round(fallback / total, 3) if total else 0.0,
        "average_selected_skill_count": round(sum(selected_counts) / total, 3) if total else 0.0,
        "knowledge_activation_rate": round(knowledge_activated / total, 3) if total else 0.0,
        "low_confidence_rate": round(low_confidence / total, 3) if total else 0.0,
        "primary_skill_counts": dict(sorted(primary_counts.items())),
        "overlay_skill_counts": dict(sorted(overlay_counts.items())),
        "fallback_reasons": dict(sorted(fallback_reasons.items())),
        "recent_fallback_queries": recent_fallback_queries,
        "log_path": str(log_path),
    }


def load_routing_benchmarks(path: Path = ROUTING_BENCHMARKS_PATH) -> list[RoutingBenchmarkCase]:
    payload = json.loads(path.read_text())
    return [
        RoutingBenchmarkCase(
            name=str(case["name"]),
            query=str(case["query"]),
            primary_skill=case.get("primary_skill"),
            overlay_skills=tuple(case.get("overlay_skills", [])),
            knowledge_skills=tuple(case.get("knowledge_skills", [])),
            fallback_reason=case.get("fallback_reason"),
        )
        for case in payload
    ]


def run_routing_benchmarks(
    cases: list[RoutingBenchmarkCase],
    repo_root: Path = REPO_ROOT,
) -> RoutingBenchmarkResult:
    failures: list[dict[str, object]] = []

    for case in cases:
        decision = classify_query(case.query, repo_root=repo_root)
        if (
            decision.primary_skill != case.primary_skill
            or tuple(decision.overlay_skills) != tuple(case.overlay_skills)
            or tuple(decision.knowledge_skills) != tuple(case.knowledge_skills)
            or decision.fallback_reason != case.fallback_reason
        ):
            failures.append(
                {
                    "name": case.name,
                    "query": case.query,
                    "expected": {
                        "primary_skill": case.primary_skill,
                        "overlay_skills": list(case.overlay_skills),
                        "knowledge_skills": list(case.knowledge_skills),
                        "fallback_reason": case.fallback_reason,
                    },
                    "actual": {
                        "primary_skill": decision.primary_skill,
                        "overlay_skills": list(decision.overlay_skills),
                        "knowledge_skills": list(decision.knowledge_skills),
                        "fallback_reason": decision.fallback_reason,
                        "confidence": decision.confidence,
                    },
                }
            )

    return RoutingBenchmarkResult(cases=tuple(cases), failures=tuple(failures))


def validate_repository(repo_root: Path = REPO_ROOT, instructions_path: Path = GLOBAL_INSTRUCTIONS) -> list[str]:
    errors: list[str] = []
    skills = discover_skills(repo_root)
    names = [skill.name for skill in skills]

    if len(names) != len(set(names)):
        errors.append("Duplicate skill names detected")

    for skill in skills:
        if not skill.description:
            errors.append(f"{skill.name}: missing description")
        if not skill.triggers:
            errors.append(f"{skill.name}: description is missing a 'Triggers on:' clause")

    for required in ("agent-orchestrator", "workflow-tdd", "workflow-skill-delivery"):
        if required not in names:
            errors.append(f"Missing required layered-routing skill: {required}")

    if not GLOBAL_INSTRUCTIONS_TEMPLATE.exists():
        errors.append(f"Missing global instructions template: {GLOBAL_INSTRUCTIONS_TEMPLATE}")
    else:
        template = GLOBAL_INSTRUCTIONS_TEMPLATE.read_text()
        if MANAGED_ROUTING_PLACEHOLDER not in template:
            errors.append("Global instructions template is missing the managed routing placeholder")

    if not LOCAL_OVERRIDE_TEMPLATE.exists():
        errors.append(f"Missing local override example template: {LOCAL_OVERRIDE_TEMPLATE}")

    if not ROUTING_BENCHMARKS_PATH.exists():
        errors.append(f"Missing routing benchmarks file: {ROUTING_BENCHMARKS_PATH}")

    if instructions_path.exists():
        contents = instructions_path.read_text()
        if MANAGED_START not in contents or MANAGED_END not in contents:
            errors.append("Global instructions are missing managed routing markers")

    return errors