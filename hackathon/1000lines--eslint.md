# Repository activity log: 1000lines/eslint

Do not record credentials or other secrets in this file.

Written at 13:57 PDT on Saturday 12 September 2026, while the work is starting.
Entries below 14:00 are observed; everything marked **Planned** has not happened yet.

## Project

- Participant: Jeremy Carroll (`jeremycarroll`, human lead)
- Source repository: `eslint/eslint`, MIT, roughly 450k LOC
- Working repository: `1000lines/eslint` (exists; default branch `main`, protected)
- Setup path: fork (`1000lines` organisation supplies App installation, secrets and variables)
- Linear project: TBC — Jeremy. No project or ticket for this work is visible from the
  Linear connection available here, which reaches workspace `orchestrabio` (teams
  `Symphony`/ABC and `Orchestra`). Team key `100` is not in that workspace. Which Linear
  workspace holds team 100, and has the project been created there yet?
- Mermaid plan / PR: not yet — the plan is produced by the planning ticket, which has not started
- Project or problem: see `eslint-project-description.md` (project code `eslint-ts-rules`).
  Advance upstream eslint/eslint#19173 inside the fork: per-core-rule TypeScript syntax
  awareness, one pull request per rule, after a reviewed rule inventory.
- Intended outcome: a reviewed inventory, then as many independent per-rule lanes as human
  review capacity allows, ending in a clean state before credentials are revoked at 16:00.

### Upstream facts, verified today

- #19173 "Change Request: Make rules TypeScript syntax-aware": **open**, labels `enhancement`,
  `core`, `accepted`, assigned to `fasttime`. Task list: 18 entries, 16 ticked, 2 open.
- Reference lane #19557 `feat: support TS syntax in \`max-params\``: opened 2025-03-22 by
  `snitin315`, merged 2025-05-06 by `mdjermanovic`, branch `ts/max-parens`, 4 files, +260/-7,
  labels `rule`, `accepted`, `feature`. Matches the brief exactly.
- Unavailable lanes confirmed open: #19563 `no-redeclare` (snitin315, 2025-03-22, +1255/-3,
  blocked) and #19812 `no-unused-vars` (Tanujkanti4441, 2025-06-02, +4746/-26, dirty).

## Activity

### 13:26 — Setup pull request opened

- First ticket: not created. No Linear project exists for this work yet (see above).
- Symphony activity: none yet. Setup is being done by hand by the human lead.
- Pull requests: [1000lines/eslint#1](https://github.com/1000lines/eslint/pull/1)
  `chore: add Symphony Copier configuration`, branch `chore/combine-copier-gitattributes`
  into `main`, open, 35 files added by Copier.
- Copier files present on the branch: `.copier-answers.yml` (`_commit: 7c99f9e`),
  `.symphony.cfg.json`, `SYMPHONY.md`, `.agents/skills/` (cadence-onboarding, linear-graphql,
  symphony-project-factory), `.github/symphony/`, seven Symphony/Cadence workflows including
  `symphony-client-setup.yml`, and `scripts/symphony/`. None of it is on `main` yet.
- Copier answers of record: `repo_slug: 1000lines/eslint`, `default_branch: main`,
  `linear_team_key: "100"`, `symphony_app_slug: 1000lines-symphony[bot]`,
  `cadence_app_slug: 1000lines-cadence`, `cadence_reviewer: codex`,
  build `npm install --no-package-lock`, test `node Makefile.js mocha`.
  The fork path uses the organisation's own Cadence App, not the shared event identity.
- Decisions: fork path rather than bring-your-own, so no App installation or Actions
  settings are configured by hand on this repository.
- Blockers or surprises: the Copier `.gitattributes` had to be combined with eslint's
  existing one; the branch name records it.

### 13:28–13:48 — CI integration onto the setup PR

- Three follow-up commits by the human lead, all on the setup branch:
  - 13:28 `fix: use npm install in Symphony CI` — eslint's install needed
    `npm install --no-package-lock`, not the generated default.
  - 13:36 `fix: make workflow trigger mappings explicit`.
  - 13:48 `style: format Symphony configuration` — eslint runs Prettier over the repository,
    including the generated JSON, so the Copier output did not pass `Verify Files` as emitted.
- This is the template's known weak point, as the event README predicts: Copier cannot infer
  an existing CI layout. Intervention here was human, not agent, and took about 22 minutes.

### 13:49–13:53 — Full upstream CI green on the setup PR

- 39 check runs on head `1939f95`, all `success`: `Verify Files` (2m06s), six
  `Test (ubuntu-latest, ...)` legs plus windows and macOS, `Browser Test`, `Test Types`,
  `Test Package Managers`, `Test pnpm Type Support`, `Test Ecosystem Plugin
  (@typescript-eslint/typescript-eslint)`, CodeQL, and `commands / Client Commands`.
- The whole matrix completes in roughly four minutes of wall clock on the fork's runners.
  That is materially cheaper than the brief assumed when it argued for narrowing.
- No Cadence review has been posted on PR #1, and no review of any kind is recorded.

### Not yet started — Planned

- **Merge the setup PR.** Generated files must reach `main` before anything else runs.
- **Run the `Symphony Client Setup` probe** on `main` and confirm both
  `Check repository-visible settings` and `Verify job-visible credentials` pass.
  TBC — Jeremy: has this probe been run yet? It is not visible from here, and the available
  GitHub tooling cannot list workflow-dispatch runs.
- **Narrow the required checks.** `.symphony.cfg.json` currently carries
  `"ci": { "requiredChecks": [] }` — the narrowing to `Verify Files` plus one ubuntu
  `test_on_node` leg described in the brief is **not yet written**. The concrete ubuntu leg
  names on this repository are `Test (ubuntu-latest, <version>)`.
  TBC — Jeremy: which ubuntu leg is the gating one, and does an empty `requiredChecks` mean
  "none gate" or "fall back to all"?
- **Create the Linear project** with `.agents/skills/symphony-project-factory/SKILL.md`,
  then move the first ticket to Active.
- **Planning ticket: derive the rule inventory** from `lib/rules/`, published as the Mermaid
  dependency graph for human review before fan-out.
- **Fan out per-rule lanes**, branch `ts/<rule-name>`, one rule plus its test, documentation
  and rule types per PR, `Refs` (not `Fixes`) #19173 in the body.
- **CI widening node**, dependent on the first wave of merged lanes; **replan checkpoint**
  after that wave reaches human review. TBC — Jeremy: confirm a first wave of six lanes?

## Defects and interventions

1. **Copier output does not satisfy the host repository's own formatter.** eslint Prettier-checks
   all JSON; the generated `.symphony.cfg.json` needed reformatting before `Verify Files` passed.
   Template defect, reproducible, cost one commit.
2. **Copier build command wrong for this repository.** `npm install` alone is not what eslint
   needs; `--no-package-lock` had to be added by hand. Expected per the README, recorded anyway.
3. **Whole-suite test command.** `node Makefile.js mocha` runs the entire eslint suite, minutes
   per agent iteration, for a change touching one rule file. Accepted knowingly for today
   rather than worked around, against the template's assumption that the repository test
   command is a reasonable per-iteration inner loop.
4. **Required-check narrowing not yet in the config**, despite being a stated project decision.
   Tracked as a planned step above rather than as a completed one.
5. **Linear project not discoverable** from the workspace this session can reach. Whether that
   is a permissions boundary or simply work not yet done is unresolved.

## End-of-day result

- What was completed: TBC — Jeremy
- What remains: TBC — Jeremy
- Where to retrieve the work: TBC — Jeremy
- Follow-up: TBC — Jeremy

Hard stop: automation credentials and write access to the fork are removed at 16:00 local;
the fork stays world-readable afterwards.
