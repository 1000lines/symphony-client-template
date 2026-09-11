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

The current package includes CI/wakeup callers, review ingress, configuration,
and client skills. The review/handoff/cleanup callers and Codex provider wiring
are deferred. Selecting a reviewer records the choice; it does not install those
missing callers. CI/wakeup callers in this revision use
`1000lines/symphony-client-workflows@alpha`, including the trusted wakeup helpers.
The moving branch is intentional; [provenance](PROVENANCE.md#workflow-alpha-integration)
records the inspected commits, and [self-instantiation](SELF-ADOPTION.md) separates
the current public template render from the migration awaiting publication.

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
