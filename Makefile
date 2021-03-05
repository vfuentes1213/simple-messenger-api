# for developers
bootstrap-api:
	python3 -m venv msg-api-venv; source msg-api-venv/bin/activate; pip install -r requirements.txt; pip install -r requirements-dev.txt
.PHONY: bootstrap-api

# Run time dependencies
# for pipeline/AWS lambda?
build-api:
	pip install -r requirements.txt
.PHONY: build-api

run-coverage-report:
	pytest --cov=api api/__test__
.PHONY: run-coverage-report

format-files:
	black
.PHONY: format-files

start-api:
	python run.py
.PHONY: start-api