init: startpd
	docker compose up

start:
	docker compose up

startd:
	docker compose up -d

startpd:
	docker compose up postgres -d 

startp:
	docker compose up postgres

down:
	docker compose down

config:
	docker compose config

delete:
	docker-compose down --volumes

alembic_gen:
	alembic --config ./web/alembic.ini revision --autogenerate

alembic_upgrade:
	alembic --config ./web/alembic.ini upgrade head

shell:
	docker compose exec backend /bin/bash

rebuild:
	docker compose build backend

guni: down startpd
	cd web; gunicorn app:app --config python:config.gunicorn -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_HOST=localhost -e POSTGRES_DB=postgres -e POSTGRES_PORT=5432

test: down startpd
	docker-compose run --rm backend pytest tests/test.py -v -s
