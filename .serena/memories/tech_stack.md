# Tech Stack & Dependencies

## Frontend Stack
### Core Framework
- **Next.js 15.3.5**: React framework với App Router, SSR/SSG
- **React 19.0.0**: UI library với concurrent features
- **TypeScript 5**: Type-safe JavaScript

### UI & Styling
- **TailwindCSS 4**: Utility-first CSS framework
- **Radix UI**: Accessible UI primitives (Accordion, Dialog, Dropdown, etc.)
- **Shadcn/UI**: Modern component library
- **Framer Motion**: Animation library
- **Lucide React**: Icon library

### Charts & Visualization
- **Chart.js 4.5.0**: Chart library
- **Recharts 2.15.4**: React chart library
- **ECharts 6.0.0**: Advanced charting
- **Chart.js Boxplot Plugin**: Statistical charts

### Development Tools
- **ESLint 9**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **Turbopack**: Fast bundler
- **Next Themes**: Dark/light mode

## Backend Stack
### Core Framework
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic 2.10.3**: Data validation

### AI & ML Libraries
- **Google GenAI**: Google Gemini AI integration
- **Lizard 1.17.10**: Code complexity analysis
- **NumPy 2.2.2**: Numerical computing
- **Pandas 2.2.3**: Data manipulation

### External APIs
- **Google API Python Client**: Google Drive integration
- **Requests 2.31.0**: HTTP client
- **AIOHTTP 3.10.11**: Async HTTP client

### File Processing
- **RarFile 4.1**: RAR archive support
- **AIOFiles**: Async file operations
- **Python Multipart**: File upload handling

## Analysis Modules (Python)
### Core Dependencies
- **NumPy 2.2.2**: Array operations
- **Pandas 2.2.3**: Data analysis
- **TQDM 4.65.0**: Progress bars
- **Matplotlib 3.5+**: Plotting
- **Seaborn 0.11+**: Statistical visualization

### Analysis Components
- **AST Analyzer**: Abstract Syntax Tree analysis
- **Human Style Analyzer**: Coding style pattern detection
- **Advanced Feature Extractor**: Feature engineering
- **Detection Models**: ML classification models

## DevOps & Infrastructure
### Containerization
- **Docker 20.10+**: Container runtime
- **Docker Compose**: Multi-container orchestration

### Web Server
- **Nginx**: Reverse proxy và load balancer
- **Let's Encrypt**: SSL certificate automation
- **Gunicorn**: WSGI server

### Development Tools
- **Git**: Version control
- **Makefile**: Build automation
- **Shell Scripts**: Deployment automation

## System Requirements
### Development
- **Python**: 3.8+
- **Node.js**: 18+
- **Docker**: 20.10+
- **Git**: Latest version

### Production
- **Ubuntu 22.04**: Recommended OS
- **4GB RAM**: Minimum
- **2 CPU cores**: Minimum
- **20GB Storage**: Minimum

## Environment Variables
### Backend (.env)
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_DRIVE_API_KEY=your_drive_api_key

# Optional
ENVIRONMENT=development
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000
MAX_FILE_SIZE=1048576
```

### Frontend (.env.local)
```bash
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_oauth_client_id

# Optional
NEXT_PUBLIC_ENABLE_CHARTS=true
NEXT_PUBLIC_MAX_CODE_LENGTH=50000
```

## Package Management
### Backend
- **requirements.txt**: Python dependencies
- **Pip**: Package installer
- **Virtual Environment**: Isolated Python environment

### Frontend
- **package.json**: Node.js dependencies
- **npm/yarn**: Package managers
- **package-lock.json**: Dependency lock file

## Build & Deployment
### Frontend Build
- **Next.js Build**: `npm run build`
- **Static Export**: `npm run export` (optional)
- **Optimization**: Turbopack for development

### Backend Build
- **Docker Build**: Multi-stage Dockerfile
- **Dependency Caching**: Docker layer optimization
- **Security**: Non-root user in production

### Production Deployment
- **Docker Compose**: Full-stack deployment
- **Nginx Proxy**: Load balancing và SSL
- **SSL Automation**: Let's Encrypt certificates
- **Health Checks**: Automated monitoring