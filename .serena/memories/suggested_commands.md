# AI Code Detection - Suggested Commands

## Workflow chính (theo FLOW.txt)

```bash
# Di chuyển vào thư mục ML pipeline và activate virtual environment
cd src/src && source venv/bin/activate

# Chạy batch feature extraction để tạo dataset features mới
python batch_feature_extraction.py --dataset dataset --max-files 2000 --output features/large_features.csv

# Chạy analysis và tạo visualization
python analyze_features.py --csv features/large_features.csv --plots-dir analysis_plots

# Train model mới trên dataset và lưu vào đúng thư mục backend
python complete_pipeline.py train dataset --max-files 2000 --save-model models/model.json
```

## Backend Development Commands

```bash
cd src/backend

# Setup và cài đặt dependencies
make setup
make install

# Development server với hot reload
make dev
# Server sẽ chạy tại: http://localhost:8000
# API docs tại: http://localhost:8000/docs

# Production server
make start

# Cleanup
make clean
```

## Frontend Development Commands

```bash
cd src/frontend

# Cài đặt dependencies
npm install

# Development server
npm run dev
# Server sẽ chạy với Turbopack

# Build production
npm run build
npm run start

# Linting và formatting
npm run lint
npm run format
npm run format:check

# Cleanup
npm run clean
npm run clean:all
```

## ML Pipeline Commands

```bash
cd src/src

# Setup virtual environment (nếu chưa có)
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Feature extraction
python batch_feature_extraction.py --dataset dataset --max-files [số lượng files]

# Analysis và visualization
python analyze_features.py --csv [path-to-features.csv] --plots-dir [output-dir]

# Complete pipeline (training)
python complete_pipeline.py train dataset --max-files [số lượng] --save-model [model-path]
```

## Linux System Commands

```bash
# Tìm files
find . -name "*.py" -type f
find . -name "*.ts" -type f
grep -r "pattern" src/

# Git operations
git status
git add .
git commit -m "message"
git push origin main

# Process management
ps aux | grep python
kill -9 [PID]
pkill -f "uvicorn"
```
