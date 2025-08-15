# AI Code Detection API Documentation

## Overview

RESTful API cho phân tích mã nguồn để phát hiện patterns của AI-generated code vs human-written code.

**Base URL**: `http://localhost:8000`  
**API Docs**: `http://localhost:8000/docs` (Swagger UI)  
**ReDoc**: `http://localhost:8000/redoc`

---

## Authentication

Hiện tại API không yêu cầu authentication (development mode).

---

## Endpoints

### Health Check

#### `GET /`
Basic health check endpoint.

**Response:**
```json
{
  "message": "AI Code Detection API",
  "status": "running", 
  "version": "1.0.0",
  "analysis_modules": true
}
```

#### `GET /health`
Detailed health check với module status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T10:30:00",
  "modules": {
    "advanced_features": true,
    "ast_analyzer": true,
    "human_style_analyzer": true
  }
}
```

---

### Analysis Endpoints

#### `POST /api/analysis/combined-analysis`
**Comprehensive analysis** sử dụng tất cả phương thức (80+ features).

**Request Body:**
```json
{
  "code": "string (required, max 50000 chars)",
  "filename": "string (optional, default: 'code.c')",
  "language": "string (required, one of: 'c', 'cpp', 'c++')"
}
```

**Response:**
```json
{
  "success": true,
  "analysis_id": "analysis_abc123def456",
  "timestamp": "2024-01-20T10:30:00",
  "code_info": {
    "filename": "test.c",
    "language": "c",
    "loc": 25,
    "file_size": 1024
  },
  "feature_groups": {
    "structure_metrics": {
      "group_name": "Structure Metrics",
      "description": "Code structure, complexity and control flow analysis",
      "features": [
        {
          "name": "loc",
          "value": 25,
          "normalized": true,
          "interpretation": "Medium codebase (25 lines)",
          "weight": 1.0
        }
      ],
      "group_score": 0.35,
      "visualization_type": "bar"
    },
    "style_metrics": { /* ... */ },
    "complexity_metrics": { /* ... */ },
    "ai_detection_metrics": { /* ... */ }
  },
  "assessment": {
    "overall_score": 0.42,
    "confidence": 0.85,
    "key_indicators": [
      "High human-style inconsistencies detected",
      "Natural code structure found"
    ],
    "summary": "Code shows mixed characteristics, manual review recommended"
  },
  "raw_features": {
    "loc": 25,
    "cyclomatic_complexity": 3.5,
    "halstead_complexity": 45.2,
    // ... 80+ features
  }
}
```

#### `POST /api/analysis/ast-analysis`
**AST-only analysis** - cấu trúc, control flow, functions, naming.

**Request:** Same as combined analysis  
**Response:**
```json
{
  "success": true,
  "analysis_id": "analysis_xyz789",
  "timestamp": "2024-01-20T10:30:00",
  "analysis_type": "ast_only",
  "code_info": { /* ... */ },
  "features": {
    "total_nodes": 45,
    "max_depth": 3,
    "if_statements": 2,
    "for_loops": 1,
    // ... AST features only
  },
  "summary": "AST analysis completed with 25 features extracted"
}
```

#### `POST /api/analysis/human-style`
**Human style analysis** - spacing, indentation, naming inconsistency, formatting.

**Request:** Same as combined analysis  
**Response:**
```json
{
  "success": true,
  "analysis_id": "analysis_def456",
  "timestamp": "2024-01-20T10:30:00",
  "analysis_type": "human_style_only",
  "code_info": { /* ... */ },
  "features": {
    "spacing_issues_ratio": 0.12,
    "indentation_issues_ratio": 0.05,
    "naming_inconsistency_ratio": 0.18,
    // ... Human style features only
  },
  "summary": "Human style analysis completed with 39 features extracted"
}
```

#### `POST /api/analysis/advanced-features`
**Advanced features** - redundancy, complexity, AI patterns.

**Request:** Same as combined analysis  
**Response:**
```json
{
  "success": true,
  "analysis_id": "analysis_ghi789",
  "timestamp": "2024-01-20T10:30:00", ư
  "analysis_type": "advanced_features_only",
  "code_info": { /* ... */ },
  "features": {
    "redundancy_duplicate_line_ratio": 0.08,
    "complexity_halstead_complexity": 45.2,
    "ai_pattern_template_usage_score": 0.15,
    // ... Advanced features only
  },
  "summary": "Advanced features analysis completed with 32 features extracted"
}
```

---

### File Upload

#### `POST /api/analysis/upload-file`
Upload và analyze file code.

**Request (multipart/form-data):**
- `file`: File upload (.c, .cpp, .cc, .cxx, .txt, max 1MB)
- `analysis_type`: string (optional, default: "combined")
  - `"combined"` - comprehensive analysis
  - `"ast"` - AST analysis only
  - `"human-style"` - human style only  
  - `"advanced"` - advanced features only
- `language`: string (optional, default: "c")

**Response:** Same as respective analysis endpoint based on `analysis_type`.

---

### Analysis Info

#### `GET /api/analysis/methods`
Lấy thông tin về các phương thức analysis có sẵn.

**Response:**
```json
{
  "methods": [
    {
      "id": "combined",
      "name": "Combined Analysis",
      "description": "Comprehensive analysis using all available methods (80+ features)",
      "features": ["AST Analysis", "Human Style", "Advanced Features", "AI Detection"],
      "estimated_time": "2-5 seconds"
    },
    {
      "id": "ast",
      "name": "AST Analysis", 
      "description": "Code structure, control flow, and naming pattern analysis",
      "features": ["Structure metrics", "Control flow", "Function analysis", "Variable naming"],
      "estimated_time": "1-2 seconds"
    }
    // ... other methods
  ],
  "supported_languages": ["c", "cpp", "c++"],
  "supported_extensions": [".c", ".cpp", ".cc", ".cxx", ".txt"],
  "max_file_size": "1MB",
  "max_code_length": 50000
}
```

---

## Error Handling

All endpoints return consistent error format:

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (validation errors)
- `413` - Payload Too Large (file size > 1MB)
- `422` - Validation Error (Pydantic validation)
- `500` - Internal Server Error
- `503` - Service Unavailable (analysis modules not loaded)

**Error Response Format:**
```json
{
  "detail": "Error message description"
}
```

**Common Errors:**

1. **Code validation:**
```json
{
  "detail": "Code cannot be empty"
}
```

2. **Language validation:**
```json
{
  "detail": "Language must be one of: ['c', 'cpp', 'c++']"
}
```

3. **File upload errors:**
```json
{
  "detail": "File too large. Maximum size is 1.0MB"
}
```

4. **Analysis module errors:**
```json
{
  "detail": "Analysis modules not available. Please check server configuration."
}
```

---

## Usage Examples

### cURL Examples

**Combined Analysis:**
```bash
curl -X POST "http://localhost:8000/api/analysis/combined-analysis" \\
  -H "Content-Type: application/json" \\
  -d '{
    "code": "#include <stdio.h>\\nint main() { printf(\\"Hello\\"); return 0; }",
    "filename": "hello.c",
    "language": "c"
  }'
```

**File Upload:**
```bash
curl -X POST "http://localhost:8000/api/analysis/upload-file" \\
  -F "file=@sample.c" \\
  -F "analysis_type=combined" \\
  -F "language=c"
```

### JavaScript/TypeScript Examples

**Fetch API:**
```typescript
// Combined analysis
const response = await fetch('http://localhost:8000/api/analysis/combined-analysis', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    code: sourceCode,
    filename: 'example.c',
    language: 'c'
  })
});

const result = await response.json();
```

**File Upload:**
```typescript
const formData = new FormData();
formData.append('file', file);
formData.append('analysis_type', 'combined');
formData.append('language', 'c');

const response = await fetch('http://localhost:8000/api/analysis/upload-file', {
  method: 'POST',
  body: formData
});
```

---

## Development

### Running the Server

```bash
cd src/backend

# Setup environment
make setup

# Run development server (with hot reload)
make dev

# Run production server  
make start
```

### Testing

```bash
# Run API tests
python test_api.py

# Manual testing với Swagger UI
# Open: http://localhost:8000/docs
```

### Dependencies

- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `python-multipart==0.0.6` - File upload support
- `pydantic==2.7.1` - Data validation
- Custom analysis modules in `../src/features/`

---

## Feature Groups Explained

### Structure Metrics
- **Purpose**: Analyze code architecture và complexity
- **Features**: LOC, AST depth, control flow density, function metrics
- **Visualization**: Bar charts
- **AI Indicators**: Unusually clean structure, perfect nesting

### Style Metrics  
- **Purpose**: Human coding style inconsistencies
- **Features**: Spacing issues, indentation problems, naming patterns
- **Visualization**: Radar charts
- **Human Indicators**: Natural inconsistencies, varied formatting

### Complexity Metrics
- **Purpose**: Code complexity và maintainability
- **Features**: Halstead complexity, cognitive load, maintainability index
- **Visualization**: Line charts
- **AI Indicators**: Optimal complexity for problem size

### AI Detection Metrics
- **Purpose**: Patterns specific to AI code generation
- **Features**: Template usage, boilerplate patterns, error handling style
- **Visualization**: Box plots
- **AI Indicators**: High template usage, systematic error handling

---

## Performance Notes

- **Combined Analysis**: ~2-5 seconds for typical code (< 1000 LOC)
- **Individual Analysis**: ~1-2 seconds each
- **File Upload**: Add ~200ms for file processing
- **Memory**: ~50-100MB per analysis request
- **Concurrent Requests**: FastAPI handles multiple requests efficiently

---

## Next Steps

1. **Authentication**: Add API keys for production
2. **Rate Limiting**: Implement request throttling  
3. **Caching**: Cache analysis results for repeated code
4. **Batch Processing**: Support multiple files
5. **Report Generation**: PDF/CSV export endpoints
6. **WebSocket**: Real-time analysis progress