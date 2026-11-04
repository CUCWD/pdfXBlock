# xblock-pdf

[![Build Status](https://circleci.com/gh/IONISx/xblock-pdf.svg?style=svg)](https://circleci.com/gh/IONISx/xblock-pdf)

> Course component (Open edX XBlock) that provides an easy way to embed a PDF

## Features

- Download button available
- (Optional) Source document download button, for example to provide your PPT file
- Create tracking logs:
  - `edx.pdf.loaded` when a student loads the PDF
  - `edx.pdf.downloaded` when a student downloads the PDF

## Customize the XBlock

By default, PDF Download Allowed is set to `True`.
The default value can  be changed in `xblock-pdf/pdf/ pdf.py`

## Ulmo dependency compatibility

Install this plugin into an environment already provisioned with Ulmo's
`openedx-platform/requirements`. Runtime dependencies are unpinned so the host
platform controls their versions. To install without changing shared packages,
run from this repository:

```shell
python -m pip install --no-deps .
python -m pip check
```

The plugin uses the resource and settings helpers included in XBlock;
`xblock-utils` is no longer required. Its package version is defined in
`pdf/__init__.py` and read by `setup.py` without importing Django.

Run standalone Python tests in an isolated environment with `tox -e ulmo`.
`requirements/ulmo-constraints.txt` records the shared runtime versions from
platform commit `46c543590c78aa1bfa846d47a4f1c5c6ec388490`, including XBlock 5.2.0.
Django is selected by tox: 5.2.11 for Ulmo, or 4.2 for compatibility tests. Refresh this snapshot when updating the target platform.
These tests cover rendering, editing, and completion events with a mock runtime;
full LMS integration still requires edx-platform.

## Install / Update the XBlock

Add it to the `EDXAPP_EXTRA_REQUIREMENTS` variable.

```yml
EDXAPP_EXTRA_REQUIREMENTS:
  - name: 'git+https://github.com/IONISx/xblock-pdf.git@v1.0.0#egg=xblock-pdf'
```

Then run your deployment playbooks.

### Restart your Open edX processes

```shell
sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:
```

# Use the XBlock

### Activate the XBlock in your course

Go to `Settings -> Advanced Settings` and set `advanced_modules` to `["pdf"]`.

### Use the XBlock in a unit

Select `Advanced -> PDF` in your unit.

## Development environment

For the code quality environment, you need to install both Python and JavaScript requirements.

Run the following:

    npm install -g grunt-cli
    npm install

Then, preferably in a [virtualenv](https://virtualenv.pypa.io), run

    pip install -r requirements.txt


Then, run `grunt test` to assess code quality.

## License

GNU Affero General Public License 3.0 (AGPL 3.0)

## GitHub automation and tox

The tox layout and GitHub workflows follow `xblock-qualtrics-survey`. CI runs
`django42`, `django52`, `quality`, and `eslint` on Python 3.11 and 3.12 with
`ubuntu-latest`. Tests exercise PDF's standalone unittest suite and generate
coverage reports in `htmlcov/`. No platform checkout is required.

```shell
python -m pip install -r requirements/pip.txt
make requirements_ci
tox
```

The default matrix requires both Python versions and Node/npm. With one Python
interpreter installed, use `tox -e django42,django52,quality,eslint`.
`tox -e ulmo` remains an alias for Ulmo's Django 5.2.11; `tox -e clean` erases
coverage data. Quality checks use pycodestyle and isort. PDF has no standalone
CSS files or Transifex project configuration, so those Qualtrics environments
are omitted. ESLint checks PDF's JavaScript with the recommended rules and its
browser/jQuery globals.

The GitHub directory includes tag-based PyPI publishing, commit lint, issue
label/assignment and DEPR routing workflows, Dependabot, Renovate, and pull
request templates. PyPI publishing needs `PYPI_UPLOAD_TOKEN`; DEPR routing needs
the GitHub App and Slack secrets named in that workflow. These workflows run
only after the configuration is pushed and the relevant events occur.

`make upgrade` regenerates tooling locks under the existing Ulmo constraints.
The requirements workflow can create update PRs using the repository token or
configured requirements bot credentials. Refresh `requirements/ulmo-constraints.txt`,
`requirements/pip.txt`, and the Django pin in tox manually when changing Ulmo
versions. Runtime dependencies remain unpinned in package metadata.
