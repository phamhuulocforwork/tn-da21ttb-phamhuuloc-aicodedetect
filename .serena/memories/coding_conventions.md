# AI Code Detection - Coding Conventions và Style Guidelines

## Python Code Style (Backend & ML Pipeline)

### General Guidelines 1

- **Python Version**: 3.12
- **Naming Conventions**:
  - snake_case cho functions, variables, modules
  - PascalCase cho classes
  - UPPER_CASE cho constants
- **Import Organization**: Standard library → Third party → Local imports

### Backend (FastAPI) Conventions

- **Models**: Sử dụng Pydantic models cho request/response
- **API Endpoints**: RESTful naming với clear paths
- **Error Handling**: Proper HTTP status codes và error messages
- **Documentation**: FastAPI auto-docs với descriptive docstrings

### ML Pipeline Conventions

- **File Structure**:
  - Tách biệt feature extraction, analysis, và training
  - Models lưu trong `models/` directory
  - Features lưu trong `features/` directory
- **Data Processing**: Sử dụng pandas cho data manipulation
- **Visualization**: Matplotlib + Seaborn cho plots và charts

## TypeScript/React Code Style (Frontend)

### General Guidelines 2

- **TypeScript**: Strict mode enabled
- **Naming Conventions**:
  - camelCase cho variables, functions
  - PascalCase cho components, interfaces, types
  - kebab-case cho file names

### React Conventions

- **Component Structure**: Functional components với hooks
- **File Organization**:
  - Components trong `components/`
  - Pages trong `app/` directory (Next.js App Router)
  - Utilities trong `lib/`
- **Styling**: Tailwind CSS classes, component-based styling

### Next.js Specific

- **App Router**: Sử dụng Next.js 15 App Router structure
- **Server Components**: Default, Client Components khi cần thiết
- **TypeScript Config**: Strict configuration trong tsconfig.json

## Code Quality Tools

### Python

- **Linting**: Sử dụng built-in Python linting
- **Formatting**: Consistent với project style
- **Dependencies**: Virtual environment với requirements.txt

### TypeScript/React

- **ESLint**: Configuration trong eslint.config.mjs
- **Prettier**: Auto-formatting với .prettierrc.cjs
- **Scripts**: `npm run lint`, `npm run format`

## Project Structure Conventions

### Directory Organization

```
src/
├── backend/          # FastAPI backend
│   ├── app/         # Main application code
│   ├── requirements.txt
│   └── Makefile
├── frontend/        # Next.js frontend
│   ├── app/         # Next.js App Router pages
│   ├── components/  # Reusable components
│   ├── lib/         # Utilities
│   └── package.json
└── src/             # ML Pipeline
    ├── dataset/     # Training data
    ├── features/    # Feature files
    ├── models/      # Trained models
    └── analysis_plots/ # Visualizations
```

## Documentation Standards

- **README**: Mỗi major component có README riêng
- **Comments**: Explain why, not what
- **API Documentation**: FastAPI auto-generates docs
- **Type Hints**: Required cho Python functions
- **Interface Definitions**: TypeScript interfaces cho data structures
