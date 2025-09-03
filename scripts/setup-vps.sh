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

# Function to create app user
create_app_user() {
    local username="${1:-appuser}"

    log_step "Creating application user: $username"

    # Create user
    useradd -m -s /bin/bash "$username"

    # Add to docker group
    usermod -aG docker "$username"

    # Create app directory
    mkdir -p "/home/$username/app"
    chown "$username:$username" "/home/$username/app"

    log_info "User $username created and configured"
}

# Function to setup SSH hardening
# setup_ssh_hardening() {
    log_step "Setting up SSH hardening..."

    # Backup original config
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

    # Configure SSH
    cat >> /etc/ssh/sshd_config << EOF

# SSH Hardening
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
EOF

    # Restart SSH
    systemctl restart ssh

    log_warn "SSH hardened. Make sure you have SSH key authentication set up!"
    log_info "You can add your public key with: ssh-copy-id user@server"
}

# Function to install monitoring tools
install_monitoring() {
    log_step "Installing monitoring tools..."

    # Install htop, iotop, and other monitoring tools
    apt install -y htop iotop ncdu tree curl wget vim git

    # Install fail2ban for SSH protection
    apt install -y fail2ban

    # Configure fail2ban for SSH
    cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

    systemctl enable fail2ban
    systemctl start fail2ban

    log_info "Monitoring tools installed"
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

# Function to create systemd service for auto-start
create_systemd_service() {
    log_step "Creating systemd service for auto-start..."

    cat > /etc/systemd/system/ai-code-detect.service << EOF
[Unit]
Description=AI Code Detection System
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/appuser/app
User=appuser
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=300

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable ai-code-detect

    log_info "Systemd service created"
}

# Function to create deployment script
create_deployment_script() {
    local script_path="/home/appuser/deploy-app.sh"

    log_step "Creating deployment script..."

    cat > "$script_path" << 'EOF'
#!/bin/bash
set -e

echo "🚀 Deploying AI Code Detection System..."

# Navigate to app directory
cd /home/appuser/app

# Pull latest changes
if [ -d ".git" ]; then
    git pull
fi

# Stop existing containers
docker-compose down

# Clean up
docker system prune -f

# Build and start
docker-compose build --no-cache
docker-compose up -d

# Wait for services
sleep 30

# Check health
if curl -f http://localhost/health; then
    echo "✅ Deployment successful!"
    echo "🌐 Application is available at:"
    echo "   - HTTP: http://your-domain.com"
    echo "   - HTTPS: https://your-domain.com"
else
    echo "❌ Health check failed. Check logs:"
    docker-compose logs
fi
EOF

    chmod +x "$script_path"
    chown appuser:appuser "$script_path"

    log_info "Deployment script created at $script_path"
}

# Function to show completion message
show_completion() {
    echo ""
    log_info "🎉 VPS setup completed successfully!"
    echo ""
    log_info "Next steps:"
    echo "1. Copy your SSH public key: ssh-copy-id appuser@your-server"
    echo "2. Switch to appuser: su - appuser"
    echo "3. Clone your repository: git clone <your-repo> app"
    echo "4. Configure environment: cd app && cp env.example .env"
    echo "5. Edit .env with your actual values"
    echo "6. Deploy: ./deploy-app.sh"
    echo ""
    log_info "Useful commands:"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Restart services: docker-compose restart"
    echo "  - Stop services: docker-compose down"
    echo ""
    log_warn "Remember to:"
    echo "  - Update your domain DNS to point to this server"
    echo "  - Configure SSL_DOMAIN in .env for HTTPS"
    echo "  - Monitor logs regularly"
}

# Main function
main() {
    log_info "🚀 Starting AI Code Detection VPS Setup..."
    echo ""

    check_root
    update_system
    install_docker
    configure_firewall
    create_app_user
    # setup_ssh_hardening
    install_monitoring
    setup_log_rotation
    create_systemd_service
    create_deployment_script

    # show_completion
}

# Run main function
main "$@"
