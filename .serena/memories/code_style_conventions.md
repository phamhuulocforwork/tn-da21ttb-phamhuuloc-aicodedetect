# Code Style and Conventions

## Python Code Style (ML Core + Backend)

### General Conventions

- **Python Version**: 3.12
- **Line Length**: 88 characters (Black formatter default)
- **Imports**: Organized với absolute imports
- **Type Hints**: Required cho function signatures
- **Docstrings**: Google style docstrings cho functions/classes

### File Structure

```python
"""Module docstring describing purpose."""

# Standard library imports
import os
import sys

# Third-party imports
import numpy as np
import pandas as pd

# Local imports
from features.advanced_features import AdvancedFeatureExtractor
```

### Naming Conventions

- **Variables**: `snake_case` (e.g., `feature_vector`, `analysis_result`)
- **Functions**: `snake_case` (e.g., `extract_features()`, `train_model()`)
- **Classes**: `PascalCase` (e.g., `AICodeDetectionPipeline`, `CppASTAnalyzer`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`, `DEFAULT_TIMEOUT`)
- **Private members**: Leading underscore `_private_method()`

### Function Documentation

```python
def extract_features(code: str, filename: str = "code.c") -> Dict[str, float]:
    """Extract comprehensive features from source code.

    Args:
        code: Source code string to analyze
        filename: Optional filename for context

    Returns:
        Dictionary mapping feature names to values

    Raises:
        ValueError: If code is empty or invalid
    """
```

## TypeScript/React Code Style (Frontend)

### General Conventions

- **TypeScript**: Strict mode enabled
- **React**: Function components với hooks
- **Line Length**: 80-100 characters
- **Semicolons**: Always required
- **Quotes**: Double quotes cho strings

### File Structure

```typescript
// React/Next.js imports
import React from "react";
import { NextPage } from "next";

// Third-party imports
import { Button } from "@/components/ui/button";

// Local imports
import { analyzeCode } from "@/lib/api-client";
import type { AnalysisResult } from "@/lib/api-types";
```

### Naming Conventions

- **Components**: `PascalCase` (e.g., `AnalysisSelector`, `CodeEditor`)
- **Files**: `kebab-case` (e.g., `analysis-selector.tsx`, `code-editor.tsx`)
- **Variables**: `camelCase` (e.g., `analysisResult`, `isLoading`)
- **Types/Interfaces**: `PascalCase` (e.g., `AnalysisResult`, `CodeInfo`)
- **Hooks**: `camelCase` với `use` prefix (e.g., `useAnalysis`, `useCodeEditor`)

### Component Structure

```typescript
interface Props {
  code: string;
  onAnalysis: (result: AnalysisResult) => void;
}

export function CodeAnalyzer({ code, onAnalysis }: Props) {
  const [isLoading, setIsLoading] = useState(false);

  // Component logic here

  return <div className="space-y-4">{/* JSX here */}</div>;
}
```

### API Type Definitions

```typescript
// Comprehensive type definitions in api-types.ts
export interface AnalysisResult {
  success: boolean;
  analysis_id: string;
  timestamp: string;
  code_info: CodeInfo;
  feature_groups: FeatureGroups;
  assessment: Assessment;
  raw_features?: Record<string, number>;
}
```

## CSS/Styling Conventions

### Tailwind CSS

- **Utility-first approach** với Tailwind v4
- **Component classes** trong components/ui/
- **Responsive design**: Mobile-first approach
- **Dark mode**: `dark:` prefix cho dark theme variants

### Class Organization

```typescript
const buttonClasses = cn(
  // Base styles
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  // State variants
  "hover:bg-accent hover:text-accent-foreground",
  // Responsive
  "h-10 px-4 py-2 md:h-11 md:px-8",
  // Conditional
  isLoading && "opacity-50 cursor-not-allowed"
);
```

## Database/Data Conventions

### JSON Structure

- **Snake_case keys** cho consistency với Python backend
- **Consistent nesting** với clear hierarchy
- **Type safety** với TypeScript interfaces

### File Naming

- **Configuration**: `.json`, `.yml` extensions
- **Data files**: Descriptive names (e.g., `large_features.csv`, `model.json`)
- **Analysis outputs**: Timestamped (e.g., `analysis_2024-01-20.json`)

## Git Conventions

### Commit Messages

```
feat: Add new feature extraction method
fix: Resolve API endpoint validation issue
docs: Update README với setup instructions
style: Format code với Prettier
refactor: Reorganize component structure
```

### Branch Naming

- **Features**: `feature/analysis-dashboard`
- **Fixes**: `fix/api-validation-error`
- **Documentation**: `docs/api-documentation`

## Development Guidelines

### Error Handling

- **Python**: Use specific exception types, comprehensive logging
- **TypeScript**: Type-safe error handling với Result patterns
- **API**: Consistent error response format

### Testing Patterns

- **Unit tests**: Focus on individual functions/components
- **Integration tests**: API endpoint testing
- **E2E tests**: Complete user workflows

### Performance Considerations

- **Python**: Efficient numpy operations, avoid loops
- **React**: Proper memoization, lazy loading
- **API**: Response caching, efficient serialization
