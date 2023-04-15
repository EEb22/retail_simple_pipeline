up:
	docker compose --env-file ./env up --build -d

down:
	docker compose down

shell:
	docker exec -ti runner bash

run-etl:
	docker exec runner python /code/etl/run_etl.py

query-warehouse:
	docker exec -it  warehouse psql -U user online_store

format:
	docker exec runner python -m black -S --line-length 79 .

isort:
	docker exec runner isort .

pytest:
	docker exec runner python -m pytest -v /code/test

type:
	docker exec runner mypy --ignore-missing-imports /code

lint:
	docker exec runner flake8 /code

ci: isort format type lint pytest
