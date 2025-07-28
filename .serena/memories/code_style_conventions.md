# Code Style và Conventions

## Python (Backend & ML)
- **PEP 8** standard formatting
- **Function names**: snake_case (vd: create_metadata, generate_code)
- **Variables**: snake_case (vd: problem_id, submission_id) 
- **Constants**: UPPER_CASE (vd: GEMINI_API_KEY)
- **Comments**: Tiếng Việt cho mô tả business logic
- **Docstrings**: Tiếng Việt với format đơn giản
- **Error handling**: Try-catch với logging chi tiết
- **File encoding**: UTF-8

### Backend FastAPI
- **Route naming**: REST-style với kebab-case 
- **Model naming**: PascalCase cho Pydantic models
- **CORS**: Đã cấu hình cho development (allow all origins)
- **API documentation**: Tự động với FastAPI Swagger

## TypeScript/React (Frontend)
- **ESLint** + **Prettier** configuration có sẵn
- **Component names**: PascalCase (VD: CodeEditor, AnalysisResult)
- **File names**: kebab-case cho components (vd: code-editor.tsx)
- **Styling**: TailwindCSS utility classes
- **Import organization**: Auto-sorted với prettier plugin
- **Type definitions**: Strict TypeScript mode

### Next.js Conventions  
- **App Router** structure (không Page Router)
- **Server Components** by default
- **File structure**: app/ directory routing
- **Styling**: Tailwind classes, CSS modules nếu cần

## General Conventions
- **Environment variables**: .env files với .env.example templates
- **Dependencies**: Lock files (package-lock.json, requirements.txt)
- **Documentation**: README files ở mỗi component chính
- **Git**: Conventional commits preferred
- **Encoding**: UTF-8 cho tất cả text files
- **Line endings**: LF (Unix style) - phù hợp WSL2

## Makefile Standards
- **Color coding**: Green, Blue, Yellow, Red cho output messages
- **Help targets**: `make help` available trong mỗi Makefile
- **PHONY targets**: Properly declared  
- **Virtual environment**: Consistent venv/ directory naming