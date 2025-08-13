# AI Code Detection - Task Completion Workflow

## Khi hoàn thành một task, cần thực hiện theo thứ tự

## 1. Code Quality Checks

### Backend (Python)

```bash
cd src/backend
# Kiểm tra syntax và potential issues
python -m py_compile app/*.py
# Kiểm tra import statements
python -c "import app.main"
```

### Frontend (TypeScript/React)

```bash
cd src/frontend
# Linting
npm run lint
# Format check
npm run formatcheck
# Type checking
npx tsc --noEmit
```

### ML Pipeline (Python)

```bash
cd src/src
# Kiểm tra syntax
python -m py_compile *.py
# Test import các modules chính
python -c "import batch_feature_extraction, analyze_features, complete_pipeline"
```

## 2. Testing

### Backend Testing

```bash
cd src/backend
# Kiểm tra server có start được không
make dev &
sleep 5
curl http//localhost8000/health
pkill -f uvicorn
```

### Frontend Testing

```bash
cd src/frontend
# Build test để kiểm tra TypeScript errors
npm run build
```

### ML Pipeline Testing

```bash
cd src/src
# Test chạy pipeline với sample data
python batch_feature_extraction.py --dataset dataset --max-files 10 --output test_features.csv
python analyze_features.py --csv test_features.csv --plots-dir test_plots
rm test_features.csv
rm -rf test_plots
```

## 3. Documentation Updates

### Khi thay đổi API endpoints

- Cập nhật FastAPI docstrings
- Kiểm tra API docs tại http//localhost8000/docs

### Khi thay đổi ML features

- Cập nhật comments trong feature extraction code
- Cập nhật analysis visualization nếu cần

### Khi thay đổi UI components

- Cập nhật component props documentation
- Kiểm tra responsive design

## 4. Git Workflow

```bash
# Kiểm tra status
git status

# Stage changes
git add .

# Commit với descriptive message
git commit -m "feat [mô tả thay đổi]"
# hoặc
git commit -m "fix [mô tả bug fix]"
# hoặc
git commit -m "docs [mô tả documentation update]"

# Push nếu cần
git push origin main
```

## 5. Environment Cleanup

### Sau khi development

```bash
# Stop all running servers
pkill -f uvicorn
pkill -f "next dev"

# Clean temporary files
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

## 6. Performance Checks

### Backend Performance

- Kiểm tra response time của API endpoints
- Memory usage khi processing large files

### Frontend Performance

- Bundle size analysis `npm run build`
- Loading speed của components

### ML Pipeline Performance

- Processing time cho batch feature extraction
- Memory usage khi load large datasets

## 7. Security Considerations

### API Security

- Validate input parameters
- Proper error handling không expose sensitive info

### File Handling

- Kiểm tra file size limits
- Validate file types khi upload

## 8. Final Verification

Trước khi kết thúc task

- [ ] All linting issues resolved
- [ ] No TypeScript compilation errors
- [ ] Backend API responses correctly
- [ ] Frontend builds successfully
- [ ] ML pipeline runs without errors
- [ ] Documentation updated if needed
- [ ] Git commit with proper message
- [ ] No temporary/test files left behind
