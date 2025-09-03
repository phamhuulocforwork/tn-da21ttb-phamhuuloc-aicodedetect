# Code Style & Conventions

## TypeScript/JavaScript (Frontend)

### ESLint Configuration
```javascript
// eslint.config.mjs
{
  extends: ["next/core-web-vitals", "next/typescript"],
  rules: {
    "@typescript-eslint/no-explicit-any": "off",        // Cho phép any type
    "react-hooks/exhaustive-deps": "warn",              // Cảnh báo về dependencies
    "jsx-a11y/role-supports-aria-props": "off",        // Tắt accessibility warnings
    "@next/next/no-img-element": "off",                // Cho phép img element
    "@typescript-eslint/no-unused-vars": ["warn", {
      argsIgnorePattern: "^_",                         // Bỏ qua args bắt đầu bằng _
      varsIgnorePattern: "^_",                         // Bỏ qua vars bắt đầu bằng _
      caughtErrorsIgnorePattern: "^_"                  // Bỏ qua caught errors bắt đầu bằng _
    }]
  }
}
```

### TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "strict": true,                          // Strict type checking
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "paths": {
      "@/*": ["./*"]                         // Path alias
    }
  }
}
```

### Prettier Configuration (via package.json)
- **Single quotes**: `true`
- **Trailing commas**: `"es5"`
- **Tab width**: `2`
- **Semi**: `true`
- **Print width**: `80`

### Naming Conventions

#### Components
```typescript
// PascalCase cho component names
export function CodeAnalysisCard() { /* ... */ }
export const FileUpload = () => { /* ... */ }

// File names: kebab-case hoặc PascalCase
// components/code-analysis-card.tsx
// components/FileUpload.tsx
```

#### Variables & Functions
```typescript
// camelCase cho variables và functions
const userName = "john";
const isLoading = false;

function processAnalysis() { /* ... */ }
const handleSubmit = () => { /* ... */ }

// Boolean variables với is/has/can prefixes
const isAuthenticated = true;
const hasPermission = false;
const canEdit = true;
```

#### Types & Interfaces
```typescript
// PascalCase cho types và interfaces
interface AnalysisResult {
  id: string;
  score: number;
}

type FileStatus = "pending" | "processing" | "completed";

// Generic types
type ApiResponse<T> = {
  data: T;
  error?: string;
};
```

#### Constants
```typescript
// UPPER_SNAKE_CASE cho constants
const MAX_FILE_SIZE = 1024 * 1024;
const API_BASE_URL = "/api";
const DEFAULT_TIMEOUT = 5000;
```

### Import/Export Style
```typescript
// Group imports by type
import React from "react";
import { useState, useEffect } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

import { apiClient } from "@/lib/api";
import { formatFileSize } from "@/lib/utils";

// Default export ở cuối file
export default function AnalysisPage() { /* ... */ }
```

### React Patterns
```typescript
// Functional components với arrow functions
const AnalysisCard: React.FC<AnalysisCardProps> = ({ 
  title, 
  score, 
  onAnalyze 
}) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div>Score: {score}</div>
        <Button onClick={onAnalyze}>
          Analyze
        </Button>
      </CardContent>
    </Card>
  );
};

// Custom hooks
function useAnalysis() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);

  const analyze = async (code: string) => {
    setIsLoading(true);
    try {
      const response = await apiClient.analyze(code);
      setResult(response);
    } finally {
      setIsLoading(false);
    }
  };

  return { isLoading, result, analyze };
}
```

## Python (Backend & Analysis)

### Code Style (PEP 8)
```python
# Imports
import os
import sys
from typing import Dict, List, Optional, Any
from pathlib import Path

# Constants
MAX_FILE_SIZE = 1024 * 1024
DEFAULT_TIMEOUT = 30

# Classes
class CodeAnalyzer:
    """Class for analyzing code patterns."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code and return results."""
        pass

# Functions
def calculate_file_size(code: str) -> int:
    """Calculate file size in bytes."""
    return len(code.encode('utf-8'))

def process_batch_analysis(files: List[str]) -> List[Dict]:
    """Process multiple files for analysis."""
    results = []
    for file_path in files:
        result = analyze_single_file(file_path)
        results.append(result)
    return results
```

### Type Hints
```python
# Comprehensive type hints
from typing import Dict, List, Optional, Union, Any, Tuple

def analyze_code(
    code: str, 
    filename: str = "", 
    language: str = "c"
) -> Dict[str, Any]:
    """Analyze code with comprehensive type hints."""
    pass

class AnalysisResult:
    def __init__(
        self, 
        success: bool,
        score: float,
        features: Dict[str, float],
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.success = success
        self.score = score
        self.features = features
        self.metadata = metadata or {}
```

### Error Handling
```python
# Comprehensive error handling
try:
    result = analyze_code(code)
    if not result.get('success'):
        logger.warning(f"Analysis failed: {result.get('error')}")
        return None
    return result
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise HTTPException(status_code=404, detail="File not found")
except ValidationError as e:
    logger.error(f"Validation error: {e}")
    raise HTTPException(status_code=400, detail="Invalid input")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

### Async/Await Patterns
```python
# Async patterns for I/O operations
async def download_file(url: str, dest_path: str) -> bool:
    """Download file asynchronously."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(dest_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                    return True
        return False
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False

# Async file processing
async def process_files_batch(files: List[str]) -> List[Dict]:
    """Process multiple files concurrently."""
    semaphore = asyncio.Semaphore(5)  # Limit concurrent operations
    
    async def limited_process(file_path: str):
        async with semaphore:
            return await analyze_file(file_path)
    
    tasks = [limited_process(file) for file in files]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

## File Organization

### Frontend Structure
```
src/frontend/
├── app/                    # Next.js app router
│   ├── (auth)/            # Route groups
│   ├── api/               # API routes
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── forms/            # Form components
│   └── charts/           # Chart components
├── lib/                  # Utilities & configurations
│   ├── api.ts            # API client
│   ├── utils.ts          # Utility functions
│   └── validations.ts    # Validation schemas
├── hooks/                # Custom React hooks
├── styles/               # Global styles
└── types/                # TypeScript type definitions
```

### Backend Structure
```
src/backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── baseline_loader.py # Baseline data loader
│   ├── chart_helpers.py   # Chart generation helpers
│   └── __init__.py
├── tests/                # Unit tests
└── requirements.txt      # Python dependencies
```

### Analysis Modules Structure
```
src/src/
├── features/             # Feature extractors
│   ├── ast_analyzer.py
│   ├── human_style_analyzer.py
│   └── advanced_features.py
├── models/               # ML models
├── dataset/              # Training data
├── analysis_plots/       # Visualization
└── utils/                # Analysis utilities
```

## Documentation Standards

### JSDoc Comments
```typescript
/**
 * Analyze code for AI-generated patterns
 * @param code - Source code to analyze
 * @param filename - Original filename
 * @param language - Programming language
 * @returns Analysis result with score and features
 */
function analyzeCode(
  code: string, 
  filename: string = "", 
  language: string = "c"
): Promise<AnalysisResult> {
  // Implementation
}
```

### Python Docstrings
```python
def analyze_code(
    code: str, 
    filename: str = "", 
    language: str = "c"
) -> Dict[str, Any]:
    """
    Analyze code for AI-generated patterns.
    
    Args:
        code: Source code to analyze
        filename: Original filename (optional)
        language: Programming language (default: 'c')
    
    Returns:
        Dictionary containing analysis results with score and features
    
    Raises:
        ValueError: If code is empty or language is unsupported
        RuntimeError: If analysis service is unavailable
    """
    pass
```

### Commit Message Conventions
```bash
# Format: type(scope): description
feat(auth): add OAuth2 Google Drive integration
fix(api): handle empty file uploads gracefully
docs(readme): update deployment instructions
refactor(frontend): optimize component re-renders
test(backend): add unit tests for file processing
chore(deps): update Python dependencies
```

## Testing Conventions

### Frontend Tests
```typescript
// __tests__/components/AnalysisCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { AnalysisCard } from '../AnalysisCard';

describe('AnalysisCard', () => {
  it('displays analysis score correctly', () => {
    render(<AnalysisCard score={0.85} />);
    expect(screen.getByText('85%')).toBeInTheDocument();
  });
  
  it('calls onAnalyze when button is clicked', () => {
    const mockOnAnalyze = jest.fn();
    render(<AnalysisCard onAnalyze={mockOnAnalyze} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(mockOnAnalyze).toHaveBeenCalledTimes(1);
  });
});
```

### Backend Tests
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "khỏe mạnh"

def test_analyze_code_valid():
    """Test code analysis with valid input."""
    payload = {
        "code": "#include <stdio.h>\nint main() { return 0; }",
        "filename": "test.c",
        "language": "c"
    }
    
    response = client.post("/api/analysis/combined-analysis", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "success" in data
    assert "analysis_id" in data
    assert "assessment" in data

def test_analyze_code_empty():
    """Test code analysis with empty code."""
    payload = {
        "code": "",
        "filename": "empty.c",
        "language": "c"
    }
    
    response = client.post("/api/analysis/combined-analysis", json=payload)
    assert response.status_code == 400
```