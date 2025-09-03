# Lệnh phát triển quan trọng

## Frontend Development

### Cài đặt và khởi chạy

```bash
# Cài đặt dependencies
cd src/frontend
npm install

# Khởi chạy development server với Turbopack
npm run dev

# Build production
npm run build

# Preview production build
npm run preview

# Khởi chạy production server
npm run start
```

### Code Quality

```bash
# Kiểm tra linting
npm run lint

# Format code với Prettier
npm run format

# Kiểm tra format (không sửa)
npm run format:check

# Clean build artifacts
npm run clean
```

## Backend Development

### Python Environment

```bash
# Tạo virtual environment
cd src/backend
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Khởi chạy development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Chạy tests
pytest

# Chạy tests với coverage
pytest --cov=app

# Chạy tests async
pytest -k "test_" --asyncio-mode=auto
```

## Full Stack Development

### Docker Development

```bash
# Khởi chạy tất cả services (development)
docker-compose -f docker-compose.dev.yml up -d

# Khởi chạy tất cả services (production)
docker-compose up -d

# Xem logs tất cả services
docker-compose logs -f

# Xem logs service cụ thể
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx

# Restart services
docker-compose restart

# Dừng tất cả services
docker-compose down
```

### Service Management Script

```bash
# Script quản lý services (khuyến nghị)
./scripts/manage.sh status          # Xem trạng thái services
./scripts/manage.sh logs            # Xem logs tất cả
./scripts/manage.sh logs nginx      # Xem logs nginx
./scripts/manage.sh restart         # Restart tất cả
./scripts/manage.sh stop            # Dừng tất cả
./scripts/manage.sh start           # Khởi động tất cả
./scripts/manage.sh rebuild         # Rebuild và restart
./scripts/manage.sh health          # Kiểm tra health
./scripts/manage.sh shell backend   # Mở shell trong container backend
```

## Analysis Modules (Python)

### Feature Extraction & Analysis

```bash
# Chạy feature extraction
cd src/src
python analyze_features.py

# Chạy batch feature extraction
python batch_feature_extraction.py

# Chạy complete pipeline
python complete_pipeline.py

# Tạo plots và visualizations
python analysis_plots/
```

### Model Training & Testing

```bash
# Train detection models
python models/train_model.py

# Test optimized binary classifier
python optimized_binary_classifier.py

# Chạy super linter integration
python super_linter_integration.py
```

## Deployment & Production

### Automated Deployment

```bash
# Setup VPS tự động (root user)
sudo ./scripts/setup-vps.sh

# Deploy tự động
./scripts/deploy.sh
```

### Manual Deployment Steps

```bash
# 1. Clone repository
git clone <repository-url> app
cd app

# 2. Cấu hình environment
cp env.example .env
nano .env  # Chỉnh sửa API keys

# 3. Deploy với Docker
docker-compose up --build -d

# 4. Kiểm tra deployment
./scripts/manage.sh health
./scripts/manage.sh status
```

### SSL & Security

```bash
# Kiểm tra SSL status
./scripts/manage.sh ssl-status

# Renew SSL certificates
./scripts/manage.sh ssl-renew

# Backup dữ liệu
./scripts/manage.sh backup
```

## Development Workflow

### Git Workflow

```bash
# Tạo branch mới
git checkout -b feature/new-feature

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/new-feature

# Merge với main
git checkout main
git pull origin main
git merge feature/new-feature
```

### Code Quality Checks

```bash
# Frontend
cd src/frontend
npm run lint
npm run format:check

# Backend
cd src/backend
python -m flake8 app/
python -m black --check app/

# Analysis modules
cd src/src
python -m pylint features/
```

## Database & Data Management

### Baseline Stats Management

```bash
# Debug baseline stats
curl http://localhost:8000/api/debug/baseline-stats

# Reload baseline stats
curl -X POST http://localhost:8000/api/debug/reload-baseline
```

## Monitoring & Debugging

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs

# Test single file analysis
curl -X POST "http://localhost:8000/api/analysis/combined-analysis" \
  -H "Content-Type: application/json" \
  -d '{"code": "#include <stdio.h>\nint main() { return 0; }", "filename": "test.c", "language": "c"}'

# Test batch analysis
curl -X POST "http://localhost:8000/api/analysis/batch/upload-zip" \
  -F "file=@test_files.zip"
```

### Container Debugging

```bash
# Mở shell trong container
docker-compose exec backend sh
docker-compose exec frontend sh
docker-compose exec nginx sh

# Xem resource usage
docker stats

# Inspect container
docker inspect <container-name>
```

## Performance & Optimization

### Frontend Optimization

```bash
# Analyze bundle size
npm run build --analyze

# Check Lighthouse score
npx lighthouse http://localhost:3000
```

### Backend Optimization

```bash
# Profile Python code
python -m cProfile app/main.py

# Memory profiling
python -m memory_profiler app/main.py
```

## Environment Setup

### Local Development Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd tn-da21ttb-phamhuuloc-aicodedetect

# 2. Setup backend
cd src/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Setup frontend
cd ../frontend
npm install

# 4. Setup environment variables
cp .env.example .env
# Edit .env với API keys

# 5. Start development servers
# Terminal 1: Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
npm run dev

# Terminal 3: Database (nếu cần)
docker-compose -f docker-compose.dev.yml up -d
```

### Production Environment Setup

```bash
# VPS Ubuntu 22.04 setup
sudo ./scripts/setup-vps.sh
su - appuser
git clone <repository-url> app
cd app
cp env.example .env
# Configure .env
./scripts/deploy.sh
```
