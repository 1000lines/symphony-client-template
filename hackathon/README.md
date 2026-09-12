# AI Tinkerers hackathon

Bring a GitHub repository and a real project or problem you want to work on. A
few paragraphs of notes are enough; Markdown documents and other existing
project material are useful. Plan to spend two or three hours in the room. You
will review the proposed work and the resulting pull requests.

## Goal for the day

The alpha release took an agent software-development workflow that worked in one
repository and turned it into a reusable template. Today we test the claim at
the heart of that work: **reuse it, then reuse it again**. We will install the
same system in repositories we did not design it for and use it on real projects
their owners want to move forward.

This is an agent experience inside the places where software engineering already
happens. The human defines the project in Linear and holds the engineering
conversation on GitHub pull requests. Symphony does the coding, Cadence takes
the review journey with the human, and the dashboard provides monitoring. The
plan appears on the pull request page as a Mermaid dependency graph: a picture
the human can question, an artifact both agents can discuss, and an execution
plan Symphony can follow. Linear and GitHub shape how the agents plan,
communicate, respond to feedback, and act; they are not wrappers around a
separate chat window.

By the end of the day, we want to show:

- a complete path from a Linear project definition to Symphony-authored code,
  Cadence review, human feedback, revision, approval, and merge;
- a human-reviewed Mermaid dependency graph that makes the proposed work,
  ordering, and parallelism visible before implementation fans out;
- repeated installation and execution across several participant repositories;
- real development completed on those repositories, not a staged demonstration;
- per-repository evidence of what worked and a concrete defect list wherever the
  reusable workflow failed or needed intervention.

A successful run demonstrates useful, controllable agents native to Linear and
GitHub. A failed run is still a deliverable when its log identifies where the
template, integration, orchestration, or recovery path broke. Together, those
runs test functionality, theme fit, technical integration, reliability, and
usefulness under real conditions.

## What we achieved

We tested whether a workflow extracted from one repository could work in others.
**Three participant repositories ran it:** Memray delivered feature code and
upstream handoff preparation; Venn delivered a first cleanup implementation;
ESLint delivered requirements and a plan. All three required human intervention.
These results combine the logs with later GitHub evidence, captured below.
The logs stopped earlier: Venn at design and ESLint at setup. Later merges
therefore count here without changing those records or treating planned work as done.

### Results by repository

- **Memray:** Symphony and HackCadence installed; Jeremy connected the existing CI.
  Symphony delivered full captures, tests and docs through Cadence review, human feedback, revision and merge.
  Jeremy also redirected upstream delivery; the [merged handoff](https://github.com/jeremycarroll/pytest-memray/pull/11) still left submission pending.
  [Repository log](jeremycarroll--pytest-memray.md).
- **Venn:** Symphony and HackCadence installed alongside Rust CI; Jeremy repaired onboarding.
  Symphony delivered a design, plan, fan-out and [first cleanup](https://github.com/jeremycarroll/venn-search-rs/pull/20); seven follow-up PRs remained open.
  Jeremy approved and merged the [design](https://github.com/jeremycarroll/venn-search-rs/pull/17) before Cadence finished, cancelling that review.
  [Repository log](jeremycarroll--venn-search-rs.md).
- **ESLint:** the organisation's Symphony/Cadence setup installed; Jeremy repaired CI and formatting.
  Symphony delivered requirements and a [plan](https://github.com/1000lines/eslint/pull/3), both merged by Jeremy.
  The plan reports 37 candidate rules and six proposed first-wave lanes; no rule implementation had landed.
  [Repository log](1000lines--eslint.md).

Memray demonstrated the complete Linear-to-code review journey. Its human-reviewed
Mermaid plan grew from three nodes to five after Jeremy changed the delivery
requirement. Venn and ESLint also merged plans, but the evidence does not establish
the complete review journey in all three. Jeremy's assessment: most of the workflow
worked; review delivery, comment cleanup and ticket transitions needed attention.

### The day's PRs

At **2026-09-12 22:55 UTC**, GitHub showed **26 PRs: 17 merged, 9 open**,
none closed unmerged. This inventory covers PRs opened or closed September 12 PDT
under `jeremycarroll` or `1000lines`, carrying `symphony` at read time. Unlabelled
setup PRs are excluded. Workflow and test-repository work is counted separately
from the three participant projects.

| Repository | Merged | Still open |
| --- | --- | --- |
| `jeremycarroll/pytest-memray` | [#2](https://github.com/jeremycarroll/pytest-memray/pull/2), [#3](https://github.com/jeremycarroll/pytest-memray/pull/3), [#4](https://github.com/jeremycarroll/pytest-memray/pull/4), [#5](https://github.com/jeremycarroll/pytest-memray/pull/5), [#6](https://github.com/jeremycarroll/pytest-memray/pull/6), [#7](https://github.com/jeremycarroll/pytest-memray/pull/7), [#8](https://github.com/jeremycarroll/pytest-memray/pull/8), [#9](https://github.com/jeremycarroll/pytest-memray/pull/9), [#10](https://github.com/jeremycarroll/pytest-memray/pull/10), [#11](https://github.com/jeremycarroll/pytest-memray/pull/11) | — |
| `jeremycarroll/venn-search-rs` | [#17](https://github.com/jeremycarroll/venn-search-rs/pull/17), [#18](https://github.com/jeremycarroll/venn-search-rs/pull/18), [#19](https://github.com/jeremycarroll/venn-search-rs/pull/19), [#20](https://github.com/jeremycarroll/venn-search-rs/pull/20) | [#21](https://github.com/jeremycarroll/venn-search-rs/pull/21), [#22](https://github.com/jeremycarroll/venn-search-rs/pull/22), [#23](https://github.com/jeremycarroll/venn-search-rs/pull/23), [#24](https://github.com/jeremycarroll/venn-search-rs/pull/24), [#25](https://github.com/jeremycarroll/venn-search-rs/pull/25), [#26](https://github.com/jeremycarroll/venn-search-rs/pull/26), [#27](https://github.com/jeremycarroll/venn-search-rs/pull/27) |
| `1000lines/eslint` | [#2](https://github.com/1000lines/eslint/pull/2), [#3](https://github.com/1000lines/eslint/pull/3) | — |
| `1000lines/symphony-client-workflows` | [#16](https://github.com/1000lines/symphony-client-workflows/pull/16) | [#18](https://github.com/1000lines/symphony-client-workflows/pull/18) |
| `1000lines/test-repo-1` | — | [#1](https://github.com/1000lines/test-repo-1/pull/1) |

The [workflow fix](https://github.com/1000lines/symphony-client-workflows/pull/16) reconciles Linear when the last linked PR
closes. The two open testing PRs do not establish a completed test campaign.

The same day's Symphony repository work also included **five merged PRs without
that label**:

| Repository | Merged work |
| --- | --- |
| `1000lines/symphony-client-template` | [Hackathon onboarding #24](https://github.com/1000lines/symphony-client-template/pull/24), [repository-only files #25](https://github.com/1000lines/symphony-client-template/pull/25), [Linear/GitHub setup #26](https://github.com/1000lines/symphony-client-template/pull/26) |
| `1000lines/symphony-client-workflows` | [Skip closed review events and trace Linear reconciliation #17](https://github.com/1000lines/symphony-client-workflows/pull/17) |
| `1000lines/symphony-example` | [Expand project colours from 9 to 24 #68](https://github.com/1000lines/symphony-example/pull/68) |

These additions bring the report to **31 PRs: 22 merged and 9 open** across six
repositories, using the labelled inventory's state snapshot above. This report's
own PR is excluded. The work includes fixes to the workflow while participants
were using it, not just changes to their applications.

### Defects and interventions

Consolidated from the linked logs; unconfirmed root causes remain attributed to them.

1. **Reviews missing or unfinished — Venn, ESLint.** Venn's [setup review](https://github.com/jeremycarroll/venn-search-rs/pull/16)
   was skipped; its [design review](https://github.com/jeremycarroll/venn-search-rs/pull/17) was cancelled by merge. The log also records
   three failed review-event jobs and one failed handoff job, with root causes unread. ESLint's log records no [setup review](https://github.com/1000lines/eslint/pull/1).
2. **Automated output left visible — Memray.** The [publication job](https://github.com/jeremycarroll/pytest-memray/pull/2)
   refused to hide a changed review and reported failure despite correct approval state.
3. **Manual ticket transitions — Venn, Memray.** Venn reconciliation failed on
   [unlinked setup](https://github.com/jeremycarroll/venn-search-rs/pull/16) but passed on the [linked design](https://github.com/jeremycarroll/venn-search-rs/pull/17).
   No ticket needed moving for the unlinked setup PR. Memray’s log could not
   distinguish automatic moves from manual recovery. Jeremy reports manual
   transitions; the exact ticket mapping remains TBC. The merged workflow fix
   does not prove that every transition recovered.
4. **Label permissions — Memray, Venn.** The shared label helper returned 403;
   the existing author credential worked through a REST fallback.
5. **CI integration — Memray, Venn, ESLint.** Duplicate workflows needed removing
   in Memray/Venn; required-check lists were empty in Memray/ESLint. ESLint's
   planned narrowing was unwritten in its log.
6. **Generated commands — Memray, ESLint.** Memray needed a real build command,
   repaired YAML quoting and Docker spelling. ESLint needed an install flag;
   whole-suite testing remained costly for single-rule work.
7. **Formatting and identities — ESLint, Venn.** ESLint needed JSON formatting
   and combined attributes; Venn needed corrected bot identities.
8. **Check names — Venn.** Cadence displayed unexpanded GitHub expressions.
9. **Runtime bundle — Memray.** Missing compiled DAG modules required an isolated build.
10. **DAG content — Memray.** Scope, files and acceptance/validation instructions
    were dropped from generated tickets and transcribed manually.
11. **Progress fetching — Memray.** Seeds outside the implementation graph were unsupported.
12. **Rerun permissions — Memray.** A network failure needed a human rerun because
    the App lacked permission. [Attempt 2 passed](https://github.com/jeremycarroll/pytest-memray/actions/runs/34713703824).
13. **Browser availability — Memray, ESLint.** Mermaid checks needed container fallbacks,
    also reported in ESLint's [plan](https://github.com/1000lines/eslint/pull/3).
14. **Dependency waits — Memray.** Finished independent work repeatedly resumed
    while its prerequisite stayed unchanged.
15. **Linear visibility — all three logs.** Logging sessions reached the wrong
    workspace; missing-project observations were not proof of absent projects.
16. **Unexplained recovery branch — Memray.** `fix/linear-team-key` had no commits;
    its purpose remains unresolved.

### What was not achieved

- **Upstream Memray delivery:** certification, submission, final news naming and
  acceptance remained pending in the log and [handoff](https://github.com/jeremycarroll/pytest-memray/pull/11).
- **Completed Venn cleanup:** seven implementation PRs remained open; the solution-count
  discrepancy was unanswered: the tests expected 16/17 solutions where the brief
  said 3/23. Symphony preserved the executable counts and asked the human to resolve it.
- **ESLint rule changes:** six lanes were proposed out of 37 candidates, none delivered.
- **Unattended operation:** installation, review cleanup and ticket transitions
  still needed humans. A completed Cadence journey was not established everywhere.
- **A nontrivial Memray replan:** the added dependency was human-requested delivery work.
  Final credential/access cutoff and completion of the workflow-test campaign were
  also not established by these snapshots.

Unresolved log questions follow. The rerun is answered above but retained for traceability.

**From [jeremycarroll--pytest-memray.md](jeremycarroll--pytest-memray.md):**


- TBC — Jeremy: did zizmor fail on the Copier-generated workflows, or was this pre-emptive?
- TBC — Jeremy: was [run 34713703824](https://github.com/jeremycarroll/pytest-memray/actions/runs/34713703824) ever rerun green?
- TBC — Jeremy: what was `fix/linear-team-key` for, and was the problem it was named for fixed another way?
- TBC — Jeremy: did any merged PR here fail to move its ticket to Done, and did you move any manually?
- TBC — Jeremy: the template README gained its "Known defect" note at 11:07 today, mid-run — was it this repository that triggered it?

**From [jeremycarroll--venn-search-rs.md](jeremycarroll--venn-search-rs.md):**


- TBC — Jeremy: why was [#15](https://github.com/jeremycarroll/venn-search-rs/pull/15) abandoned rather than merged — template revision, the deferred Cadence caller, or something else?
- TBC — Jeremy: what does the "Reconcile current PR associations" step log say — is it the unlinked-PR case failing loudly, or a genuine Linear API/permission failure?
- TBC — Jeremy: what are `Cadence AI Review Events` and `Cadence Review Handoff` failing on after merge?
- TBC — Jeremy: what does "the full Rust workload" (100-96) actually cover, is it venn-search-rs, and has the rehearsal it refers to happened?
- TBC — Jeremy: is the 16/17 vs 3/23 discrepancy a stale brief, or a real regression in the N=4/N=5 tests on main?

**From [1000lines--eslint.md](1000lines--eslint.md):**


- TBC — Jeremy: which Linear workspace holds team 100, and has the ESLint project been created there yet?
- TBC — Jeremy: has the ESLint setup probe been run yet?
- TBC — Jeremy: which ubuntu leg is the gating one, and does an empty `requiredChecks` mean "none gate" or "fall back to all"?
- TBC — Jeremy: confirm a first wave of six lanes?
- What was completed: TBC — Jeremy
- What remains: TBC — Jeremy
- Where to retrieve the work: TBC — Jeremy
- Follow-up: TBC — Jeremy

## What it does

**Software engineering is and has always been a conversation between engineers;
a journey, not a single waterfall.**

Fifty years ago, much of that conversation happened face to face around a
chalkboard; later, around a whiteboard. GitHub took it out of the meeting room
and onto the web, on the pull request page, where the conversation became
durable and asynchronous. 1000lines brings agents into that same conversation
without removing the human decisions.

Coding and review agents already participate in parts of this flow, but they
are rarely immersed in the whole journey. They arrive for one task or one diff,
without the project context, decisions, and feedback that shaped it. Our agents
are there for the journey. Cadence stays with the human across the project's PR
conversation, carrying review context from one decision to the next. Symphony
does the coding: it turns ready work into branches and pull requests, then
revises them in response to the conversation.

You define the project in Linear, then respond to requirements, design, plans,
and working software through GitHub pull requests. Your comments change what
happens next; approval and merge move the project forward.

Both agents join you on the pull request page. Symphony presents its work and
responds to your comments. Cadence explains its review and stays in the review
conversation as the pull request changes.

1000lines provides those two roles. Cadence accompanies the human through the
review journey; Symphony implements the work. Ticket state and workpads carry
context and handoffs across Linear and GitHub. The Symphony UI lets you watch
the work without having to operate it ticket by ticket.

The agents also need their own conversation. Cadence and Symphony communicate
through Linear. Symphony agents working on different tickets, often at different
times, leave context for one another in hidden documents in the repository.
Those channels let later agents continue the journey instead of starting each
task from an isolated prompt.

Some coding agents do not participate in a conversation at all. They suck up the
air with a huge diff, ignore the niceties of the pull request medium, and are
hard to correct. A different response is to set guardrails and a direction, then
get out of the agent's way. That gives the agent room to run, but delays the
moment when a human discovers that it ran in the wrong direction.

1000lines uses a dependency graph of small tasks to keep the work correctable
while it is moving. Projects are cheap enough that a half-finished project going
in the wrong direction does not have to be rescued. Keep what you learned,
discard the project, and start a better one.

### The plan is a Mermaid graph

Every project plan is a Mermaid dependency graph. It renders directly on the
GitHub pull request page, so the human and both agents can discuss the same
picture in the same medium as the rest of the engineering conversation. The
nodes are focused tasks that can become pull requests. The arrows state which
results must exist before other work can begin. Unconnected branches show where
Symphony can work in parallel.

The graph is both a human-readable proposal and Symphony's machine-readable
execution plan. Reviewing it before fan-out makes missing work, false
dependencies, unsafe parallelism, and unnecessary scope visible before they
turn into a pile of code. When implementation changes what the team understands,
the graph changes too. It records the replan instead of pretending the first
plan was final.

### A real replan

The template-enhancement
[`fan-out-plan-100-67-template-enhancements.mmd`](../docs/symphony-plans/fan-out-plan-100-67-template-enhancements.mmd)
has four recorded versions across the repository's branch history. Two changes
substantially altered its structure. This diagram shows only the lanes that
changed:

```mermaid
flowchart TB
  subgraph FIRST["Initial plan · dfbc564"]
    direction LR
    D1["D · Generate diagrams"] --> G1["G · Align guidance"] --> A1["A · Publish guidance"]
    X1["X · Execute cleanup"] --> L1["L · Add cleanup caller"] --> W1["W · Final adoption"]
    B1["B · Publish review"] --> I1["I · Migrate ingress"] --> W1
  end

  subgraph SECOND["Replan · e6573b1"]
    direction LR
    G2["G · Establish root validation"] --> D2["D · Generate diagrams"] --> A2["A · Publish guidance"]
    X2["X · Execute cleanup"] --> L2["L · Add cleanup caller"]
    B2["B · Publish review"] --> L2 --> I2["I · Migrate ingress"] --> W2["W · Final adoption"]
  end

  subgraph THIRD["Later discovery · ffa1ef6"]
    direction LR
    P3["P · Review publication"] --> C3["C · Review communication"] --> B3["B · Publish review"]
    S3["S · Existing status comment"] --> T3["T · Settings and timings"] --> B3
  end

  FIRST -->|Ownership and validation clarified| SECOND
  SECOND -->|New work discovered while executing| THIRD
```

The [first plan](https://github.com/1000lines/symphony-client-template/commit/dfbc564988876f3b39d76c3a0376eae6ce08782a)
assumed diagrams could precede guidance alignment and that cleanup and review
publication could remain mostly parallel. Eight minutes later, the
[first replan](https://github.com/1000lines/symphony-client-template/commit/e6573b1839f434bba16247598b8c40df5ecca16a)
recorded two discoveries: root validation had to exist before generating files,
so `D → G` became `G → D`; and shared inventory ownership required review
publication, cleanup, and ingress migration to run in order. The longest path
grew from eight rounds to ten rather than hiding those dependencies.

Later, an existing status-comment task became relevant. The
[second structural amendment](https://github.com/1000lines/symphony-client-template/commit/ffa1ef6e19a529a3272d71393c04183118c37b24)
added it as `S` and split presentation from the broader communication task:
`C → T` became `S → T`, while `C → B` preserved the review-publication handoff.
The project kept moving while the graph recorded what the team had learned.

## Architecture

```mermaid
flowchart LR
  HUMAN[Human]

  subgraph LINEAR[Linear]
    PROJECT[Project definition]
    DAG[Human-reviewed Mermaid DAG<br/>machine-readable execution plan]
    AGENTLINEAR[Cadence and Symphony<br/>ticket state and workpads]
  end

  subgraph SERVICE[Symphony]
    ORCHESTRATOR[Hosted coding agents<br/>different tickets and times]
    MONITOR[symphony.1000lines.dev<br/>monitoring]
  end

  subgraph GITHUB[GitHub repository]
    CODE[Branches, code, and workflows]
    HIDDEN[Hidden agent documents<br/>cross-ticket context]
    PR[Pull requests]
    CADENCE[Cadence AI review]
  end

  HUMAN -->|Define the goal| PROJECT
  HUMAN <-->|Review conversation| PR
  HUMAN -.->|Watch| MONITOR

  PROJECT --> DAG
  DAG <--> ORCHESTRATOR
  ORCHESTRATOR <--> AGENTLINEAR
  CADENCE <--> AGENTLINEAR
  MONITOR -.-> ORCHESTRATOR
  ORCHESTRATOR <-->|Agent to future agent| HIDDEN
  ORCHESTRATOR -->|Symphony codes| CODE
  CODE --> PR
  ORCHESTRATOR -->|Replies and revisions| PR
  PR -->|Human feedback and merge signals| ORCHESTRATOR
  PR <-->|Cadence review conversation| CADENCE
```

The human works through the Linear project definition and GitHub pull requests.
Cadence and Symphony use Linear to talk to one another; individual ticket state
and workpads support automation and troubleshooting rather than acting as the
participant's day-to-day control surface. Hidden repository documents carry
context between Symphony agents across tickets and time. Symphony does the
coding, Cadence takes the review journey with the human, and the participant
owns approval and merge decisions. The Symphony UI is the monitoring surface.

Create a separate log in this folder for every repository worked on. Name it
`OWNER--REPO.md`, using the working repository's owner and name, and start from
[`repo-log-template.md`](repo-log-template.md). Keep each repository's activity
separate during the event. The logs will be consolidated at the end of the day.

## 1. Join Linear

1. Create a Linear account.
2. Ask Jeremy to add you to the Linear team.
3. Create a Linear API key. Do not paste it into chat, a Copier answer, a commit,
   or an issue.
4. Save the raw key locally at `~/.linear-token`.

## 2. Connect Linear to a bring-your-own repository

If you are keeping the repository in its current account or organization,
Linear's GitHub integration must include that GitHub owner. Otherwise, merging
a linked pull request will not move its Linear ticket to Done. Participants
using the `1000lines` fork path can skip this section because that owner is
already connected.

1. Open [Linear's GitHub integration settings](https://linear.app/settings/integrations/github).
2. Add or connect the GitHub owner that owns the target repository. For
   `jeremycarroll/pytest-memray`, connect **jeremycarroll**.
3. Install Linear's GitHub App for that owner and grant it access to the target
   repository. For this test, include **pytest-memray**.
4. In Linear's GitHub workflow settings for team **100**, confirm that the
   **PR merged** target state is **Done**.
5. Test the connection with a new pull request whose title or branch name
   contains a team-100 issue identifier such as `100-NNN`. Merge the pull
   request, then confirm that Linear moves the matching ticket to Done.

Closing a pull request without merging it does not exercise the **PR merged**
workflow and should not be expected to move the ticket to Done.

## 3. Choose where the repository will live

### Required for either bring-your-own path: install Symphony

Install the
[`1000lines-symphony` GitHub App](https://github.com/apps/1000lines-symphony/installations/new)
on the target repository:

1. Open the installation link and choose the personal account or organization
   that owns the repository.
2. Choose **Only select repositories** and select the target repository.
3. Review the permissions, then choose **Install**. The App reads Actions and
   checks and writes contents, workflows, issues, and pull requests so Symphony
   can create branches and PRs and respond to feedback.
4. If GitHub offers **Request** instead of **Install**, ask an organization owner
   to approve it. If approval cannot happen during the event, use the fork path.

You do not receive or configure this App's private key. Its signing key stays on
the hosted Symphony worker. The Cadence review App is installed separately using
one of the next two paths.

### Fast bring-your-own path: HackCadence

Keep the repository in its current account or organization and
[`install HackCadence`](https://github.com/apps/hackcadence/installations/new)
on only that repository:

1. Open the installation link and choose the personal account or organization
   that owns the repository.
2. Choose **Only select repositories** and select the target repository.
3. Review the grants, then choose **Install**. You need repository admin access.
4. If GitHub offers **Request** instead of **Install**, ask an organization owner
   to approve it. If approval cannot happen during the event, use the fork path.

Installing the App and configuring its Actions settings are separate steps; do
both for the same target repository.

Jeremy will invite you to a private event-credentials repository containing the
temporary private key. Configure these GitHub Actions settings at repository
scope, or through an organization grant that includes the repository:

| Setting | Kind | Value |
| --- | --- | --- |
| `CADENCE_APP_ID` | Variable | `4921338` |
| `CADENCE_APP_PRIVATE_KEY` | Secret | The temporary HackCadence PEM |
| `CADENCE_REVIEWER` | Variable | `hackcadence[bot]` |
| `SYMPHONY_BOT_USER` | Variable | `1000lines-symphony[bot]` |
| `CADENCE_LINEAR_API_TOKEN` | Secret | Your Linear API key |
| `CADENCE_OPENAI_API_KEY` | Secret | Your OpenAI API key for Codex review |
| `CADENCE_AI_REVIEW_ANTHROPIC_API_KEY` | Secret | Your Anthropic API key |
| `CADENCE_CLAUDE_MODEL` | Variable | `claude-opus-5` |

At least one provider key is required. An OpenAI key selects Codex, including
when both provider keys are present. Otherwise, an Anthropic key selects Claude
and requires `CADENCE_CLAUDE_MODEL=claude-opus-5`. The Claude path is tested;
the OpenAI-only event path still needs testing.

HackCadence is a shared event identity. Its private key can authenticate across
its event installations until it is revoked. At 4 p.m., Jeremy will delete the
HackCadence App, its key, and the private event-credentials repository.

### Isolated bring-your-own path: create a Cadence App

Create a Cadence GitHub App under your personal account or organization and
install it on the target repository. Use these repository permissions:

- Metadata, Contents, and Actions: read
- Pull requests, Issues, and Checks: read and write
- Everything else: no access

Disable webhooks and leave OAuth callbacks, client secrets, and event
subscriptions unused. Retain the App's numeric ID, PEM private key, and actual
`slug[bot]` login, then use them for the Actions settings in the table above.
The Symphony author identity remains `1000lines-symphony[bot]`; its signing key
is managed on the hosted worker.

### Fork path

1. Ask Jeremy to add you to the `1000lines` GitHub organization.
2. Fork your chosen repository into `1000lines`.
3. Clone the fork and enter its root directory.

The `1000lines` organization supplies the App installation, secrets, and
variables, so skip the GitHub App and Actions-setting instructions above. The
fork remains world-readable after the event, so you can copy its work later. At
4 p.m., its automation credentials will be disabled and your write access will
be removed.

## 4. Copy the Symphony/Cadence files

Check out the working repository and enter its root directory. The tested Copier
installation is Homebrew:

```sh
brew install copier
```

Then run:

```sh
copier copy -r main gh:1000lines/symphony-client-template .
```

Answer the prompts as follows:

| Prompt | Answer |
| --- | --- |
| Repository | The working `OWNER/REPO` |
| Default branch | The repository's default branch, usually `main` |
| Linear team key | `100` |
| Symphony App slug | `1000lines-symphony` |
| Cadence App slug | `hackcadence` for HackCadence; otherwise the installed App's actual slug |
| Reviewer | `claude` or `codex`; current execution chooses from the configured provider keys |
| Build command | The repository's build command |
| Test command | The repository's test command |

Review the generated changes and open the first setup pull request. Its CI will
probably need work: Copier adds Symphony CI files, but it cannot infer how the
repository's existing CI is structured or which checks it produces.

From the repository root, open Codex or Claude and ask it to connect the new
Symphony CI from Copier to the existing CI. Have it inspect both systems,
preserve the working application workflows, align the build and test commands,
and configure Symphony to recognize the real checks produced for the current PR
head. Add that integration to the same setup PR and let its CI run again.

A useful prompt is:

```text
Inspect this repository's existing CI and the Symphony CI/configuration added by
Copier. Connect them so the existing application checks still run and Symphony
can recognize the required current-head CI results. Preserve existing workflows,
update the generated Symphony configuration and callers where needed, run the
available checks, and add the changes to this setup PR.
```

Review and merge the setup PR only when its CI behavior is understood and the
integration is ready. The generated files must be on the default branch before
continuing.

Before creating the Linear project, run the generated **Symphony Client Setup**
workflow from the repository's Actions page, or use:

```sh
gh workflow run symphony-client-setup.yml --repo OWNER/REPO --ref DEFAULT_BRANCH
```

Inspect both **Check repository-visible settings** and **Verify job-visible
credentials**. Both jobs must pass. This probe catches a missing App
installation, a repository omitted from the installation, an incorrect App ID
or private key, and missing Linear or provider credentials before the first
live Cadence review. Fix the named input before retrying the workflow.

## 5. Set the shared tooling checkout

Clone `symphony-example` as a separate checkout outside the repository you are
working on:

```sh
git clone https://github.com/1000lines/symphony-example.git /absolute/path/to/symphony-example
```

Use the real absolute path on your machine. Start Codex from the participant
repository and tell it:

```text
Use /absolute/path/to/symphony-example as SYMPHONY_TOOLING_ROOT for this session.
```

Alternatively, export the value in the shell before starting Codex:

```sh
export SYMPHONY_TOOLING_ROOT=/absolute/path/to/symphony-example
```

`SYMPHONY_TOOLING_ROOT` points to shared Symphony planning and proof tooling; it
must not point to the participant repository.

## 6. Create and start the Linear project

Start Codex from the repository root. Have a conversation about the project:
explain the problem, share your notes and Markdown documents, and answer its
questions. When the project is clear, ask Codex to create a Symphony Linear
project using:

```text
.agents/skills/symphony-project-factory/SKILL.md
```

Choose when work starts:

- Ask Codex to put the tickets in **Active** to start immediately.
- Ask Codex to leave the first ticket in **Backlog** if you want to inspect the
  project in Linear first. Move it to **Active** when you are ready.

An Active ticket means the project has started. Open
<https://symphony.1000lines.dev> to watch Symphony work on it. If expected
activity does not appear, especially the creation of tickets in Linear, ask
Jeremy for help. Individual ticket state is mainly for troubleshooting; do not
manage the project ticket by ticket when the automation is progressing normally.

## 7. Review the work

When Symphony finishes a ticket, review its pull request. Cadence will normally
add an advisory review at low effort for faster event turnaround. Cadence's
approval does not satisfy merge requirements; you remain responsible for the
decision.

The first two pull requests deserve particular attention:

1. **Requirements and design:** confirm the acceptance criteria describe what
   you want and that the proposed approach makes sense.
2. **Plan:** inspect the task boundaries, dependencies, and proposed parallel
   work carefully. This plan controls the implementation fan-out.

For ordinary feedback, use GitHub's **Start a review** flow, collect your inline
comments, and submit them together with **Comment**. Do not approve while you
still want changes. When you are satisfied, submit **Approve** and merge the pull
request yourself. Reserve **Request changes** for a major failure.

Cadence normally decides when a draft is ready for review. If it is stuck asking
for validation that can only happen after merge, use your judgment and mark the
pull request **Ready for review** yourself.

After merge, the project should advance on its own: Linear tickets appear, ready
work starts, and focused implementation pull requests follow. Continue the same
review loop and escalate to Jeremy if the expected activity stops.
