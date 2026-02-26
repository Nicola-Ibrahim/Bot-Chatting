# ============================================================
#  Stage 1 — deps: install all dependencies
# ============================================================
FROM node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

# ============================================================
#  Stage 2 — dev: hot-reload development server
#  Usage:  docker compose build --target dev
# ============================================================
FROM deps AS dev
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
# Source code is bind-mounted via docker-compose volumes
EXPOSE 3000
CMD ["npm", "run", "dev"]

# ============================================================
#  Stage 3 — builder: compile production bundle
# ============================================================
FROM deps AS builder
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app
COPY . .
RUN npm run build

# ============================================================
#  Stage 4 — runner: minimal production image
#  Usage:  docker compose build  (default target)
# ============================================================
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser  --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
