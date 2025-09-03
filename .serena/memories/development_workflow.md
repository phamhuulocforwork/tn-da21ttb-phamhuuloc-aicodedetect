# Development Workflow

## Git Workflow

### Branch Strategy
```
main (production-ready)
├── develop (integration branch)
│   ├── feature/auth-integration
│   ├── feature/batch-analysis
│   ├── bugfix/api-validation
│   └── refactor/frontend-optimization
└── hotfix/critical-security-fix
```

### Branch Naming Convention
```bash
# Feature branches
feature/add-oauth2-support
feature/improve-analysis-accuracy
feature/add-chart-visualization

# Bugfix branches
bugfix/handle-empty-files
bugfix/fix-memory-leak
bugfix/correct-validation-logic

# Refactor branches
refactor/optimize-database-queries
refactor/simplify-api-endpoints
refactor/cleanup-unused-code

# Hotfix branches (from main)
hotfix/security-vulnerability-patch
hotfix/critical-api-fix
```

### Commit Message Format
```bash
# Format: type(scope): description

# Feature commits
feat(auth): implement OAuth2 Google Drive integration
feat(api): add batch file analysis endpoint
feat(frontend): add real-time analysis progress

# Fix commits
fix(validation): handle edge case for empty C files
fix(memory): prevent memory leaks in large file processing
fix(ui): correct chart rendering on mobile devices

# Documentation
docs(readme): update API usage examples
docs(api): add Swagger documentation for new endpoints

# Refactoring
refactor(backend): extract common analysis logic to utils
refactor(frontend): optimize component re-renders
refactor(db): improve query performance

# Testing
test(api): add unit tests for file validation
test(frontend): add integration tests for analysis flow
test(e2e): add end-to-end test for complete user journey

# Chore/Maintenance
chore(deps): update Python dependencies to latest versions
chore(docker): optimize container build process
chore(ci): configure automated testing pipeline
```

## Development Process

### 1. Task Planning
```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# Or create bugfix branch
git checkout -b bugfix/issue-description
```

### 2. Development Cycle
```bash
# Start development environment
cd src/frontend && npm run dev    # Terminal 1
cd src/backend && uvicorn app.main:app --reload  # Terminal 2

# Or use Docker for full environment
docker-compose -f docker-compose.dev.yml up -d
```

### 3. Code Quality Checks
```bash
# Frontend checks
cd src/frontend
npm run lint
npm run format
npm run type-check

# Backend checks
cd src/backend
python -m flake8 app/
python -m black --check app/
python -m mypy app/

# Analysis modules
cd src/src
python -m pylint features/
```

### 4. Testing
```bash
# Frontend tests
cd src/frontend
npm run test
npm run test:coverage

# Backend tests
cd src/backend
pytest
pytest --cov=app --cov-report=html

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### 5. Commit & Push
```bash
# Stage changes
git add .

# Commit with proper message
git commit -m "feat(api): add batch analysis endpoint

- Add new POST /api/analysis/batch endpoint
- Support ZIP and RAR file uploads
- Implement concurrent file processing
- Add progress tracking and error handling"

# Push to remote
git push origin feature/new-feature
```

### 6. Pull Request Process
```markdown
## Pull Request Template

### Description
Brief description of the changes made.

### Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactoring

### Changes Made
- Change 1: Description
- Change 2: Description
- Change 3: Description

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

### Screenshots (if applicable)
Add screenshots of UI changes.

### Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added for new functionality
- [ ] All CI checks pass
- [ ] Reviewed by at least one team member
```

## Code Review Process

### Review Checklist
```markdown
## Code Review Checklist

### Functionality
- [ ] Code works as expected
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] Security considerations addressed

### Code Quality
- [ ] Follows coding standards
- [ ] Proper type hints (Python) / types (TypeScript)
- [ ] No linting errors
- [ ] Code is readable and maintainable
- [ ] DRY principle followed
- [ ] SOLID principles followed

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Test coverage maintained
- [ ] Edge cases tested

### Documentation
- [ ] Code is well-documented
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Comments added for complex logic

### Performance
- [ ] No performance regressions
- [ ] Efficient algorithms used
- [ ] Memory usage optimized
- [ ] Database queries optimized
```

### Review Comments Format
```markdown
## Code Review Comments

### ✅ Good Practices
- Great error handling implementation
- Clean separation of concerns
- Good test coverage

### 🔄 Suggestions
- Consider extracting this logic to a separate function
- Add type hints for better clarity
- Consider using async/await for better performance

### ⚠️ Issues to Fix
- Missing input validation
- Potential security vulnerability
- Memory leak in this function

### ❓ Questions
- Why did you choose this approach over alternative X?
- Is this the best place for this logic?
- Have you considered the performance impact?
```

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install backend dependencies
      run: |
        cd src/backend
        pip install -r requirements.txt
    
    - name: Install frontend dependencies
      run: |
        cd src/frontend
        npm ci
    
    - name: Run backend tests
      run: |
        cd src/backend
        pytest --cov=app --cov-report=xml
    
    - name: Run frontend tests
      run: |
        cd src/frontend
        npm run test:ci
    
    - name: Build frontend
      run: |
        cd src/frontend
        npm run build
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
```

### Pre-commit Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Frontend checks
cd src/frontend
npm run lint
npm run format:check
npm run type-check

# Backend checks
cd ../backend
python -m flake8 app/
python -m black --check app/

# Analysis modules
cd ../src
python -m pylint features/

echo "Pre-commit checks completed!"
```

## Release Process

### Version Management
```bash
# Semantic versioning
MAJOR.MINOR.PATCH

# Examples:
1.0.0 - Initial release
1.1.0 - New features added
1.1.1 - Bug fixes
2.0.0 - Breaking changes
```

### Release Steps
```bash
# 1. Create release branch
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# 2. Update version numbers
# Update package.json
# Update requirements.txt versions
# Update Dockerfile labels

# 3. Run full test suite
npm run test:full
pytest --cov=app

# 4. Update changelog
# docs/CHANGELOG.md
# - New features
# - Bug fixes
# - Breaking changes

# 5. Merge to main
git checkout main
git merge release/v1.2.0

# 6. Create git tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags

# 7. Deploy to production
./scripts/deploy.sh

# 8. Merge back to develop
git checkout develop
git merge release/v1.2.0
git push origin develop
```

## Environment Management

### Local Development Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd tn-da21ttb-phamhuuloc-aicodedetect

# 2. Setup Python environment
cd src/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Setup Node.js environment
cd ../frontend
npm install

# 4. Setup environment variables
cp .env.example .env
# Configure API keys and settings

# 5. Start development servers
# Backend: uvicorn app.main:app --reload
# Frontend: npm run dev
```

### Docker Development
```bash
# Development environment
docker-compose -f docker-compose.dev.yml up -d

# With hot reload
docker-compose -f docker-compose.dev.yml up

# Clean rebuild
docker-compose -f docker-compose.dev.yml build --no-cache
```

## Monitoring & Debugging

### Logging Standards
```python
# Backend logging
import logging

logger = logging.getLogger(__name__)

def analyze_code(code: str):
    logger.info(f"Starting code analysis for {len(code)} characters")
    try:
        result = perform_analysis(code)
        logger.info("Analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise
```

```typescript
// Frontend logging
const logger = {
  info: (message: string, data?: any) => {
    console.log(`[INFO] ${message}`, data);
  },
  error: (message: string, error?: any) => {
    console.error(`[ERROR] ${message}`, error);
  },
  warn: (message: string, data?: any) => {
    console.warn(`[WARN] ${message}`, data);
  }
};
```

### Performance Monitoring
```python
# Performance tracking
import time
from functools import wraps

def performance_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f}s: {e}")
            raise
    return wrapper
```

## Security Practices

### Code Security
```bash
# Security scanning
# Use tools like:
npm audit          # Frontend dependencies
safety check       # Python dependencies
bandit -r .        # Python security linting
snyk test          # General security scanning
```

### API Security
```python
# Input validation
from pydantic import BaseModel, validator
from fastapi import HTTPException

class CodeAnalysisRequest(BaseModel):
    code: str
    
    @validator('code')
    def validate_code_length(cls, v):
        if len(v) > 50000:  # 50KB limit
            raise ValueError('Code too long')
        return v

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/analysis/")
@limiter.limit("10/minute")
async def analyze_code(request: CodeAnalysisRequest):
    # Analysis logic
    pass
```

### Environment Security
```bash
# Environment variables
# Never commit secrets to git
# Use .env files for local development
# Use Docker secrets or cloud secret managers for production

# .env structure
GEMINI_API_KEY=your_secure_key_here
GOOGLE_DRIVE_API_KEY=your_drive_key_here
SECRET_KEY=your_jwt_secret_here
```

## Documentation

### API Documentation
```python
# FastAPI automatic documentation
from fastapi import FastAPI

app = FastAPI(
    title="AI Code Detection API",
    description="API for detecting AI-generated code patterns",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # ReDoc
)

@app.post("/api/analysis/", 
    summary="Analyze code for AI patterns",
    description="Comprehensive analysis of code to detect AI-generated patterns",
    response_model=AnalysisResponse
)
async def analyze_code(request: CodeAnalysisRequest):
    """Analyze code for AI-generated patterns."""
    pass
```

### Component Documentation
```typescript
/**
 * AnalysisCard component for displaying code analysis results
 * 
 * @param score - AI probability score (0-1)
 * @param confidence - Analysis confidence level
 * @param features - Extracted code features
 * @param onRetry - Callback for retrying analysis
 */
interface AnalysisCardProps {
  score: number;
  confidence: number;
  features: CodeFeatures;
  onRetry?: () => void;
}
```