# AI CI/CD Failure Analyzer

AI CI/CD Failure Analyzer is a full-stack application for collecting workflow
run failures, storing failure logs, and producing structured analysis of
pipeline problems.

## Stack

- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL, and Pydantic Settings
- **Frontend:** Next.js, React, TypeScript, and Tailwind CSS
- **Local infrastructure:** Docker Compose for PostgreSQL

## Project structure

```text
backend/
  app/
    api/          HTTP routes
    core/         configuration and database setup
    models/       SQLAlchemy models
    schemas/      API schemas
    services/     application services
  migrations/     Alembic migrations
frontend/
  src/app/        Next.js application
docker-compose.yml
```

## Prerequisites

- Python 3.11 or newer
- Node.js 20 or newer, or Bun 1.4+
- Docker Desktop

## Getting started

1. Copy the example environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Start PostgreSQL:

   ```powershell
   docker compose up -d postgres
   ```

3. Create a Python environment and install the backend dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r backend\requirements.txt
   ```

4. Run database migrations:

   ```powershell
   cd backend
   alembic upgrade head
   ```

5. Start the API from the `backend` directory:

   ```powershell
   uvicorn app.main:app --reload
   ```

   The API is available at <http://localhost:8000>. Interactive API
   documentation is available at <http://localhost:8000/docs>.

6. Install frontend dependencies and start the Next.js development server:

   ```powershell
   cd frontend
   bun install
   bun run dev
   ```

   The web application is available at <http://localhost:3000>.

## Configuration

Runtime configuration is loaded from `.env`. Use `.env.example` as the
template, and do not commit `.env` or other credentials. The default local
configuration connects the API to the PostgreSQL instance started by
`docker-compose.yml`.

## API areas

The versioned API is mounted under `/api/v1` and currently includes routes for:

- Health checks
- Repositories
- Workflow runs
- Failure logs
- AI analyses

## Development checks

From `frontend`, run:

```powershell
bun run lint
bun run build
```

Backend tests and type checks can be added alongside the corresponding
application modules as the project grows.

## License

No license has been selected yet.
