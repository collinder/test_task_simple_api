down: 
	docker compose down

init: startpd
	docker compose up

start: down
	docker compose up

startd: down
	docker compose up -d

startpd: down
	docker compose up postgres -d 

startp: down
	docker compose up postgres

config:
	docker compose config

delete:
	docker-compose down --volumes

alembic_gen: startpd
	docker-compose run --rm backend alembic revision --autogenerate

alembic_upgrade: startpd
	docker-compose run --rm backend alembic upgrade head

alembic_down: startpd
	docker-compose run --rm backend alembic downgrade base

alembic_h: startpd
	docker-compose run --rm backend alembic history

shell:
	docker compose exec backend /bin/bash

rebuild:
	docker compose build backend

guni: down startpd
	cd web; gunicorn app:app --config python:config.gunicorn -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_HOST=localhost -e POSTGRES_DB=postgres -e POSTGRES_PORT=5432

test: down startpd
	docker-compose run --rm backend pytest tests/test.py -v -s

	
