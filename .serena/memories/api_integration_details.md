# API Integration and Technical Details

## API Architecture Overview

### Base Configuration

- **Base URL**: `http://localhost:8000`
- **Protocol**: RESTful HTTP API
- **Content-Type**: `application/json`
- **File Upload**: `multipart/form-data`
- **Documentation**: Swagger UI at `/docs`, ReDoc at `/redoc`

### Authentication & Security

- **Current**: No authentication (development mode)
- **CORS**: Enabled cho localhost:3000
- **File Size Limit**: 1MB maximum
- **Rate Limiting**: Not implemented (planned)

## Complete API Endpoint Reference

### 1. Health & Info Endpoints

#### `GET /`

- **Purpose**: Basic API status
- **Response Time**: < 100ms
- **Response**: `{"message": "AI Code Detection API", "status": "running"}`

#### `GET /health`

- **Purpose**: Detailed system health
- **Response**: Module availability status
- **Use Case**: System monitoring, readiness checks

#### `GET /api/analysis/methods`

- **Purpose**: Available analysis methods info
- **Response**: Method details, supported languages, limitations
- **Use Case**: Dynamic UI generation, capability discovery

### 2. Analysis Endpoints

#### `POST /api/analysis/combined-analysis`

- **Purpose**: Comprehensive 80+ feature analysis
- **Processing Time**: 2-5 seconds
- **Memory Usage**: ~50-100MB per request
- **Response Structure**:
  ```json
  {
    "success": boolean,
    "analysis_id": string,
    "timestamp": ISO8601,
    "code_info": {...},
    "feature_groups": {
      "structure_metrics": {...},
      "style_metrics": {...},
      "complexity_metrics": {...},
      "ai_detection_metrics": {...}
    },
    "assessment": {
      "overall_score": 0.0-1.0,
      "confidence": 0.0-1.0,
      "key_indicators": string[],
      "summary": string
    },
    "raw_features": {...}
  }
  ```

#### `POST /api/analysis/ast-analysis`

- **Purpose**: AST structure analysis only
- **Features**: ~25 structural features
- **Processing Time**: 1-2 seconds
- **Focus**: Code structure, control flow, function patterns

#### `POST /api/analysis/human-style`

- **Purpose**: Human coding style inconsistencies
- **Features**: ~39 style-related features
- **Processing Time**: 1-2 seconds
- **Focus**: Spacing, indentation, naming patterns

#### `POST /api/analysis/advanced-features`

- **Purpose**: Advanced complexity và AI patterns
- **Features**: ~32 sophisticated features
- **Processing Time**: 1-3 seconds
- **Focus**: Redundancy, complexity metrics, AI patterns

#### `POST /api/analysis/upload-file`

- **Purpose**: File-based analysis
- **Input**: Multipart form với file upload
- **Supported**: .c, .cpp, .cc, .cxx, .txt
- **Max Size**: 1MB
- **Analysis Type**: Configurable via form parameter

## Request/Response Patterns

### Standard Request Format

```json
{
  "code": "string (required, max 50000 chars)",
  "filename": "string (optional, default: 'code.c')",
  "language": "string (required, 'c'|'cpp'|'c++')"
}
```

### Error Response Format

```json
{
  "detail": "string (error message)"
}
```

### HTTP Status Codes

- `200 OK`: Successful analysis
- `400 Bad Request`: Invalid input parameters
- `413 Payload Too Large`: File size exceeds limit
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Analysis engine errors
- `503 Service Unavailable`: Analysis modules unavailable

## Feature Groups Detailed

### Structure Metrics Group

```json
{
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
}
```

### Assessment Scoring

- **overall_score**: 0.0 = human-like, 1.0 = AI-like
- **confidence**: 0.0 = low confidence, 1.0 = high confidence
- **key_indicators**: Human-readable insights
- **summary**: Overall assessment text

## Frontend Integration Patterns

### API Client Setup

```typescript
// lib/api-client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function analyzeCode(
  code: string,
  method: AnalysisMethod,
  options?: AnalysisOptions
): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE_URL}/api/analysis/${method}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      code,
      filename: options?.filename || "code.c",
      language: options?.language || "c",
    }),
  });

  if (!response.ok) {
    throw new Error(`Analysis failed: ${response.status}`);
  }

  return response.json();
}
```

### Error Handling Pattern

```typescript
try {
  const result = await analyzeCode(code, "combined-analysis");
  setAnalysisResult(result);
} catch (error) {
  if (error instanceof Error) {
    toast.error(`Analysis failed: ${error.message}`);
  }
  setError(error);
} finally {
  setIsLoading(false);
}
```

### File Upload Implementation

```typescript
export async function uploadAndAnalyze(
  file: File,
  analysisType: AnalysisMethod = "combined-analysis"
): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("analysis_type", analysisType);
  formData.append("language", detectLanguageFromFilename(file.name));

  const response = await fetch(`${API_BASE_URL}/api/analysis/upload-file`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}
```

## Performance Optimization

### Response Caching

```typescript
// Simple in-memory cache
const analysisCache = new Map<string, AnalysisResult>();

export async function analyzeCodeCached(
  code: string,
  method: AnalysisMethod
): Promise<AnalysisResult> {
  const cacheKey = `${method}:${hashCode(code)}`;

  if (analysisCache.has(cacheKey)) {
    return analysisCache.get(cacheKey)!;
  }

  const result = await analyzeCode(code, method);
  analysisCache.set(cacheKey, result);

  return result;
}
```

### Concurrent Analysis

```typescript
// Run multiple analysis methods in parallel
export async function runAllAnalysisMethods(code: string): Promise<{
  combined: AnalysisResult;
  ast: AnalysisResult;
  style: AnalysisResult;
  advanced: AnalysisResult;
}> {
  const [combined, ast, style, advanced] = await Promise.all([
    analyzeCode(code, "combined-analysis"),
    analyzeCode(code, "ast-analysis"),
    analyzeCode(code, "human-style"),
    analyzeCode(code, "advanced-features"),
  ]);

  return { combined, ast, style, advanced };
}
```

## Development & Testing

### API Testing Commands

```bash
# Health check
curl http://localhost:8000/health

# Method info
curl http://localhost:8000/api/analysis/methods

# Combined analysis
curl -X POST http://localhost:8000/api/analysis/combined-analysis \
  -H "Content-Type: application/json" \
  -d '{"code":"#include <stdio.h>\nint main(){return 0;}", "language":"c"}'

# File upload
curl -X POST http://localhost:8000/api/analysis/upload-file \
  -F "file=@sample.c" \
  -F "analysis_type=combined" \
  -F "language=c"
```

### Load Testing

```bash
# Install apache benchmark
sudo apt-get install apache2-utils

# Test API performance
ab -n 100 -c 10 -p request.json -T application/json \
  http://localhost:8000/api/analysis/ast-analysis

# Expected: ~10-20 requests/second
```

## Backend Module Integration

### Analysis Module Structure

```python
# Backend integrates với analysis modules từ ../src/features/
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from features.advanced_features import AdvancedFeatureExtractor
from features.ast_analyzer import CppASTAnalyzer
from features.human_style_analyzer import HumanStyleAnalyzer
```

### Feature Extraction Pipeline

```python
def extract_all_features(code: str, filename: str) -> Dict[str, Any]:
    """Complete feature extraction pipeline."""
    extractor = AdvancedFeatureExtractor()
    ast_analyzer = CppASTAnalyzer()
    style_analyzer = HumanStyleAnalyzer()

    # Extract features from all modules
    advanced_features = extractor.extract_features(code, filename)
    ast_features = ast_analyzer.analyze(code)
    style_features = style_analyzer.analyze_style(code)

    # Combine và normalize
    return combine_and_normalize_features(
        advanced_features, ast_features, style_features
    )
```

## Production Considerations

### Deployment Settings

```python
# Production environment variables
ENVIRONMENT = "production"
LOG_LEVEL = "warning"
CORS_ORIGINS = ["https://yourdomain.com"]
MAX_FILE_SIZE = 1048576  # 1MB
```

### Monitoring & Logging

```python
import logging

# Setup comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log analysis requests
logger.info(f"Analysis request: {method}, LOC: {loc}, Duration: {duration}s")
```

### Error Recovery

```python
try:
    result = extract_features(code, filename)
except Exception as e:
    logger.error(f"Feature extraction failed: {str(e)}")
    return {"error": "Analysis failed", "fallback": True}
```
