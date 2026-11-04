Change Log
##########

Unreleased
**********

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
