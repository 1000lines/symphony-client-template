# Symphony client template

Copier template for connecting a repository to Symphony. Only `template/` is
rendered into client repositories; root tests and documentation stay here.

## Use

Install Python 3.12 and Copier, then render into a scratch directory:

```sh
python -m pip install copier==9.18.2
copier copy --vcs-ref=alpha https://github.com/1000lines/symphony-client-template.git ./my-client
```

Answer the repository, branch, Linear team, App slugs, reviewer and build/test
questions. Review the generated diff before applying it to an existing repo.
Keep secrets out of answers and preserve existing application files.

After generation or update, use the generated
[Cadence onboarding skill](template/.agents/skills/cadence-onboarding/SKILL.md).
It covers every Cadence secret and identity/model variable, secure repository or
organization provisioning, and the native `Symphony Client Setup` probe. Record
files generated, credentials configured and live review verified separately;
secret presence and a successful probe do not establish live review readiness.

The package includes CI/wakeup, review event/manual, handoff and cleanup callers,
configuration, and client skills. Both provider secrets are explicitly forwarded:
`CADENCE_OPENAI_API_KEY` selects Codex, otherwise
`CADENCE_AI_REVIEW_ANTHROPIC_API_KEY` selects Claude. Both selects Codex; neither
fails early. The reviewer answer is an onboarding preference. See the generated
[review context](template/.github/symphony/REVIEW.md.jinja) for the exact secret
mapping and provisioning boundary with 100-62.

CI/wakeup callers in this revision use
`1000lines/symphony-client-workflows@alpha`, including the trusted wakeup helpers.
Review/handoff/cleanup callers retain their matching workflow/helper commit pins
until that implementation is published on workflow alpha. The moving branch is
intentional; [provenance](PROVENANCE.md#workflow-alpha-integration) records the
inspected commits, and [self-instantiation](SELF-ADOPTION.md) separates the public
template render from the migration awaiting publication.

## Development

Run the render tests from the parent directory so fixtures stay outside the package:

```sh
python -m pip install -r tests/requirements.txt
cd ..
python -m unittest discover -s symphony-client-template/tests -v
```

[Client guidance](template/SYMPHONY.md.jinja), [source provenance](PROVENANCE.md),
and [license](LICENSE).

## This repository uses its own template

The root client files are generated from the public template; reusable source
remains under `template/`. See [self-instantiation](SELF-ADOPTION.md) and
[recorded answers](.copier-answers.yml).
