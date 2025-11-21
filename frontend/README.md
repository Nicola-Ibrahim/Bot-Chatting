<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1vqOh3dFsGnYssbcS9X96urmAQiIg72Ut

## Run Locally

**Prerequisites:** Node.js 18+, Docker (optional but recommended)

1. Install dependencies: `npm install`
2. Configure the backend proxy by creating `.env.local` (or exporting env vars) with at least:
   ```env
   BACKEND_URL=http://localhost:8000
   BACKEND_CHAT_PATH=/api/chat
   BACKEND_TITLE_PATH=/api/title
   # Optional: change if the frontend proxy is mounted elsewhere
   NEXT_PUBLIC_FRONTEND_API_BASE=/api
   ```
   When running everything via `docker-compose.dev.yml`, the `frontend` service sets `BACKEND_URL=http://app:8000` automatically.
3. Start the Next.js dev server: `npm run dev`
4. Open `http://localhost:3000` to use the app. All chat and title requests are proxied through `/api/chat` and `/api/title` and forwarded to the FastAPI backend—no external LLM API key is required.
