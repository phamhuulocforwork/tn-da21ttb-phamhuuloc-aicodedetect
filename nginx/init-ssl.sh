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

generate_selfsigned() {
    log_info "Generating self-signed certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/selfsigned.key \
        -out /etc/nginx/ssl/selfsigned.crt \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    log_info "Self-signed certificate generated"
}

get_letsencrypt_cert() {
    local domain="$1"
    local email="$2"

    if [ -z "$domain" ]; then
        log_error "Domain not provided, skipping Let's Encrypt certificate"
        return 1
    fi

    if [ -z "$email" ]; then
        log_warn "Email not provided, using default email for Let's Encrypt"
        email="admin@${domain}"
    fi

    log_info "Requesting Let's Encrypt certificate for ${domain}..."

    mkdir -p "/etc/letsencrypt/live/${domain}"

    certbot certonly \
        --standalone \
        --non-interactive \
        --agree-tos \
        --email "${email}" \
        --domain "${domain}" \
        --http-01-port=80 \
        --cert-name "${domain}" \
        --logs-dir /var/log/certbot \
        --config-dir /etc/letsencrypt \
        --work-dir /var/lib/certbot \
        --preferred-challenges http-01

    if [ $? -eq 0 ]; then
        log_info "Let's Encrypt certificate obtained successfully"

        mkdir -p /etc/letsencrypt/live/default
        ln -sf "/etc/letsencrypt/live/${domain}/fullchain.pem" /etc/letsencrypt/live/default/fullchain.pem
        ln -sf "/etc/letsencrypt/live/${domain}/privkey.pem" /etc/letsencrypt/live/default/privkey.pem

        return 0
    else
        log_error "Failed to obtain Let's Encrypt certificate"
        return 1
    fi
}

main() {
    local domain="${SSL_DOMAIN:-}"
    local email="${SSL_EMAIL:-}"
    local use_staging="${SSL_STAGING:-false}"

    log_info "Initializing SSL certificates..."

    export SSL_DOMAIN="$domain"
    export SSL_EMAIL="$email"

    generate_selfsigned

    if [ -n "$domain" ] && [ "$domain" != "localhost" ]; then
        if [ "$use_staging" = "true" ]; then
            log_info "Using Let's Encrypt staging environment"
            export CERTBOT_FLAGS="--staging"
        fi

        if get_letsencrypt_cert "$domain" "$email"; then
            log_info "SSL initialization completed successfully"
        else
            log_warn "Using self-signed certificate as fallback"
        fi
    else
        log_info "Domain not specified, using self-signed certificate"
    fi
}

main "$@"
