# 🐳 Docker Setup (Full Stack)

The fastest way to get the entire Horizon Chat System up and running is through Docker Compose. This starts the backend, frontend, database, and NGINX proxy in a single command.

---

## 🛠️ Prerequisites

- **Docker Desktop**: [Download and Install](https://www.docker.com/products/docker-desktop/) (includes Docker Compose).

---

## 🚀 Development Stack (Hot Reload)

Perfect for exploring the system or making quick changes.

```bash
docker compose -f docker-compose.dev.yml up --build
```

**Once the containers are running:**
- **Frontend UI**: [http://localhost:3000](http://localhost:3000)
- **API Documentation**: [http://localhost/docs](http://localhost/docs)
- **Database (PostgreSQL)**: Internal to the network.

---

## 🏗️ Production-Like Stack

Use this to see how the system behaves in a compiled, production-ready state.

```bash
docker compose -f docker-compose.prod.yml up --build
```

> [!IMPORTANT]
> In production mode, hot-reloading is disabled. You must rebuild the containers if you change the code.

---

## ⏹️ Stop and Clean Up

To stop all services:
```bash
docker compose -f docker-compose.dev.yml down
```

To reset the database (remove all data):
```bash
docker compose -f docker-compose.dev.yml down -v
```

---

> [!TIP]
> If you encounter ports conflicts (e.g., port 80 or 3000 already in use), you can adjust the port mappings in the `docker-compose.dev.yml` file.
