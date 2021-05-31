setup:
	python3 -m venv .venv
	pip3 install pre-commit
	pip3 install --upgrade pip

setup-test:
	@echo "Setup test environment"
	pip3 install -r requirements-dev.txt
	pip3 install -e .

setup-pre-commit:
	pre-commit install
	pre-commit install-hooks
