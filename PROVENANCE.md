# Provenance

The primary source is
[`Orchestra-Bio/symphony-example`](https://github.com/Orchestra-Bio/symphony-example).
Credit its contributors for the upstream Symphony example and tooling from which
the `1000lines/symphony-example` development repository derives.

This package was developed at `templates/symphony-client/` in
[`1000lines/symphony-example`](https://github.com/1000lines/symphony-example)
and is now maintained in
[`1000lines/symphony-client-template`](https://github.com/1000lines/symphony-client-template).
`template/` alone maps to generated participant files.

The current distribution contains 26 generated paths, including twelve
skill/resource files for project factory, Linear GraphQL and replan. Per
[Jeremy's 100-63 decision](https://linear.app/1000lines/issue/100-63), the two
Karpathy skill files and their loading references are no longer bundled.
The conversion counts below describe earlier revisions.

CT-Q adds the question configuration, development documentation, tests, and CI.
The interface and layout follow the
[accepted plan at `873f511aea3e1d858e216d1a890ed1cd9a709d61`](https://github.com/1000lines/symphony-example/blob/873f511aea3e1d858e216d1a890ed1cd9a709d61/docs/symphony-plans/client-template/implementation-items.md#ct-q--define-and-test-the-seven-copier-answers)
and its linked design D4, amended by
[Jeremy's reviewer-choice decision](https://github.com/1000lines/symphony-example/pull/42#discussion_r3991277811)
to add the eighth answer, `cadence_reviewer` (`claude` or `codex`).
CT-Q's temporary question fixtures are synthetic examples. CT-T's separate
fixtures render the real client tree; the source mapping follows below.
CT-L gates the integrated release. No publication, installed host,
provider execution or live client operation is claimed here.

`LICENSE` is copied unchanged from the seed's Apache-2.0 license at that accepted
commit. The seed records its upstream extraction history in
[README.md](https://github.com/1000lines/symphony-example/blob/873f511aea3e1d858e216d1a890ed1cd9a709d61/README.md).
Retain source notices and record the reviewed source/destination commits when
the package is extracted. Copier and the Python dependencies retain their own
licenses; they are installed for tests, not copied into participant output.

Future publication uses a moving `alpha` branch selected by the operator's
`--vcs-ref=alpha`. Preserve ordinary `_src_path` and `_commit` in generated
answers, and record actual template/workflow/helper commits with each validation
run. A fixture commit proves only that fixture's rendering, not a public release
or every later `alpha` tip.

## Initial conversion — CT-T

CT-T starts from main `baa646a45721713231a1801c2271f524ccfc37ce`, containing the
accepted [CT-Q package (#42)](https://github.com/1000lines/symphony-example/pull/42)
and [corrected CT-M copy (#44)](https://github.com/1000lines/symphony-example/pull/44).
The [frozen client-copy manifest](https://github.com/1000lines/symphony-example/blob/baa646a45721713231a1801c2271f524ccfc37ce/docs/symphony-plans/client-template/client-copy.txt)
records all 22 source paths, modes and Git blobs at
`d5e9692b84c3f338014b964fd9713143fb723b55`. The
[inventory](https://github.com/1000lines/symphony-example/blob/baa646a45721713231a1801c2271f524ccfc37ce/docs/symphony-plans/client-template/client-inventory.md)
authorizes this conversion and its four new generated paths. Template sources
may gain `.jinja`; rendered names retain the inventory's paths.

| Copied source / generated path                                                                                   | Initial conversion                                                                                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.github/workflows/cadence-review-ingress.yml`                                                                   | Preserve native triggers, name, title fields and secret-free signal. Substitute App slugs plus `[bot]` only in login defaults.                                                                                               |
| `.symphony.cfg.json`                                                                                             | Team and serialized build/test arrays; reference `SYMPHONY.md`; native mode by omission, required checks explicitly unconfigured.                                                                                            |
| `.gitattributes`                                                                                                 | Unchanged generic planning rules; review merges with existing target rules.                                                                                                                                                  |
| Fourteen client skill/resource paths                                                                             | Retain paths/resources. Prefix external tooling references in factory/Linear guidance and five ticket resources with `SYMPHONY_TOOLING_ROOT`. Replan reads the client-local guide. No helper code or skill behavior changes. |
| `SYMPHONY.md`, `.github/symphony/REVIEW.md`, `.github/symphony/cadence-app-manifest.json`, `.copier-answers.yml` | New approved guidance, inert direct App manifest and ordinary Copier metadata.                                                                                                                                               |
| Five copied workflow bodies                                                                                      | Removed from output; CT-L's exact additions are listed below.                                                                                                                                                                |

The 21 initial paths were seven workflow/config/guidance/metadata files plus all
fourteen skills/resources. Six skill/resource files were byte-identical to the
copy: factory project-description, Linear agent metadata/helper, replan guide,
and Karpathy skill/examples. Eight Markdown files changed only path resolution.
That revision preserved the MIT declaration, Karpathy attribution and source
whitespace.
The seed NOTICE attribution is retained in generated `SYMPHONY.md`:
**Orchestra Bio symphony-example / Copyright 2026 Orchestra Bio, Inc.**
Generated output never replaces the application's LICENSE or NOTICE. The package
retains its Apache-2.0 license and primary-source credit above.

External tooling stays at the reviewed source `d5e9692` above with its own
README/locked dependencies. It supplies `scripts/symphony/runtime-bundle/workflow/WORKFLOW.md`,
`scripts/symphony/project-colors.ts`, `tools/symphony-dag/`, shared guides under
`docs/engineering/` and optional shared Linear helpers. These are references,
not extra client files. CT-O records actual client/tooling refs and verifies
session loading; replan's nested path, local guide and factory templates remain
in the generated client. Project-factory stays outside the unattended profile.

## Pending CT-L additions — publication gate

All paths below are under the generated `.github/workflows/` directory. None is
emitted as an empty stub, invented interface or raw reusable body.

| Generated path                       | Required reviewed boundary and remaining integration                                                                                                                                                                     |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `symphony-client-review.yml`         | CT-R events/manual/trigger entry points; name `Symphony Client Review`; explicit `cadence_reviewer` and App/Linear/optional OpenAI/Anthropic secrets. Verify selection/matching-key failure and advisory/ready behavior. |
| `symphony-client-handoff.yml`        | CT-R reusable feedback entry; ingress listener, App/Linear secrets only.                                                                                                                                                 |
| `symphony-client-review-cleanup.yml` | CT-R reusable cleanup; native completion listener for `Symphony Client Review`, App key only.                                                                                                                            |

CT-C's reviewed code exists on main through
[#45](https://github.com/1000lines/symphony-example/pull/45), merge
`fd383f5760a2ba62ea6f6295bd6dd21cc0cb9e9e`. The independent CI integration below
consumes that accepted artifact. CT-R's [#43](https://github.com/1000lines/symphony-example/pull/43)
proves App identity only; it does not supply the required provider interface.
CT-L must inspect actual accepted workflow artifacts, pin full seed refs,
verify explicit review secrets at every hop, exercise cancellation/recovery and
reconcile this remaining list before CT-U/O/V.
Existing application CI is retained; no default client Dockerfile is emitted.

## CT-L independent CI checkpoint

Base `7a7b2cc4f7875c2e8d7822ba3f9b20d6dd6f4ef0` includes accepted CT-T
[#47](https://github.com/1000lines/symphony-example/pull/47). This checkpoint
renders **23 paths**, adding two callers to CT-T's 21 while preserving all
fourteen skill/resource files, licenses and Copier source/version metadata.

| Generated caller              | Accepted workflow and helper source                                                                                       | Boundary                                                                                                             |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `symphony-client-ci.yml`      | `.github/workflows/symphony-client-commands.yml` at `1000lines/symphony-example@fd383f5760a2ba62ea6f6295bd6dd21cc0cb9e9e` | Exact target SHA and serialized build/test arrays; no named secrets. Optional when existing application CI suffices. |
| `symphony-client-wakeups.yml` | `.github/workflows/symphony-linear-wakeups.yml` and trusted helper checkout at the same full seed commit                  | Target/default branch, original event name/payload; only `CADENCE_LINEAR_API_TOKEN`.                                 |

Native/Docker/remote guidance uses CT-C's existing optional `ci.mode`; generated
config keeps the native omission and unconfigured required-check list. No
question, generic Dockerfile, workflow implementation or export list changes.
The external client-session tooling checkout advances to that accepted CT-C
merge so its reader supports `ci.mode`; the copied skill/resources remain
unchanged. Record hosted-reader compatibility separately before activating
explicit modes; a tooling checkout does not update the running host.

Seed render-check registration uses the observed `Client template tests` /
`.github/workflows/client-template-test.yml` / GitHub Actions App `15368`, from
CT-T head `9d185defbe2c8f2c6c0e5aa5bbd30520f0381b0a`,
[run 34634679441](https://github.com/1000lines/symphony-example/actions/runs/34634679441),
attempt 1. The workflow runs on every PR update, including template-only changes;
ordinary lint/format discovery still excludes raw templates. This records check
identity; the checkpoint PR records its own current-head validation.

**Waiting on CT-R artifact:** at this base the trigger has no `cadence_reviewer`
input or OpenAI secret declaration, events/manual calls still inherit internal
secrets, and handoff/cleanup have no `workflow_call`. The planned provider adapter
and common instructions in `review-export.txt` are absent. Existing
[early review evidence](https://github.com/1000lines/symphony-example/blob/7a7b2cc4f7875c2e8d7822ba3f9b20d6dd6f4ef0/docs/symphony-plans/client-template/early-review-evidence.md)
also leaves the real Codex proof open. Preserve 100-49's terminal acceptance;
Jeremy must identify the accepted follow-up artifact/proof for this remaining
CT-R work. Once it merges to main, CT-L can pin and integrate the three callers,
verify both explicit reviewer/key matrices and cleanup recovery, and close the
publication gate. This checkpoint cannot establish full CT-L acceptance.

The current tests establish rendering, config shape, expression preservation,
resource paths and collisions only. They do not establish publication, actual
skill loading, provider execution, runtime rollout or current-head review of a
consumer. Later `alpha` migration remains CT-F-owned as described above.

## Initial public publication

Imported from `1000lines/symphony-example@e362e5ad76fa8070ef27bf54fec9d6750195466c`. Jeremy directed publication of the available subset on September 11, 2026; prior completeness gates are deferred. Package CI runs tests from the parent directory to avoid recursive fixture copying. No seed files were changed.

## Workflow alpha integration

[100-57](https://linear.app/1000lines/issue/100-57) consumes the publications
accepted in [100-55](https://linear.app/1000lines/issue/100-55) and
[100-56](https://linear.app/1000lines/issue/100-56). Their current publication
decisions supersede the historical completeness gates above: integrate the
available subset and keep deferred reviewer functionality visible.

The initial September 11, 2026 readback resolved template `main` and `alpha` to
`58021a73ac3a6c2141a1217fc88c27e590df8143`, and workflow `main` and `alpha` to
`77cfb2d1f4e0e488af207096b1785b63ffc0398b`. Neither repository had an `alpha` tag.
The workflow publication's [mapping](https://github.com/1000lines/symphony-client-workflows/blob/77cfb2d1f4e0e488af207096b1785b63ffc0398b/PROVENANCE.md)
and [passing package CI](https://github.com/1000lines/symphony-client-workflows/actions/runs/34641368861)
identify the inspected code, not a migrated consumer run.

| Generated caller              | Workflow destination at literal `@alpha`                                             | Onward source and secrets                                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `symphony-client-ci.yml`      | `1000lines/symphony-client-workflows/.github/workflows/symphony-client-commands.yml` | Checks out the exact target SHA to run target commands; no named secrets or nested workflow calls.                         |
| `symphony-client-wakeups.yml` | `1000lines/symphony-client-workflows/.github/workflows/symphony-linear-wakeups.yml`  | Explicit `helpers-repository: 1000lines/symphony-client-workflows`, `helpers-ref: alpha`; only `CADENCE_LINEAR_API_TOKEN`. |

The wakeup workflow checks out those trusted helpers separately from the target
configuration. Its imported wakeup, Linear, workpad, actor and config-reader
dependencies exist at the recorded workflow commit. Both supported boundaries
declare the supplied inputs and secrets; neither makes an onward workflow call.
Review ingress remains a local, secret-free signal. The root uses the same
wakeup mapping and preserves its dedicated package CI instead of the optional
command caller. There are no active seed-workflow refs in emitted or root
callers; historical source/tooling references above remain valid.

The later accepted [100-64 template PR #6](https://github.com/1000lines/symphony-client-template/pull/6)
advanced template main to `d2dd1dd` and added five review/handoff/cleanup callers.
Its root Copier metadata records source `e8d6f36`; this migration preserves that
newer regeneration. Their workflow/helper pins remain
`ac15fc1567865eb738cd53409c6fddf297e78a09`: the latest workflow main/alpha readback
is still `77cfb2d1f4e0e488af207096b1785b63ffc0398b`. Those provider interfaces must
be published before the remaining callers can use literal `@alpha`.

All eight answers, explicit secret names, client resources and package CI are
preserved from main. PR #6 carries 100-64's newer key-presence provider contract,
superseding the older selection notes above. This integration does not establish
reviewer execution or cleanup recovery. After human acceptance, publish only
accepted main code to template `refs/heads/alpha`, repeat the public render and
record actual workflow/helper commits from live runs in [SELF-ADOPTION.md](SELF-ADOPTION.md).

## 100-98 status-comment revision

The generated review, handoff and recovery callers and `helpers-ref` now pin
shared workflows commit `ddc9eb0f2a1a24643b6350db9003ed27089548a6`, proposed in
[workflows PR #10](https://github.com/1000lines/symphony-client-workflows/pull/10).
This adds one editable Cadence status/result comment and a measured footer.
Accept that implementation before adopting these caller changes through Copier.
No alpha branch is advanced here. The root retains its recorded older Copier
source until a reviewed self-adoption; current-source render/update tests and
recorded-root tests remain separate. No live review execution is claimed by
these source changes.

## 100-99 single review message

The five template review/handoff/cleanup callers and their helpers pin
`1000lines/symphony-client-workflows@05451a7c520e295c415012cf468ec24e6460bb48`.
[100-99](https://linear.app/1000lines/issue/100-99) supersedes 100-98's duplicate
formal-review messaging. Cleanup also forwards the existing Linear token for
completion handoff recovery. The implementation is central; this package only
changes caller refs, secret forwarding and adopter guidance.

Accept the shared implementation before activating this template in a client.
Copier propagation and live review/check/Linear execution are separate evidence;
these template files alone do not claim deployment.
