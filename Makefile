APP_SERVICE = backend
DB_SERVICE = db
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs

.PHONY: all

up:
	${DC} up --build -d

restart:
	${DC} restart

down:
	${DC} down

logs:
	${DC} logs --follow

logs_backend:
	${DC} logs --follow ${APP_SERVICE}

logs_db:
	${DC} logs --follow ${DB_SERVICE}

shell:
	${DC} exec ${APP_SERVICE} /bin/bash

ruff-check:
	${DC} exec -T ${APP_SERVICE} ruff check .

ruff-fix:
	${DC} exec -T ${APP_SERVICE} ruff check . --fix

mypy:
	${DC} exec -T ${APP_SERVICE} mypy --explicit-package-bases .

test:
	pytest . -vs

test-coverage:
	pytest --cov=. .

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1
