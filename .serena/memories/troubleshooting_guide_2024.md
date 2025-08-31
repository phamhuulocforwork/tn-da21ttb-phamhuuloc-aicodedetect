# Troubleshooting Guide 2024

## 🚨 **Common Development Issues & Solutions**

### **1. Port Conflicts**

#### **Problem**: Port 8000 or 3000 already in use
```bash
# Error: [Errno 98] Address already in use
# Error: Port 3000 is already in use
```

#### **Solutions**:
```bash
# Find and kill process on port
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend

# Alternative: Use different port
cd src/backend && uvicorn app.main:app --port 8001
cd src/frontend && npm run dev -- --port 3001

# Check what's using the port
lsof -i :8000
netstat -tulpn | grep :8000
```

### **2. Python Virtual Environment Issues**

#### **Problem**: Import errors, missing modules
```bash
# ModuleNotFoundError: No module named 'fastapi'
# ImportError: No module named 'features'
```

#### **Solutions**:
```bash
# Recreate virtual environment
cd src/backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# For ML Core
cd src/src
rm -rf venv
make setup
source venv/bin/activate

# Verify Python path
python -c "import sys; print(sys.path)"
which python  # Should point to venv/bin/python
```

### **3. Node.js & NPM Issues**

#### **Problem**: Package installation failures, version conflicts
```bash
# npm ERR! peer dep missing
# Error: Cannot resolve module '@/components/ui/button'
```

#### **Solutions**:
```bash
# Clear npm cache and reinstall
cd src/frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Fix peer dependency issues
npm install --legacy-peer-deps

# Verify Node version (should be 18+)
node --version
npm --version

# Update NPM
npm install -g npm@latest
```

### **4. API Connection Issues**

#### **Problem**: Frontend can't connect to backend
```bash
# Failed to fetch
# CORS policy error
# Network error
```

#### **Solutions**:
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify CORS configuration in backend
cd src/backend
grep -r "CORS" app/  # Check CORS settings

# Check environment variables
cd src/frontend
cat .env.local | grep API_URL
# Should be: NEXT_PUBLIC_API_URL=http://localhost:8000

# Test API endpoint directly
curl -X POST http://localhost:8000/api/analysis/ast-analysis \
  -H "Content-Type: application/json" \
  -d '{"code":"int main(){return 0;}", "language":"c"}'
```

### **5. Google Drive Integration Issues**

#### **Problem**: OAuth2 authentication failures
```bash
# Error: invalid_client
# Error: redirect_uri_mismatch
```

#### **Solutions**:
```bash
# Verify Google OAuth credentials
cd src/frontend
grep -E "GOOGLE_CLIENT|GOOGLE_SECRET" .env.local

# Check redirect URIs in Google Console
# Should include: http://localhost:3000/auth/callback

# Test OAuth flow manually
curl -X GET "https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:3000/auth/callback&scope=https://www.googleapis.com/auth/drive.readonly&response_type=code"

# Verify Drive API is enabled in Google Console
```

### **6. File Upload Issues**

#### **Problem**: File upload failures, size limits
```bash
# Error: File too large
# Error: Unsupported file type
# Error: Request entity too large
```

#### **Solutions**:
```bash
# Check file size (max 1MB for single files, 50MB for ZIP)
ls -lh uploaded_file.c

# Verify file types allowed
grep -r "allowed_extensions" src/backend/app/

# Check backend upload limits
grep -r "max_file_size" src/backend/app/

# Test file upload with curl
curl -X POST http://localhost:8000/api/analysis/upload-file \
  -F "file=@test.c" \
  -F "analysis_type=combined-analysis" \
  -F "language=c"
```

### **7. Analysis Engine Errors**

#### **Problem**: Feature extraction failures
```bash
# Error in AST parsing
# Error in feature calculation
# Timeout in analysis
```

#### **Solutions**:
```bash
# Test individual feature extractors
cd src/src
source venv/bin/activate

# Test AST analyzer
python -c "
from features.ast_analyzer import CppASTAnalyzer
analyzer = CppASTAnalyzer()
code = '#include <stdio.h>\nint main(){return 0;}'
try:
    result = analyzer.analyze(code)
    print(f'AST analysis successful: {len(result)} features')
except Exception as e:
    print(f'AST analysis failed: {e}')
"

# Test advanced features
python -c "
from features.advanced_features import AdvancedFeatureExtractor
extractor = AdvancedFeatureExtractor()
code = '#include <stdio.h>\nint main(){return 0;}'
try:
    result = extractor.extract_features(code, 'test.c')
    print(f'Advanced features successful: {len(result)} features')
except Exception as e:
    print(f'Advanced features failed: {e}')
"

# Check for missing dependencies
pip list | grep -E "numpy|pandas|scipy"
```

### **8. Database & Storage Issues**

#### **Problem**: File write permissions, storage errors
```bash
# Permission denied
# No space left on device
# Cannot create directory
```

#### **Solutions**:
```bash
# Check disk space
df -h

# Check permissions
ls -la src/backend/uploads/
ls -la src/src/features/

# Fix permissions
sudo chown -R $USER:$USER src/
chmod -R 755 src/

# Clean up old files
find src/ -name "*.tmp" -delete
find src/ -name "__pycache__" -type d -exec rm -rf {} +
```

### **9. Performance Issues**

#### **Problem**: Slow analysis, high memory usage
```bash
# Analysis taking too long
# Out of memory errors
# High CPU usage
```

#### **Solutions**:
```bash
# Monitor system resources
htop
free -h
iostat -x 1

# Check Python memory usage
python -c "
import psutil
process = psutil.Process()
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"

# Optimize Python performance
cd src/backend
python -O app/main.py  # Run with optimizations

# Reduce file size for testing
head -n 50 large_file.c > small_test.c

# Check for memory leaks
valgrind --tool=memcheck python your_script.py
```

### **10. Git & Version Control Issues**

#### **Problem**: Merge conflicts, repository issues
```bash
# error: Your local changes would be overwritten
# fatal: not a git repository
```

#### **Solutions**:
```bash
# Reset to clean state
git status
git stash  # Save local changes
git pull origin main
git stash pop  # Restore local changes

# Fix merge conflicts
git merge --abort  # Cancel problematic merge
git reset --hard origin/main  # Reset to remote state

# Check repository health
git fsck
git gc --prune=now  # Clean up repository
```

## 🔧 **Development Environment Recovery**

### **Complete Environment Reset**
```bash
# Full reset procedure (nuclear option)
cd /home/huuloc/Github/tn-da21ttb-phamhuuloc-aicodedetect

# 1. Kill all running processes
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# 2. Clean all environments
cd src/backend && rm -rf venv
cd src/frontend && rm -rf node_modules package-lock.json .next
cd src/src && rm -rf venv

# 3. Recreate everything
cd src/backend && make setup
cd src/frontend && npm install
cd src/src && make setup

# 4. Test everything
cd src/backend && make dev &
cd src/frontend && npm run dev &
curl http://localhost:8000/health
curl http://localhost:3000
```

### **Environment Verification Script**
```bash
#!/bin/bash
echo "=== AI Code Detection Environment Check ==="

# Check Python versions
echo "Python versions:"
python3 --version
cd src/backend && source venv/bin/activate && python --version
cd src/src && source venv/bin/activate && python --version

# Check Node.js
echo "Node.js version:"
node --version
npm --version

# Check running services
echo "Running services:"
lsof -i :8000 && echo "Backend running on 8000" || echo "Backend not running"
lsof -i :3000 && echo "Frontend running on 3000" || echo "Frontend not running"

# Check API connectivity
echo "API connectivity:"
curl -s http://localhost:8000/health && echo "API healthy" || echo "API not responding"

echo "Environment check complete."
```

## 📊 **Monitoring & Debugging Tools**

### **Real-time Monitoring**
```bash
# Monitor API requests
tail -f src/backend/logs/access.log

# Monitor system resources
watch -n 1 'ps aux | grep -E "(python|node)" | head -10'

# Monitor network connections
watch -n 1 'netstat -tulpn | grep -E "(3000|8000)"'

# Monitor file changes
inotifywait -m -r src/ --format '%w%f %e' | grep -v __pycache__
```

### **Advanced Debugging**
```bash
# Python debugging with pdb
cd src/backend
python -m pdb app/main.py

# Node.js debugging
cd src/frontend
npm run dev -- --inspect

# API debugging with verbose curl
curl -v -X POST http://localhost:8000/api/analysis/combined-analysis \
  -H "Content-Type: application/json" \
  -d '{"code":"int main(){return 0;}", "language":"c"}'
```

## 🚀 **Performance Optimization**

### **Backend Optimization**
```bash
# Use production server
cd src/backend
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Profile Python code
python -m cProfile -o profile.stats your_script.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats()"

# Monitor memory usage
python -m memory_profiler your_script.py
```

### **Frontend Optimization**
```bash
# Analyze bundle size
cd src/frontend
npm run build
npx @next/bundle-analyzer

# Performance testing
npx lighthouse http://localhost:3000

# Monitor React performance
npm run dev -- --profile
```

**Summary**: Comprehensive troubleshooting guide covering all common issues in AI Code Detection project development. Updated with latest solutions and best practices as of December 2024.