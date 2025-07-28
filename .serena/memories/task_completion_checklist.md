# Task Completion Checklist - Checklist khi hoàn thành task

## Trước khi commit code

### Backend Changes
- [ ] **Code formatting**: Đảm bảo code tuân thủ PEP 8
- [ ] **Virtual environment**: Test trong clean venv  
- [ ] **Dependencies**: Update requirements.txt nếu có package mới
- [ ] **API testing**: Test endpoints qua http://localhost:8000/docs
- [ ] **Error handling**: Có try-catch và logging phù hợp
- [ ] **CORS**: Đảm bảo frontend có thể access API

### Frontend Changes  
- [ ] **Linting**: `npm run lint` không có errors
- [ ] **Formatting**: `npm run format` đã chạy
- [ ] **Type checking**: TypeScript compilation thành công
- [ ] **Build**: `npm run build` successful
- [ ] **Browser testing**: Test trên localhost:3000
- [ ] **Responsive**: Check mobile/desktop views

### ML/Data Science Changes
- [ ] **Data validation**: Đảm bảo input/output data đúng format
- [ ] **Jupyter outputs**: Clear outputs trước khi commit .ipynb files
- [ ] **File paths**: Đảm bảo relative paths hoạt động trên WSL
- [ ] **Dependencies**: Update requirements.txt trong src/src/
- [ ] **Sample data**: Có sample data để test

## General Quality Checks
- [ ] **File encoding**: UTF-8 cho all text files
- [ ] **Environment files**: .env.example updated if needed
- [ ] **Documentation**: Comments/docstrings cập nhật
- [ ] **Git**: Proper commit message
- [ ] **No secrets**: Không commit API keys hay sensitive data
- [ ] **File permissions**: Appropriate cho WSL environment

## Testing Workflow
1. **Backend**: `cd src/backend && make dev` - verify server starts
2. **Frontend**: `cd src/frontend && npm run dev` - verify app loads  
3. **ML components**: Test script execution manually
4. **Integration**: Test frontend-backend communication nếu có

## Deployment Readiness
- [ ] **Production builds**: Frontend build thành công
- [ ] **Environment configs**: Production-ready configs  
- [ ] **Dependencies**: Production dependencies only
- [ ] **Performance**: No obvious performance issues
- [ ] **Security**: No hardcoded secrets or vulnerabilities

## Documentation Updates
- [ ] **README**: Update nếu có changes significant
- [ ] **API docs**: Auto-generated FastAPI docs current
- [ ] **Comments**: Code comments cập nhật với changes
- [ ] **Thesis notes**: Document technical decisions cho luận văn