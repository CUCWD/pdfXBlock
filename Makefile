PYTHON ?= python

.PHONY: requirements_ci requirements_js upgrade
requirements_ci: requirements_js
	$(PYTHON) -m pip install -r requirements/ci.txt

requirements_js:
	npm ci --ignore-scripts --no-audit --no-fund

# Refresh tooling only. Runtime declarations and the Ulmo snapshot are maintained manually.
upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade:
	$(PYTHON) -m pip install -r requirements/pip.txt -r requirements/pip_tools.txt
	$(PYTHON) -m piptools compile --upgrade --strip-extras --no-emit-index-url --no-emit-trusted-host -o requirements/pip_tools.txt requirements/pip_tools.in
	$(PYTHON) -m piptools compile --upgrade --strip-extras --no-emit-index-url --no-emit-trusted-host -o requirements/ci.txt requirements/ci.in
	$(PYTHON) -m piptools compile --upgrade --strip-extras --no-emit-index-url --no-emit-trusted-host -o requirements/quality.txt requirements/quality.in
