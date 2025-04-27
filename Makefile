.PHONY: run lint format type-check test clean clean-volumes clean-all db-init db-migrations db-upgrade

run:
	docker-compose up --build

db-migrations:
	SECRET_KEY=x poetry run litestar database make-migrations --autogenerate

db-upgrade:
	SECRET_KEY=x poetry run litestar database upgrade

lint:
	ruff check .

format:
	black .
	ruff check --fix .
	isort .

type-check:
	mypy app

clean:
	docker-compose down
	docker-compose rm -f

clean-volumes:
	docker-compose down -v
	docker-compose rm -f -v

clean-all:
	docker-compose down -v --rmi all
	docker-compose rm -f -v