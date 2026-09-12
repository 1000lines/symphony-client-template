# Repository activity log: jeremycarroll/venn-search-rs

Do not record credentials or other secrets in this file.

## Project

- Participant: Jeremy Carroll (jeremycarroll) — repository owner and participant; bring-your-own repo.
- Source repository: https://github.com/jeremycarroll/venn-search-rs
- Working repository: same (no fork)
- Setup path: HackCadence (`hackcadence` App 4921338, installation 161170747)
- Linear project: "Venn cleanup for the next stage"
  (`linear.app/1000lines/project/venn-cleanup-for-the-next-stage-75b1ed33f42c`), first
  ticket 100-110 "Create requirements and design doc". Both links are taken from PR #17's
  body, not read from Linear: the Linear connector available while writing this log is
  scoped to the `orchestrabio` workspace, where team key `100` resolves to nothing. The
  project lives in the `1000lines` workspace. Ticket contents are therefore unread here.
- Mermaid plan / PR: none yet. No `.mmd` exists on any branch. PR #17 states the fan-out
  plan follows human acceptance of the requirements/design seed.
- Project or problem: onboard, then commission a cleanup project over the existing
  Phase 7 codebase to make it safer and easier to extend.
- Intended outcome: Symphony and Cadence installed alongside the existing Rust CI with the
  setup probe green, then a Symphony-authored requirements-and-design document reviewed
  and merged.

### What this codebase is

Rust port (of the author's C program in `c-reference/`) of the search for monotone simple
6-Venn diagrams drawable with six triangles, per Carroll (2000). Non-deterministic
backtracking with a trail-based state system (O(1) restore), composed as predicates over
three phases: 5-face degree signature, 64 facial cycles, then an edge-to-corner mapping
where no two lines cross twice; constraint propagation and canonicality filtering under
D6; GraphML output. ~10.8k lines in 42 `src/*.rs`. Phase 7 complete: all 233 N=6 solutions
in ~3.5s, N=3/4/5/6 tests passing. PRs #1–#13 (Oct 2025) are that phase-by-phase
build-out, #7 "Monotonicity Constraints and Cycle Lookup Tables" through #13.

## Activity

### Fri 11 Sep, 13:29 PDT — First onboarding attempt (PR #15), later abandoned

- PR #15 "Onboard with the Symphony client template", branch `chore/symphony-onboarding`,
  from template `58021a7`. 24 files, +2834/-2. CI failed twice (13:29, 13:36 PDT) then
  passed at 13:53 PDT. Closed **without merging** at 21:29 PDT; its body notes the
  template's full Cadence review caller was "deferred" in that attempt. Branch `copier`
  started instead at 22:12 PDT (137c92d).
- TBC — Jeremy: why was #15 abandoned rather than merged — template revision, the
  deferred Cadence caller, or something else?

### Sat 12 Sep, 12:26–12:32 PDT — PR #16, the onboarding that landed

- 12:26 — 2697cd3 updates Copier to template main `7c99f9e`; 12:27:10 — PR #16 "Onboard
  Symphony with existing Rust CI and HackCadence" opened, 38 files, +3140/-2.
- **CI reconciliation.** Existing `.github/workflows/ci.yml` preserved; the generated
  Symphony build/test workflow was deleted as redundant. `.symphony.cfg.json` sets
  `ci.mode: remote` and registers the six real checks by name with GitHub Actions App
  provenance `appId: 15368`: Test Suite (NCOLORS=3/4/5/6), Clippy (Linting), Format
  Check; wakeups fire on completion of `CI`. Copier answers: build/test
  `cargo build --release` / `cargo test --release`, reviewer `codex`. Copier also wrote
  lowercase App slugs, corrected to `hackcadence[bot]` and `1000lines-symphony[bot]`.
- **Two red CI runs before green.** Runs at 12:27 and 12:28 failed on pre-existing Clippy
  `useless_borrows_in_formatting` in the library and the shared test helper — not caused by
  Copier but surfaced by it, current Clippy being stricter than when the code was written.
  Fixed in 4de1f89 (12:28) and 13f73ca (12:30); all six checks green on 13f73ca at 12:30
  (run 34714345757). No local Rust toolchain; GitHub runners did all validation.
- 12:32:21 — merged by jeremycarroll, squashed to 2af35ba on main.

### Sat 12 Sep, 12:32–12:34 PDT — Post-merge automation

- **Setup probe passed.** `Symphony Client Setup` dispatched on main at 12:32:35
  (run 34714470796): both "Check repository-visible settings" and "Verify job-visible
  credentials" succeeded. `Symphony Client Wakeups` succeeded on push and at 12:33:40.
- **Defect — Linear reconciliation failed on merge.** `Cadence AI Review Trigger` on the
  closed PR (run 34714461575) finished `failure`: job "review / Reconcile Linear after PR
  close", step "Reconcile current PR associations". This is the merge-to-Done path named
  as a known defect in the hackathon README, and it bit here. No ticket needed moving
  manually: PR #16 carries no `100-NNN` identifier, so nothing was linked. Job logs need
  authentication (public API returns 403), so the root cause is unread.
  TBC — Jeremy: what does the "Reconcile current PR associations" step log say — is it the
  unlinked-PR case failing loudly, or a genuine Linear API/permission failure?
- **Defect — unexpanded expressions in job names.** Check runs in that workflow appear
  literally as `review / Accept PR #${{ (inputs.pr_number || github.event.pull_request.number) }}`
  and `review / Publish Cadence result for PR #${{ ... }}`: the generated job names leave
  the expression unevaluated in the checks UI. Cosmetic, but template-wide.
- **Cadence never reviewed the setup PR.** "Review PR #16", "Accept" and "Publish Cadence
  result" were all `skipped`; PR #16 has zero comments and zero reviews. It was open five
  minutes and merged by its author. Live Cadence review, the review check and the Linear
  handoff therefore remain unverified here — as the PR body itself predicted.

### Sat 12 Sep, 13:57–14:17 PDT — Symphony's first real ticket: PR #17 (100-110)

- 13:57:23 — **PR #17 "[100-110]: Define Venn cleanup requirements and design"** opened by
  `1000lines-symphony[bot]` from branch `symphony/venn-cleanup/100-110/requirements-and-design`.
  Labels `symphony`, `red`, `cadence-loop-1`; assigned to jeremycarroll.
- Content: one new file, `docs/symphony-plans/venn-cleanup/requirements-and-design.md`,
  +631 lines, no code. It reconciles the old `docs/CLEANUP.md` list (92 historical items
  and subitems) against current main and the unmerged PR #14, evaluates twelve candidate
  work units, proposes an owned indexed undo log to replace independently mutable
  state/trail APIs, and records deferrals (LP, CLI, parallelism).
- **Material open question raised by Symphony (its "O1").** Main's active N=4/N=5 tests
  assert **16/17** solutions, and main CI passes them, while the commissioning brief says
  **3/23**. Symphony did not claim to have observed 3/23; it preserved executable behaviour
  and flagged the discrepancy for Jeremy. This is the one substantive content finding of
  the day.
- All six required CI checks green on head 4216c45 at 13:57–13:58 (run 34718573718).
- **Cadence review did not complete.** `hackcadence[bot]` posted a "Cadence · Reviewing —
  Review in progress" status comment at 13:58 and never posted a result; the `Cadence
  review` check run ended `cancelled` at 14:16. Jeremy approved at 14:14:44 and merged at
  14:15:45, which cancelled the in-flight review. So on the day's only Symphony PR, the
  human out-ran the review agent and no Cadence verdict exists — twice now (PR #16, #17)
  Cadence has produced no review in this repository.
- **Linear reconciliation succeeded this time.** "review / Reconcile Linear after PR close"
  passed at 14:16 on PR #17 — the PR carried a `100-110` identifier. Contrast PR #16,
  where the same job failed with no ticket linked.
- **Defect — label helper 403.** PR #17's body reports that the shared `ensure-pr-labels.mjs`
  helper is scoped to `pull_requests: read` + `issues: write` and received HTTP 403 when
  labelling this PR; the same App's configured credentials succeeded through the narrow
  REST label endpoint as a fallback. Symphony raised it as an advisory process change; no
  shared-tooling fix is included.
- **Defect — post-merge Cadence workflows failing.** `Cadence AI Review Events` finished
  `failure` three times and `Cadence Review Handoff` once between 14:14 and 14:15 on main.
  Root causes unread (job logs need authentication; the public API returns 403).
  TBC — Jeremy: what are `Cadence AI Review Events` and `Cadence Review Handoff` failing on
  after merge?
- Merge commit 8c3df8b on main at 14:15. `Symphony Client Wakeups` succeeded at 14:17.

### Symphony dashboard state (not readable from Linear here)

Read from the Symphony Observability dashboard at symphony.1000lines.dev at 21:23Z
(14:23 PDT); ticket identities below are as the dashboard labels them, not read from
Linear, and none of them appear in this repository's branches, commits or PR titles.

- 100-112 "Trigger fan out" — Active, gated by 100-111 (Active, labels red / improvement).
  Numbering places these in the same venn-cleanup sequence as the merged 100-110, so
  these two are very probably this repository's plan and fan-out tickets.
- 100-96 "Repeat the full Rust workload after rehearsal" — Active, green, gated by 100-94
  (Active, green), reason "not terminal; missing maturity label". 100-97 "Audit acceptance
  cleanup and human handoff" — Active, gated by 100-96 and 100-95.
- The 100-9x link to venn-search-rs is **inferred** only from "Rust" and the fact that this
  is the only Rust repository in play today. Nothing in this repository references 100-94,
  100-95, 100-96 or 100-97 — no branch, no commit message, no PR title, no file.
  TBC — Jeremy: what does "the full Rust workload" (100-96) actually cover, is it
  venn-search-rs, and has the rehearsal it refers to happened?

### Other branches and PRs — all pre-existing, not today's work

- `origin/cleanup1` — tip c3b2534, **30 Oct 2025**. Head of open **PR #14 "Cleanup1"**,
  opened 2025-10-30 and still open nearly a year later. Pre-existing; untouched today. It
  is the Phase 7 cleanup pass (debug-output removal, symmetry reorg, `EdgeDynamic` ->
  `DynamicEdge`) tracked in `docs/CLEANUP.md`. PR #17's document treats it as still-useful
  unmerged work to reconcile, so #14 is now an input to the cleanup project, not dead.
- `origin/docs1` — tip 68f474f, **30 Oct 2025**. Leftover branch from merged PR #13.
- `origin/copier` and `symphony/venn-cleanup/100-110/requirements-and-design` are today's
  PR #16 and #17 head branches, both left behind after merge.

## End-of-day result

- What was completed: Symphony/Cadence template installed and merged to main (PR #16);
  existing Rust CI preserved and reconciled with Symphony's remote check validation; two
  pre-existing Clippy failures fixed; `Symphony Client Setup` probe green on main; a
  cleanup project commissioned in Linear and its first ticket (100-110) delivered,
  reviewed by the human, approved and merged as PR #17.
- What landed in the repository itself: two commits on main today — the onboarding squash
  (2af35ba) and one 631-line design document (8c3df8b). **No production Rust changed.**
  The run reached the end of the requirements step, not implementation; the Mermaid plan
  and fan-out are still ahead, and the dashboard shows their tickets Active.
- Defects found: (1) merged-PR Linear reconciliation job failed on PR #16 (passed on #17,
  which had a linked ticket); (2) unexpanded `${{ ... }}` GitHub expressions in generated
  Cadence job names; (3) Copier emitted lowercase App slugs needing manual correction;
  (4) Copier's generated build/test workflow duplicates an existing CI and had to be
  deleted by hand; (5) `ensure-pr-labels.mjs` 403 on PR labelling, worked around by
  Symphony; (6) `Cadence AI Review Events` and `Cadence Review Handoff` failing on main
  after merge; (7) no Cadence review verdict was produced on either of today's PRs — on
  #16 the jobs were skipped, on #17 the in-flight review was cancelled by the human's
  merge.
- Where to retrieve the work: main at 8c3df8b; PRs
  https://github.com/jeremycarroll/venn-search-rs/pull/16 and /pull/17; the design document
  at `docs/symphony-plans/venn-cleanup/requirements-and-design.md`; an onboarding-time log
  also lives in-repo at `hackathon/jeremycarroll--venn-search-rs.md`.
- Follow-up: answer Symphony's O1 (16/17 vs 3/23 solution counts) before any count-changing
  work; accept the design doc so 100-111/100-112 can produce the Mermaid plan and fan out;
  give Cadence time to finish a review on the next PR; fold PR #14 into the plan.
- TBC — Jeremy: is the 16/17 vs 3/23 discrepancy a stale brief, or a real regression in the
  N=4/N=5 tests on main?
