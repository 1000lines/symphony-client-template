"""Keep transport guidance and its loopback rehearsal in mandatory Python CI."""

from pathlib import Path
import re
import subprocess
import unittest

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
FACTORY = PACKAGE / "template/.agents/skills/symphony-project-factory/SKILL.md"
GRAPHQL = PACKAGE / "template/.agents/skills/linear-graphql/SKILL.md"
SYMPHONY = PACKAGE / "template/SYMPHONY.md.jinja"


class FactoryGuidanceTest(unittest.TestCase):
    def test_concise_consistent_transport_contract_and_local_links(self):
        for path in (FACTORY, GRAPHQL, SYMPHONY):
            with self.subTest(path=path):
                text = path.read_text()
                self.assertLessEqual(len(text.splitlines()), 120)
                self.assertIn("linear_graphql", text)
                self.assertIn("human-operated", text)
                self.assertIn("injected", text)
                self.assertNotIn("fallback script does not replace it", text)
                for target in re.findall(r"\]\(([^)]+)\)", text):
                    if "://" not in target:
                        # SYMPHONY links refer to rendered names; render tests resolve them.
                        if path != SYMPHONY:
                            self.assertTrue((path.parent / target).is_file(), target)
        factory = FACTORY.read_text()
        for contract in ("viewer ID", "workspace ID/name", "team ID/key", "Unavailable source",
                         "project-colors.ts", "label IDs", "assignee", "Backlog", "Active",
                         "concrete GraphQL input objects", "no second confirmation", "preview-only",
                         "both relation directions", "Partial creation/relation failure",
                         "reuse", "unless held", "symphony-dag-manifest/v1"):
            self.assertIn(contract, factory)
        metadata = yaml.safe_load((GRAPHQL.parent / "agents/openai.yaml").read_text())
        self.assertIn("prefer the injected tool", metadata["interface"]["default_prompt"])

    def test_transport_rehearsal(self):
        result = subprocess.run(["node", "--test", str(PACKAGE / "tests/test-factory-transport.mjs")],
                                cwd=PACKAGE, capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
