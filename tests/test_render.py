"""Render the real client tree; package/question fixtures live in test_answers."""

import json
from pathlib import Path
import re
import shlex
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
REVIEW_REF = "ddc9eb0f2a1a24643b6350db9003ed27089548a6"
REPLAN = "scripts/symphony/runtime-bundle/skills/symphony-replan/SKILL.md"
FACTORY = ".agents/skills/symphony-project-factory"
SKILLS = {
    f"{FACTORY}/SKILL.md",
    f"{FACTORY}/templates/project-description.md",
    *(f"{FACTORY}/templates/tickets/{name}.md" for name in (
        "requirements-and-design", "plan-project", "trigger-fan-out",
        "broaden-fanout-integration", "standup")),
    ".agents/skills/cadence-onboarding/SKILL.md",
    ".agents/skills/cadence-onboarding/scripts/check-credentials.mjs",
    ".agents/skills/linear-graphql/SKILL.md",
    ".agents/skills/linear-graphql/agents/openai.yaml",
    ".agents/skills/linear-graphql/scripts/linear-graphql.mjs",
    REPLAN,
    "docs/engineering/symphony/replanning.md",
}
PR_FILES = {
    "scripts/symphony/render-pr-progress.mjs", "scripts/symphony/fetch-pr-progress.mjs",
    ".github/pull_request_template.md", "docs/engineering/symphony/pull-requests.md",
}
GENERATED = SKILLS | REVIEW_CALLERS | PR_FILES | {
    INGRESS, ".symphony.cfg.json", ".gitattributes", "SYMPHONY.md",
    ".github/symphony/REVIEW.md", ".github/symphony/cadence-app-manifest.json",
    ".github/symphony/symphony-app-manifest.json", ".github/symphony/setup-app.mjs",
    ".github/symphony/APP-SETUP.md",
    ".copier-answers.yml", CI, WAKEUPS, ".github/workflows/symphony-client-setup.yml",
}


def file_set(directory):
    return {p.relative_to(directory).as_posix() for p in directory.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(directory).parts}


# Package-owned files are not generated client output (SELF-ADOPTION.md).
# Keep this separate from GENERATED: current source can add/remove client paths
# before the next root adoption. Everything else in the root must be accounted for.
PACKAGE_FILES = {
    ".gitignore", ".prettierignore", "LICENSE", "PROVENANCE.md", "README.md",
    "SELF-ADOPTION.md", "copier.yml", ".github/workflows/ci.yml",
}
PACKAGE_TREES = ("template/", "tests/", "docs/symphony-plans/")


def recorded_inventory(source, revision):
    if not re.fullmatch(r"[a-f0-9]{7,40}", revision):
        raise ValueError("Recorded source must be a committed hexadecimal revision")
    paths = subprocess.check_output(
        ["git", "-C", str(source), "ls-tree", "-r", "--name-only", revision, "--", "template"],
        text=True, stderr=subprocess.PIPE).splitlines()
    if not paths:
        raise ValueError("Recorded source has no template")
    # Inventory comes from the committed source tree, never the render under test.
    inventory = {path.removeprefix("template/").removesuffix(".jinja") for path in paths}
    inventory.remove("[[ _copier_conf.answers_file ]]")
    inventory.add(".copier-answers.yml")
    if any("[[" in path or "[%" in path for path in inventory):
        raise ValueError("Unaccounted recorded template path expression")
    return inventory


class RecordedRootTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix=".recorded-root-", dir=Path.cwd())
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.directory = Path(cls.temporary.name).resolve()
        cls.saved = yaml.safe_load((PACKAGE / ".copier-answers.yml").read_text())
        if cls.saved["_src_path"] != "https://github.com/1000lines/symphony-client-template.git":
            raise ValueError("Unexpected recorded template source URL")
        # Full local checkouts can supply the immutable object without network.
        # Shallow CI checks out only the PR head: acquire history in a separate
        # clone from the recorded URL, never substitute current source or skip.
        available = subprocess.run(["git", "-C", str(PACKAGE), "cat-file", "-e",
                                    cls.saved["_commit"] + "^{commit}"], capture_output=True)
        cls.source = PACKAGE
        if available.returncode:
            cls.source = cls.directory / "recorded-source"
            subprocess.run(["git", "clone", "--quiet", "--no-checkout", "--",
                            cls.saved["_src_path"], str(cls.source)], check=True,
                           capture_output=True, timeout=60)
        cls.inventory = recorded_inventory(cls.source, cls.saved["_commit"])
        data = cls.directory / "answers.yml"
        data.write_text(yaml.safe_dump({k: v for k, v in cls.saved.items() if not k.startswith("_")}))
        cls.output = cls.directory / "render"
        subprocess.run([sys.executable, "-m", "copier", "copy", "--defaults",
                        "--vcs-ref=" + cls.saved["_commit"], "--data-file", str(data),
                        str(cls.source), str(cls.output)], check=True, capture_output=True, timeout=60)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=self.directory)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "client"
        shutil.copytree(PACKAGE, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def check_root(self, root):
        output = self.output
        self.assertEqual(file_set(output), self.inventory)
        actual = {p for p in file_set(root) if p not in PACKAGE_FILES and not p.startswith(PACKAGE_TREES)}
        self.assertEqual(actual, self.inventory - {CI})
        self.assertEqual(yaml.safe_load((root / ".copier-answers.yml").read_text()), self.saved)
        for relative in self.inventory - {CI, ".copier-answers.yml", ".symphony.cfg.json"}:
            self.assertEqual((root / relative).read_bytes(), (output / relative).read_bytes(), relative)
        self.assertFalse((root / CI).exists())
        root_config = json.loads((root / ".symphony.cfg.json").read_text())
        rendered_config = json.loads((output / ".symphony.cfg.json").read_text())
        # This package also validates the generated credential and App setup helpers with Node.
        rendered_config["commands"]["test"].append(["node", "--test", "tests/test-credentials.mjs"])
        rendered_config["commands"]["test"].append(["node", "--test", "tests/test-app-setup.mjs"])
        package_ci = yaml.safe_load((root / ".github/workflows/ci.yml").read_text())
        self.assertEqual(root_config["ci"]["requiredChecks"], [{
            "name": package_ci["jobs"]["render"]["name"],
            "workflow": ".github/workflows/ci.yml", "appId": 15368,
        }])
        self.assertEqual({key: value for key, value in root_config.items() if key != "ci"},
                         {key: value for key, value in rendered_config.items() if key != "ci"})

    def test_root_matches_its_recorded_source(self):
        self.check_root(self.root)

    def test_source_only_addition_does_not_require_root_adoption(self):
        added = ".github/future-source-only.md"
        path = self.root / "template" / added
        path.write_text("Future source increment\n")
        # A downstream task updates this explicit current inventory in the same PR.
        current_inventory = GENERATED | {added}
        data = self.directory / "future.yml"
        data.write_text(yaml.safe_dump({k: v for k, v in self.saved.items() if not k.startswith("_")}))
        subprocess.run(["git", "init", "--initial-branch=main", str(self.root)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c",
                        "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                        "commit", "-m", "Source-only increment"], check=True, capture_output=True)
        output = self.root.parent / "fresh"
        subprocess.run([sys.executable, "-m", "copier", "copy", "--defaults", "--vcs-ref=HEAD",
                        "--data-file", str(data), str(self.root), str(output)],
                       check=True, capture_output=True, timeout=30)
        self.assertEqual(file_set(output), current_inventory)
        self.assertNotIn(added, self.inventory)
        self.check_root(self.root)
        for change in ("unexpected", "missing"):
            with self.subTest(change=change):
                if change == "unexpected":
                    (output / "extra.txt").write_text("Unexpected output\n")
                else:
                    (output / "extra.txt").unlink()
                    (output / added).unlink()
                with self.assertRaises(AssertionError):
                    self.assertEqual(file_set(output), current_inventory)

    def test_root_byte_membership_and_config_drift_fail(self):
        for change in ("bytes", "missing", "unexpected", "config", "ci", "answers"):
            with self.subTest(change=change):
                path = self.root / "SYMPHONY.md"
                original = path.read_bytes()
                other = None
                if change == "bytes":
                    path.write_text("Altered recorded bytes\n")
                elif change == "missing":
                    path.unlink()
                elif change == "unexpected":
                    other = self.root / ".agents/unexpected.md"
                    other.write_text("Unexpected generated root output\n")
                else:
                    path = self.root / {"config": ".symphony.cfg.json", "ci": CI,
                                        "answers": ".copier-answers.yml"}[change]
                    original = path.read_bytes() if path.exists() else None
                    if change == "config":
                        config = json.loads(path.read_text())
                        config["ci"]["requiredChecks"] = []
                        path.write_text(json.dumps(config))
                    else:
                        path.write_text("invalid: true\n")
                with self.assertRaises(AssertionError):
                    self.check_root(self.root)
                if original is None:
                    path.unlink()
                else:
                    path.write_bytes(original)
                if other:
                    other.unlink()

    def test_unavailable_or_moving_recorded_source_fails(self):
        with self.assertRaises(subprocess.CalledProcessError):
            recorded_inventory(self.source, "0" * 40)
        with self.assertRaises(ValueError):
            recorded_inventory(self.source, "main")


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
        self.copy_messages = result.stdout + result.stderr
        return output

    def check_lifecycle_messages(self, text, action, answers):
        before, after = {
            "copy": ("Before copying", "Generated Symphony/Cadence files for"),
            "update": ("Before updating", "Updated Symphony/Cadence files for"),
        }[action]
        self.assertEqual(text.count(before), 1)
        self.assertEqual(text.count(after), 1)
        before_text, after_text = text.split(after)
        self.assertIn(answers["repo_slug"], after_text)
        settings = {
            "CADENCE_APP_ID", "CADENCE_APP_PRIVATE_KEY", "CADENCE_REVIEWER",
            "SYMPHONY_BOT_USER", "CADENCE_LINEAR_API_TOKEN", "CADENCE_OPENAI_API_KEY",
            "CADENCE_AI_REVIEW_ANTHROPIC_API_KEY", "CADENCE_CLAUDE_MODEL",
        }
        for message in (before_text, after_text):
            for setting in settings:
                self.assertIn(setting, message)
            self.assertIn("OpenAI wins", message)
            self.assertIn("at least one provider key", message.lower())
            self.assertIn(".github/symphony/APP-SETUP.md", message)
            self.assertIn(".agents/skills/cadence-onboarding/SKILL.md", message)
            self.assertNotIn("[bot][bot]", message)
            self.assertNotIn("[[", message)
            self.assertNotIn("project_name", message)
            self.assertNotIn("PYPI", message.upper())
            self.assertNotIn("CODECOV", message.upper())
        self.assertIn("required only for Claude", before_text)
        self.assertIn("For Claude only:", after_text)
        self.assertIn("Personal-account repositories use repository settings", after_text)
        self.assertIn("GitHub Free private repos cannot use org settings", after_text)
        self.assertIn("Public-only visibility does not cover private repos", after_text)
        self.assertIn("preserve other grants", after_text)
        self.assertIn(".github/symphony/setup-app.mjs", after_text)
        self.assertIn("live provider review", after_text)
        self.assertLess(after_text.index("1."), after_text.index("2."))
        self.assertLess(after_text.index("2."), after_text.index("3."))
        self.assertLess(after_text.index("3."), after_text.index("4."))
        commands = [shlex.split(line.strip()) for line in after_text.splitlines()
                    if line.strip().startswith("gh ")]
        repository_commands = [cmd for cmd in commands if "--repo" in cmd]
        for cmd in repository_commands:
            self.assertEqual(cmd[cmd.index("--repo") + 1], answers["repo_slug"])
        setting_commands = {cmd[3]: cmd for cmd in repository_commands
                            if cmd[1] in ("secret", "variable")}
        self.assertEqual(set(setting_commands), settings)
        for setting, key in (("CADENCE_REVIEWER", "cadence_app_slug"),
                             ("SYMPHONY_BOT_USER", "symphony_app_slug")):
            cmd = setting_commands[setting]
            self.assertEqual(cmd[cmd.index("--body") + 1],
                             answers[key].removesuffix("[bot]") + "[bot]")
        for cmd in setting_commands.values():
            if cmd[1] == "secret":
                self.assertNotIn("--body", cmd)
        for kind in ("secret", "variable"):
            org = next(cmd for cmd in commands if cmd[1] == kind and "--org" in cmd)
            self.assertEqual(org[org.index("--visibility") + 1], "selected")
            self.assertIn("--repos", org)
        probe = next(cmd for cmd in commands if cmd[1:3] == ["workflow", "run"])
        self.assertEqual(probe[3], "symphony-client-setup.yml")
        self.assertEqual(probe[probe.index("--ref") + 1], answers["default_branch"])

    def check_bot_identities(self, output, answers):
        self.check_ingress(output, answers)
        for role in ("symphony", "cadence"):
            slug = answers[f"{role}_app_slug"].removesuffix("[bot]")
            manifest = json.loads((output / f".github/symphony/{role}-app-manifest.json").read_text())
            self.assertEqual(manifest["name"], slug)
            self.assertIn(json.dumps(slug), (output / "SYMPHONY.md").read_text())
        for relative in GENERATED - {".copier-answers.yml"}:
            self.assertNotIn("[bot][bot]", (output / relative).read_text(), relative)

    def test_lifecycle_copy_with_editable_defaults_and_bot_logins(self):
        minimal = {key: value for key, value in self.answers().items() if key not in
                   {"default_branch", "linear_team_key", "symphony_app_slug", "cadence_app_slug"}}
        defaults = dict(minimal, default_branch="main", linear_team_key="100",
                        symphony_app_slug="1000lines-symphony[bot]",
                        cadence_app_slug="jeremycarroll-cadence[bot]")
        custom = dict(self.answers(1), symphony_app_slug="custom-author[bot]",
                      cadence_app_slug="custom-reviewer[bot]")
        for index, (data, expected) in enumerate(((minimal, defaults), (custom, custom))):
            with self.subTest(answers=expected):
                output = self.render(data, f"lifecycle-copy-{index}")
                self.check_lifecycle_messages(self.copy_messages, "copy", expected)
                self.assertNotIn("Before updating", self.copy_messages)
                self.check_bot_identities(output, expected)
                saved = yaml.safe_load((output / ".copier-answers.yml").read_text())
                self.assertEqual({key: saved[key] for key in expected}, expected)
                self.assertEqual(set(saved), set(expected) | {"_src_path", "_commit"})

    def test_lifecycle_update_from_prior_template_preserves_answers(self):
        paths = ["copier.yml", "template/SYMPHONY.md.jinja",
                 f"template/{INGRESS}.jinja",
                 "template/.github/symphony/cadence-app-manifest.json.jinja",
                 "template/.github/symphony/symphony-app-manifest.json.jinja"]
        current = {path: (self.source / path).read_text() for path in paths}
        # A self-contained previous revision, usable in shallow CI checkouts.
        old = yaml.safe_load(current["copier.yml"])
        for key in list(old):
            if key.startswith("_message_"):
                del old[key]
        for key in ("linear_team_key", "cadence_app_slug", "symphony_app_slug"):
            old[key].pop("default", None)
            old[key].pop("validator", None)
        (self.source / "copier.yml").write_text(yaml.safe_dump(old))
        for path in paths[1:]:
            (self.source / path).write_text(current[path].replace(".removesuffix('[bot]')", ""))
        self.git(self.source, "add", ".")
        self.git(self.source, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-m", "Prior lifecycle fixture")
        self.git(self.source, "branch", "-f", "alpha", "HEAD")
        answers = [dict(self.answers(1), cadence_app_slug="1000lines-cadence",
                        symphony_app_slug="1000lines-symphony"),
                   dict(self.answers(1), cadence_app_slug="custom-reviewer[bot]",
                        symphony_app_slug="custom-author[bot]")]
        clients = []
        for index, data in enumerate(answers):
            output = self.render(data, f"lifecycle-update-{index}")
            (output / "application.txt").write_text("Preserve the adopter's application\n")
            self.git(output, "init", "--initial-branch=main")
            self.git(output, "add", ".")
            self.git(output, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                     "-c", "commit.gpgsign=false", "commit", "-m", "Existing adopter")
            clients.append(output)
        for path, content in current.items():
            (self.source / path).write_text(content)
        self.git(self.source, "add", ".")
        self.git(self.source, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-m", "Add lifecycle guidance")
        self.git(self.source, "branch", "-f", "alpha", "HEAD")
        for output, expected in zip(clients, answers):
            with self.subTest(client=output.name):
                result = subprocess.run([sys.executable, "-m", "copier", "update", "--defaults",
                                         "--vcs-ref=alpha"], cwd=output, stdin=subprocess.DEVNULL,
                                        capture_output=True, text=True, timeout=30)
                text = result.stdout + result.stderr
                self.assertEqual(result.returncode, 0, text)
                self.check_lifecycle_messages(text, "update", expected)
                self.assertNotIn("Before copying", text)
                self.check_bot_identities(output, expected)
                saved = yaml.safe_load((output / ".copier-answers.yml").read_text())
                self.assertEqual({key: saved[key] for key in expected}, expected)
                self.assertEqual(set(saved), set(expected) | {"_src_path", "_commit"})
                self.assertEqual((output / "application.txt").read_text(),
                                 "Preserve the adopter's application\n")

    def test_real_tree_matrix(self):
        for index in range(2):
            answers = self.answers(index)
            with self.subTest(repo=answers["repo_slug"]):
                output = self.render(answers, f"output-{index}")
                files = file_set(output)
                self.assertEqual(files, GENERATED)
                # Exercise the actual Copier-installed renderer without live credentials.
                snapshot = self.root / "progress.json"
                snapshot.write_text(json.dumps({
                    "graph": {"direction": "LR", "nodes": [
                        {"id": "A", "label": "Done checkpoint; artifact pending"},
                        {"id": "B", "label": "Done checkpoint; proof pending"},
                        {"id": "C", "label": "Current work"}],
                        "edges": [{"from": "A", "to": "C"}, {"from": "B", "to": "C"}]},
                    "states": {"A": "Done", "B": "Done", "C": "Active"},
                    "prs": {}, "currentNode": "C", "snapshotTime": "2026-09-12T03:00:00Z",
                }))
                progress = subprocess.check_output(["node", str(output / "scripts/symphony/render-pr-progress.mjs"),
                                                    str(snapshot)], text=True, timeout=15)
                self.assertEqual(progress.count(":::completed"), 2)
                self.assertIn("style C stroke:#8250df,stroke-width:4px", progress)
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

    def test_repeat_onboarding_is_clean_and_keeps_credentials_out_of_answers(self):
        output = self.render(self.answers(), "repeat")
        (output / "application.txt").write_text("adopter-owned file\n")
        self.git(output, "init", "--initial-branch=main")
        self.git(output, "add", ".")
        self.git(output, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-m", "Adopt generated files")
        result = subprocess.run([sys.executable, "-m", "copier", "update", "--defaults", "--vcs-ref=alpha"],
                                cwd=output, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git(output, "status", "--porcelain"), "")
        self.assertEqual((output / "application.txt").read_text(), "adopter-owned file\n")
        saved = yaml.safe_load((output / ".copier-answers.yml").read_text())
        self.assertEqual(set(saved), set(self.answers()) | {"_src_path", "_commit"})
        workflow = yaml.safe_load((output / ".github/workflows/symphony-client-setup.yml").read_text())
        self.assertEqual(set(workflow[True]), {"workflow_dispatch"})
        repository_job = workflow["jobs"]["repository-settings"]
        protected_job = workflow["jobs"]["credentials"]
        self.assertNotIn("environment", repository_job)
        self.assertEqual(protected_job["environment"], "cadence-controller")
        self.assertEqual(protected_job["needs"], "repository-settings")
        settings = {"CADENCE_APP_PRIVATE_KEY", "CADENCE_LINEAR_API_TOKEN", "CADENCE_OPENAI_API_KEY",
                    "CADENCE_AI_REVIEW_ANTHROPIC_API_KEY"}
        for job in (repository_job, protected_job):
            check = next(step for step in job["steps"] if "CADENCE_OPENAI_API_KEY" in step.get("env", {}))
            self.assertEqual(set(check["env"]), settings)
            for key in settings:
                self.assertEqual(check["env"][key], "${{ secrets." + key + " }}")
            checkout = job["steps"][0]
            self.assertEqual(checkout["with"]["ref"], "${{ github.event.repository.default_branch }}")
            self.assertFalse(checkout["with"]["persist-credentials"])
        mint = next(step for step in protected_job["steps"] if step.get("id") == "app-token")["with"]
        for grant in ("metadata", "contents", "actions"):
            self.assertEqual(mint[f"permission-{grant}"], "read")
        for grant in ("pull-requests", "issues", "checks"):
            self.assertEqual(mint[f"permission-{grant}"], "write")
        self.assertNotIn("codex-action", str(workflow))
        self.assertNotIn("claude-code-action", str(workflow))

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
            self.assertEqual(ref, REVIEW_REF)
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
            "pull_request_target", "workflow_run", "check_run", "status", "push", "schedule",
        })
        self.assertEqual(wakeups[True]["push"], {"branches": [answers["default_branch"]]})
        self.assertEqual(wakeups[True]["schedule"], [{"cron": "7,22,37,52 * * * *"}])
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
            expression = "[[ (" + key + ".removesuffix('[bot]') ~ '[bot]') | replace(\"'\", \"''\") ]]"
            source = source.replace(expression, answers[key].removesuffix("[bot]") + "[bot]")
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
        caller = self.source / "template" / (WAKEUPS + ".jinja")
        caller.write_text(caller.read_text().replace(
            '  push:\n    branches: [[ [default_branch] | to_json ]]\n  schedule:\n    - cron: "7,22,37,52 * * * *"\n', ''))
        # A prior template revision with the removed distribution. Keep the
        # fixture self-contained so updates also run in shallow CI checkouts.
        added = ".github/workflows/symphony-client-setup.yml"
        (self.source / "template" / (added + ".jinja")).unlink()
        for relative in PR_FILES:
            (self.source / "template" / relative).unlink()
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
            ".symphony.cfg.json": '{"adopter": "config"}\n',
            ".github/workflows/ci.yml": "name: Adopter CI\n",
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
        fresh = self.render(self.answers(), "current-fresh")
        for output in clients:
            with self.subTest(client=output.name):
                # Copier 9.18.2 deletes removed template paths even when locally
                # modified. Exclude the reviewed adopter-owned file explicitly.
                options = ["--exclude", skill, "--exclude", ".symphony.cfg.json"] if output.name == "adopter" else []
                result = subprocess.run(
                    [sys.executable, "-m", "copier", "update", "--defaults",
                     "--vcs-ref=alpha", *options], cwd=output, stdin=subprocess.DEVNULL,
                    capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(file_set(output), GENERATED | (set(preserved) if output.name == "adopter" else set()))
                self.assertEqual((output / added).read_bytes(),
                                 (PACKAGE / "template" / (added + ".jinja")).read_bytes())
                for relative in GENERATED - {".copier-answers.yml"} - (set(preserved) if output.name == "adopter" else set()):
                    self.assertEqual((output / relative).read_bytes(), (fresh / relative).read_bytes(), relative)
                self.assertFalse((output / examples).exists())
                self.check_ci_callers(output, self.answers())
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
