# Code Style Conventions - Chuẩn code style cho dự án

## Cập nhật: 2025-08-07

### 🐍 Python Code Style (Backend & ML)

#### General Principles:
- **PEP 8 Compliance**: Strict adherence to Python style guide
- **Type Hints**: Comprehensive type annotations
- **Docstrings**: Google-style documentation
- **Error Handling**: Explicit exception handling

#### Naming Conventions:
```python
# Classes: PascalCase
class AdvancedFeatureExtractor:
    pass

# Functions/Methods: snake_case
def extract_all_features(code: str, filename: str) -> FeatureResult:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 1024 * 1024
DEFAULT_THRESHOLD = 0.5

# Variables: snake_case
feature_count = 0
ai_probability = 0.85
```

#### Function Documentation:
```python
def analyze_code(self, code: str, filename: str) -> Dict[str, Any]:
    """Analyze code and extract features.
    
    Args:
        code: Source code to analyze
        filename: Name of the source file
        
    Returns:
        Dictionary containing extracted features
        
    Raises:
        ValueError: If code is empty or invalid
        ProcessingError: If analysis fails
    """
    pass
```

#### Import Organization:
```python
# Standard library imports
import json
import os
from typing import Dict, List, Optional, Tuple

# Third-party imports
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Local imports
from features.ast_analyzer import CppASTAnalyzer
from evaluation.model_evaluator import ModelEvaluator
```

#### Error Handling Pattern:
```python
def safe_feature_extraction(code: str) -> Optional[Dict]:
    """Extract features với safe error handling."""
    try:
        features = self.extractor.extract_all_features(code)
        return features.to_dict()
    except Exception as e:
        self.logger.error(f"Feature extraction failed: {e}")
        return None
```

#### Class Structure:
```python
class DetectionModel:
    """AI code detection model."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize model với configuration."""
        self.config = config or {}
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup private method với underscore prefix."""
        return logging.getLogger(__name__)
        
    def train(self, X: np.ndarray, y: np.ndarray) -> 'DetectionModel':
        """Public method với type hints."""
        # Implementation
        return self
```

### ⚡ FastAPI Code Style (Backend API)

#### Router Organization:
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["detection"])

class CodeAnalysisRequest(BaseModel):
    """Request model cho code analysis."""
    code: str
    language: str = "cpp"
    detector_type: str = "hybrid"

@router.post("/analyze-code")
async def analyze_code(request: CodeAnalysisRequest) -> Dict[str, Any]:
    """Analyze code for AI detection."""
    try:
        result = await detector.analyze(request.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Dependency Injection:
```python
from fastapi import Depends

def get_detector() -> DetectionPipeline:
    """Dependency injection cho detector."""
    return DetectionPipeline()

@router.post("/analyze")
async def analyze(
    request: CodeRequest,
    detector: DetectionPipeline = Depends(get_detector)
):
    """Endpoint với dependency injection."""
    return await detector.process(request.code)
```

### ⚛️ TypeScript/React Code Style (Frontend)

#### Component Structure:
```typescript
// Interface definitions
interface CodeAnalysisProps {
  initialCode?: string;
  onAnalysisComplete?: (result: AnalysisResult) => void;
}

interface AnalysisResult {
  prediction: 'AI-generated' | 'Human-written';
  confidence: number;
  features: Record<string, any>;
}

// Component implementation
export function CodeAnalysis({ 
  initialCode = "", 
  onAnalysisComplete 
}: CodeAnalysisProps) {
  const [code, setCode] = useState<string>(initialCode);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  const handleAnalysis = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await analyzeCode(code);
      setResult(response);
      onAnalysisComplete?.(response);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setIsLoading(false);
    }
  }, [code, onAnalysisComplete]);
  
  return (
    <div className="space-y-4">
      {/* Component JSX */}
    </div>
  );
}
```

#### Hook Patterns:
```typescript
// Custom hook cho API calls
export function useCodeAnalysis() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const analyzeCode = useCallback(async (code: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/analyze-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });
      
      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }
      
      return await response.json() as AnalysisResult;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  return { analyzeCode, isLoading, error };
}
```

#### Styling với TailwindCSS:
```typescript
// Organized class names
const buttonStyles = cn(
  // Base styles
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  // State styles
  "hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2",
  // Size variants
  "h-10 px-4 py-2",
  // Color variants
  "bg-primary text-primary-foreground",
  // Conditional styles
  isLoading && "cursor-not-allowed opacity-50"
);

return (
  <button className={buttonStyles} disabled={isLoading}>
    {isLoading ? <Spinner /> : "Analyze Code"}
  </button>
);
```

### 📋 File Organization Standards

#### Python Module Structure:
```
module/
├── __init__.py          # Module exports
├── core.py             # Core functionality
├── utils.py            # Utility functions
├── exceptions.py       # Custom exceptions
├── types.py           # Type definitions
└── tests/             # Test files
    ├── __init__.py
    ├── test_core.py
    └── test_utils.py
```

#### TypeScript Module Structure:
```
components/
├── index.ts           # Barrel exports
├── CodeAnalysis.tsx   # Main component
├── CodeAnalysis.types.ts # Type definitions
├── CodeAnalysis.hooks.ts # Custom hooks
└── __tests__/         # Test files
    └── CodeAnalysis.test.tsx
```

### 🧪 Testing Conventions

#### Python Testing:
```python
import pytest
from unittest.mock import Mock, patch

class TestAdvancedFeatures:
    """Test class cho AdvancedFeatureExtractor."""
    
    @pytest.fixture
    def extractor(self):
        """Fixture cho extractor instance."""
        return AdvancedFeatureExtractor()
    
    def test_extract_features_success(self, extractor):
        """Test successful feature extraction."""
        code = "#include <iostream>\nint main() { return 0; }"
        result = extractor.extract_all_features(code, "test.cpp")
        
        assert result is not None
        assert result.redundancy is not None
        assert result.naming_patterns is not None
    
    def test_extract_features_empty_code(self, extractor):
        """Test feature extraction với empty code."""
        with pytest.raises(ValueError, match="Code cannot be empty"):
            extractor.extract_all_features("", "test.cpp")
    
    @patch('features.advanced_features.some_external_service')
    def test_extract_features_with_mock(self, mock_service, extractor):
        """Test với mocked external dependencies."""
        mock_service.return_value = Mock(result="success")
        # Test implementation
```

#### TypeScript Testing:
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CodeAnalysis } from './CodeAnalysis';

describe('CodeAnalysis Component', () => {
  it('renders correctly với initial props', () => {
    render(<CodeAnalysis initialCode="test code" />);
    expect(screen.getByDisplayValue('test code')).toBeInTheDocument();
  });
  
  it('handles analysis submission', async () => {
    const mockOnComplete = jest.fn();
    render(<CodeAnalysis onAnalysisComplete={mockOnComplete} />);
    
    const analyzeButton = screen.getByRole('button', { name: /analyze/i });
    fireEvent.click(analyzeButton);
    
    await waitFor(() => {
      expect(mockOnComplete).toHaveBeenCalledWith(
        expect.objectContaining({
          prediction: expect.stringMatching(/AI-generated|Human-written/),
          confidence: expect.any(Number),
        })
      );
    });
  });
});
```

### 📝 Documentation Standards

#### README Structure:
```markdown
# Component Name

Brief description of the component's purpose.

## Features
- Feature 1
- Feature 2

## Usage
```python
from module import Component

component = Component(config)
result = component.process(data)
```

## API Reference
### Methods
#### `process(data: str) -> Result`
Description of method functionality.

## Examples
Complete usage examples.

## Testing
How to run tests for this component.
```

#### Code Comments:
```python
def complex_algorithm(data: List[str]) -> Dict[str, float]:
    """Complex algorithm requiring detailed explanation.
    
    This algorithm implements the Smith-Jones method for
    feature extraction với optimization for C++ code.
    """
    # Step 1: Preprocess input data
    cleaned_data = [item.strip() for item in data if item]
    
    # Step 2: Apply transformation (see paper XYZ for details)
    transformed = self._apply_transformation(cleaned_data)
    
    # Step 3: Calculate final scores
    scores = {}
    for key, value in transformed.items():
        # Normalize using z-score method
        scores[key] = (value - self.mean) / self.std
    
    return scores
```

### 🔧 Configuration Standards

#### Environment Variables:
```python
import os
from typing import Optional

class Config:
    """Application configuration."""
    
    # API Settings
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # ML Settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "1048576"))
    
    # Optional settings với defaults
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
```

#### Configuration Files:
```json
{
  "ml_config": {
    "feature_extraction": {
      "max_depth": 10,
      "include_comments": true,
      "parallel_processing": true
    },
    "detection_models": {
      "rule_based": {
        "threshold": 0.5,
        "weights": {
          "comment_ratio": 0.2,
          "naming_quality": 0.25
        }
      }
    }
  }
}
```

### 🚀 Performance Standards

#### Async/Await Patterns:
```python
import asyncio
from typing import List

async def process_batch(codes: List[str]) -> List[Dict]:
    """Process multiple codes concurrently."""
    tasks = [
        self.analyze_code_async(code) 
        for code in codes
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle exceptions
    valid_results = []
    for result in results:
        if isinstance(result, Exception):
            self.logger.error(f"Processing failed: {result}")
        else:
            valid_results.append(result)
    
    return valid_results
```

#### Memory Management:
```python
def process_large_dataset(self, file_paths: List[str]) -> Iterator[Dict]:
    """Process large dataset với memory efficiency."""
    for batch in self._batch_files(file_paths, batch_size=100):
        # Process batch
        results = self._process_batch(batch)
        
        # Yield results immediately to avoid memory buildup
        for result in results:
            yield result
        
        # Optional: explicit garbage collection
        import gc
        gc.collect()
```

### 🎯 Code Review Standards

#### Checklist Items:
- [ ] **Type Safety**: All functions have type hints
- [ ] **Error Handling**: Appropriate exception handling
- [ ] **Documentation**: Functions have docstrings
- [ ] **Testing**: Unit tests cover new functionality
- [ ] **Performance**: No obvious performance issues
- [ ] **Security**: No security vulnerabilities
- [ ] **Style**: Follows project conventions
- [ ] **Dependencies**: No unnecessary dependencies

#### Review Comments Format:
```
// Suggestion: Consider using async/await pattern
// async def analyze_code(self, code: str) -> Dict[str, Any]:

// Nitpick: Variable name could be more descriptive
// result -> feature_extraction_result

// Question: Should this handle empty input gracefully?
// if not code.strip():
//     return self._get_default_result()
```

**🎯 STYLE GUIDE STATUS: COMPREHENSIVE & ENFORCED** ✅