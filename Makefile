.PHONY: install-requirements
install-requirements:
	pip install -r requirements.txt

.PHONY: format
format:
	black *.py && isort *.py

.PHONY: run-sync-jobs
run-sync-jobs:
	python main.py