# AI Code Detection - Codebase Structure

## Tổng quan cấu trúc dự án

```
tn-da21ttb-phamhuuloc-aicodedetect/
├── FLOW.txt                    # Workflow chính cho development
├── README.md                   # Project documentation
├── progress-report/            # Báo cáo tiến độ luận văn
├── thesis/                     # Tài liệu luận văn
│   ├── pdf/                   # PDF files
│   ├── abs/                   # Abstract files  
│   ├── docx/                  # Word documents
│   ├── drawio/                # Diagrams và flowcharts
│   ├── images/                # Images cho luận văn
│   └── context/               # Context files
└── src/                       # Source code chính
    ├── backend/               # FastAPI backend
    ├── frontend/              # Next.js frontend  
    └── src/                   # ML Pipeline
```

## Backend Structure (`src/backend/`)

```
backend/
├── Makefile                   # Build và development commands
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── app/                      # Main application
    ├── __init__.py           # Package initialization
    ├── main.py               # FastAPI app entry point
    ├── basic_analysis.py     # Basic code analysis functions
    ├── enhanced_ml_integration.py  # ML model integration
    └── analysis_service.py   # Analysis service logic
```

### Key Backend Files:
- **main.py**: FastAPI application với API endpoints
- **analysis_service.py**: Core logic cho code analysis
- **enhanced_ml_integration.py**: Integration với trained ML models

## Frontend Structure (`src/frontend/`)

```
frontend/
├── package.json              # NPM dependencies và scripts
├── package-lock.json         # Lock file
├── tsconfig.json            # TypeScript configuration
├── next.config.ts           # Next.js configuration
├── eslint.config.mjs        # ESLint configuration
├── .prettierrc.cjs          # Prettier configuration
├── .editorconfig            # Editor configuration
├── postcss.config.mjs       # PostCSS configuration
├── components.json          # UI components configuration
├── README.md                # Frontend documentation
├── .gitignore               # Git ignore rules
├── app/                     # Next.js App Router
│   ├── layout.tsx           # Root layout
│   ├── analysis/            # Analysis page
│   │   ├── page.tsx         # Main analysis page
│   │   └── _components/     # Analysis-specific components
│   │       ├── code-editor.tsx    # Code editor component
│   │       ├── header.tsx         # Analysis header
│   │       ├── providers.tsx      # Context providers
│   │       └── onedarkpro.json   # Editor theme
│   └── home/                # Home page
│       ├── page.tsx         # Home page component
│       └── layout.tsx       # Home layout
├── components/              # Reusable components
│   ├── theme-toggle.tsx     # Dark/light theme toggle
│   └── ui/                  # UI components library
│       ├── badge.tsx        # Badge component
│       ├── button.tsx       # Button component
│       ├── card.tsx         # Card component
│       ├── select.tsx       # Select component
│       └── separator.tsx    # Separator component
├── lib/                     # Utilities
│   └── utils.ts             # Utility functions
├── public/                  # Static assets
│   └── placeholder.svg      # Placeholder images
└── styles/                  # Global styles
    └── globals.css          # Global CSS với Tailwind
```

## ML Pipeline Structure (`src/src/`)

```
src/
├── Makefile                           # Build commands
├── requirements.txt                   # Python ML dependencies
├── .env.example                      # Environment template
├── .gitignore                        # Git ignore rules
├── .cursorignore                     # Cursor editor ignore
├── feature_ranking.txt               # Feature importance ranking
├── feature_stats.json               # Feature statistics
├── batch_feature_extraction.py      # Batch processing cho features
├── analyze_features.py              # Feature analysis và visualization
├── complete_pipeline.py             # End-to-end ML pipeline
├── optimized_binary_classifier.py   # Optimized classifier
├── super_linter_integration.py      # Static analysis integration
├── dataset/                          # Training và testing data
│   ├── code/                        # Code samples
│   │   └── c/                       # C language samples
│   │       ├── human/               # Human-written code (86 problems)
│   │       │   ├── problem_1/       # Các problems từ online judges
│   │       │   ├── problem_2/
│   │       │   └── ...
│   │       └── ai/                  # AI-generated code
│   │           ├── problem_1/
│   │           ├── problem_2/
│   │           └── ...
│   ├── metadata/                    # Dataset metadata
│   └── ithub_oj_metadata.md        # Dataset documentation
├── features/                        # Feature extraction outputs
│   ├── detection_models.py         # Detection model definitions
│   ├── ast_analyzer.py             # AST analysis features
│   └── advanced_features.py       # Advanced feature extraction
├── models/                         # Trained models
│   └── model.json                  # Saved model file
└── analysis_plots/                # Generated visualizations
    ├── boxplots_comparison.png     # Box plots
    ├── mean_comparison.png         # Mean comparisons
    ├── correlation_matrix.png      # Feature correlations
    └── feature_distributions.png  # Feature distributions
```

### Key ML Pipeline Files:
- **batch_feature_extraction.py**: Extract features từ code samples
- **analyze_features.py**: Analyze và visualize extracted features  
- **complete_pipeline.py**: Complete training pipeline
- **features/**: Feature extraction modules (AST, complexity, style)
- **dataset/**: Organized code samples cho training

## Development Workflow Integration

### Typical Development Flow:
1. **Data Preparation**: `src/src/dataset/` → Feature extraction
2. **Model Training**: `src/src/` → Train và save models
3. **Backend Integration**: `src/backend/` → API endpoints sử dụng trained models
4. **Frontend Interface**: `src/frontend/` → Web UI cho end users

### Cross-Component Communication:
- **Models**: Trained trong ML pipeline, được load trong backend
- **API**: Backend expose endpoints, frontend consume
- **Features**: Feature definitions shared giữa training và inference