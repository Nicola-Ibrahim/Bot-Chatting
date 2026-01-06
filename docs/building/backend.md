# 🐍 Local Backend Setup

Choose this path if you want to develop, debug, or test the FastAPI backend directly on your host machine.

---

## 🛠️ Prerequisites

- **Python 3.12+**: [Download from python.org](https://www.python.org/downloads/)
- **uv**: Our chosen package manager. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **PostgreSQL**: A local instance running. [Download here](https://www.postgresql.org/download/)

---

## ⚙️ Environment Configuration

The backend uses a standard settings loader. For local development, it looks for an `.env.dev` file.

1. **Copy the example**:
   ```bash
   cp .env.example .env.dev
   ```
2. **Key Variables**:
   - `APP_DATABASE_URL`: Ensure this points to your local Postgres (e.g., `postgresql+asyncpg://user:pass@localhost:5432/db`).
   - `APP_SECRET_KEY`: Used for JWT signing.

---

## 🚀 Step-by-Step Launch

### 1. Install Dependencies
We use `uv` for lightning-fast installs.
```bash
cd backend
uv install
```

### 2. Apply Database Migrations
Ensures your local database schema is up-to-date.
```bash
cd backend
uv run alembic upgrade head
```

### 3. Start the Server
Run with hot-reloading for a smooth development experience.
```bash
cd backend
uv run uvicorn src.api.main:app --reload --port 8000
```

---

## 🧪 Verification & Docs

- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

> [!NOTE]
> If you are running the frontend locally as well, ensure it is configured to point to `http://127.0.0.1:8000` via its own environment variables.
