setup-pre-commit:
	pip3 install pre-commit
	pre-commit install
	pre-commit install-hooks

dev:
	@echo "Setup test environment"
	pip3 install -r requirements-dev.txt
	pip3 install -e .

test:
	python -m pytest tests

test-cov:
	python -m pytest --cov="site_checker" --cov-report term-missing

run:
	docker-compose up --build -d

logs:
	docker-compose logs -f

clean:
	docker-compose stop
	docker-compose rm -f
