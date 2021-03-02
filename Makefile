# for developers
bootstrap-api:
	pip install -r requirements.txt; pip install -r requirements-dev.txt
.PHONY: bootstrap-api

# Run time dependencies
# for pipeline/AWS lambda
build-api:
	pip install -r requirements.txt
.PHONY: build-api