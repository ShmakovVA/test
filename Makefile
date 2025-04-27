.PHONY: run lint format type-check test clean clean-volumes clean-all db-init db-migrations db-upgrade

# Compose
run:
	docker-compose up --build

rebuild: clean
	docker-compose build --no-cache

clean:
	docker-compose down
	docker-compose rm -f

clean-volumes:
	docker-compose down -v
	docker-compose rm -f -v

clean-all:
	docker-compose down -v --rmi all
	docker-compose rm -f -v

scratch: clean-all
	docker-compose build --no-cache

# DB
db-migrations:
	SECRET_KEY=x poetry run litestar database make-migrations --autogenerate

db-upgrade:
	SECRET_KEY=x poetry run litestar database upgrade

# Codebase
lint:
	ruff check .

format:
	black .
	ruff check --fix .
	isort .

type-check:
	mypy app
