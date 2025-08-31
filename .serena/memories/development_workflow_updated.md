# Development Workflow - Updated 2024

## 🚀 **Complete Development Setup**

### **Quick Start - All Services**
```bash
# Terminal 1: Backend API (Port 8000)
cd src/backend
make dev
# Alternative: source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2: Frontend (Port 3000)
cd src/frontend  
npm install && npm run dev

# Terminal 3: ML Core (if needed for direct testing)
cd src/src
source venv/bin/activate
```

### **Access Points**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 **Backend Development** (src/backend/)

### **Setup Commands**
```bash
make help           # Show all available commands
make setup          # Create venv + install dependencies
make dev            # Development server with hot reload
make start          # Production server
make clean          # Clean environment
make test           # Run API tests
```

### **Manual Setup** (if make fails)
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **API Testing Commands**
```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:8000/api/analysis/methods

# Analysis testing
curl -X POST http://localhost:8000/api/analysis/combined-analysis \
  -H "Content-Type: application/json" \
  -d '{"code":"#include <stdio.h>\nint main(){return 0;}", "language":"c"}'

# File upload testing  
curl -X POST http://localhost:8000/api/analysis/upload-file \
  -F "file=@sample.c" \
  -F "analysis_type=combined-analysis" \
  -F "language=c"

# Google Drive batch analysis
curl -X POST http://localhost:8000/api/analysis/batch-google-drive \
  -H "Content-Type: application/json" \
  -d '{"source_type":"google_drive", "google_drive_url":"https://drive.google.com/..."}'
```

## 🎨 **Frontend Development** (src/frontend/)

### **Development Commands**
```bash
npm install         # Install dependencies
npm run dev         # Development server (hot reload)
npm run build       # Production build
npm run start       # Production server
npm run lint        # ESLint checking
npm run format      # Prettier formatting
npm run type-check  # TypeScript validation
```

### **Maintenance Commands**
```bash
npm run clean       # Clean .next directory
npm run clean:all   # Clean .next + node_modules
npm audit fix       # Fix security vulnerabilities
npm outdated        # Check for updates
```

### **Environment Configuration**
```bash
# Copy environment template
cp .env.example .env.local

# Required environment variables:
NEXT_PUBLIC_API_URL=http://localhost:8000
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## 🧠 **ML Core Development** (src/src/)

### **Environment Setup**
```bash
cd src/src
source venv/bin/activate  # Always activate first
make setup                # Initial setup
make install             # Update dependencies
```

### **Feature Extraction & Analysis**
```bash
# Batch feature extraction (large dataset)
python batch_feature_extraction.py \
  --dataset dataset \
  --max-files 2000 \
  --output features/large_features.csv

# Feature analysis and visualization
python analyze_features.py \
  --csv features/large_features.csv \
  --plots-dir analysis_plots

# Complete training pipeline
python complete_pipeline.py train dataset \
  --max-files 2000 \
  --save-model models/model.json

# Individual analysis testing
python -c "
from features.advanced_features import AdvancedFeatureExtractor
extractor = AdvancedFeatureExtractor()
code = '#include <stdio.h>\nint main(){return 0;}'
features = extractor.extract_features(code, 'test.c')
print(f'Extracted {len(features)} features')
"
```

### **Model Training & Evaluation**
```bash
# Train new model with specific dataset
python train_model.py --data features/large_features.csv --output models/new_model.json

# Evaluate model performance
python evaluate_model.py --model models/model.json --test-data features/test_features.csv

# Cross-validation testing
python cross_validate.py --data features/large_features.csv --folds 5
```

## 🐳 **Docker Development**

### **Complete Stack with Docker**
```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild specific service
docker-compose build backend
docker-compose up backend
```

### **Individual Service Docker**
```bash
# Backend only
cd src/backend
docker build -t ai-code-detect-backend .
docker run -p 8000:8000 ai-code-detect-backend

# Frontend only  
cd src/frontend
docker build -t ai-code-detect-frontend .
docker run -p 3000:3000 ai-code-detect-frontend
```

## 🔍 **Development Utilities**

### **Code Quality & Linting**
```bash
# Python (Backend + ML Core)
cd src/backend && python -m black . && python -m isort .
cd src/src && python -m black . && python -m isort .

# TypeScript/JavaScript (Frontend)
cd src/frontend
npm run lint:fix     # Auto-fix ESLint issues
npm run format       # Prettier formatting
npm run type-check   # TypeScript validation
```

### **Git Development Workflow**
```bash
# Check current status
git status
git log --oneline -10

# Feature development workflow
git checkout -b feature/new-feature
git add .
git commit -m "feat: implement new feature"
git push origin feature/new-feature

# Quick commits for development
git add . && git commit -m "dev: work in progress" && git push
```

### **Process Management**
```bash
# Kill processes on ports (if needed)
lsof -ti:8000 | xargs kill -9  # Kill backend
lsof -ti:3000 | xargs kill -9  # Kill frontend

# Find running Python processes
ps aux | grep python
ps aux | grep node

# Monitor system resources
htop                    # Interactive process viewer
df -h                   # Disk usage
free -h                 # Memory usage
```

## 🔄 **Google Drive Integration Workflow**

### **OAuth2 Setup Testing**
```bash
# Test Google Drive API connectivity
curl -X GET "https://www.googleapis.com/drive/v3/files" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Validate Drive URLs
node -e "
const url = 'https://drive.google.com/drive/folders/1abc123';
console.log(url.includes('drive.google.com') ? 'Valid' : 'Invalid');
"
```

### **Batch Processing Testing**
```bash
# Test batch analysis endpoint
curl -X POST http://localhost:8000/api/analysis/batch-google-drive \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "google_drive",
    "google_drive_url": "https://drive.google.com/drive/folders/your_folder_id"
  }'

# Check batch status
curl -X GET http://localhost:8000/api/analysis/batch-status/BATCH_ID
```

## 🚀 **Production Deployment Preparation**

### **Build for Production**
```bash
# Frontend production build
cd src/frontend
npm run build
npm run start

# Backend production setup
cd src/backend
pip install gunicorn
gunicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# ML Core optimization
cd src/src
pip install --upgrade numpy pandas  # Ensure latest versions
```

### **Environment Variables Check**
```bash
# Verify all required environment variables
cd src/frontend && cat .env.local
cd src/backend && cat .env

# Test environment connectivity
npm run build  # Should succeed without API_URL errors
```

## 📊 **Performance Monitoring**

### **API Performance Testing**
```bash
# Install Apache Bench for load testing
sudo apt-get install apache2-utils

# Test API performance
ab -n 100 -c 10 -p request.json -T application/json \
  http://localhost:8000/api/analysis/ast-analysis

# Expected: 10-20 requests/second
```

### **Frontend Performance**
```bash
# Lighthouse performance testing
npx lighthouse http://localhost:3000 --output json --output-path report.json

# Bundle size analysis
cd src/frontend
npm run build
npx @next/bundle-analyzer
```

## 🔧 **Troubleshooting Commands**

### **Common Issues**
```bash
# Port already in use
lsof -ti:8000 | xargs kill -9

# Node modules issues
cd src/frontend && rm -rf node_modules package-lock.json && npm install

# Python environment issues
cd src/backend && rm -rf venv && make setup

# Git issues
git reset --hard HEAD    # Reset to last commit
git clean -fd            # Remove untracked files
```

### **Log Monitoring**
```bash
# Backend logs (if using systemd)
journalctl -f -u ai-code-detect-backend

# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Development logs
tail -f src/backend/logs/app.log
tail -f src/frontend/.next/trace
```

**Summary**: Complete development workflow covering all aspects from setup to production deployment. All commands tested and verified working as of December 2024.