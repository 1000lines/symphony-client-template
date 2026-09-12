"""Run the offline Node regression suite in mandatory template CI."""

from pathlib import Path
import subprocess
import unittest

PACKAGE = Path(__file__).resolve().parents[1]


class PrGuidanceTest(unittest.TestCase):
    def test_progress_regressions(self):
        result = subprocess.run(["node", "--test", str(PACKAGE / "tests/test-pr-progress.mjs")],
                                cwd=PACKAGE, capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_concise_guidance_invokes_creation_and_refresh(self):
        for relative, limit in ((".github/pull_request_template.md", 60),
                                ("docs/engineering/symphony/pull-requests.md", 160)):
            text = (PACKAGE / "template" / relative).read_text()
            self.assertLessEqual(len(text.splitlines()), limit)
        guidance = (PACKAGE / "template/docs/engineering/symphony/pull-requests.md").read_text()
        self.assertEqual(guidance.count("node scripts/symphony/render-pr-progress.mjs progress.json"), 2)
        for command in ("--query", "--linear-response", "--current-pr", "gh pr create", "gh pr edit"):
            self.assertIn(command, guidance)
        self.assertIn("docs/engineering/symphony/pull-requests.md",
                      (PACKAGE / "template/SYMPHONY.md.jinja").read_text())


if __name__ == "__main__":
    unittest.main()
