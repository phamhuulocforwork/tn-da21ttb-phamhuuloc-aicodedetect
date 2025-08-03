# Tech Stack Details - Chi tiết công nghệ sử dụng

## Core ML/Data Science Stack
### Python Dependencies (src/src/requirements.txt):
- **numpy==1.26**: Numerical computing
- **pandas==2.0.3**: Data manipulation và analysis
- **scikit-learn==1.3.0**: Machine learning algorithms
- **matplotlib==3.7.2**: Data visualization
- **seaborn==0.12.2**: Statistical visualization
- **tqdm==4.65.0**: Progress bars

<<<<<<< Updated upstream
## Backend API (src/backend/)
- **FastAPI** 0.104.1 - Modern Python web framework
- **uvicorn** 0.24.0 - ASGI server với hot reload
- **python-multipart** 0.0.6 - File upload support
- **CORS middleware** - Cho phép frontend truy cập API
- **Cổng mặc định**: 8000
- **API Documentation**: http://localhost:8000/docs
=======
### Development Environment:
- **Python**: Version 3.x
- **Jupyter Notebook**: Interactive development (index.ipynb)
- **Environment**: WSL2 Linux (6.6.87.2-microsoft-standard-WSL2)

## Frontend Stack (Next.js Application)
### Core Framework:
- **Next.js**: 15.3.5 (với App Router)
- **React**: 19.0.0 (latest stable)
- **TypeScript**: ^5.x
- **Node.js**: Version compatible với Next.js 15
>>>>>>> Stashed changes

### UI Libraries và Components:
- **TailwindCSS**: ^4.x (utility-first CSS)
- **Radix UI**: 
  - @radix-ui/react-select: ^2.2.5 (dropdown components)
  - radix-ui: ^1.4.2 (general components)
- **Lucide React**: ^0.525.0 (icons)
- **@firecms/neat**: ^0.4.0 (UI enhancements)

### Code Editor Integration:
- **@monaco-editor/react**: ^4.7.0 (VS Code editor trong browser)
- **highlight.js**: ^11.11.1 (syntax highlighting)

### Styling và Animation:
- **Framer Motion**: ^12.23.6 (animations)
- **next-themes**: ^0.4.6 (dark/light mode)
- **class-variance-authority**: ^0.7.1 (conditional styling)
- **clsx**: ^2.1.1 (className utilities)
- **tailwind-merge**: ^3.3.1 (merge Tailwind classes)

### 3D Graphics:
- **three.js**: ^0.77.1 (3D graphics, có thể cho visualization)

### Development Tools:
- **ESLint**: ^9 với config-next
- **Prettier**: ^3.5.2 với multiple plugins:
  - prettier-plugin-organize-imports: ^4.1.0
  - prettier-plugin-tailwindcss: ^0.6.11
  - @trivago/prettier-plugin-sort-imports: ^5.2.2
- **@tailwindcss/postcss**: ^4
- **tw-animate-css**: ^1.3.5

### Scripts Available:
```bash
npm run dev          # Development với Turbopack
npm run build        # Production build
npm run start        # Production server
npm run lint         # ESLint check
npm run format       # Prettier formatting
npm run clean        # Remove .next
npm run clean:all    # Remove .next và node_modules
```

## Backend Stack (FastAPI)
### Core:
- **FastAPI**: Python web framework
- **uvicorn**: ASGI server
- **python-multipart**: File upload support

### Environment:
- **Virtual Environment**: `src/backend/venv/`
- **Development**: Makefile cho setup commands

## AI Integration
### APIs:
- **Google Gemini API**: Code generation cho AI samples
- **Environment Variables**: API keys trong .env files

## Development Environment
### OS & Shell:
- **Linux**: 6.6.87.2-microsoft-standard-WSL2
- **Shell**: /usr/bin/zsh
- **Workspace**: `/home/huuloc/Github/tn-da21ttb-phamhuuloc-aicodedetect-ml-py`

### IDE/Editor:
- **Cursor**: Primary IDE
- **VS Code**: Compatible environment
- **Configuration files**:
  - .cursorignore, .editorconfig
  - ESLint, Prettier configs

## Build Tools & Configuration
### Package Managers:
- **npm**: Frontend dependencies
- **pip**: Python dependencies
- **Makefile**: Automation scripts

### Configuration Files:
- **next.config.ts**: Next.js configuration
- **tsconfig.json**: TypeScript settings
- **postcss.config.mjs**: PostCSS processing
- **components.json**: Radix UI setup

## Version Control & Quality
- **Git**: Source control với .gitignore files
- **Code Quality**: ESLint + Prettier integration
- **Type Safety**: Full TypeScript coverage
- **Performance**: Next.js 15 với Turbopack bundler

## Current Issues với Tech Stack:
- ML dependencies có thể cần update (scikit-learn 1.3.0 không phải latest)
- Model performance issues có thể do version compatibility
- Cần review Python package versions cho production readiness
