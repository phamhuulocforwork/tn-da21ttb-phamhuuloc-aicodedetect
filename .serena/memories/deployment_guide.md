# Deployment Guide

## Production Architecture

### Infrastructure Overview
```
Internet
    ↓
[Nginx Reverse Proxy - SSL Termination]
    ↓
[Docker Compose Stack]
├── Frontend (Next.js - Static)
├── Backend (FastAPI - API)
└── Nginx (Static File Serving)

[External Services]
├── Google Drive API
├── Google Gemini AI
└── Let's Encrypt (SSL)
```

### Server Requirements
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 20GB+ available space
- **Network**: Public IP with DNS configuration

## Automated Deployment

### One-Command Deployment
```bash
# VPS Setup (run as root)
sudo ./scripts/setup-vps.sh

# Switch to appuser
su - appuser

# Clone and deploy
git clone <repository-url> app
cd app
./scripts/deploy.sh
```

### What the Scripts Do

#### setup-vps.sh
```bash
#!/bin/bash
# Automated VPS setup script

# 1. Update system packages
apt update && apt upgrade -y

# 2. Install required packages
apt install -y docker.io docker-compose git curl wget ufw

# 3. Configure firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable

# 4. Create appuser
useradd -m -s /bin/bash appuser
usermod -aG docker appuser

# 5. Setup Docker
systemctl enable docker
systemctl start docker

# 6. Install SSL tools
apt install -y certbot python3-certbot-nginx
```

#### deploy.sh
```bash
#!/bin/bash
# Automated deployment script

# 1. Load environment variables
if [ ! -f .env ]; then
    cp env.example .env
    echo "Please configure .env file with your API keys"
    exit 1
fi

# 2. Stop existing services
docker-compose down

# 3. Pull latest changes
git pull origin main

# 4. Build and start services
docker-compose build --no-cache
docker-compose up -d

# 5. Wait for services to start
sleep 30

# 6. Run health checks
./scripts/manage.sh health

# 7. Setup SSL if domain is configured
if [ ! -z "$SSL_DOMAIN" ]; then
    ./scripts/setup-ssl.sh
fi

# 8. Show status
./scripts/manage.sh status
```

## Manual Deployment Steps

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
sudo apt install -y docker.io docker-compose git curl

# Start and enable Docker
sudo systemctl enable docker
sudo systemctl start docker

# Add user to docker group (optional)
sudo usermod -aG docker $USER

# Install Nginx (if not using container)
sudo apt install -y nginx certbot python3-certbot-nginx
```

### 2. Application Deployment
```bash
# Clone repository
git clone <repository-url> ai-code-detect
cd ai-code-detect

# Configure environment
cp env.example .env
nano .env  # Add your API keys

# Build and start services
docker-compose up --build -d

# Check deployment
docker-compose ps
docker-compose logs
```

### 3. SSL Configuration
```bash
# Configure domain in .env
SSL_DOMAIN=your-domain.com
SSL_EMAIL=your-email@example.com

# Get SSL certificate
sudo certbot certonly --standalone -d your-domain.com

# Or use DNS challenge for wildcard certificates
sudo certbot certonly --manual --preferred-challenges dns -d your-domain.com

# Configure Nginx for SSL
sudo nano /etc/nginx/sites-available/ai-code-detect

# Nginx configuration
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Docker Configuration

### Production Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - nginx_logs:/var/log/nginx
      - nginx_ssl:/etc/nginx/ssl
      - letsencrypt:/etc/letsencrypt
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

  frontend:
    build:
      context: ./src/frontend
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    build:
      context: ./src/backend
      dockerfile: Dockerfile
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./logs:/app/logs
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  nginx_logs:
  nginx_ssl:
  letsencrypt:
  redis_data:
```

### Dockerfile Examples

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/out /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Backend Dockerfile
```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Environment Configuration

### Production Environment Variables
```bash
# .env production configuration
ENVIRONMENT=production
LOG_LEVEL=warning

# API Keys
GEMINI_API_KEY=your_production_gemini_key
GOOGLE_DRIVE_API_KEY=your_production_drive_key

# SSL Configuration
SSL_DOMAIN=your-domain.com
SSL_EMAIL=admin@your-domain.com
SSL_STAGING=false

# Database (if applicable)
DATABASE_URL=postgresql://user:pass@localhost/db

# Redis (for caching/session)
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_256_bit_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Performance
MAX_WORKERS=4
WORKER_TIMEOUT=300
MAX_REQUEST_SIZE=104857600  # 100MB

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
LOGSTASH_HOST=logstash.example.com
```

## Monitoring & Maintenance

### Health Checks
```bash
# Service health checks
./scripts/manage.sh health

# Individual service checks
curl -f http://localhost/health
curl -f http://localhost/api/health
curl -f http://localhost/api/debug/baseline-stats
```

### Log Management
```bash
# View all logs
./scripts/manage.sh logs

# View specific service logs
./scripts/manage.sh logs backend
./scripts/manage.sh logs nginx

# Follow logs in real-time
./scripts/manage.sh logs -f

# Export logs for analysis
./scripts/manage.sh logs > logs_$(date +%Y%m%d_%H%M%S).txt
```

### Backup Strategy
```bash
# Automated backup
./scripts/manage.sh backup

# Manual backup
docker run --rm -v $(pwd):/backup \
  -v nginx_logs:/nginx_logs \
  -v nginx_ssl:/nginx_ssl \
  -v letsencrypt:/letsencrypt \
  alpine tar czf /backup/backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  -C / nginx_logs nginx_ssl letsencrypt

# Database backup (if applicable)
docker exec -t postgres pg_dump -U username dbname > backup.sql
```

### SSL Certificate Management
```bash
# Check certificate status
./scripts/manage.sh ssl-status

# Renew certificates
./scripts/manage.sh ssl-renew

# Manual renewal
sudo certbot renew --quiet

# Test SSL configuration
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

## Scaling & Performance

### Horizontal Scaling
```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  frontend:
    deploy:
      replicas: 2

  nginx:
    deploy:
      placement:
        constraints:
          - node.role == manager
```

### Performance Optimization
```bash
# Enable gzip compression
# nginx.conf
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Database optimization (if applicable)
# postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Redis optimization
# redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
tcp-keepalive 300
```

## Troubleshooting

### Common Issues

#### Services Won't Start
```bash
# Check Docker status
sudo systemctl status docker

# Check Docker Compose logs
docker-compose logs

# Check resource usage
docker system df
docker stats

# Clean up and restart
docker system prune -f
docker-compose down
docker-compose up -d
```

#### SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in /etc/letsencrypt/live/your-domain.com/cert.pem -text -noout

# Test SSL connection
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# Renew certificate manually
sudo certbot certonly --standalone -d your-domain.com
```

#### API Connection Issues
```bash
# Test backend connectivity
curl -f http://localhost:8000/health

# Check backend logs
docker-compose logs backend

# Test API endpoints
curl -X POST http://localhost:8000/api/analysis/combined-analysis \
  -H "Content-Type: application/json" \
  -d '{"code": "test", "filename": "test.c", "language": "c"}'
```

#### Database Connection Issues
```bash
# Test database connectivity
docker exec -it postgres psql -U username -d dbname -c "SELECT 1;"

# Check database logs
docker-compose logs postgres

# Reset database connection
docker-compose restart postgres
```

### Performance Issues
```bash
# Monitor resource usage
docker stats

# Check application metrics
curl http://localhost:8000/metrics

# Profile application performance
python -m cProfile -s cumtime app/main.py

# Database query analysis
docker exec -it postgres psql -U username -d dbname -c "SELECT * FROM pg_stat_activity;"
```

## Security Hardening

### Server Security
```bash
# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Disable root login
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Setup fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Application Security
```python
# Security headers middleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["your-domain.com"]
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Data Security
```bash
# Encrypt sensitive data at rest
# Use Docker secrets for sensitive environment variables
echo "GEMINI_API_KEY" | docker secret create gemini_key -
echo "your_actual_key_here" | docker secret create gemini_key_value -

# Regular security updates
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y

# Backup encryption
tar czf - /path/to/backup | openssl enc -aes-256-cbc -salt -out backup.enc
```

## Disaster Recovery

### Backup Recovery
```bash
# Stop services
docker-compose down

# Restore volumes
docker run --rm -v $(pwd):/backup \
  -v nginx_logs:/nginx_logs \
  -v nginx_ssl:/nginx_ssl \
  -v letsencrypt:/letsencrypt \
  alpine tar xzf /backup/backup_file.tar.gz

# Restore database
docker exec -i postgres psql -U username -d dbname < backup.sql

# Start services
docker-compose up -d
```

### Rollback Strategy
```bash
# Quick rollback to previous version
git log --oneline -10
git checkout <previous-commit-hash>
docker-compose build --no-cache
docker-compose up -d

# Or rollback specific service
docker-compose up -d --no-deps backend
```

### Monitoring Alerts
```bash
# Setup monitoring with health checks
#!/bin/bash
# /usr/local/bin/health-monitor.sh

if ! curl -f http://localhost/health > /dev/null 2>&1; then
    echo "$(date): Health check failed" >> /var/log/health-monitor.log
    # Send alert (email, Slack, etc.)
    mail -s "Service Down Alert" admin@example.com << EOF
Service is down. Please check immediately.
EOF
fi
```

## Cost Optimization

### Resource Optimization
```yaml
# Production resource limits
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M

  frontend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
```

### Auto-scaling (Docker Swarm/Kubernetes)
```yaml
# docker-compose.swarm.yml
services:
  backend:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
      restart_policy:
        condition: on-failure
```

### Cloud Cost Optimization
```bash
# Use spot instances for non-critical workloads
# Implement auto-shutdown for development environments
# Use CDN for static assets
# Implement caching layers
# Monitor and optimize database queries
# Use serverless functions for occasional tasks
```

This deployment guide covers everything from initial setup to production maintenance, ensuring a robust and scalable AI Code Detection System deployment.