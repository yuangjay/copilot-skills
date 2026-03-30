import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from skilllib.system import (
    classify_query,
    discover_skills,
    generate_index,
    load_routing_benchmarks,
    record_routing_event,
    render_global_instructions,
    run_routing_benchmarks,
    summarize_routing_metrics,
)


REPO_ROOT = Path("/root/.copilot/skills")


class SkillSystemTests(unittest.TestCase):
    def test_discovers_new_skill_layers(self):
        names = {skill.name for skill in discover_skills(REPO_ROOT)}

        self.assertIn("agent-orchestrator", names)
        self.assertIn("workflow-tdd", names)
        self.assertIn("workflow-skill-delivery", names)

    def test_issue_fix_query_uses_tdd_and_delivery_layers(self):
        decision = classify_query(
            "fix an issue in the skill system, update tests first, then commit and push the skills repo"
        )

        self.assertEqual("agent-customization", decision.primary_skill)
        self.assertIn("workflow-tdd", decision.overlay_skills)
        self.assertIn("workflow-skill-delivery", decision.overlay_skills)

    def test_layered_routing_query_prefers_orchestrator(self):
        decision = classify_query(
            "how should Copilot auto choose layered skills without wasting tokens"
        )

        self.assertEqual("agent-orchestrator", decision.primary_skill)

    def test_generated_index_contains_new_skills(self):
        index = generate_index(discover_skills(REPO_ROOT), today=date(2026, 3, 30))

        self.assertIn("| `agent-orchestrator` |", index)
        self.assertIn("| `workflow-tdd` |", index)
        self.assertIn("| `workflow-skill-delivery` |", index)

    def test_low_confidence_queries_fall_back_instead_of_forcing_a_skill(self):
        decision = classify_query("hello there")

        self.assertIsNone(decision.primary_skill)
        self.assertEqual("low_score", decision.fallback_reason)

    def test_render_global_instructions_uses_template_and_local_override(self):
        with TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            template_path = temp_root / "copilot-instructions.base.md"
            override_path = temp_root / "copilot-instructions.local.md"

            template_path.write_text(
                "# Base Instructions\n\nBefore\n\n{{MANAGED_ROUTING_BLOCK}}\n\nAfter\n"
            )
            override_path.write_text("- local machine override\n")

            rendered = render_global_instructions(
                REPO_ROOT,
                template_path=template_path,
                override_path=override_path,
            )

            self.assertIn("# Base Instructions", rendered)
            self.assertIn("<!-- BEGIN MANAGED: layered-skill-routing -->", rendered)
            self.assertIn("## Local Overrides", rendered)
            self.assertIn("local machine override", rendered)

    def test_metrics_summary_aggregates_logged_routing_events(self):
        with TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "routing.jsonl"
            matched = classify_query(
                "fix an issue in the skill system, update tests first, then commit and push the skills repo"
            )
            fallback = classify_query("hello there")

            record_routing_event("issue query", matched, log_path=log_path, source="test")
            record_routing_event("greeting", fallback, log_path=log_path, source="test")

            summary = summarize_routing_metrics(log_path=log_path)

            self.assertEqual(2, summary["total_queries"])
            self.assertEqual(1, summary["matched_queries"])
            self.assertEqual(1, summary["fallback_queries"])
            self.assertIn("agent-customization", summary["primary_skill_counts"])

    def test_routing_benchmarks_pass(self):
        cases = load_routing_benchmarks(REPO_ROOT / "benchmarks" / "routing.json")
        result = run_routing_benchmarks(cases)

        self.assertEqual(0, len(result.failures))
        self.assertGreater(len(result.cases), 0)


if __name__ == "__main__":
    unittest.main()