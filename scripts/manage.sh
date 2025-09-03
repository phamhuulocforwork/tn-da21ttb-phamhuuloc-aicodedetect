#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

show_usage() {
    echo "AI Code Detection System - Management Script"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  status          Show service status"
    echo "  logs [service]  Show logs (all services or specific service)"
    echo "  restart         Restart all services"
    echo "  stop            Stop all services"
    echo "  start           Start all services"
    echo "  rebuild         Rebuild and restart services"
    echo "  backup          Create backup of data and logs"
    echo "  cleanup         Clean up Docker resources"
    echo "  ssl-renew       Renew SSL certificates"
    echo "  ssl-status      Check SSL certificate status"
    echo "  health          Check service health"
    echo "  shell <service> Open shell in container"
    echo ""
    echo "Examples:"
    echo "  $0 status"
    echo "  $0 logs nginx"
    echo "  $0 restart"
    echo "  $0 shell backend"
}

check_services() {
    if ! docker-compose ps | grep -q "Up"; then
        log_error "Services are not running. Use '$0 start' to start them."
        exit 1
    fi
}

cmd_status() {
    log_step "Service Status:"
    echo ""
    docker-compose ps
    echo ""
    log_info "Service URLs:"
    echo "  - HTTP:  http://localhost"
    echo "  - HTTPS: https://localhost (if SSL configured)"
    echo "  - API:   http://localhost/api"
}

cmd_logs() {
    local service="${1:-}"

    if [ -n "$service" ]; then
        log_step "Showing logs for $service..."
        docker-compose logs -f "$service"
    else
        log_step "Showing logs for all services..."
        docker-compose logs -f
    fi
}

cmd_restart() {
    log_step "Restarting all services..."
    docker-compose restart
    log_info "Services restarted"
}

cmd_stop() {
    log_step "Stopping all services..."
    docker-compose down
    log_info "Services stopped"
}

cmd_start() {
    log_step "Starting all services..."
    docker-compose up -d
    log_info "Services started"
}

cmd_rebuild() {
    log_step "Rebuilding and restarting services..."
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    log_info "Services rebuilt and restarted"
}

cmd_backup() {
    local backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
    log_step "Creating backup in ${backup_dir}..."

    mkdir -p "$backup_dir"

    if docker volume ls | grep -q "tn-da21ttb-phamhuuloc-aicodedetect"; then
        log_info "Backing up Docker volumes..."
        docker run --rm -v "$(pwd)":/backup \
            -v tn-da21ttb-phamhuuloc-aicodedetect_nginx_logs:/nginx_logs \
            -v tn-da21ttb-phamhuuloc-aicodedetect_nginx_ssl:/nginx_ssl \
            -v tn-da21ttb-phamhuuloc-aicodedetect_letsencrypt:/letsencrypt \
            alpine tar czf "/backup/${backup_dir}/volumes.tar.gz" -C / nginx_logs nginx_ssl letsencrypt 2>/dev/null || true
    fi

    cp docker-compose.yml "$backup_dir/" 2>/dev/null || true
    cp .env "$backup_dir/" 2>/dev/null || true
    cp nginx/nginx.conf "$backup_dir/" 2>/dev/null || true
    cp nginx/conf.d/default.conf "$backup_dir/" 2>/dev/null || true

    cat > "${backup_dir}/README.md" << EOF

Created: $(date)
Location: $(pwd)/${backup_dir}

This backup contains:
- Docker volumes (nginx logs, ssl certificates, letsencrypt data)
- Configuration files (docker-compose.yml, .env, nginx configs)

To restore:
1. Stop all services: docker-compose down
2. Restore volumes: docker run --rm -v \$(pwd):/backup -v nginx_logs:/nginx_logs alpine tar xzf /backup/${backup_dir}/volumes.tar.gz
3. Copy config files back
4. Start services: docker-compose up -d
EOF

    log_info "Backup created successfully in ${backup_dir}"
}

cmd_cleanup() {
    log_step "Cleaning up Docker resources..."

    docker-compose down

    docker system prune -f

    log_warn "Removing unused volumes..."
    docker volume prune -f

    docker image prune -f

    log_info "Docker cleanup completed"
}

cmd_ssl_renew() {
    check_services

    log_step "Renewing SSL certificates..."
    docker-compose exec nginx certbot renew --quiet

    docker-compose exec nginx nginx -s reload

    log_info "SSL certificates renewed and nginx reloaded"
}

cmd_ssl_status() {
    check_services

    log_step "SSL Certificate Status:"
    echo ""
    docker-compose exec nginx certbot certificates
}

cmd_health() {
    log_step "Health Check:"

    if docker-compose ps | grep -q "Up"; then
        log_info "✅ Containers are running"
    else
        log_error "❌ Containers are not running"
        return 1
    fi

    if docker-compose exec -T nginx curl -f http://localhost/health &>/dev/null; then
        log_info "✅ Nginx health check passed"
    else
        log_error "❌ Nginx health check failed"
    fi

    if docker-compose exec -T backend curl -f http://localhost:8000/health &>/dev/null; then
        log_info "✅ Backend health check passed"
    else
        log_error "❌ Backend health check failed"
    fi

    if docker-compose exec -T frontend curl -f http://localhost:3000 &>/dev/null; then
        log_info "✅ Frontend health check passed"
    else
        log_error "❌ Frontend health check failed"
    fi
}

cmd_shell() {
    local service="$1"

    if [ -z "$service" ]; then
        log_error "Please specify a service name"
        echo "Available services: backend, frontend, nginx"
        exit 1
    fi

    check_services

    case "$service" in
        backend|frontend|nginx)
            log_step "Opening shell in $service container..."
            docker-compose exec "$service" sh
            ;;
        *)
            log_error "Unknown service: $service"
            echo "Available services: backend, frontend, nginx"
            exit 1
            ;;
    esac
}

main() {
    local command="$1"
    shift

    case "$command" in
        status)
            cmd_status
            ;;
        logs)
            cmd_logs "$@"
            ;;
        restart)
            cmd_restart
            ;;
        stop)
            cmd_stop
            ;;
        start)
            cmd_start
            ;;
        rebuild)
            cmd_rebuild
            ;;
        backup)
            cmd_backup
            ;;
        cleanup)
            cmd_cleanup
            ;;
        ssl-renew)
            cmd_ssl_renew
            ;;
        ssl-status)
            cmd_ssl_status
            ;;
        health)
            cmd_health
            ;;
        shell)
            cmd_shell "$@"
            ;;
        *)
            log_error "Unknown command: $command"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

main "$@"
