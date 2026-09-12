# Symphony client template

Copier template for connecting a repository to Symphony. Only `template/` is
rendered into client repositories; root tests and documentation stay here.

## Use

Install Python 3.12 and Copier, then render into a scratch directory:

```sh
python -m pip install copier==9.18.2
copier copy --vcs-ref=main https://github.com/1000lines/symphony-client-template.git ./my-client
```

Answer the repository, branch, Linear team, App identities, reviewer and build/test
questions. Review the generated diff before applying it to an existing repo.
Keep secrets out of answers and preserve existing application files.

Copy and update print a prerequisites checklist and ordered setup commands using
the chosen repository and branch. The editable suggestions are `main`, Linear
team `100`, author `1000lines-symphony[bot]` and reviewer
`jeremycarroll-cadence[bot]`. Either an App slug or its bot login is accepted:
manifests use the slug, while Actions identities add `[bot]` exactly once.
Existing answers stay in use on update, including the eight existing answer keys.

These are suggestions for the operator to replace with their own identities.
The supplied 1000lines inventory has App ID `4866513`, reviewer
`1000lines-cadence[bot]`, author `1000lines-symphony[bot]` and Claude model
`claude-opus-5`; the reviewer suggestion intentionally differs. All eight reference
settings had public-repository access on September 11, 2026. Their presence does
not grant another adopter access: use repository settings for personal owners,
or organization settings with target access and an eligible plan. Organization
settings are unavailable to private repositories on GitHub Free; repository
settings are the alternative ([GitHub scope guidance](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)).

Register or reuse the reviewer App first with the generated
[App setup command](template/.github/symphony/APP-SETUP.md). Separate Cadence and
Symphony JSON presets cover browser registration, secure key handoff and effective
installation readback. Registration still requires GitHub's browser approval.

After generation or update, use the generated
[Cadence onboarding skill](template/.agents/skills/cadence-onboarding/SKILL.md).
It covers every Cadence secret and identity/model variable, secure repository or
organization provisioning, and the native `Symphony Client Setup` probe. Record
files generated, credentials configured and live review verified separately;
secret presence and a successful probe do not establish live review readiness.

The generated wakeup caller also detects merge conflicts after base-branch pushes,
with scheduled recovery for unknown mergeability. See the generated
[conflict setup and evidence guide](template/SYMPHONY.md.jinja#merge-conflict-wakeups)
for permissions, publication order and live verification.

The package includes CI/wakeup, review event/manual, handoff and cleanup callers,
configuration, and client skills. Both provider secrets are explicitly forwarded:
`CADENCE_OPENAI_API_KEY` selects Codex, otherwise
`CADENCE_AI_REVIEW_ANTHROPIC_API_KEY` selects Claude. Both selects Codex; neither
fails early. The reviewer answer is an onboarding preference. See the generated
[review context](template/.github/symphony/REVIEW.md.jinja) for the exact secret
mapping and provisioning boundary with 100-62.

All generated CI, wakeup, review, handoff and cleanup callers use
`1000lines/symphony-client-workflows@main`, with `helpers-ref: main` wherever
helpers are checked out. Merged shared-workflow changes reach clients on their
next run without a template pin update. Client workflow definitions still update
through Copier. Third-party Actions retain their existing version pins.

## Development

Run the render tests from the parent directory so fixtures stay outside the package:

```sh
python -m pip install -r tests/requirements.txt
cd ..
python -m unittest discover -s symphony-client-template/tests -v
```

Run the App setup fixtures with `node --test tests/test-app-setup.mjs` from this
checkout (Node 20+). These fixtures do not register or install a live App.

[Client guidance](template/SYMPHONY.md.jinja), [source provenance](PROVENANCE.md),
and [license](LICENSE).

## This repository uses its own template

The root client files are generated from the public template; reusable source
remains under `template/`. See [self-instantiation](SELF-ADOPTION.md) and
[recorded answers](.copier-answers.yml).
