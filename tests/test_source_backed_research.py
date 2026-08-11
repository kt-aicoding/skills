from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills/source-backed-research"
SKILL = SKILL_ROOT / "SKILL.md"
REFERENCE = SKILL_ROOT / "references/evidence-model.md"
INTERFACE = SKILL_ROOT / "agents/openai.yaml"


class SourceBackedResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.interface = INTERFACE.read_text(encoding="utf-8")

    def test_description_is_concise_and_front_loads_research_triggers(self) -> None:
        match = re.search(r"^description: (.+)$", self.skill, re.MULTILINE)

        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertLessEqual(len(description), 140)
        for trigger in ("Research current", "high-stakes", "primary sources"):
            self.assertIn(trigger, description)

    def test_workflow_preserves_ownership_and_evidence_boundaries(self) -> None:
        for required_text in (
            "Use `openai-docs` for OpenAI product/API questions",
            "Use `investigate` for code failures",
            "Build a claim ledger",
            "analysis/inference",
            "Privacy And Copyright",
            "Completion Gate",
            "time-sensitive claims have an as-of date",
        ):
            self.assertIn(required_text, self.skill)

    def test_evidence_model_preserves_source_levels_and_claim_statuses(self) -> None:
        for source_level in (
            "A - authoritative primary",
            "B - independent primary",
            "C - high-quality secondary",
            "D - discovery only",
        ):
            self.assertIn(source_level, self.reference)

        for status in (
            "`verified`",
            "`corroborated`",
            "`source-reported`",
            "`inferred`",
            "`conflicted`",
            "`unknown`",
        ):
            self.assertIn(status, self.reference)

    def test_interface_routes_to_the_named_skill(self) -> None:
        self.assertIn('display_name: "Source-Backed Research"', self.interface)
        self.assertIn("$source-backed-research", self.interface)


if __name__ == "__main__":
    unittest.main()
