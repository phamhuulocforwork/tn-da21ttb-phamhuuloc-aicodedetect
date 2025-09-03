#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

update_system() {
    log_step "Updating system packages..."
    apt update && apt upgrade -y
    log_info "System updated"
}

install_docker() {
    log_step "Installing Docker and Docker Compose..."

    apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    systemctl start docker
    systemctl enable docker

    log_info "Docker installed and started"
}

configure_firewall() {
    log_step "Configuring firewall..."

    apt install -y ufw

    ufw allow ssh
    ufw allow 22

    ufw allow 80
    ufw allow 443

    echo "y" | ufw enable

    log_info "Firewall configured"
}

setup_log_rotation() {
    log_step "Setting up log rotation..."

    cat > /etc/logrotate.d/app-logs << EOF
/home/appuser/app/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 appuser appuser
    postrotate
        docker-compose -f /home/appuser/app/docker-compose.yml logs --no-color > /dev/null 2>&1 || true
    endscript
}
EOF

    log_info "Log rotation configured"
}

main() {
    log_info "🚀 Starting AI Code Detection VPS Setup..."
    echo ""

    check_root
    update_system
    install_docker
    configure_firewall
    setup_log_rotation
}

main "$@"
