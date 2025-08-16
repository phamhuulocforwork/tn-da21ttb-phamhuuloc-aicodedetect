# Suggested Development Commands

## Core ML Engine (src/src/)

### Setup và Environment

```bash
cd src/src && source venv/bin/activate
make setup                    # Tạo virtual environment và install dependencies
make install                  # Update dependencies
```

### Feature Extraction và Analysis

```bash
# Batch feature extraction (tạo dataset features mới)
python batch_feature_extraction.py --dataset dataset --max-files 2000 --output features/large_features.csv

# Analysis và visualization
python analyze_features.py --csv features/large_features.csv --plots-dir analysis_plots

# Complete pipeline training
python complete_pipeline.py train dataset --max-files 2000 --save-model models/model.json
```

## Backend API (src/backend/)

### Development Commands

```bash
cd src/backend
make help                     # Show all available commands
make setup                    # Setup virtual environment
make dev                      # Run development server (http://localhost:8000)
make start                    # Run production server
make clean                    # Clean up environment

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### API Testing

```bash
python test_api.py           # Run API tests
curl http://localhost:8000/health  # Health check
```

### Docker Deployment

```bash
docker-compose up --build    # Build và run với Docker
```

## Frontend (src/frontend/)

### Development Commands

```bash
cd src/frontend
npm install                   # Install dependencies
npm run dev                   # Start development server (http://localhost:3000)
npm run build                 # Build for production
npm run start                 # Start production server
npm run lint                  # Run ESLint
npm run format                # Format code với Prettier
```

### Development Utilities

```bash
npm run clean                 # Clean .next directory
npm run clean:all            # Clean .next và node_modules
npm run preview              # Build và preview production
```

## System Commands (Linux)

### Project Navigation

```bash
ls -la                       # List files với details
find . -name "*.py" -type f  # Find Python files
grep -r "keyword" src/       # Search in source files
cd src/backend && pwd        # Navigate và show current path
```

### Process Management

```bash
lsof -ti:8000 | xargs kill -9  # Kill process on port 8000
ps aux | grep python           # Find Python processes
kill -9 PID                    # Kill specific process
```

### Git Operations

```bash
git status                   # Check repository status
git add .                    # Stage all changes
git commit -m "message"      # Commit changes
git push origin main         # Push to remote
git log --oneline -10        # Show recent commits
```

## Complete Development Workflow

### 1. Start Full Development Environment

```bash
# Terminal 1: Backend
cd src/backend && make dev

# Terminal 2: Frontend
cd src/frontend && npm run dev

# Terminal 3: ML Core (if needed)
cd src/src && source venv/bin/activate
```

### 2. Run Analysis Pipeline

```bash
cd src/src && source venv/bin/activate
python batch_feature_extraction.py --dataset dataset --max-files 2000 --output features/large_features.csv
python analyze_features.py --csv features/large_features.csv --plots-dir analysis_plots
```

### 3. Access Applications

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
