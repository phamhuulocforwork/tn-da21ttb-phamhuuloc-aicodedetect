# Troubleshooting and Development Tips

## Common Development Issues

### Python Environment Issues

#### Virtual Environment Problems

```bash
# Issue: Module not found errors
# Solution: Ensure virtual environment is activated
cd src/src && source venv/bin/activate
which python  # Should show venv/bin/python

# Issue: Wrong Python version
# Solution: Recreate venv với correct version
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Import Path Issues

```bash
# Issue: Cannot import from ../src/features/
# Solution: Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/../src"

# Or in Python code:
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
```

#### Dependency Conflicts

```bash
# Issue: Package version conflicts
# Solution: Check và resolve conflicts
pip list --outdated
pip install --upgrade package_name

# Create fresh environment if needed
pip freeze > old_requirements.txt
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Backend API Issues

#### Port Already In Use

```bash
# Issue: Address already in use: :::8000
# Solution: Find và kill process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001 --reload
```

#### FastAPI Module Errors

```bash
# Issue: Analysis modules not loaded
# Error: "Analysis modules not available"
# Solution: Check import paths

cd src/backend
python -c "from app.main import app; print('Import successful')"

# Debug module loading
python -c "
import sys
sys.path.append('../src')
from features.advanced_features import AdvancedFeatureExtractor
print('Module loaded successfully')
"
```

#### CORS Issues

```bash
# Issue: Frontend cannot connect to API
# Solution: Check CORS configuration trong main.py

# Test CORS manually
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     http://localhost:8000/api/analysis/combined-analysis
```

### Frontend Development Issues

#### Node.js Environment Problems

```bash
# Issue: Node version compatibility
# Solution: Use correct Node version
node --version  # Should be >= 18

# Install via nvm if needed
nvm install 20
nvm use 20
```

#### Package Installation Issues

```bash
# Issue: npm install fails
# Solution: Clear cache và reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# Or use yarn
yarn install
```

#### TypeScript Errors

```bash
# Issue: Type checking errors
# Solution: Check types manually
npx tsc --noEmit

# Common fixes:
# 1. Update @types/* packages
npm install --save-dev @types/react@latest @types/node@latest

# 2. Check tsconfig.json configuration
cat tsconfig.json
```

#### Build Issues

```bash
# Issue: Next.js build fails
# Solution: Debug build process
npm run build 2>&1 | tee build.log

# Common causes:
# 1. TypeScript errors
# 2. Missing environment variables
# 3. Import path issues
# 4. Static file problems
```

### Integration Issues

#### API Connection Problems

```bash
# Issue: Frontend cannot reach backend
# Diagnosis steps:

# 1. Check backend is running
curl http://localhost:8000/health

# 2. Check frontend environment
cat src/frontend/.env.local
# Should have: NEXT_PUBLIC_API_URL=http://localhost:8000

# 3. Test from frontend directory
cd src/frontend
curl $NEXT_PUBLIC_API_URL/health
```

#### File Upload Issues

```bash
# Issue: File upload returns 413 or 422
# Solutions:

# 1. Check file size (< 1MB)
ls -lh your_file.c

# 2. Check file extension
# Supported: .c, .cpp, .cc, .cxx, .txt

# 3. Test upload manually
curl -X POST http://localhost:8000/api/analysis/upload-file \
     -F "file=@test.c" \
     -F "analysis_type=combined" \
     -F "language=c"
```

#### Analysis Timeout Issues

```bash
# Issue: Analysis takes too long
# Diagnosis:

# 1. Check code size
wc -l your_code.c  # Should be reasonable (< 1000 lines)

# 2. Monitor backend logs
tail -f backend.log

# 3. Test với simpler code
echo '#include <stdio.h>\nint main(){return 0;}' > simple.c
```

## Performance Optimization

### Backend Performance

```bash
# Monitor memory usage
cd src/backend
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"

# Profile analysis performance
time python -c "
from app.main import analyze_code_comprehensive
code = '#include <stdio.h>\nint main(){return 0;}'
result = analyze_code_comprehensive(code, 'test.c', 'c')
print('Analysis completed')
"
```

### Frontend Performance

```bash
# Check bundle size
cd src/frontend
npm run build
du -sh .next/

# Analyze bundle composition
npx @next/bundle-analyzer

# Monitor runtime performance
# Use browser devtools Performance tab
```

### Database Performance (if applicable)

```bash
# Monitor any data storage
du -sh src/src/models/
du -sh src/src/features/
du -sh src/src/dataset/
```

## Debugging Strategies

### Backend Debugging

```python
# Add debug logging to main.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Add try-catch với detailed errors
try:
    result = extract_features(code, filename)
except Exception as e:
    logger.error(f"Feature extraction error: {str(e)}", exc_info=True)
    raise
```

### Frontend Debugging

```typescript
// Add console debugging
console.log("Analysis request:", { code, method, options });

// Use React DevTools
// Install browser extension

// Add error boundaries
import { ErrorBoundary } from "react-error-boundary";

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <h2>Something went wrong:</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}
```

### Network Debugging

```bash
# Monitor HTTP traffic
# Browser DevTools Network tab

# Command line monitoring
tcpdump -i lo -A port 8000

# Curl với verbose output
curl -v -X POST http://localhost:8000/api/analysis/combined-analysis \
     -H "Content-Type: application/json" \
     -d '{"code":"test", "language":"c"}'
```

## Development Best Practices

### Local Development Setup

```bash
# Use tmux/screen cho multiple terminals
# Terminal 1: Backend
cd src/backend && make dev

# Terminal 2: Frontend
cd src/frontend && npm run dev

# Terminal 3: Monitoring/logs
tail -f src/backend/app.log

# Terminal 4: Development commands
cd src/src && source venv/bin/activate
```

### Git Workflow

```bash
# Before making changes
git status
git pull origin main

# Create feature branch
git checkout -b feature/your-feature

# Regular commits với clear messages
git add .
git commit -m "feat: Add specific functionality"

# Before pushing
npm run lint           # Frontend
python -m py_compile *.py  # Backend
make test             # If tests exist

git push origin feature/your-feature
```

### Testing Strategies

```bash
# Manual testing checklist
# 1. Backend health check
curl http://localhost:8000/health

# 2. Individual endpoints
curl -X POST http://localhost:8000/api/analysis/ast-analysis \
     -H "Content-Type: application/json" \
     -d '{"code":"int main(){return 0;}", "language":"c"}'

# 3. Frontend functionality
# - Visit http://localhost:3000
# - Test code editor input
# - Test analysis submission
# - Test results display
# - Test file upload

# 4. Integration testing
# - Full workflow from code input to results
# - Error handling
# - Large file processing
```

### Monitoring and Maintenance

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Monitor log files
tail -f src/backend/*.log
tail -f src/frontend/.next/build.log

# Check for errors
grep -r "ERROR\|CRITICAL" src/
```

## Quick Problem Resolution

### "Service Unavailable" Errors

1. Check virtual environment activation
2. Verify Python path includes ../src
3. Test individual module imports
4. Restart backend service

### "Cannot Connect" Errors

1. Verify backend is running on port 8000
2. Check frontend .env.local configuration
3. Test CORS settings
4. Verify no firewall blocking

### "Analysis Failed" Errors

1. Check code validity (valid C/C++)
2. Verify file size < 1MB
3. Check backend logs cho specific errors
4. Test với minimal code sample

### Performance Issues

1. Monitor memory usage during analysis
2. Check for large datasets in /dataset
3. Optimize code complexity
4. Consider increasing timeout limits

## Emergency Recovery

### Complete Environment Reset

```bash
# Backend reset
cd src/backend
rm -rf venv __pycache__
make setup

# Frontend reset
cd src/frontend
rm -rf .next node_modules
npm install

# Core ML reset
cd src/src
rm -rf venv __pycache__
make setup
```

### Backup Important Data

```bash
# Before major changes
cp -r src/src/models models_backup
cp -r src/src/features features_backup
cp src/src/feature_stats.json feature_stats_backup.json
```
