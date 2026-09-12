"""Render the real client tree; package/question fixtures live in test_answers."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


PACKAGE = Path(__file__).resolve().parents[1]
INGRESS = ".github/workflows/cadence-review-ingress.yml"
CI = ".github/workflows/symphony-client-ci.yml"
WAKEUPS = ".github/workflows/symphony-client-wakeups.yml"
REVIEW_CALLERS = {
    '.github/workflows/cadence-ai-review-events.yml',
    '.github/workflows/cadence-ai-review-trigger.yml',
    '.github/workflows/cadence-ai-review.yml',
    '.github/workflows/cadence-linear-rework.yml',
    '.github/workflows/cadence-review-check-cleanup.yml',
}
CI_SOURCE = "1000lines/symphony-client-workflows"
CI_REF = "alpha"
REPLAN = "scripts/symphony/runtime-bundle/skills/symphony-replan/SKILL.md"
FACTORY = ".agents/skills/symphony-project-factory"
SKILLS = {
    f"{FACTORY}/SKILL.md",
    f"{FACTORY}/templates/project-description.md",
    *(f"{FACTORY}/templates/tickets/{name}.md" for name in (
        "requirements-and-design", "plan-project", "trigger-fan-out",
        "broaden-fanout-integration", "standup")),
    ".agents/skills/linear-graphql/SKILL.md",
    ".agents/skills/linear-graphql/agents/openai.yaml",
    ".agents/skills/linear-graphql/scripts/linear-graphql.mjs",
    REPLAN,
    "docs/engineering/symphony/replanning.md",
}
GENERATED = SKILLS | REVIEW_CALLERS | {
    INGRESS, ".symphony.cfg.json", ".gitattributes", "SYMPHONY.md",
    ".github/symphony/REVIEW.md", ".github/symphony/cadence-app-manifest.json",
    ".github/symphony/symphony-app-manifest.json", ".github/symphony/setup-app.mjs",
    ".github/symphony/APP-SETUP.md",
    ".copier-answers.yml", CI, WAKEUPS,
}


class RenderTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".client-render-", dir=Path.cwd())
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.source = self.root / "source"
        shutil.copytree(PACKAGE, self.source, ignore=shutil.ignore_patterns("__pycache__"))
        # Root self-use assets must not leak even when they share generated names.
        for relative in ("SYMPHONY.md", ".symphony.cfg.json", ".copier-answers.yml",
                         ".github/workflows/root-only.yml", "tests/root-only.txt"):
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("ROOT-ONLY-SENTINEL\n")
        self.git(self.source, "init", "--initial-branch=main")
        self.git(self.source, "add", ".")
        self.git(self.source, "-c", "user.name=Fixture", "-c",
                 "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                 "commit", "-m", "Real client fixture")
        self.commit = self.git(self.source, "rev-parse", "HEAD").strip()
        self.git(self.source, "branch", "alpha")

    def git(self, directory, *args):
        return subprocess.check_output(
            ["git", "-C", str(directory), *args], text=True, stderr=subprocess.STDOUT
        )

    def answers(self, index=0):
        slug, branch, team, reviewer = [
            ("example/widget", "main", "100", "claude"),
            ("another-owner/second-repo", "release/next", "OPS", "codex"),
        ][index]
        return dict(repo_slug=slug, default_branch=branch, linear_team_key=team,
                    symphony_app_slug=f"author-{index}", cadence_app_slug=f"reviewer-{index}",
                    cadence_reviewer=reviewer,
                    build_command="printf '%s\\n' 'build: \"quoted\"'\nmake build\n",
                    test_command="printf '%s' \"backslash: \\\\ and $HOME\"\nmake test --flag='yes'\n")

    def render(self, answers, name="output", *options):
        data_file = self.root / f"{name}.yml"
        data_file.write_text(yaml.safe_dump(answers))
        output = self.root / name
        result = subprocess.run(
            [sys.executable, "-m", "copier", "copy", "--defaults", "--vcs-ref=alpha",
             "--data-file", str(data_file), *options, str(self.source), str(output)],
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git(self.source, "status", "--porcelain"), "")
        return output

    def test_real_tree_matrix(self):
        for index in range(2):
            answers = self.answers(index)
            with self.subTest(repo=answers["repo_slug"]):
                output = self.render(answers, f"output-{index}")
                files = {p.relative_to(output).as_posix() for p in output.rglob("*")
                         if p.is_file()}
                self.assertEqual(files, GENERATED)
                for relative in files:
                    content = (output / relative).read_text()
                    self.assertNotIn("ROOT-ONLY-SENTINEL", content, relative)
                    self.assertNotIn("karpathy", content.lower(), relative)
                    self.assertNotRegex(content, r"\[\[\s*[a-zA-Z_]")
                    self.assertNotIn("[%", content, relative)
                    if relative.endswith((".yml", ".yaml")):
                        yaml.safe_load(content)
                    if relative.endswith(".json"):
                        json.loads(content)

                saved = yaml.safe_load((output / ".copier-answers.yml").read_text())
                self.assertEqual(set(saved), set(answers) | {"_src_path", "_commit"})
                self.assertEqual({key: saved[key] for key in answers}, answers)
                self.assertEqual(saved["_src_path"], str(self.source))
                self.assertEqual(self.git(self.source, "rev-parse", saved["_commit"]).strip(), self.commit)
                config = json.loads((output / ".symphony.cfg.json").read_text())
                self.assertEqual(config, {
                    "schemaVersion": "symphony-repository/v1",
                    "linear": {"teamKey": answers["linear_team_key"]},
                    "workingDirectory": ".", "instructions": ["SYMPHONY.md"],
                    "commands": {name: [["bash", "-lc", answers[f"{name}_command"]]]
                                 for name in ("build", "test")},
                    "ci": {"requiredChecks": []},
                })
                self.assertIn("unconfigured", (output / "SYMPHONY.md").read_text())
                review = (output / ".github/symphony/REVIEW.md").read_text()
                self.assertIn(json.dumps(answers["cadence_reviewer"]), review)
                self.assertIn("CADENCE_OPENAI_API_KEY" if index else
                              "CADENCE_AI_REVIEW_ANTHROPIC_API_KEY", review)
                self.check_ingress(output, answers)
                self.check_ci_callers(output, answers)
                self.check_review_callers(output)
                manifest = json.loads((output / ".github/symphony/cadence-app-manifest.json").read_text())
                self.assertEqual(manifest["name"], answers["cadence_app_slug"])
                self.assertEqual(manifest["url"], f"https://github.com/{answers['repo_slug']}")
                self.assertEqual(manifest["default_permissions"], {
                    "metadata": "read", "contents": "read", "actions": "read",
                    "pull_requests": "write", "issues": "write", "checks": "write",
                })
                self.assertFalse(manifest["public"])
                self.assertEqual(manifest["default_events"], [])
                author_manifest = json.loads((output / ".github/symphony/symphony-app-manifest.json").read_text())
                self.assertEqual(author_manifest["name"], answers["symphony_app_slug"])
                self.assertEqual(author_manifest["default_permissions"], {
                    "metadata": "read", "contents": "write", "actions": "read",
                    "pull_requests": "write", "issues": "write", "checks": "read",
                    "statuses": "read", "workflows": "write",
                })
                self.check_skills(output)

    def test_root_client_matches_render_preserving_package_ci(self):
        saved = yaml.safe_load((PACKAGE / ".copier-answers.yml").read_text())
        answers = {key: value for key, value in saved.items() if not key.startswith("_")}
        output = self.render(answers, "root-client")
        # Metadata records the last render from a committed source. The optional
        # command caller is replaced by this repository's dedicated package CI.
        for relative in GENERATED - {CI, ".copier-answers.yml", ".symphony.cfg.json"}:
            self.assertEqual((PACKAGE / relative).read_bytes(),
                             (output / relative).read_bytes(), relative)
        self.assertFalse((PACKAGE / CI).exists())
        root_config = json.loads((PACKAGE / ".symphony.cfg.json").read_text())
        rendered_config = json.loads((output / ".symphony.cfg.json").read_text())
        package_ci = yaml.safe_load((PACKAGE / ".github/workflows/ci.yml").read_text())
        self.assertEqual(root_config["ci"]["requiredChecks"], [{
            "name": package_ci["jobs"]["render"]["name"],
            "workflow": ".github/workflows/ci.yml", "appId": 15368,
        }])
        self.assertEqual({key: value for key, value in root_config.items() if key != "ci"},
                         {key: value for key, value in rendered_config.items() if key != "ci"})

    def check_review_callers(self, output):
        for relative in REVIEW_CALLERS:
            workflow = yaml.safe_load((output / relative).read_text())
            job, = workflow["jobs"].values()
            secrets = {"CADENCE_APP_PRIVATE_KEY"}
            if not relative.endswith("cadence-review-check-cleanup.yml"):
                secrets.add("CADENCE_LINEAR_API_TOKEN")
            if "cadence-ai-review" in relative:
                secrets.update({"CADENCE_OPENAI_API_KEY", "CADENCE_AI_REVIEW_ANTHROPIC_API_KEY"})
            self.assertEqual(job["secrets"], {
                key: "${{ secrets." + key + " }}" for key in secrets
            })
            source, ref = job["uses"].split("@")
            self.assertEqual(source, "1000lines/symphony-client-workflows/" + relative)
            self.assertRegex(ref, r"^[a-f0-9]{40}$")
            self.assertEqual(job["with"]["helpers-ref"], ref)
            self.assertLessEqual(set(job), {"uses", "with", "secrets", "if"})
            self.assertNotIn("inherit", (output / relative).read_text())
        review = (output / ".github/symphony/REVIEW.md").read_text()
        for phrase in ("Both | Codex", "Neither | Early configuration error", "openai-api-key"):
            self.assertIn(phrase, review)

    def check_ci_callers(self, output, answers):
        ci = yaml.safe_load((output / CI).read_text())
        self.assertEqual(ci[True], {
            "push": {"branches": [answers["default_branch"]]},
            "pull_request": {"types": ["opened", "synchronize", "reopened"]},
        })
        self.assertEqual(ci["permissions"], {"contents": "read"})
        command_job = ci["jobs"]["commands"]
        self.assertEqual(json.loads(command_job["with"]["commands"]), [
            ["bash", "-lc", answers["build_command"]],
            ["bash", "-lc", answers["test_command"]],
        ])
        self.assertEqual(command_job["with"]["tested-ref"],
                         "${{ github.event.pull_request.head.sha || github.sha }}")
        self.assertNotIn("secrets", (output / CI).read_text())

        wakeups = yaml.safe_load((output / WAKEUPS).read_text())
        self.assertEqual(set(wakeups[True]), {
            "pull_request_target", "workflow_run", "check_run", "status",
        })
        self.assertEqual(wakeups[True]["workflow_run"], {
            "workflows": ["*"], "types": ["completed"],
        })
        self.assertEqual(wakeups["permissions"], dict.fromkeys(
            ("actions", "checks", "contents", "pull-requests", "statuses"), "read"))
        wake_job = wakeups["jobs"]["wake"]
        self.assertEqual(wake_job["with"], {
            "target-repository": answers["repo_slug"],
            "target-default-branch": answers["default_branch"],
            "event-name": "${{ github.event_name }}",
            "event-payload": "${{ toJSON(github.event) }}",
            "helpers-repository": CI_SOURCE,
            "helpers-ref": CI_REF,
        })
        self.assertEqual(wake_job["secrets"], {
            "CADENCE_LINEAR_API_TOKEN": "${{ secrets.CADENCE_LINEAR_API_TOKEN }}",
        })
        for path, job, entry in (
            (CI, command_job, "symphony-client-commands.yml"),
            (WAKEUPS, wake_job, "symphony-linear-wakeups.yml"),
        ):
            self.assertEqual(job["uses"], f"{CI_SOURCE}/.github/workflows/{entry}@{CI_REF}")
            self.assertLessEqual(set(job), {"uses", "with", "if", "secrets"})
            self.assertNotIn("inherit", (output / path).read_text())
            source = (PACKAGE / "template" / (path + ".jinja")).read_text()
            self.assertEqual(re.findall(r"\$\{\{.*?\}\}", (output / path).read_text(), re.S),
                             re.findall(r"\$\{\{.*?\}\}", source, re.S))

    def test_rendered_ci_commands_execute_and_fail_without_secrets(self):
        answers = self.answers()
        answers.update(build_command="printf '%s' 'literal: \"quotes\" \\ $HOME' > result",
                       test_command="test \"$(cat result)\" = 'literal: \"quotes\" \\ $HOME'")
        output = self.render(answers)
        workflow = yaml.safe_load((output / CI).read_text())
        commands = json.loads(workflow["jobs"]["commands"]["with"]["commands"])
        for argv in commands:
            subprocess.run(argv, cwd=output, check=True, capture_output=True, timeout=10)
        (output / "result").write_text("wrong build result")
        self.assertNotEqual(subprocess.run(commands[1], cwd=output, timeout=10).returncode, 0)

    def check_ingress(self, output, answers):
        text = (output / INGRESS).read_text()
        # The only expression edits replace the two seed login defaults.
        source = (PACKAGE / "template" / (INGRESS + ".jinja")).read_text()
        for key in ("symphony_app_slug", "cadence_app_slug"):
            expression = "[[ (" + key + " ~ '[bot]') | replace(\"'\", \"''\") ]]"
            source = source.replace(expression, answers[key] + "[bot]")
        self.assertEqual(text, source)
        self.assertEqual(re.findall(r"\$\{\{.*?\}\}", text, re.S),
                         re.findall(r"\$\{\{.*?\}\}", source, re.S))
        workflow = yaml.safe_load(text)
        self.assertEqual(workflow["name"], "Cadence Review Ingress")
        self.assertEqual(workflow["permissions"], {})
        # PyYAML's YAML 1.1 resolver reads the unquoted GitHub `on` key as True.
        self.assertEqual(set(workflow[True]), {
            "pull_request_target", "issue_comment", "pull_request_review",
            "pull_request_review_comment",
        })
        self.assertNotIn("secrets", workflow)
        self.assertEqual(workflow["jobs"]["ingress"]["steps"], [{
            "name": "Signal main consumers",
            "run": "echo 'Current feedback will be resolved by the main controller.'",
        }])

    def check_skills(self, output):
        for relative in SKILLS:
            self.assertEqual((output / relative).read_bytes(),
                             (PACKAGE / "template" / relative).read_bytes(), relative)
            if relative.endswith("SKILL.md"):
                header = yaml.safe_load((output / relative).read_text().split("---", 2)[1])
                self.assertTrue(header["name"])
                self.assertTrue(header["description"])
        self.assertIn("docs/engineering/symphony/replanning.md", (output / REPLAN).read_text())
        # Resolve actual local Markdown links from the client, including replan resources.
        for relative in ("SYMPHONY.md", "docs/engineering/symphony/replanning.md"):
            path = output / relative
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" not in target:
                    self.assertTrue((path.parent / target).is_file(), (relative, target))

    def test_update_removes_bundled_skill_and_preserves_adopter_changes(self):
        skill = ".agents/skills/karpathy-guidelines/SKILL.md"
        examples = ".agents/skills/karpathy-guidelines/EXAMPLES.md"
        # A prior template revision with the removed distribution. Keep the
        # fixture self-contained so updates also run in shallow CI checkouts.
        for relative in (skill, examples):
            path = self.source / "template" / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Bundled Karpathy fixture\n")
        for relative in ("SYMPHONY.md.jinja", f"{FACTORY}/SKILL.md"):
            path = self.source / "template" / relative
            path.write_text(path.read_text() + f"\nLoad `{skill}`.\n")
        self.git(self.source, "add", "template")
        self.git(self.source, "-c", "user.name=Fixture", "-c",
                 "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                 "commit", "-m", "Prior template with bundled skill")
        self.git(self.source, "branch", "-f", "alpha", "HEAD")
        clients = [self.render(self.answers(), name) for name in ("unchanged", "adopter")]
        preserved = {
            skill: "Adopter's modified coding guidelines\n",
            ".agents/skills/karpathy-guidelines/LOCAL.md": "Adopter's added notes\n",
            ".agents/skills/adopter/SKILL.md": "Independent adopter skill\n",
            "src/application.txt": "Existing application\n",
        }
        for relative, content in preserved.items():
            path = clients[1] / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        for output in clients:
            self.git(output, "init", "--initial-branch=main")
            self.git(output, "add", ".")
            self.git(output, "-c", "user.name=Fixture", "-c",
                     "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                     "commit", "-m", "Existing generated client")

        self.git(self.source, "restore", f"--source={self.commit}",
                 "--staged", "--worktree", "template")
        self.git(self.source, "-c", "user.name=Fixture", "-c",
                 "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                 "commit", "-m", "Remove bundled skill")
        self.git(self.source, "branch", "-f", "alpha", "HEAD")
        for output in clients:
            with self.subTest(client=output.name):
                # Copier 9.18.2 deletes removed template paths even when locally
                # modified. Exclude the reviewed adopter-owned file explicitly.
                options = ["--exclude", skill] if output.name == "adopter" else []
                result = subprocess.run(
                    [sys.executable, "-m", "copier", "update", "--defaults",
                     "--vcs-ref=alpha", *options], cwd=output, stdin=subprocess.DEVNULL,
                    capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse((output / examples).exists())
                for relative in ("SYMPHONY.md", f"{FACTORY}/SKILL.md"):
                    self.assertNotIn("karpathy", (output / relative).read_text().lower())
                saved = yaml.safe_load((output / ".copier-answers.yml").read_text())
                self.assertEqual(saved["_src_path"], str(self.source))
                self.assertEqual(self.git(self.source, "rev-parse", saved["_commit"]),
                                 self.git(self.source, "rev-parse", "alpha"))
        self.assertFalse((clients[0] / ".agents/skills/karpathy-guidelines").exists())
        for relative, content in preserved.items():
            self.assertEqual((clients[1] / relative).read_text(), content, relative)

    def test_existing_repository_preservation_and_reviewed_attributes_merge(self):
        output = self.root / "existing"
        existing = {
            "AGENTS.md": "Application worker rules\n", "CLAUDE.md": "Application review rules\n",
            "README.md": "Application README\n", "LICENSE": "Application license\n",
            "NOTICE": "Application notice\n", "src/application.txt": "Application payload\n",
            ".github/workflows/ci.yml": "name: Existing application CI\n",
            ".gitattributes": "*.dat binary\n",
            ".symphony.cfg.json": json.dumps({"existing": "target config"}) + "\n",
            ".copier-answers.yml": "previous_answer: retained\n",
        }
        existing.update({path: f"Existing reviewed resource: {path}\n" for path in SKILLS})
        for relative, content in existing.items():
            path = output / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.render(self.answers(), "existing", "--skip", "*")
        for relative, content in existing.items():
            self.assertEqual((output / relative).read_text(), content, relative)

        # The documented manual merge retains target rules and adds the reviewed globs.
        clean = self.render(self.answers(), "clean")
        attributes = clean / ".gitattributes"
        self.assertEqual(attributes.read_bytes(), (PACKAGE / "template/.gitattributes").read_bytes())
        (output / ".gitattributes").write_text(existing[".gitattributes"] + attributes.read_text())
        self.git(output, "init", "--initial-branch=main")
        for relative in ("docs/symphony-plans/project/notes.md",
                         "docs/symphony-plans/project/graph.mmd", "docs/symphony-plans/plan.md"):
            path = output / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Planning fixture\n")
        result = self.git(output, "check-attr", "linguist-generated", "--",
                          "docs/symphony-plans/project/notes.md",
                          "docs/symphony-plans/project/graph.mmd", "docs/symphony-plans/plan.md")
        self.assertEqual([line.rsplit(": ", 1)[1] for line in result.splitlines()],
                         ["set", "unset", "unspecified"])
        self.assertIn("binary: set", self.git(output, "check-attr", "binary", "--", "data.dat"))


if __name__ == "__main__":
    unittest.main()
