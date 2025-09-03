# Memory Index - AI Code Detection System

## Tổng quan Memories

Dự án AI Code Detection System đã được cập nhật đầy đủ với các memories sau:

## 📋 Danh sách Memories

### 1. project_overview
**Mục đích**: Tổng quan về dự án AI Code Detection System
**Nội dung**:
- Thông tin dự án (trường, khoa, sinh viên, giảng viên)
- Mục tiêu nghiên cứu và các tính năng chính
- Kiến trúc hệ thống và các thành phần
- Đối tượng sử dụng

### 2. tech_stack
**Mục đích**: Thông tin về công nghệ và dependencies
**Nội dung**:
- Frontend: Next.js, TypeScript, TailwindCSS, Radix UI, Chart.js
- Backend: FastAPI, Python, Uvicorn, Pydantic
- Analysis: Google Gemini AI, AST analyzer, feature extractors
- DevOps: Docker, Docker Compose, Nginx, Let's Encrypt
- Requirements và environment variables

### 3. suggested_commands
**Mục đích**: Các lệnh phát triển quan trọng
**Nội dung**:
- Frontend: npm install, npm run dev, npm run build, npm run lint
- Backend: pip install, uvicorn, pytest
- Docker: docker-compose commands
- Management: ./scripts/manage.sh commands
- Development workflow và debugging

### 4. code_style
**Mục đích**: Quy ước code style và conventions
**Nội dung**:
- TypeScript/JavaScript: ESLint config, naming conventions, import style
- Python: PEP 8, type hints, error handling
- File organization structure
- Documentation standards (JSDoc, docstrings)
- Testing conventions

### 5. development_workflow
**Mục đích**: Quy trình phát triển và best practices
**Nội dung**:
- Git workflow và branching strategy
- Code review process và checklist
- CI/CD pipeline với GitHub Actions
- Testing strategy và coverage
- Security practices và monitoring
- Release process và versioning

### 6. deployment_guide
**Mục đích**: Hướng dẫn triển khai production
**Nội dung**:
- Automated deployment với scripts
- Manual deployment steps
- Docker configuration và optimization
- SSL setup với Let's Encrypt
- Monitoring, backup và recovery
- Security hardening và cost optimization

## 🔍 Cách sử dụng Memories

### Đọc Memory cụ thể
```bash
# Đọc memory về tech stack
mcp_serena_read_memory memory_name: "tech_stack"

# Đọc memory về commands
mcp_serena_read_memory memory_name: "suggested_commands"
```

### Tìm kiếm trong Memories
Sử dụng các memory files để:
- **Bắt đầu phát triển**: Đọc `tech_stack` và `suggested_commands`
- **Viết code**: Tham khảo `code_style` cho conventions
- **Quy trình**: Đọc `development_workflow` cho Git workflow
- **Triển khai**: Đọc `deployment_guide` cho production setup

## 📚 Quick Reference

### Development Setup
```bash
# 1. Cài đặt dependencies
cd src/frontend && npm install
cd ../backend && pip install -r requirements.txt

# 2. Khởi chạy development
npm run dev          # Frontend (port 3000)
uvicorn app.main:app --reload  # Backend (port 8000)

# 3. Hoặc dùng Docker
docker-compose -f docker-compose.dev.yml up -d
```

### Production Deployment
```bash
# Automated deployment
./scripts/setup-vps.sh
./scripts/deploy.sh

# Manual deployment
docker-compose up --build -d
./scripts/manage.sh health
```

### Code Quality
```bash
# Frontend
npm run lint && npm run format

# Backend
python -m flake8 app/ && python -m black app/

# Testing
pytest && npm run test
```

## 🎯 Key Information Summary

### Tech Stack
- **Frontend**: Next.js 15, TypeScript, TailwindCSS
- **Backend**: FastAPI, Python 3.8+, Google Gemini AI
- **Database**: PostgreSQL (optional)
- **Deployment**: Docker, Nginx, Let's Encrypt SSL

### Main Features
- Single file analysis với AI patterns
- Batch analysis từ ZIP/RAR hoặc Google Drive
- Real-time progress tracking
- Interactive charts và visualizations
- RESTful API với comprehensive documentation

### Development Commands
- `npm run dev` - Frontend development
- `uvicorn app.main:app --reload` - Backend development
- `docker-compose up -d` - Full stack development
- `./scripts/manage.sh status` - Service monitoring

### Production URLs
- Frontend: `https://your-domain.com`
- API: `https://your-domain.com/api`
- Docs: `https://your-domain.com/docs`

## 📞 Support & Resources

### Documentation
- README.md: Project overview và setup
- API Docs: `/docs` (Swagger UI)
- Code comments: Comprehensive inline documentation

### Useful Links
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/
- Docker: https://docs.docker.com/
- Google AI Studio: https://makersuite.google.com/

### Maintenance
- Health checks: `./scripts/manage.sh health`
- Logs: `./scripts/manage.sh logs`
- Backup: `./scripts/manage.sh backup`
- SSL renewal: `./scripts/manage.sh ssl-renew`

## 🔄 Memory Updates

Khi có thay đổi trong dự án, hãy cập nhật memories tương ứng:
- `tech_stack`: Khi thêm/cập nhật dependencies
- `suggested_commands`: Khi thêm scripts hoặc workflows
- `code_style`: Khi thay đổi coding conventions
- `development_workflow`: Khi cải thiện development process
- `deployment_guide`: Khi cập nhật infrastructure

## ✅ Onboarding Complete

Tất cả memories đã được tạo và cập nhật cho dự án AI Code Detection System. Bạn có thể bắt đầu phát triển ngay bây giờ với đầy đủ thông tin cần thiết về:
- Kiến trúc và công nghệ sử dụng
- Quy trình phát triển và best practices
- Commands và workflows
- Deployment và maintenance
- Code style và conventions

Chúc bạn phát triển dự án thành công! 🚀