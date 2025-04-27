# Backend Service

This is a backend service that provides user management functionality.

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── router.py
│   │   │   └── user.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── base.py
│   │   └── user.py
│   ├── repositories/
│   │   └── user.py
│   ├── schemas/
│   │   ├── base.py
│   │   └── user.py
│   ├── services/
│   │   └── user.py
│   ├── utils/
│   │   └── hashing.py
│   └── app.py
├── tests/
│   ├── __init__.py
│   └── test_users.py
├── migrations/
│   ├── versions
│   │   ├── __init__.py
│   │   └── 37ecd115a292_dfh.py
│   ├── __init__.py
│   ├── script.py.mako
│   └── env.py
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── poetry.lock
├── pyproject.toml
├── .gitignore
├── .env (not included in git repo)
└── README.md
```

## Makefile

### Development

- Use `make lint` to run linters
- Use `make format` to format code
- Use `make type-check` to format code

### Run

- Use `make migrations` to autogenerate migrations
- Use `make upgrade` to apply migrations on db
- Use `make run` to run all services

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
