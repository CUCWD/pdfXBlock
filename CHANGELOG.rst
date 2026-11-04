Change Log
##########

Unreleased
**********

1.0.5 - 2026-11-04
******************

Added
=====

* Align tox environment ordering and GitHub automation with xblock-qualtrics-survey,
  including Python 3.11/3.12 and Django 4.2/5.2 tests, JavaScript lint, and Python quality checks.
* Add pinned CI tooling and a reproducible JavaScript dependency lock file.
* Add tag-based PyPI publishing, commit checks, issue automation, dependency update workflows,
  and pull request templates. Preserve the Ulmo dependency snapshot during tooling upgrades.

Changed
========

* Select Django per tox environment and retain ``ulmo`` as a Django 5.2.11 alias.
* Clean up Python formatting and remove unused JavaScript completion placeholders for lint checks.

1.0.4 - 2026-11-03
******************

Changed
========

* Move the package version to ``pdf/__init__.py`` and read it from ``setup.py``
  without importing runtime dependencies.
* Use the resource and settings helpers bundled with Ulmo's XBlock instead of
  requiring the legacy ``xblock-utils`` package.
* Import ``Fragment`` directly from ``web_fragments`` and declare Django, XBlock,
  web-fragments, and setuptools as unpinned direct runtime dependencies.
* Keep Ulmo dependency constraints isolated to standalone tests so the host
  edx-platform installation controls runtime versions.

Added
=====

* Add standalone rendering, Studio editing, and completion tests using Ulmo's
  Django 5.2.11 and XBlock 5.2.0 dependencies.
* Include this changelog in the source distribution.
