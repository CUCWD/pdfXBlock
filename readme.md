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
platform commit `46c543590c78aa1bfa846d47a4f1c5c6ec388490`, including Django
5.2.11 and XBlock 5.2.0. Refresh this snapshot when updating the target platform.
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
