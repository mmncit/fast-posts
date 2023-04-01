API=fast-post-api
IS_PORT ?= 8081

dev-requirements:
	pip install -r requirements_dev.txt

setup: dev-requirements
	pre-commit install

run-sql:
	uvicorn sql.main:app --reload

run-orm:
	uvicorn orm.main:app --reload
