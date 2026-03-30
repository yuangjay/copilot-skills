import unittest
from datetime import date
from pathlib import Path

from skilllib.system import classify_query, discover_skills, generate_index


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


if __name__ == "__main__":
    unittest.main()