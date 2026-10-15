# Phase 0.3 - REST API with FastAPI + PostgreSQL

A **Notes CRUD API** built with FastAPI and PostgreSQL, mirroring patterns you'd use in Express + MongoDB.

## Concepts demonstrated

- **FastAPI routing** - `APIRouter` maps to Express routers
- **Pydantic models** - request/response validation (like Zod/Joi schemas)
- **SQLAlchemy ORM** - database models and async queries (like Mongoose)
- **Alembic migrations** - schema versioning (like Prisma migrate)
- **Middleware** - request logging on every HTTP call
- **Dependency injection** - `Depends(get_db)` injects a DB session per request
- **Auto-generated OpenAPI docs** - visit `/docs` or `/redoc`

## Stack

- Python 3.10+
- FastAPI + Uvicorn
- Pydantic + pydantic-settings
- SQLAlchemy 2.0 (async) + asyncpg
- PostgreSQL 17/18
- Alembic

## Setup

### 1. Virtual environment

```powershell
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create the PostgreSQL database

Using `psql` (adjust user/port if needed):

```sql
CREATE DATABASE notes_db;
```

Or from the shell:

```powershell
psql -U postgres -c "CREATE DATABASE notes_db;"
```

### 3. Configure environment

Copy the example env file and set your Postgres credentials:

```powershell
copy .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/notes_db
```

Format: `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE`

### 4. Run migrations

```powershell
alembic upgrade head
```

This creates the `notes` table in your database.

## Run

```powershell
uvicorn app.main:app --reload
```

Server: http://127.0.0.1:8000  
Interactive docs: http://127.0.0.1:8000/docs

Every request is logged to the terminal, for example:

```text
2026-09-07 11:30:00 | INFO | app.requests | GET /notes -> 200 (12.34 ms)
```

## API endpoints

| Method | Path           | Description        |
|--------|----------------|--------------------|
| GET    | `/`            | API info           |
| GET    | `/health`      | Health + DB ping   |
| GET    | `/notes`       | List all notes     |
| GET    | `/notes/{id}`  | Get one note       |
| POST   | `/notes`       | Create a note      |
| PUT    | `/notes/{id}`  | Update a note      |
| DELETE | `/notes/{id}`  | Delete a note      |

## Example requests

**Create a note**

```powershell
curl -X POST http://127.0.0.1:8000/notes -H "Content-Type: application/json" -d "{\"title\": \"Learn FastAPI\", \"content\": \"Build CRUD routes like Express\"}"
```

**List notes**

```powershell
curl http://127.0.0.1:8000/notes
```

**Health check (includes DB connection test)**

```powershell
curl http://127.0.0.1:8000/health
```

## Project structure

```
app/
├── main.py              # FastAPI app + middleware
├── config.py            # Settings from .env
├── database.py          # Async engine + session factory
├── db_models.py         # SQLAlchemy table models (ORM)
├── models.py            # Pydantic schemas (API layer)
├── crud.py              # Database queries
├── middleware/
│   └── logging.py       # Request logging middleware
└── routers/
    └── notes.py         # Notes routes
alembic/                 # Database migrations
.env                     # Local secrets (not committed)
```

## Express vs FastAPI cheat sheet

| Express / Mongoose       | FastAPI / SQLAlchemy              |
|--------------------------|-----------------------------------|
| `mongoose.model()`       | SQLAlchemy `class NoteDB(Base)`   |
| `Note.find()`            | `await db.execute(select(NoteDB))`|
| `app.use(middleware)`    | `app.add_middleware(...)`         |
| `req.body` validation    | Pydantic model parameter          |
| `.env` + `process.env`   | `.env` + `pydantic-settings`      |
| Prisma migrate           | `alembic upgrade head`            |

## Useful commands

```powershell
# Create a new migration after changing db_models.py
alembic revision --autogenerate -m "describe change"

# Apply pending migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1
```
