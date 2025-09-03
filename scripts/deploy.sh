#!/bin/bash

set -e

# Colors for output
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

# Function to check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        log_error ".env file not found!"
        log_info "Please copy env.example to .env and configure your settings:"
        log_info "cp env.example .env"
        log_info "Then edit .env with your actual values"
        exit 1
    fi
}

# Function to check Docker and Docker Compose
check_docker() {
    log_step "Checking Docker installation..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi

    # Check for Docker Compose (v2 first, then v1)
    if command -v docker &> /dev/null && docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
        log_info "Docker Compose v2 is available"
    elif command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
        log_info "Docker Compose v1 is available"
    else
        log_error "Docker Compose is not installed or not in PATH"
        log_info "Please install Docker Compose:"
        log_info "  Ubuntu/Debian: apt install docker-compose-plugin"
        log_info "  Or install standalone: https://docs.docker.com/compose/install/"
        exit 1
    fi

    log_info "Docker and Docker Compose are available"
}

# Function to pull latest changes (if using git)
pull_latest_changes() {
    if [ -d ".git" ]; then
        log_step "Pulling latest changes from git..."
        git pull
        log_info "Latest changes pulled"
    else
        log_info "Not a git repository, skipping git pull"
    fi
}

# Function to stop existing containers
stop_containers() {
    log_step "Stopping existing containers..."
    $COMPOSE_CMD down || true
    log_info "Existing containers stopped"
}

# Function to clean up unused resources
cleanup_docker() {
    log_step "Cleaning up Docker resources..."
    docker system prune -f || true
    docker volume prune -f || true
    log_info "Docker resources cleaned up"
}

# Function to build and start containers
build_and_start() {
    log_step "Building and starting containers..."

    # Build with no cache for fresh builds
    if [ "$1" = "--no-cache" ]; then
        log_info "Building without cache..."
        $COMPOSE_CMD build --no-cache
    else
        $COMPOSE_CMD build
    fi

    # Start services
    $COMPOSE_CMD up -d

    log_info "Containers built and started"
}

# Function to wait for services to be ready
wait_for_services() {
    log_step "Waiting for services to be ready..."

    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if $COMPOSE_CMD exec -T nginx curl -f http://localhost/health &>/dev/null; then
            log_info "All services are ready!"
            return 0
        fi

        log_info "Waiting for services... (attempt ${attempt}/${max_attempts})"
        sleep 10
        ((attempt++))
    done

    log_error "Services failed to start within ${max_attempts} attempts"
    log_info "Check logs with: $COMPOSE_CMD logs"
    exit 1
}

# Function to show status
show_status() {
    log_step "Checking service status..."
    echo ""
    $COMPOSE_CMD ps
    echo ""
    log_info "Service URLs:"
    echo "  - HTTP:  http://localhost"
    echo "  - HTTPS: https://localhost (if SSL configured)"
    echo "  - API:   http://localhost/api"
    echo ""
    log_info "Useful commands:"
    echo "  - View logs: $COMPOSE_CMD logs -f"
    echo "  - Stop services: $COMPOSE_CMD down"
    echo "  - Restart services: $COMPOSE_CMD restart"
}

# Function to backup current deployment
backup_current() {
    if [ -d "data" ] || [ -d "logs" ]; then
        local backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
        log_step "Creating backup in ${backup_dir}..."

        mkdir -p "$backup_dir"

        # Backup data directory if exists
        if [ -d "data" ]; then
            cp -r data "$backup_dir/"
        fi

        # Backup logs if exists
        if [ -d "logs" ]; then
            cp -r logs "$backup_dir/"
        fi

        log_info "Backup created in ${backup_dir}"
    fi
}

# Main deployment function
deploy() {
    local no_cache=false
    local skip_backup=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-cache)
                no_cache=true
                shift
                ;;
            --skip-backup)
                skip_backup=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Usage: $0 [--no-cache] [--skip-backup]"
                exit 1
                ;;
        esac
    done

    log_info "🚀 Starting AI Code Detection System deployment..."
    echo ""

    # Pre-deployment checks
    check_env_file
    check_docker

    # Backup current deployment
    if [ "$skip_backup" = false ]; then
        backup_current
    fi

    # Deployment steps
    pull_latest_changes
    stop_containers
    cleanup_docker
    build_and_start "$no_cache"
    wait_for_services

    echo ""
    log_info "✅ Deployment completed successfully!"
    echo ""
    show_status
}

# Function to show help
show_help() {
    echo "AI Code Detection System - Deployment Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --no-cache    Rebuild all containers without cache"
    echo "  --skip-backup Skip creating backup before deployment"
    echo "  --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Normal deployment"
    echo "  $0 --no-cache         # Force rebuild all containers"
    echo "  $0 --skip-backup      # Skip backup (faster deployment)"
}

# Main script logic
case "${1:-}" in
    --help|-h)
        show_help
        ;;
    *)
        deploy "$@"
        ;;
esac
