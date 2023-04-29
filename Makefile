# Virtual Environment
POETRY_RUN	:= poetry run

# Configuration
FILE_TOML 	:= pyproject.toml

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: lint
lint:
	$(POETRY_RUN) black .
	$(POETRY_RUN) isort .
	$(POETRY_RUN) mypy retirement_accelerator
