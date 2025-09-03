FROM nginx:alpine

RUN apk add --no-cache \
    certbot \
    certbot-nginx \
    openssl \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

RUN mkdir -p /etc/letsencrypt/live /var/www/certbot \
    && mkdir -p /etc/nginx/ssl \
    && mkdir -p /var/log/nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

COPY init-ssl.sh /usr/local/bin/init-ssl.sh
RUN chmod +x /usr/local/bin/init-ssl.sh

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

RUN openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048

EXPOSE 80 443

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]
