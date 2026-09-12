# Repository activity log: jeremycarroll/pytest-memray

Do not record credentials or other secrets in this file.

## Project

- Participant: Jeremy Carroll (jeremycarroll)
- Source repository: https://github.com/bloomberg/pytest-memray
- Working repository: https://github.com/jeremycarroll/pytest-memray
- Setup path: HackCadence (bring-your-own, repository kept under `jeremycarroll`)
- Linear project: "Full-fidelity Memray captures", https://linear.app/1000lines/project/full-fidelity-memray-captures-b6e86c398fab (tickets 100-101…100-108, 100-113, 100-114)
- Mermaid plan / PR: `docs/symphony-plans/fan-out-plan-100-102-full-captures.mmd`, proposed in PR #3, replanned in PR #8
- Project or problem: upstream [bloomberg/pytest-memray#160](https://github.com/bloomberg/pytest-memray/issues/160) — captures are aggregated, so `memray stats` and allocation-level reporters cannot run against them
- Intended outcome: opt-in `--memray-full` / `memray_full` retaining full captures, aggregated default unchanged, delivered upstream as a clean PR

## Activity

Times are America/Los_Angeles (UTC-7).

### 07:58 — Onboarding, PR #1 (merged 08:10)

- Symphony activity: none yet; human-run Copier install, three commits.
- `7f83eaa` 07:58: raw Copier output, 36 files / 3066 insertions, no existing file touched.
- `d708407` 08:07: **the CI reconciliation, and the only interesting part of onboarding.** Copier left `build_command: 'true'`, a `test_command` mangled by YAML block-scalar quoting into a leading/trailing-newline string, and `"ci": {"requiredChecks": []}`. The fix deleted the generated `symphony-client-ci.yml` rather than running a parallel lane, set real commands (`pipx run build[virtualenv] --sdist --wheel`, `docker compose run --rm test tox` — note `docker-compose` → `docker compose`), and hand-enumerated the repository's 13 real checks by name, workflow and app id (`Source and wheel distributions` from `build_dist.yml`; `check docs`, `lint`, `test py38`…`test py315` from `build.yml`).
- `2fb5c3b` 08:09: removed `Run zizmor 🌈` from `requiredChecks` and switched `zizmor.yml` from `push`/`pull_request` to `workflow_dispatch`. TBC — Jeremy: did zizmor fail on the Copier-generated workflows, or was this pre-emptive?
- Blockers or surprises: Copier's YAML quoting corrupts the test command, and the generated required-checks list is empty by construction — every bring-your-own repo has to write it by hand.

### 08:47 — Project start, PRs #2–#7 (all merged by 12:06)

- First ticket: 100-101, Active. Nine bot-authored PRs followed; Cadence (`hackcadence[bot]`, Codex provider) reviewed each head; Jeremy approved and merged every one himself.
- #2 requirements/design 08:47→09:23 · #3 plan 10:20→10:29 · #4 fan-out 10:37→10:41 · #5 docs 10:40→11:42 · #6 implementation 10:44→11:06 · #7 combined validation 11:14→12:06.
- Implementation evidence (#6): 397 additions across 3 files; 162 targeted tests pass on Memray 1.20.0 and 1.19.1, `make check` 198 passed, 12 object-tracking tests via a Docker fallback on Python 3.13.15, real `memray stats` output on a live capture.

### 11:58 — Replan, PR #7 review → PR #8 (merged 12:54)

- Jeremy on #7: "the upstream repo wants a pull request of a particular form, so we need a branch with the change, without our working … maybe we need a further ticket". Cadence had approved at 11:53, re-reviewed as Blocked at 12:01 to carry the direction into the plan; Jeremy approved and merged at 12:06.
- PR #8 appended FC-D (100-113, clean upstream-based branch) and FC-E (100-114, DCO, upstream PR, news rename) as `C → D → E`.
- What the graph records: four `.mmd` versions (`d403161`, `6e83a69`, `4ad23af`, `e3401eb`), only one structural — 3 nodes / 2 edges to 5 nodes / 4 edges, a linear tail appended. No edge reversed, no dependency discovered, nothing re-ordered.
- Jeremy's assessment (his, not this log's): memray "had a trivial plan, followed by a trivial replan — it sort of illustrates the point but" is unsatisfying as a demonstration, because the problem was trivially decomposable: one defect, one fix. The artifacts support him. A→C and B→C were obvious; the replan was a delivery change a human asked for, not something execution taught the team. Contrast the template's own `100-67` plan, which reversed `D → G` and split `C` after implementation changed what was understood.

### 13:07 — Delivery, PRs #9–#11 (in flight)

- #9 applied the fan-out (merged 13:40). #10 (100-113) published the six-file product-only artifact `9cb7f48` on upstream `92a9c85`; Cadence approved at 13:12.
- Jeremy rejected it at 13:45: "The branch prepared is in the wrong direction … No one wants to read your long list … We are delivering the code." Cadence blocked at 13:48, Symphony rewrote the upstream body to match merged Bloomberg PRs #107 and #185, Cadence approved the new head at 13:54. **#10 is open, awaiting Jeremy.**
- #11 (100-114) opened 13:55 as a draft. The runtime App's upstream bind returned HTTP 404, so DCO certification and the actual submission must come from Jeremy's own account.

## Defects and friction

- **Label helper HTTP 403** (#2, #5, #8 — three runs). Shared `ensure-pr-labels.mjs` fails with its narrowed `pull_requests: read` / `issues: write` token; the same App's worker credential then applies the labels through the REST endpoint. Permission-selection bug in the helper.
- **Cadence review cleanup** (#2). Publication job [34703990527](https://github.com/jeremycarroll/pytest-memray/actions/runs/34703990527) failed with "Cadence review changed before hiding; leaving the original review visible". Approval, ready state and review request were all correct; the workflow still reports failure.
- **Runtime bundle missing compiled DAG modules** (#6). The hosted `SYMPHONY_TOOLING_ROOT` checkout lacked modules the required PR-progress helper needs; the run built an isolated checkout of the same revision to proceed.
- **Shared DAG renderer drops node content** (#3, #4). It emits metadata and links but not inline scope, file lists, acceptance checks or validation commands, so fan-out transcribed them by hand into ticket bodies.
- **Progress fetcher requires a current node** (#8, #9). Planning and fan-out seeds sit outside the implementation graph; the renderer tolerates no current node, the fetcher does not.
- **Actions grant is read-only** (#8). Push Run [34713703824](https://github.com/jeremycarroll/pytest-memray/actions/runs/34713703824) failed when `docs.python.org/3/objects.inv` reset the connection; the App's rerun attempt returned `Resource not accessible by integration`. TBC — Jeremy: was that run ever rerun green?
- **No host browser** (#5, #9). Mermaid render verification needed a pinned Playwright container.
- **Dependency-wait churn** (#5). Before FC-A merged, the Active dependency-wait contract repeatedly resumed 100-105 although its independent work was complete and its soft prerequisite unchanged.
- **Local branch `fix/linear-team-key`**: local clone only, created from `HEAD` at 08:10 (the PR #1 merge), zero commits, identical to `main`, never pushed, never a PR. The Copier answer `linear_team_key: '100'` matches the template default and README. TBC — Jeremy: what was this branch for, and was the problem it was named for fixed another way?

## Known-defect check: Linear "PR merged → Done"

- Ten PRs merged today with `100-NNN` in title and branch. Symphony's progress graphs later render 100-104/105/106 as **Done**, so ticket state was moving by some route.
- Not verifiable from here: this session's Linear connection is scoped to the `orchestrabio` workspace (teams `ABC`, `ORC`), while the project and tickets live in `1000lines`; `100` resolves to no team over this connection. Worth noting on its own — the participant-facing team key `100` is unreachable from a default Linear MCP connection.
- TBC — Jeremy: did any merged PR here fail to move its ticket to Done, and did you move any manually?
- TBC — Jeremy: the template README gained its "Known defect" note at 11:07 today, mid-run — was it this repository that triggered it?

## End-of-day result

- What was completed: Symphony/Cadence installed and CI-reconciled on a bring-your-own repository; requirements, plan, fan-out, implementation, documentation and combined validation merged to `main` (PRs #1–#9); the feature is implemented and tested against two Memray versions; a clean six-file upstream artifact exists at `9cb7f48`.
- What remains: #10 awaits acceptance and merge; #11 is draft and needs Jeremy's DCO certification and the actual submission to `bloomberg/pytest-memray`; `docs/news/160.feature.rst` still carries the issue number and must be renamed to the observed upstream PR number.
- Where to retrieve the work: `jeremycarroll/pytest-memray` `main`; artifact commit `9cb7f4814daf9a50dec0101b2fc592c7ea2a0346`; plans under `docs/symphony-plans/`.
- Follow-up: the label-helper 403 and the Cadence cleanup failure are shared-template defects that reproduced on every run here; both deserve tickets in the template repository.
