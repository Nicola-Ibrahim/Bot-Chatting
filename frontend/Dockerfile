# ---------- Build stage ----------
FROM node:18-alpine AS builder

# Disable Next.js telemetry
ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR /app

# Install dependencies using lockfile for reproducible builds
COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

# Copy the rest of the frontend source
COPY . .

# Build the production version of the Next.js app (Tailwind included)
RUN npm run build

# ---------- Runtime stage ----------
FROM node:18-alpine

ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app

# Copy built application and runtime deps from builder
COPY --from=builder /app ./

# Expose the Next.js port
EXPOSE 3000

# Start Next.js server
CMD ["npm", "start"]
