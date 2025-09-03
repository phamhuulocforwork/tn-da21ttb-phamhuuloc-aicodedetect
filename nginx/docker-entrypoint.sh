#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

wait_for_service() {
    local host="$1"
    local port="$2"
    local service_name="$3"
    local max_attempts="${4:-30}"
    local attempt=1

    log_info "Waiting for ${service_name} at ${host}:${port}..."

    while [ $attempt -le $max_attempts ]; do
        if nc -z "$host" "$port" 2>/dev/null; then
            log_info "${service_name} is ready!"
            return 0
        fi

        log_info "Attempt ${attempt}/${max_attempts}: ${service_name} not ready yet..."
        sleep 2
        ((attempt++))
    done

    log_error "${service_name} failed to start within ${max_attempts} attempts"
    return 1
}

init_ssl() {
    log_info "Initializing SSL certificates..."

    if [ -f "/usr/local/bin/init-ssl.sh" ]; then
        /usr/local/bin/init-ssl.sh
    else
        log_error "SSL initialization script not found"
        exit 1
    fi
}

start_nginx() {
    log_info "Starting Nginx..."

    touch /var/log/nginx/access.log /var/log/nginx/error.log

    exec nginx -g "daemon off;"
}

main() {
    log_info "Starting AI Code Detection Nginx container..."

    if ! wait_for_service "${BACKEND_HOST:-backend}" "${BACKEND_PORT:-8000}" "Backend API"; then
        log_error "Backend service is not available, exiting..."
        exit 1
    fi

    if ! wait_for_service "${FRONTEND_HOST:-frontend}" "${FRONTEND_PORT:-3000}" "Frontend"; then
        log_error "Frontend service is not available, exiting..."
        exit 1
    fi

    init_ssl

    if [ -n "${SSL_DOMAIN}" ] && [ "${SSL_DOMAIN}" != "localhost" ]; then
        log_info "Setting up SSL certificate renewal cron job..."

        echo "0 12 * * * /usr/bin/certbot renew --quiet --no-self-upgrade" > /etc/crontabs/root
        echo "0 0 * * * /usr/local/bin/init-ssl.sh" >> /etc/crontabs/root

        crond -f -l 8 &
        log_info "SSL certificate renewal cron job configured"
    fi

    start_nginx
}

main "$@"
