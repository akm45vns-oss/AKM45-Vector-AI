# ─────────────────────────────────────────────────────────────
# Frontend Dockerfile — Multi-stage build
# Stage: development  → hot reload with Next.js turbopack
# Stage: production   → optimised static build with standalone output
# ─────────────────────────────────────────────────────────────

FROM node:20-alpine AS base

WORKDIR /app
ENV NODE_ENV=development

# ─────────────────────────────────────────────────────────────
# Dependencies stage
# ─────────────────────────────────────────────────────────────
FROM base AS deps

# Install dependencies based on the preferred package manager
COPY package.json package-lock.json* ./
RUN npm ci

# ─────────────────────────────────────────────────────────────
# Development stage
# ─────────────────────────────────────────────────────────────
FROM base AS development

COPY --from=deps /app/node_modules ./node_modules
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]

# ─────────────────────────────────────────────────────────────
# Build stage
# ─────────────────────────────────────────────────────────────
FROM base AS builder

ENV NODE_ENV=production

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Generate the production build
RUN npm run build

# ─────────────────────────────────────────────────────────────
# Production stage
# ─────────────────────────────────────────────────────────────
FROM node:20-alpine AS production

ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy standalone build output
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

CMD ["node", "server.js"]
