# redir_svc

URL redirect service with short links, click analytics, and JWT authentication.

## Stack

### Backend
- **Python 3.12** + **FastAPI** — async REST API
- **SQLAlchemy 2.0** (async) + **asyncpg** — PostgreSQL ORM
- **AuthX** — JWT auth (access/refresh tokens via cookies)
- **Redis** — caching redirects + batched click counter
- **Pydantic v2** — validation & settings
- **bcrypt** — password hashing
- **Poetry** — dependency management

### Frontend
- **React 18** + **TypeScript** — SPA
- **Vite** — bundler + dev server
- **Tailwind CSS** — styling
- **React Router** — routing
- **Axios** — HTTP client

### Infrastructure
- **Docker** multi-stage builds (test / production)
- **Docker Compose** — full stack (Postgres, Redis, FastAPI, Nginx)
- **Nginx** — reverse proxy + static files + SPA routing
- **GitHub Actions** — CI (lint + test)
- **Ruff** — linting & formatting

## Project structure

```
redir_svc/
├── backend/
│   ├── src/
│   │   ├── core/           # settings, security, exceptions, logger, middleware
│   │   ├── db/             # models, session, base
│   │   ├── cache/          # Redis cache layer
│   │   ├── modules/
│   │   │   ├── auth/       # register, login (router → service → repository)
│   │   │   └── redir/      # CRUD redirects (router → service → repository)
│   │   └── main.py         # FastAPI app
│   ├── tests/
│   │   ├── test_unit/      # unit tests (mocks)
│   │   └── test_api/       # integration tests (httpx + ASGI)
│   ├── Dockerfile
│   ├── docker-compose.prod.yml
│   ├── docker-compose.test.yml
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/            # axios + endpoint functions
│   │   ├── components/     # UI components
│   │   ├── context/        # auth provider
│   │   ├── pages/          # login, register, dashboard
│   │   └── types/          # TypeScript types
│   ├── Dockerfile
│   ├── vite.config.ts
│   └── tailwind.config.js
├── infra/
│   ├── docker-compose.yml  # production stack (redis, db, app, nginx)
│   └── nginx/
│       ├── Dockerfile      # multi-stage: builds frontend + nginx
│       └── nginx.conf      # reverse proxy + static files
└── .github/workflows/      # CI/CD
```

## Quick start

### Backend

```bash
cd backend

# install dependencies
poetry install

# copy env file
cp .env.example .env

# start dev server
uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

### Docker (production)

```bash
cd infra

# build and start all services (redis, db, app, nginx)
docker compose up --build -d

# stop
docker compose down

# stop and delete data
docker compose down -v
```

### VPS deploy

```bash
# install Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# re-login

# clone
git clone <repo> redir_svc
cd redir_svc

# create .env and add your server IP to CORS_ALLOWED_ORIGINS
cp backend/.env.example backend/.env

# run
cd infra
docker compose up --build -d
```

Open port 80 on VPS firewall. Access at `http://YOUR_SERVER_IP`.

### Frontend

```bash
cd frontend

# install dependencies
npm install

# start dev server (proxies /api to :8080)
npm run dev
```

## Dev commands

```bash
# ruff — lint
ruff check .

# ruff — auto-fix
ruff check --fix .

# ruff — format
ruff format .

# pytest — run all tests
pytest

# pytest — run with verbose output
pytest -v

# pytest — run only unit tests
pytest tests/test_unit/

# pytest — run only API tests
pytest tests/test_api/

# typecheck frontend
cd frontend && npx tsc --noEmit
```

## API endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/register` | No | Create account |
| `POST` | `/api/auth/login` | No | Sign in |
| `POST` | `/api/redir/add` | Yes | Create short URL |
| `GET` | `/api/redir/list` | Yes | List user's redirects |
| `DELETE` | `/api/redir/del/{url}` | Yes | Delete redirect |
| `GET` | `/go/{url}` | No | Redirect to target URL |
| `GET` | `/health` | No | Health check |

## Error format

Custom errors return `4xx` with:
```json
{
  "message": "Human readable message",
  "error_type": "ErrorClassName"
}
```

Pydantic validation errors return `422`:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "login"],
      "msg": "String should have at least 4 characters"
    }
  ]
}
```
