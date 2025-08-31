# AI Code Detection Backend

FastAPI backend cho hệ thống phân tích mã nguồn AI vs Human detection.

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Setup environment
make setup

# Run development server
make dev

# Server will be available at: http://localhost:8000
# API docs: http://localhost:8000/docs
```

### Option 2: Docker

```bash
# Build and run với Docker Compose
docker-compose up --build

# Server available at: http://localhost:8000
```

### Option 3: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

## 📁 Project Structure

```
src/backend/
├── app/
│   ├── __init__.py
│   └── main.py              # Main FastAPI application
├── test_api.py              # API test suite
├── API_DOCUMENTATION.md     # Complete API documentation
├── Dockerfile               # Docker container setup
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
└── Makefile                # Development commands
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Detailed health status |
| `/api/analysis/combined-analysis` | POST | Complete analysis (80+ features) |
| `/api/analysis/ast-analysis` | POST | AST analysis only |
| `/api/analysis/human-style` | POST | Human style analysis only |
| `/api/analysis/advanced-features` | POST | Advanced features only |
| `/api/analysis/upload-file` | POST | File upload analysis |
| `/api/analysis/methods` | GET | Available analysis methods |

## 🧪 Testing

```bash
# Run API tests (server must be running)
python test_api.py

# Or test individual endpoints
curl http://localhost:8000/health
```

## 📚 Documentation

- **API Documentation**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Development

### Available Make Commands

```bash
make help     # Show all available commands
make setup    # Setup virtual environment
make install  # Install/update dependencies  
make dev      # Run development server
make start    # Run production server
make clean    # Clean up environment
```

### Environment Variables

Create `.env` file (optional):

```bash
ENVIRONMENT=development
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
MAX_FILE_SIZE=1048576  # 1MB in bytes
```

## 🏗️ Architecture

### Analysis Modules Integration

Backend tích hợp với analysis modules từ `../src/features/`:

- **AdvancedFeatureExtractor**: Complete feature extraction (80+ features)
- **CppASTAnalyzer**: AST structure analysis
- **HumanStyleAnalyzer**: Human coding style patterns

### Response Format

Tất cả endpoints trả về structured JSON với:

- **Basic Info**: filename, language, LOC, file size
- **Feature Groups**: Organized features for visualization
- **Assessment**: Overall score, confidence, key indicators
- **Raw Features**: All extracted features for advanced usage

### Error Handling

- Comprehensive error handling với HTTP status codes
- Graceful degradation khi analysis modules không available
- Input validation với Pydantic models

## 🔄 Frontend Integration

Backend được thiết kế để tích hợp với Next.js frontend:

- **CORS enabled** cho localhost:3000
- **Structured responses** cho easy chart rendering
- **Feature grouping** cho organized visualization
- **File upload support** với validation

## 📈 Performance

- **Response Time**: 1-5 seconds tùy analysis type
- **Memory Usage**: ~50-100MB per request
- **Concurrency**: FastAPI async support
- **File Size Limit**: 1MB per upload

## 🛠️ Next Features

- [ ] **Authentication**: API key validation
- [ ] **Rate Limiting**: Request throttling
- [ ] **Caching**: Redis integration cho repeated analysis
- [ ] **Database**: PostgreSQL để store analysis history
- [ ] **Batch Processing**: Multiple file analysis
- [ ] **Report Export**: PDF/CSV generation
- [ ] **WebSocket**: Real-time analysis progress

## 🐛 Troubleshooting

### Common Issues

1. **Analysis modules not found**:
   ```bash
   # Check Python path includes ../src
   export PYTHONPATH="${PYTHONPATH}:../src"
   ```

2. **Port already in use**:
   ```bash
   # Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

3. **CORS errors**:
   - Ensure frontend URL is in CORS_ORIGINS
   - Check browser developer tools for exact error

4. **File upload fails**:
   - Check file size < 1MB
   - Verify file extension (.c, .cpp, .txt)
   - Ensure UTF-8 encoding

## 📞 Support

- **API Issues**: Check `/health` endpoint
- **Analysis Errors**: Review server logs
- **Feature Requests**: Update PLAN.md
- **Documentation**: Read API_DOCUMENTATION.md