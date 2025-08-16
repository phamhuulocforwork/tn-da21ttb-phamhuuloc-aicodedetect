# Task Completion Guidelines

## Khi Hoàn Thành Task

### 1. Code Quality Checks

#### Python Code (ML Core + Backend)

```bash
# Ensure virtual environment is activated
cd src/src && source venv/bin/activate

# Run basic syntax check
python -m py_compile *.py

# Test critical functions manually
python -c "from complete_pipeline import AICodeDetectionPipeline; print('Import successful')"
```

#### Backend API Testing

```bash
cd src/backend

# Start server trong background
make dev &

# Wait for server startup
sleep 5

# Test endpoints
curl http://localhost:8000/health
python test_api.py

# Kill background server
kill %1
```

#### Frontend Testing

```bashs
cd src/frontend

# Lint check
npm run lint

# Format check
npm run format:check

# Build test
npm run build

# Type checking
npx tsc --noEmit
```

### 2. Integration Testing

#### Full Stack Integration

```bash
# Terminal 1: Start backend
cd src/backend && make dev

# Terminal 2: Start frontend
cd src/frontend && npm run dev

# Terminal 3: Manual testing
curl -X POST http://localhost:8000/api/analysis/combined-analysis \
  -H "Content-Type: application/json" \
  -d '{"code":"#include <stdio.h>\nint main(){return 0;}", "language":"c"}'

# Visit http://localhost:3000 và test UI
```

#### API Endpoint Validation

```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:8000/api/analysis/methods

# Sample analysis tests
curl -X POST http://localhost:8000/api/analysis/ast-analysis \
  -H "Content-Type: application/json" \
  -d '{"code":"int main(){printf(\"test\");return 0;}", "language":"c"}'
```

### 3. Performance Verification

#### ML Pipeline Performance

```bash
cd src/src && source venv/bin/activate

# Test batch processing performance
time python batch_feature_extraction.py --dataset dataset --max-files 100 --output test_features.csv

# Verify model training
time python complete_pipeline.py train dataset --max-files 100 --save-model test_model.json

# Cleanup test files
rm test_features.csv test_model.json
```

#### API Response Times

```bash
# Time individual endpoints
time curl -X POST http://localhost:8000/api/analysis/combined-analysis \
  -H "Content-Type: application/json" \
  -d '{"code":"#include <stdio.h>\nint main(){return 0;}", "language":"c"}'

# Expected: < 5 seconds for combined analysis
# Expected: < 2 seconds for individual analysis methods
```

### 4. File and Directory Cleanup

#### Development Artifacts

```bash
# Clean Python cache files
find . -type d -name "__pycache__" -delete
find . -type f -name "*.pyc" -delete

# Clean temporary analysis files
cd src/src
rm -f *.log *.tmp
rm -rf analysis_plots/*.png (if temporary)

# Clean Node.js artifacts
cd src/frontend
npm run clean
```

#### Log File Management

```bash
# Check for error logs
grep -r "ERROR" src/backend/
grep -r "CRITICAL" src/src/

# Clean old logs if any
find . -name "*.log" -mtime +7 -delete
```

### 5. Documentation Updates

#### Code Documentation

- Ensure new functions have proper docstrings
- Update API documentation if endpoints changed
- Add comments cho complex algorithms

#### Configuration Validation

```bash
# Verify requirements.txt is updated
cd src/backend && pip freeze > requirements_check.txt
diff requirements.txt requirements_check.txt
rm requirements_check.txt

# Verify package.json dependencies
cd src/frontend && npm outdated
```

### 6. Security Checks

#### File Permissions

```bash
# Ensure sensitive files không có inappropriate permissions
find . -name "*.env*" -exec chmod 600 {} \;
find . -name "*.key" -exec chmod 600 {} \;

# Check for exposed secrets
grep -r "password\|secret\|key" src/ --exclude-dir=node_modules --exclude-dir=venv
```

#### API Security

```bash
# Verify CORS settings
curl -H "Origin: http://malicious-site.com" http://localhost:8000/health

# Check file upload validation
curl -X POST http://localhost:8000/api/analysis/upload-file \
  -F "file=@/etc/passwd" \
  -F "language=c"
```

### 7. Final Verification Checklist

#### ✅ Before Task Completion

- [ ] All services start without errors
- [ ] API endpoints return expected responses
- [ ] Frontend loads và displays correctly
- [ ] File upload functionality works
- [ ] Analysis results are reasonable
- [ ] No critical errors trong logs
- [ ] Code follows project conventions
- [ ] No sensitive data exposed
- [ ] Dependencies are properly documented
- [ ] Integration tests pass

#### ✅ Production Readiness

- [ ] Environment variables properly configured
- [ ] Error handling covers edge cases
- [ ] Performance meets requirements (< 5s analysis)
- [ ] UI responsive trên mobile devices
- [ ] API documentation is current
- [ ] Logging is appropriate level
- [ ] No debug code left trong production
- [ ] Database connections are stable (if applicable)

### 8. Deployment Verification

#### Docker Deployment Test

```bash
cd src/backend
docker-compose up --build -d

# Test containerized API
curl http://localhost:8000/health

# Cleanup
docker-compose down
```

#### Frontend Build Test

```bash
cd src/frontend
npm run build
npm run start &

# Test production build
curl http://localhost:3000

# Kill production server
kill %1
```

## Common Issues và Solutions

### Backend Issues

- **Import errors**: Check PYTHONPATH includes ../src
- **Port conflicts**: Use `lsof -ti:8000 | xargs kill -9`
- **Module not found**: Ensure virtual environment activated

### Frontend Issues

- **Build failures**: Check TypeScript errors với `npx tsc --noEmit`
- **API connection**: Verify NEXT_PUBLIC_API_URL in .env.local
- **Styling issues**: Check Tailwind configuration

### Integration Issues

- **CORS errors**: Verify backend CORS_ORIGINS setting
- **Timeout errors**: Check analysis processing time
- **File upload issues**: Verify file size và type validation

## Success Criteria

Task completion is successful when:

1. **All components start cleanly** without errors
2. **API responses** are consistent và well-formed
3. **Frontend functionality** works end-to-end
4. **Performance requirements** are met
5. **Code quality standards** are maintained
6. **Documentation is updated** appropriately
7. **No regressions** trong existing functionality
