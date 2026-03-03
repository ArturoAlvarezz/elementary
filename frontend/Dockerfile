# Multi-stage build for ARM64
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .

# Production stage - nginx
FROM nginx:alpine
RUN apk add --no-cache curl

# Copy static files
COPY --from=builder /app/index.html /usr/share/nginx/html/
COPY --from=builder /app/style.css /usr/share/nginx/html/
COPY --from=builder /app/app.js /usr/share/nginx/html/
RUN chmod 644 /usr/share/nginx/html/*

# Copy custom nginx config with API proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
