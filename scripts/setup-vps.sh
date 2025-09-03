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

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "This script must be run as root"
        exit 1
    fi
}

# Function to update system
update_system() {
    log_step "Updating system packages..."
    apt update && apt upgrade -y
    log_info "System updated"
}

# Function to install Docker and Docker Compose
install_docker() {
    log_step "Installing Docker and Docker Compose..."

    # Install Docker
    apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    # Start and enable Docker
    systemctl start docker
    systemctl enable docker

    log_info "Docker installed and started"
}

# Function to configure firewall
configure_firewall() {
    log_step "Configuring firewall..."

    # Install ufw if not present
    apt install -y ufw

    # Allow SSH
    ufw allow ssh
    ufw allow 22

    # Allow HTTP and HTTPS
    ufw allow 80
    ufw allow 443

    # Enable firewall
    echo "y" | ufw enable

    log_info "Firewall configured"
}

# Function to setup log rotation
setup_log_rotation() {
    log_step "Setting up log rotation..."

    # Create logrotate config for app logs
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
