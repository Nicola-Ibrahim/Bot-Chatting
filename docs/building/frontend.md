# ⚛️ Local Frontend Setup

Develop, style, and iterate on the Next.js user interface.

---

## 🛠️ Prerequisites

- **Node.js LTS**: [Download from nodejs.org](https://nodejs.org/)
- **npm** (included with Node) or **pnpm** (recommended for speed).

---

## 🚀 Quick Launch

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Environment Configuration
Copy the template and point it to your backend.
```bash
cp .env.example .env.local
```
- **Local Backend**: `BACKEND_URL=http://127.0.0.1:8000`
- **Docker Stack**: `BACKEND_URL=http://localhost`

### 3. Run Development Server
```bash
npm run dev
```

---

## 🌐 Next Steps

- **Open in Browser**: [http://localhost:3000](http://localhost:3000)
- **Production Build**: To test a production build locally, run `npm run build && npm start`.

---

> [!TIP]
> If you are using **pnpm**, you can use `pnpm install` and `pnpm dev` for even faster setup.
