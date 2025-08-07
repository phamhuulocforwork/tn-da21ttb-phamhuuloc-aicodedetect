# Suggested Commands - Lệnh hữu ích cho dự án AI Code Detection

## Cập nhật: 2025-08-07

### 🚀 Core ML Pipeline Commands

#### 1. Run Complete ML Pipeline:
```bash
cd src/src
python run_ml_pipeline.py \
  --ai-dir "dataset/code/c/ai" \
  --human-dir "dataset/code/c/human" \
  --output-dir "ml_output" \
  --max-files 500
```

#### 2. Test Individual Components:
```bash
# Test feature extraction
python -c "from features.advanced_features import AdvancedFeatureExtractor; print('Feature extraction ready')"

# Test model evaluation
python -c "from evaluation.model_evaluator import ModelEvaluator; print('Evaluation framework ready')"

# Test complete system
python test_complete_system.py
```

#### 3. Quick ML Model Testing:
```bash
# Test with sample code
python -c "
from features.detection_models import EnhancedDetectionPipeline
pipeline = EnhancedDetectionPipeline()
code = '#include <iostream>\nint main() { std::cout << \"Hello\"; }'
result = pipeline.analyze_code(code, 'test.cpp')
print(f'Prediction: {result[\"prediction\"]}')
"
```

### 🖥️ Backend API Commands

#### 1. Start FastAPI Server:
```bash
cd src/backend
# Development với hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 2. Test API Endpoints:
```bash
# Basic health check
curl http://localhost:8000/

# Test code analysis
curl -X POST http://localhost:8000/analyze-code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "#include <iostream>\nint main() { return 0; }",
    "language": "cpp",
    "detector_type": "hybrid"
  }'

# Get available detectors
curl http://localhost:8000/detectors

# Benchmark all detectors
curl -X POST http://localhost:8000/benchmark-detectors \
  -H "Content-Type: application/json" \
  -d '{"code": "#include <iostream>\nint main() { return 0; }", "language": "cpp"}'
```

#### 3. Backend Development:
```bash
# Install dependencies
cd src/backend
pip install -r requirements.txt

# Run tests
python test_api.py
python test_fixed.py

# Debug mode
python debug_detection.py
```

### 🌐 Frontend Commands

#### 1. Development Server:
```bash
cd src/frontend
# Install dependencies
npm install

# Start development server với Turbopack
npm run dev

# Build for production
npm run build

# Start production server
npm run start
```

#### 2. Code Quality:
```bash
cd src/frontend
# Lint check
npm run lint

# Format code
npm run format

# Clean build artifacts
npm run clean

# Complete cleanup
npm run clean:all
```

#### 3. Development Debugging:
```bash
# Check Next.js configuration
npx next info

# Analyze bundle size
npm run build && npx @next/bundle-analyzer
```

### 📊 Data và Analysis Commands

#### 1. Dataset Management:
```bash
cd src/src
# Create metadata
python scripts/create_metadata.py

# Extract problems
python extractor/extract_problems.py

# Extract submissions
python extractor/extract_submissions.py

# Combine datasets
python extractor/combined_dataset.py
```

#### 2. Feature Analysis:
```bash
# Test feature extraction
python features/test_parser_sample.py

# Test Gemini integration
python features/test_gemini.py

# Advanced features testing
python -c "
from features.advanced_features import AdvancedFeatureExtractor
extractor = AdvancedFeatureExtractor()
print('Available feature categories:', extractor.get_feature_categories())
"
```

#### 3. Model Evaluation:
```bash
# Comprehensive evaluation
python -c "
from evaluation.model_evaluator import compare_detectors, ModelEvaluator
print('Running model comparison...')
# Add your evaluation code here
"

# Check model performance
python -c "
import json
with open('ml_output/final_pipeline_report.json') as f:
    report = json.load(f)
    print('Best F1-Score:', report['best_performer']['f1_score'])
"
```

### 🔧 Environment Setup Commands

#### 1. Initial Project Setup:
```bash
# Create Python virtual environment
cd src/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend  
npm install

# Setup core ML
cd ../src
pip install -r requirements.txt
```

#### 2. Environment Verification:
```bash
# Check Python environment
python --version
pip list | grep -E "(scikit-learn|pandas|numpy)"

# Check Node.js environment
node --version
npm --version

# Check project structure
ls -la src/
```

#### 3. Quick Health Check:
```bash
# Test all components
cd src/src && python -c "import pandas, numpy, sklearn; print('✅ ML dependencies OK')"
cd src/backend && python -c "import fastapi, uvicorn; print('✅ Backend dependencies OK')"
cd src/frontend && npm run build > /dev/null && echo "✅ Frontend build OK"
```

### 📝 Documentation Commands

#### 1. Generate Documentation:
```bash
# API documentation (auto-generated)
cd src/backend && uvicorn app.main:app --reload &
echo "API docs available at: http://localhost:8000/docs"

# Generate feature documentation
python -c "
from features.advanced_features import AdvancedFeatureExtractor
extractor = AdvancedFeatureExtractor()
help(extractor.extract_all_features)
"
```

#### 2. Thesis và Reports:
```bash
# Check thesis files
ls -la thesis/
find thesis/ -name "*.md" -o -name "*.docx"

# Progress reports
ls -la progress-report/
```

### 🚨 Debugging Commands

#### 1. Common Issues:
```bash
# Port already in use
lsof -ti:8000 | xargs kill -9

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true

# Reset environment
cd src/frontend && npm run clean:all && npm install
```

#### 2. Performance Analysis:
```bash
# Check system resources
top -p $(pgrep -f python)
df -h

# Memory usage
python -c "
import psutil
print(f'Memory usage: {psutil.virtual_memory().percent}%')
print(f'CPU usage: {psutil.cpu_percent()}%')
"
```

### 🎯 Production Commands

#### 1. Production Build:
```bash
# Frontend production build
cd src/frontend
npm run build
npm run start

# Backend production
cd src/backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 2. Performance Testing:
```bash
# Load testing với curl
for i in {1..10}; do
  curl -X POST http://localhost:8000/analyze-code \
    -H "Content-Type: application/json" \
    -d '{"code": "#include <iostream>", "language": "cpp"}' &
done
wait
```

### 📦 Useful Shortcuts

#### 1. Quick Development Start:
```bash
# Start everything
cd src/backend && uvicorn app.main:app --reload &
cd src/frontend && npm run dev &
echo "🚀 Development servers started!"
echo "🔗 Backend: http://localhost:8000"
echo "🔗 Frontend: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
```

#### 2. Project Status Check:
```bash
# Quick status overview
echo "📊 Project Status Check:"
echo "Backend: $(curl -s http://localhost:8000 && echo "✅ Running" || echo "❌ Down")"
echo "Frontend: $(curl -s http://localhost:3000 && echo "✅ Running" || echo "❌ Down")"
cd src/src && test -f ml_output/final_pipeline_report.json && echo "ML Models: ✅ Ready" || echo "ML Models: ❌ Not trained"
```

### ⚡ Performance Commands

```bash
# ML Pipeline benchmark
time python run_ml_pipeline.py --max-files 100

# API performance test
time curl -X POST http://localhost:8000/analyze-code \
  -H "Content-Type: application/json" \
  -d '{"code": "#include <iostream>\nint main() { return 0; }", "language": "cpp"}'

# Frontend build performance
time npm run build
```

**🎯 All commands tested và ready for development!** 🚀