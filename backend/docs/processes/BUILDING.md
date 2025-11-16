# 🚀 **Setup and Run Guide**

## **Installing the Environment**

1. **Install `uv` Package Manager**
   The application uses the `uv` package manager for dependency management. Follow the steps below to install `uv`:

   - **Linux/MacOS:**
      Download the installer from [uv.sh](https://docs.astral.sh/uv/getting-started/installation/) and follow the installation instructions.

      or alternatively:

     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

   - **Windows:**
     Download the installer from [uv.sh](https://docs.astral.sh/uv/getting-started/installation/) and follow the installation instructions.

2. **Install Project Dependencies:**
   After installing `uv`, run the following command in the root directory of the project to install all dependencies:

    ```bash
    uv install
    ```

## **Setting Up the Environment**

1. **Create a `.env` File:**
   Use the template `.env.example` provided in the repository to create a `.env` file. Ensure you fill in the necessary environment variables such as:
   - `DATABASE_URL`
   - `JWT_SECRET_KEY`
   - Other configuration values.

2. **Verify the Environment Variables:**
   Double-check that all required variables are set correctly before proceeding.

3. **Install Dependencies:**
   Ensure you have Python and `uv` installed. Then, installing the decencies will be automatically by `uv` when running the application

4. **Apply Database Migrations:**
   Run the following command to apply database migrations:

   ```bash
   alembic upgrade head
   ```

## **Running the Application**

There are several ways to run the system depending on whether you want to use the backend APIs only or include the example frontend.

### 🧪 Running Unit Tests

To verify that the codebase is working correctly, run the tests from the project root:

```bash
pytest
```

### 🧠 Backend Only (Local)

If you only wish to run the FastAPI backend locally (without Docker), install dependencies via `uv` and start the server using uvicorn:

```bash
uvicorn src.api.main:app --reload --port 8000
```

After the server starts you can explore the API documentation at <http://127.0.0.1:8000/docs> or the alternative Redoc docs at <http://127.0.0.1:8000/redoc>.

### 🐳 Running with Docker Compose (Recommended)

The easiest way to spin up the entire stack—including the FastAPI backend, PostgreSQL, pgAdmin, NGINX and the example Next.js frontend—is via Docker Compose.  Two compose files are provided:

- `docker-compose.dev.yml` for development with hot reloading and convenient volume mounts.
- `docker-compose.prod.yml` for a production‑like environment.

To run the development stack, execute from the repository root:

```bash
docker compose -f docker-compose.dev.yml up --build
```

This command will:

- Build and start the FastAPI backend on the internal Docker network (`app`).
- Create a PostgreSQL database (`postgres_db`) and pgAdmin instance (`pgadmin`).
- Start an NGINX container that proxies API requests to the backend on port 80.
- Launch the example Next.js frontend (`frontend`) on port 3000 with hot reloading.  The UI communicates with the backend via the `BACKEND_URL` environment variable set in the compose file.

Once started, you can access:

- API docs at `http://localhost/docs` (via NGINX).
- Example UI at `http://localhost:3000`.

When you are finished, stop the services with `Ctrl+C` or `docker compose down`.

To build a production‑like stack (without hot reloading), run:

```bash
docker compose -f docker-compose.prod.yml up --build
```

This will run each service in production mode.  The frontend is served on port 3000 and the backend remains available via the proxy on port 80.  Adjust your `.env` and `.env.dev` files accordingly.

### 💻 Running the Example UI Outside Docker

To work on the frontend independently, navigate into the `frontend` directory and start the development server:

```bash
cd frontend
npm install
npm run dev
```

Copy `.env.local.example` to `.env.local` and update `BACKEND_URL` to point at your running backend (for example `http://127.0.0.1:8000`).  Open <http://localhost:3000> to interact with the API through the UI.  When deploying for production you can instead run `npm run build && npm start`.
