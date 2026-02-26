# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

Ku-Pomogu — Russian-language online education platform (React frontend + FastAPI backend). See `README.md` for the tech stack summary.

### Architecture

| Service | Port | Notes |
|---------|------|-------|
| Backend (FastAPI) | 8000 | Uvicorn with `--reload` for dev |
| Frontend (React) | 3000 | `npm start` dev server |
| PostgreSQL 13.3 | 5432 | Docker container `postgres` |
| Redis | 6379 | Docker container `redis` (redis-stack image) |

### Starting infrastructure services

```bash
sudo dockerd &>/tmp/dockerd.log &
# Wait a few seconds, then:
sudo docker compose -f docker-compose-local.yml up -d postgres redis
```

### Running the backend

```bash
cd backend
set -a && source /workspace/.env && set +a
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Alembic migrations (run once after fresh DB or after new migrations):
```bash
cd backend && set -a && source /workspace/.env && set +a && poetry run alembic upgrade head
```

### Running the frontend

```bash
cd frontend
BROWSER=none PORT=3000 npm start
```

The frontend needs `REACT_APP_API_URL=http://localhost:8000/` — this is set in `frontend/.env`.

### Lint / Test commands

- **Backend lint:** `cd backend && poetry run ruff check .` (also `ruff format --check .`)
- **Frontend lint:** `cd frontend && npx eslint "**/*.{js,jsx}"`
- **Frontend tests:** `cd frontend && CI=true npm test` (no test files exist currently)

### Non-obvious gotchas

- **CORS:** `FRONT_URL` in `.env` must NOT have a trailing slash (use `http://localhost:3000`, not `http://localhost:3000/`), otherwise the browser origin won't match and frontend-to-backend requests will fail with network errors.
- **User registration via API fails** because it tries to send an activation email (SMTP). For local dev, create users directly in the DB and set `is_active=true`. Use the backend's `passlib` bcrypt context to hash passwords.
- **`pydantic-settings`** reads only from environment variables, not from `.env` files automatically. Always `source /workspace/.env` before running backend commands natively.
- **Subscription enum values** in the DB use the raw enum names (`NO_SUBSCRIPTION`, `DEMO`, `LEARN_ALL`), not the Russian display values from `SubscriptionType`.
- **Docker in the VM** requires `fuse-overlayfs` storage driver and `iptables-legacy` due to nested container constraints.
- **Node version:** Use Node 18 (matches the frontend Dockerfile). Available via nvm: `nvm use 18`.
- **Python version:** Use Python 3.11 (matches the backend Dockerfile). Poetry virtualenv is bound to it.
