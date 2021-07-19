Dev Requirements
================

- flake8
- mock
- pytest
- bumpversion

Contribution Checklist
======================

- All patches must be signed. [Signing Commits](#signing-commits)
- All contributed code must conform to flake8. [Code Style](#code-style)
- All new code contributions must be accompanied by a test.
    - Tests must pass and coverage remain above 90%. [Unit & Integration Tests](#unit-&-integration-tests)
- Follow Semantic Versioning. [Versions & Releases](#versions-&-releases)

Versions & Releases
===================

**gceimgutils** adheres to Semantic versioning; see <http://semver.org/> for
details.

[bumpversion](https://pypi.python.org/pypi/bumpversion/) is used for
release version management, and is configured in `setup.cfg`:

```shell
$ bumpversion major|minor|patch
$ git push
$ git push --tags
```

Unit & Integration Tests
========================

New code should be covered by unit tests and all tests should pass.

The tests can be run via pytest.

```shell
$ pytest
```

Code Style
==========

Source should pass flake8 and pep8 standards.

```shell
$ flake8
$ flake8 gce*img
```

Signing Commits
===============

The repository and the code base patches sent for inclusion must be GPG
signed. See the GitHub article, [Signing commits using
GPG](https://help.github.com/articles/signing-commits-using-gpg/), for
more information.
