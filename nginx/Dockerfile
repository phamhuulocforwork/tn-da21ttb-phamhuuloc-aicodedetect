FROM nginx:alpine

# Install certbot and dependencies
RUN apk add --no-cache \
    certbot \
    certbot-nginx \
    openssl \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

# Create directories for SSL certificates and challenges
RUN mkdir -p /etc/letsencrypt/live /var/www/certbot \
    && mkdir -p /etc/nginx/ssl \
    && mkdir -p /var/log/nginx

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# Copy SSL certificate generation script
COPY init-ssl.sh /usr/local/bin/init-ssl.sh
RUN chmod +x /usr/local/bin/init-ssl.sh

# Copy custom entrypoint
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Create dhparam for better SSL security
RUN openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048

# Expose ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Use custom entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Default command
CMD ["nginx", "-g", "daemon off;"]
