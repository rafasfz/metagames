# MetaGames

## Running in develop

```bash
    poetry install
    docker compose up -d
    cp .env.example .env
    alembic upgrade head
    fastapi dev src/main.py
``` 

## Run tests
```bash
    poetry install
    pytest src
```