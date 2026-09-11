# Symphony client template enhancements: requirements and design

```yaml
project-code: template-enhancements
project-color: cyan
repository: 1000lines/symphony-client-template
workflow-repository: 1000lines/symphony-client-workflows
base-branch: main
human-lead: Jeremy Carroll
design-issue: 100-66
plan-issue: 100-67
fan-out-issue: 100-68
```

Proposed for human review, September 11, 2026; canonical input to
[100-67](https://linear.app/1000lines/issue/100-67) after acceptance and merge.
Requirement IDs are outcomes, not tickets or a DAG. The three Active seeds have
verified blockers 100-66 → 100-67 → 100-68; each successor waits for predecessor
Done. No planning-seed `mature` before human review/merge; no execution authorized here.

## Goal and boundaries

Make the public client template easier to adopt, review and maintain by delivering
the reconciled backlog and [September 11 project brief][brief]. Demonstrate useful
increments through this repository's own Copier-managed root client. The template
owns generated assets and guidance; reusable behavior belongs in the workflow
repository, with thin native callers in clients. `symphony-example` is historical
evidence and an existing adoption target, not the implementation source for new work.

Exclude unrelated application backlog, shared-host reconstruction, dormant
controller revival, new orchestration/planning infrastructure, evidence archives,
and wholesale recommissioning of canceled work. Preserve existing ticket ownership,
human merge authority and operational proof obligations. No cleanup, project
cancellation, implementation tickets, workflow edits or fan-out occur in 100-66.

## Source reads and reconciliation

Snapshot: September 11, 2026, 21:41 UTC. Read live issue/project content, the complete
64-issue team 100 listing, and candidate/overlap descriptions, comments and relations.
Exactly four were Backlog. No required source is unavailable: the brief reproduces
the laptop notes in full. Recheck scope and acceptance before planning.

| Input                            | Evidence read                                                                                                                                                | Consequence                                                                                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Current brief and original notes | [Project content][brief], [100-66](https://linear.app/1000lines/issue/100-66)                                                                                | All five note groups and later factory/GraphQL request are covered below.                                                                       |
| Template baseline                | [main at 58021a7][template-base]: README, SYMPHONY, SELF-ADOPTION, REVIEW, provenance, questions/answers, factory/GraphQL resources, config, workflows/tests | Published subset has CI/wakeups/ingress; root answers consume `01ccd00`. No generated PR template or review caller.                             |
| Workflow baseline                | [main at 77cfb2d][workflow-base]: exported workflows, native review/handoff/check/workpad helpers, CI and workflow guidance                                  | Current native handoff parses prose; Human input needed takes a human-review-only branch. Existing check cleanup is not project-folder cleanup. |
| Historical planning              | [Design][old-design] D1–D9 and [accepted fan-out decisions][old-plan], including alpha/self-use amendments                                                   | Retain ownership and evidence boundaries; newer brief/100-62/64 override old provider choice, seed-only development and update exclusions.      |
| Historical human feedback        | [Example #6][e6], [#11][e11], [#16][e16], [#32][e32], [#36][e36], [#40][e40], [#48][e48], [#49][e49]: PR bodies, reviews, comments and threads               | All merged. Preserve concise colleague-facing reviews, verified human authority, minimum diagram size and recorded live-proof limits.           |

“Delivered” denotes the stated source artifact, separately from publication,
installation and live execution. “Underway” denotes open work, not acceptance;
“still needed” denotes a gap; exclusion does not authorize ticket closure.

| Candidate / owner                                                                                                 | Observed disposition                                                                                             | Required planning treatment                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [100-44](https://linear.app/1000lines/issue/100-44), Backlog                                                      | Still needed: optional model/effort and real timings; baseline verifier has a single-model allowlist             | Reuse this owner for R3. Preserve intentional fast/low-effort default and key-driven selection; no mandatory Copier question.                                                                                   |
| [100-60](https://linear.app/1000lines/issue/100-60), Backlog                                                      | Still needed: [#48's COMMENTED Human input needed review][e48] did not wake 100-53; Jeremy recovered it manually | Reuse for R2 routing. Trace the actual delivery, fix template/shared source and prove Copier propagation. Preserve explicit Copier-readiness hold.                                                              |
| [100-61](https://linear.app/1000lines/issue/100-61), Backlog                                                      | Still needed: [#49][e49] renders Done tickets 100-49/53 grey because checkpoint labels mention pending artifacts | Reuse for R4 and generated PR guidance. Preserve explicit Copier-readiness hold; known Done state wins over label prose.                                                                                        |
| [100-65](https://linear.app/1000lines/issue/100-65), Backlog in Misc                                              | Still needed: client/provider ingress filename collision on workflow-repository adoption                         | Reuse for R9; preserve Misc/Backlog until explicit human direction to move/activate.                                                                                                                            |
| [100-57](https://linear.app/1000lines/issue/100-57), Inactive                                                     | Underway: [template #1][t1], draft at `544d439`; Jeremy approved, still unmerged                                 | Existing owner of alpha caller/root migration and real root review/check/ready/cancellation proof. Do not duplicate or call approval a release.                                                                 |
| [100-62](https://linear.app/1000lines/issue/100-62), Inactive                                                     | Underway: [template #4][t4], draft at `ef04515`, guided setup/probes                                             | Owns provisioning/readiness, not provider implementation. Jeremy's 21:37 UTC comment reports org secrets/variable added: verify effective delivery, not historical empty inventories.                           |
| [100-63](https://linear.app/1000lines/issue/100-63), Inactive                                                     | Underway: [template #2][t2], draft at `e702cc6`, bundled Karpathy removal and Copier propagation                 | Consume removal; no replacement skill or personal/global removal. Preserve adopter modifications, including selective exclusions for deleted template files.                                                    |
| [100-64](https://linear.app/1000lines/issue/100-64), Inactive                                                     | Underway: [template #3][t3] at `fcecd50`, [workflow #1][w1] at `ac15fc1`, both draft                             | Owns provider execution, named secret forwarding and review/event/manual/handoff/check-cleanup callers. Reuse interfaces; R1 adds missing structured coordinator boundary, not another provider implementation. |
| [100-58](https://linear.app/1000lines/issue/100-58) / [100-59](https://linear.app/1000lines/issue/100-59), Active | Existing example-adoption and consumer-census/retirement obligations; no attached PR                             | Preserve live native/Docker/remote, failure/recovery, onboarding and both-consumer evidence. New periodic root checkpoints supplement these owners; R5 does not retire their code.                              |

| Original note                                                           | Reconciled disposition / requirement                                                                                                                                                                                            |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1: coordinator, pluggable reviewer, one comment, approval readies draft | Historical isolation/comment code in #11 is delivered reference; current native path still couples reviewer publication. R1/R2 remain needed. Draft-readiness helper from #40 is delivered source, with live proof outstanding. |
| 1: PR template and linked, colored, current-node DAG                    | #16 guidance and #32 minimum size are delivered in example; template coverage and deterministic generation remain R4/100-61.                                                                                                    |
| 1: fix noise before build day                                           | Prefer small useful increments with R7 behavior evidence; timing rationale does not waive review or create a new deadline/feature.                                                                                              |
| 2: contract first; reviewer location/payment; same PR/two providers     | R1 defines structured output. R3 retains accepted native Actions, adopter-supplied keys and 100-64 selection; the earlier “hosted probably cleaner” suggestion is superseded, not an open architecture decision.                |
| 3: clean/stale project-folder cleanup                                   | Still needed, R5 in full. Weekly/manual, default 60 days, dry-run, forced stale closure, deletion PR and retained history are inseparable requirements.                                                                         |
| 4: plan bloat and waiting for #11                                       | #11 merged, so that wait is satisfied. #6/#11 human feedback informs R6. #36 diff-collapse rules are already delivered in template; preserve them.                                                                              |
| 5: line limits and 40% less text                                        | R6 sets proportionate budgets without deleting requirements/decisions/acceptance. 100-63 removal is existing work.                                                                                                              |

## Locked decisions and design contracts

The source mandates and concrete engineering defaults below are proposed for acceptance.

### R1 — Structured reviewer, deterministic coordinator

Cadence acquires trusted context, invokes the provider, validates JSON, persists
findings and performs publication/transitions using native Actions and the existing
ledger. Reuse 100-64's provider adapters; give assessment only read access and no
GitHub/Linear mutation credentials or write-capable tools. The reviewer returns
data; the trusted coordinator owns writes. No prose parser drives new verdicts.

The small provider result has the following required shape. It is an adapter
input to existing `cadence-review/v1` acceptance and `cadence-workpad/v1alpha1`
storage, not a replacement controller schema or a second finding history.

| Field                                            | Contract                                                                                                                                                                                                                                      |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `repository`, `prNumber`, `headSha`, `requestId` | Exact target/correlation echo; repository slug, positive PR integer, full SHA, coordinator-issued request ID. Validate against trusted acquisition, never accept routing supplied by the model.                                               |
| `verdict`                                        | Exactly `approve`, `request_changes` or `escalate_to_replan`.                                                                                                                                                                                 |
| `summary`                                        | Short human-readable disposition, independent of machine routing.                                                                                                                                                                             |
| `requirements`                                   | Existing requirement IDs, `satisfied` / `unsatisfied` / `human-needed`, source/evidence links. Preserve coverage without restating source documents.                                                                                          |
| `findings`                                       | Existing stable ID, class (`blocker`, `human-needed`, `should-fix`, `suggestion`), status, mandatory flag, summary and evidence; optional path/line. Mandatory open findings include a concrete next action/owner and recommended resolution. |
| `humanFeedback`                                  | Existing ledger IDs and addressed/deferred/blocked disposition, with reason and source link; include human commits as well as all comment/review surfaces.                                                                                    |

The coordinator owns run/attempt, provider/model/effective effort, App identity,
base/head and trusted workflow/helper refs, and the accepted-feedback watermark.
Validate correlation, enums, coverage and verdict consistency before writes.
`approve` requires no open mandatory/blocker/human-needed finding and complete
required inputs. `escalate_to_replan` identifies the changed requirement, affected
scope and recommended decision; unavailable credentials alone are
`request_changes` plus a human-needed execution input, not a new plan.
Malformed/missing output, provider failure or missing durable workpad cannot
approve. Preserve prior unresolved findings; reject stale output without acting.

Persist through the existing workpad helper before success publication; bind the
result to the App-authored review ID, head and request/run. Handoff consumes this
validated record; a review marker carries correlation only. Missing structured
records produce a diagnostic and fresh review request, never prose reinterpretation.
Release publisher/consumers compatibly so new reviews are not dropped; retain
deduplication, per-PR concurrency and loop cap without reviving dormant acquisition.

### R2 — Communication, readiness and reactivation

Update one App-owned main PR comment by stable marker: disposition, at most three
points, head/workpad links and timing footer. Details stay in the Cadence workpad.
Preserve submitted reviews as event/history records with minimal disposition/link
bodies. Never delete human comments or treat the main comment as verdict authority.

| Validated result                                                         | Coordinator action                                                                                                                                                                            |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Clean `approve`                                                          | Submit `APPROVE`; fresh current-head review with no newer accepted feedback readies a draft via repository workflow identity, then requests eligible human assignees. No Linear reactivation. |
| `request_changes`, including Human input needed                          | Submit `COMMENT`; matching structured non-approval reactivates the eligible waiting issue to Active. Known fixes run; unavailable input is recorded by Symphony before it returns Inactive.   |
| `escalate_to_replan`                                                     | Submit `COMMENT`, reactivate eligible waiting issue and route the existing replan/human-decision handoff with proposed resolution. No automatic extra tickets or scope approval.              |
| Ordinary comment, absent/invalid/stale result, duplicate, terminal issue | No verdict-driven wake or readiness. Record the actual skip/error. Preserve existing verified human-comment routing separately.                                                               |

Reuse author/App permission checks, `symphony` association, team-config resolution,
current PR/review/head checks and terminal-state preservation. Human approvals
with notes receive a Cadence re-look without directly waking Linear. Verified
human write-access feedback and commits can revise design; bots cannot manufacture
that authority. Fresh feedback invalidates earlier acceptance even on the same SHA.
No GitHub `REQUEST_CHANGES` event is emitted by Cadence. Human acceptance/merge
remain separate; advisory review checks never become required CI.

Reuse #40's repository-token readiness and App check publisher. Recheck head/feedback
before mutations and read back `isDraft: false`; already-ready PRs need no repeat.
Findings/stale/failed runs never ready drafts. Denial or absent confirmation reports
“review approved; marking ready failed” with operator/readback action, without App
grant expansion. Immediate checks narrow the head race; they do not make it atomic.

### R3 — Providers, settings and credentials

100-64/62's newer contract supersedes historical explicit reviewer selection:
OpenAI only or both keys → Codex; Anthropic only → Claude; neither → early error.
`CADENCE_OPENAI_API_KEY` maps to Codex `openai-api-key`;
`CADENCE_AI_REVIEW_ANTHROPIC_API_KEY` maps to Claude `anthropic_api_key`.
Both secrets are optional declarations; runtime requires one. Invalid selected
credentials never fall back. Retain eight compatible Copier answers; existing
`cadence_reviewer` is an onboarding preference, not an override of effective selection.
Do not add mandatory provider/model/effort questions.

100-44 exposes optional per-provider model/effort settings through existing
workflow inputs/Actions variables, removes the single-model allowlist and preserves
the fast focused default. Validate supported values clearly; do not silently
claim an unsupported effort was applied. Record requested/effective values,
queue time (accepted request to provider start), execution time (provider start
to finish), and unavailable measurements explicitly. Use observed timestamps,
not LLM estimates, in check details and the compact footer.

Keep explicit named secret forwarding at each boundary: review App/Linear/provider;
handoff App/Linear; advisory cleanup App; wakeup Linear; CI/ingress none.
100-62 owns actual repository/organization delivery, installation/grants and
`cadence-controller` admission without environment-secret shadowing. No secret
values in answers/logs/docs, no new credential service or worker authentication.

### R4 — Generated PR guidance and Mermaid

100-61 owns a small deterministic renderer in template/shared tooling, invoked
on client PR creation and refresh. Reuse the accepted plan format and shared
`tools/symphony-dag/` parser. Fetch live state/PR associations separately; pure
rendering receives plan nodes/edges, states, PR URLs, current node and snapshot time.
Preserve topology and IDs; escape labels/URLs without executable interpolation.

Done is green; Active/Evaluating and legacy implementation states are blue;
Inactive/Unhappy and legacy waiting states are amber; Backlog, canceled, duplicate
and unknown are neutral. Label the state explicitly; a missing lookup is unknown.
Known Done stays green even with pending-artifact prose; report that remaining
scope separately. A separate purple outline and “Current PR” identify the current
node in every state. Keep PR links and mark missing associations “no PR yet”.
Omit diagrams with fewer than three meaningful nodes **or** fewer than two genuine
edges; never invent topology. Generated guidance/template explains value, linked
goal, concise summary, selected base and relevant tests; no legend or repeated logs.

### R5 — Project-folder cleanup

Deliver a thin client workflow and shared implementation distinct from advisory
check cleanup. Native weekly schedule (Monday 03:00 UTC) and `workflow_dispatch`
produce a dry-run report. The sole configurable input is positive integer
`stale_days`, default 60. No arbitrary path, force, provider or mode inputs.
Execution requires a human approving the reported candidate set in a protected
cleanup environment. Verify required human reviewers, trusted-base restriction and
disabled admin bypass before offering execution; absent/unreadable protection is
dry-run only. Never create an unprotected environment implicitly. No approval means
no mutations. Target admins configure this [native approval mechanism][environments];
bots cannot approve the job or the resulting deletion PR. No extra mode input.

Eligibility is per project, after complete paginated acquisition:

- **Clean end:** project completed or canceled **and** every project ticket
  closed **and** every associated PR closed or merged. Closed tickets mean
  completed/canceled/duplicate terminal categories, including legacy spellings;
  archived alone is not closed. A completed project with one open ticket fails.
- **Stale:** clean-end checks fail and `now - last_activity >= stale_days × 24h`.
  Use UTC and the maximum of project/ticket creation/update times, ticket-comment
  creation/edits, associated PR creation/update/closure/merge, review/comment
  creation/edits, PR commit committer times and commit committer times touching the
  eligible folder on the selected base. Include human and bot activity. Missing or future timestamps
  produce unknown, not stale; no-activity objects use their creation time.
- Include archived tickets and deduplicated PRs from ticket links, plan associations
  and title/branch identities across all explicitly project-owned repositories.
  Incomplete access/pages or ambiguous identity block that project only. Dry-run
  output stays in Actions summaries/artifacts, avoiding artificial project activity.

Only the tracked directory `docs/symphony-plans/<project-code>/` on a reviewed
base is eligible, and only when the accepted plan explicitly assigns that exact
directory to this project and all its contents are disposable project coordination
artifacts. Project code must uniquely match Linear metadata. No guessed legacy
aliases, glob deletion, traversal, symlink traversal or nested repository removal.
Mixed ownership or unrelated files excludes the directory until reviewed mapping
is corrected. Top-level requirements/design/plans/`.mmd`, shared docs, application
files and `.github` remain outside eligibility. This design stays top-level.

For an approved clean candidate, propose only folder deletion in a PR against the
selected base. For approved stale candidates, in order: cancel each open ticket,
cancel the project (deterministic default; already completed/canceled stays so),
close each open associated PR, read back **all** clean-end predicates, then create
the deletion PR. The same run may do all steps. Never directly push deletion to
base, merge/approve the bot's PR, delete branches/history, or delete Linear records.
The cleanup PR is created after checking source PRs; identify it as the cleanup
proposal so it cannot close itself or duplicate a prior proposal.

Serialize execution per project using native concurrency. Refresh membership,
activity, paths and state after approval and before each mutation; unrelated new
activity aborts the remaining actions for that project. Record confirmed partial
steps in existing run/workpad evidence; retry reuses IDs and the existing deletion
PR, and distinguishes its own confirmed changes from external activity. Never
infer rollback or success after an API error. A final folder/base diff check
prevents a deletion PR from silently including newly added unrelated files.
State cancellation and PR closure retain Linear/GitHub history; git retains files.

### R6 — Concision

Retain useful requirements, decisions, acceptance and unresolved findings; link
existing workpads/history instead of copying deliberation into plans. Preserve
`.gitattributes`: nested project bookkeeping collapses, top-level docs and `.mmd`
remain visible. Consume 100-63's removal without introducing a replacement skill.

Prose budgets: PR template ≤60 lines; focused skill or generated SYMPHONY ≤120;
focused reference ≤160; this design ≤360 formatted lines. Explain useful exceptions
in PRs; never hide text in extra files or omit requirements. Revise verbose output
toward 40% less prose, preserving contracts. Implementation tickets need proportional
budgets counting helpers/tests alongside YAML, not only wrapper length.

### R7 — Periodic self-adoption and real behavior

Plan useful increments with root self-adoption after each: factory/guidance,
review/routing and cleanup are demonstrable groups, not a ticket sequence.
Coordinate alpha migration with 100-57, preserve 100-58/59's adoption/retirement
proof, and reuse evidence rather than competing over the same PR/settings.

After acceptance/publication, resolve both `alpha` refs and update an isolated root
with Copier 9.18.2. Review collisions, preserving package CI/config and adopter files
with normal exclusions/conflict handling, including removed customized files.
Record truthful `_src_path`/`_commit`, workflow/helper refs and generated diff;
no self-referential SHA, recursive hook or release updater.

Run render/update checks, then AC2–AC11's affected real behaviors after trusted
callers land. Record target/head, consumed refs, run/attempt, before/after state
and links, including advisory queued/running/result. Credentials/rollout/authorization
gate only dependent live steps; rendering/probes do not prove execution or recovery.
Feed findings into the remaining plan through existing replanning tools.

### R8 — Factory and Linear GraphQL instructions

Align template SYMPHONY, factory/GraphQL skills and resource links, then self-adopt:
prefer injected `linear_graphql`; when absent in a human-operated factory session,
use shipped `.agents/skills/linear-graphql/scripts/linear-graphql.mjs` with its
documented token source. Auth failure stops dependent writes, without identity
switching. Hosted workers retain injected-tool auth and no factory installation.

Both transports verify viewer/workspace/team identity before source acquisition
and writes. Retain source/color/label/state/assignee preflight and a concrete
write preview. Create only authorized seeds staged in Backlog, create/read back
the two blocker relations (`issueId` blocker → `relatedIssueId` blocked), then
activate all three unless held. Preserve existing IDs on retries; preview-only
does no writes, partial failure leaves staged work unactivated. Read back project
metadata, labels, assignees, states and relations. No second confirmation for
already-authorized writes; no extra tickets or unrelated moves.

Verify fallback on an authorized disposable project in a Copier-generated/updated
human client; test tool preference, preview, wrong workspace, missing auth/source/label,
partial failure and retry. Fixtures prove guards, real setup/readback proves operation;
Jeremy supplies test authorization/credentials, not a new product decision.

### R9 — Ingress ownership

100-65 selects `cadence-client-review-ingress.yml` / “Cadence Client Review Ingress”,
authoritative for the workflow repo's own PRs after onboarding. Preserve provider-owned
ingress while retiring overlapping admission. Update event/handoff subscriptions
and `cadence-forwarded-event.mjs` exact trusted paths together. Copier retires only
the old generated path; prove repeat updates, provider-file preservation and one
review/handoff per event without accepting arbitrary workflow names.

## Acceptance and planning handoff

These are required evidence targets, not observed results of this design PR.
100-67 maps every row to existing ownership or a bounded new deliverable, with
file/resource ownership and only necessary hard dependencies; 100-68 alone fans out.
Use shared Symphony DAG tooling and existing schemas. All task/PR bases are main;
never commit unmerged predecessor work. Reconcile new human decisions before planning.

| ID   | Acceptance                                                                                                                                                                                                                               | Owner boundary / prerequisite                                                                                                                  |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| AC1  | Every candidate/note classified with current issue/PR/source evidence; no duplicate 100-57/62/63/64 or removed holds                                                                                                                     | 100-66 design; 100-67 refresh.                                                                                                                 |
| AC2  | Both providers return R1 data for the same PR/head using unchanged implementation; malformed, stale, missing and inconsistent outputs cannot act; findings/feedback survive                                                              | Shared workflow contract owner consumes accepted 100-64; 100-62 credentials gate live runs only.                                               |
| AC3  | One main comment updates; current clean draft becomes ready; stale/new-feedback/failure/denial/duplicate cases do not; failed handoff remains explicit                                                                                   | Shared coordinator owner; template root checkpoint with actual PR/review/check/workpad links.                                                  |
| AC4  | Trace #48; App-authored COMMENTED human-needed and ordinary changes verdict each wake eligible wait; approvals/ordinary bot comments do not; authority/terminal/dedup guards pass                                                        | Existing 100-60, released structured publisher and Copier-readiness hold.                                                                      |
| AC5  | Optional settings reach provider; effective provider/model/effort and separate actual timings visible; unset settings preserve fast behavior; all four key cases verified                                                                | Existing 100-44 with 100-64 boundary; no new provider implementation.                                                                          |
| AC6  | Creation and refresh invoke pure renderer; #49 Done regression green; colors/highlight/links/topology retained; undersized diagrams omitted; actual GitHub rendering verified                                                            | Existing 100-61 and generated client; preserve Copier-readiness hold.                                                                          |
| AC7  | Weekly/manual dry-run has zero mutations; clean/stale boundary, one-open-ticket, incomplete access, unsafe path, fresh activity, partial failure and retry tests pass; controlled stale run closes state/PRs then opens deletion-only PR | Shared cleanup implementation + thin template caller; Jeremy authorizes controlled live target/environment. No real project cleanup by 100-66. |
| AC8  | Budgets/40% revision preserve all required content, removed skill stays removed, diff-collapse exceptions unchanged                                                                                                                      | Concision owner consumes 100-63; no personal/global changes.                                                                                   |
| AC9  | Each useful increment consumed from published revisions in root, preserves adopter files/config/CI, passes actual affected behavior and feeds findings back                                                                              | Increment owners coordinate with 100-57; 100-58/59 obligations stay intact.                                                                    |
| AC10 | Both Linear transports follow identical preflight/staging/readback; real absent-tool factory setup succeeds in generated client; root correction adopted; hosted auth unchanged                                                          | Template factory correction owner; Jeremy supplies authorized human-session test target.                                                       |
| AC11 | Workflow repo onboards/updates without provider-file loss; renamed ingress passes trust checks, rejects impersonation and causes one downstream delivery                                                                                 | Existing 100-65; explicit hold release and accepted ingress migration required for this adoption only.                                         |
| AC12 | Reviewed source, published refs, installed client and live outcomes distinguished; passing local checks and exact-head CI; fresh configured review and human acceptance before completion                                                | Every delivery owner; remaining external operations named with exact action/readback.                                                          |

Material open decisions: none required to plan. R1/R4/R5/R6 offer explicit defaults
for human review. IDs, CI names, model compatibility, App grants and secret delivery
are implementation/admin lookups; missing access gates only dependent operations.
Unknowns never count as observed values or passing evidence.

100-66 validates formatting, whitespace, references/coverage and published-head
template CI (`Client template tests`, `.github/workflows/ci.yml`, App 15368).
Local pass skips Docker; no provider, cleanup, adoption or live workflow claim.

[brief]: https://linear.app/1000lines/project/symphony-client-template-enhancements-c24c56d5ad02
[template-base]: https://github.com/1000lines/symphony-client-template/tree/58021a73ac3a6c2141a1217fc88c27e590df8143
[workflow-base]: https://github.com/1000lines/symphony-client-workflows/tree/77cfb2d1f4e0e488af207096b1785b63ffc0398b
[old-design]: https://github.com/1000lines/symphony-example/blob/e362e5ad76fa8070ef27bf54fec9d6750195466c/docs/symphony-plans/client-template-design.md
[old-plan]: https://github.com/1000lines/symphony-example/blob/e362e5ad76fa8070ef27bf54fec9d6750195466c/docs/symphony-plans/fan-out-plan-100-39-client-template.md
[e6]: https://github.com/1000lines/symphony-example/pull/6
[e11]: https://github.com/1000lines/symphony-example/pull/11
[e16]: https://github.com/1000lines/symphony-example/pull/16
[e32]: https://github.com/1000lines/symphony-example/pull/32
[e36]: https://github.com/1000lines/symphony-example/pull/36
[e40]: https://github.com/1000lines/symphony-example/pull/40
[e48]: https://github.com/1000lines/symphony-example/pull/48
[e49]: https://github.com/1000lines/symphony-example/pull/49
[t1]: https://github.com/1000lines/symphony-client-template/pull/1
[t2]: https://github.com/1000lines/symphony-client-template/pull/2
[t3]: https://github.com/1000lines/symphony-client-template/pull/3
[t4]: https://github.com/1000lines/symphony-client-template/pull/4
[w1]: https://github.com/1000lines/symphony-client-workflows/pull/1
[environments]: https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
