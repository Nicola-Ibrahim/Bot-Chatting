# 🚀 Build and Run Guide

Choose the workflow that fits your development needs. Whether you want to preview the whole system quickly or dive deep into backend development, we have a path for you.

---

## 🏗️ Setup Options at a Glance

| Method | Best For... | Setup Time | Prerequisites |
| :--- | :--- | :--- | :--- |
| **[Docker (Full Stack)](docker.md)** | Getting started quickly, testing the whole flow. | ⚡ Fast | Docker, Docker Compose |
| **[Backend (Local)](backend.md)** | Debugging backend, running tests, iterating on API. | 🐢 Medium | Python 3.12+, `uv` |
| **[Frontend (Local)](frontend.md)** | UI development, styling, and JS-specific work. | 🐢 Medium | Node.js, `npm` |

---

## 🛠️ Prerequisites

Before you start, ensure you have the following installed:
- **[uv](https://docs.astral.sh/uv/)**: Our chosen Python package manager (highly recommended for its speed).
- **Docker & Docker Compose**: For the containerized environment.
- **Node.js**: If you plan to work on the frontend locally.

---

## 📋 General Workflow

1. **Clone the repository**.
2. **Environment Variables**: Use the templates provided (`.env.example` in modules) to create your local `.env` files.
3. **Choose your path**:
    - For a one-command setup: `docker compose -f docker-compose.dev.yml up --build`
    - For local backend: Follow the **[Local Backend Guide](backend.md)**.
    - For local frontend: Follow the **[Local Frontend Guide](frontend.md)**.

---

## 🧪 Verification

Once running, always verify your setup:
- **Health Check**: Visit `http://localhost:8000/health` (backend) or `http://localhost:3000` (frontend).
- **Interactive Docs**: Explore the API at `http://localhost/docs`.
- **Run Tests**: Execute `pytest` in the `backend/` directory to ensure your environment is healthy.

---

> [!NOTE]
> For detailed dependency management and backend-specific details, refer to the [Internal Backend Building Guide](../../backend/docs/processes/BUILDING.md).
