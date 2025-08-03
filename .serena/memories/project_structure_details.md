# Project Structure Details - Cấu trúc dự án chi tiết (Cập nhật 2025-01-27)

## Root Level
```
tn-da21ttb-phamhuuloc-aicodedetect-ml-py/
├── .serena/          # Serena configuration
├── src/              # Source code components  
├── thesis/           # Luận văn documentation
├── progress-report/  # Báo cáo tiến độ
└── README.md         # Project overview (hiện tại trống)
```

## Core ML Component (src/src/) - **CẬP NHẬT**
```
src/src/
├── dataset/          # Dataset files và metadata
│   ├── metadata/     # Generated metadata files
│   └── code/c/       # C/C++ code samples
│       ├── ai/       # AI-generated code
│       └── human/    # Human-written code  
├── scripts/          # Utility scripts
│   └── create_metadata.py  # Tạo metadata từ dataset
├── features/         # Feature extraction
│   ├── gemini_res.py # AI code generation với Gemini
│   └── test_*.py     # Test scripts
├── extractor/        # Data extraction tools
├── rules/            # Rule-based detection logic
├── evaluation/       # **MỚI** - Model evaluation code
│   └── __pycache__/  # Python cache files
├── ml_output/        # **MỚI** - ML Pipeline outputs
│   ├── comparison/   # Model comparison results
│   ├── models/       # Trained model files
│   ├── features/     # Extracted features data
│   ├── evaluation/   # Detailed evaluation results
│   └── final_pipeline_report.json  # Tổng kết kết quả training
├── index.ipynb       # Main Jupyter notebook
├── requirements.txt  # Python dependencies (pandas==2.3.1)
├── Makefile         # Setup commands
├── .env.example     # Environment template
├── .gitignore       # Python gitignore
└── .cursorignore    # Cursor IDE ignore
```

## Backend API (src/backend/)
```
src/backend/
├── app/
│   └── main.py      # FastAPI application entry point
├── venv/            # Python virtual environment
├── requirements.txt # FastAPI, uvicorn, python-multipart
├── Makefile        # Development commands
└── .gitignore      # Python gitignore
```

## Frontend Web App (src/frontend/) - **CẬP NHẬT**
```
src/frontend/
├── .next/          # Next.js build output
├── app/            # Next.js App Router pages
├── components/     # React components  
├── lib/            # Utility libraries
├── styles/         # CSS và styling
├── public/         # Static assets
├── package.json    # **CẬP NHẬT** - Dependencies và scripts
├── package-lock.json # Lock file
├── components.json # Radix UI components config
├── tsconfig.json   # TypeScript configuration
├── next.config.ts  # Next.js configuration
├── next-env.d.ts   # Next.js type declarations
├── postcss.config.mjs # PostCSS configuration
├── eslint.config.mjs # ESLint rules
├── .eslintrc.json  # ESLint config
├── .prettierrc.cjs # Prettier formatting
├── .editorconfig   # Editor configuration
├── .gitignore      # Git ignore
└── README.md       # Frontend documentation
```

## Thesis Documentation (thesis/)
```
thesis/
├── images/    # Hình ảnh cho luận văn
├── docx/      # Word documents  
├── pdf/       # PDF exports
├── abs/       # Abstracts
├── drawio/    # Diagrams
└── md/        # Markdown notes
```

## Key Configuration Files
- **Environment**: .env files cho API keys (Gemini)
- **Dependencies**: requirements.txt (Python), package.json (Node.js)  
- **Build tools**: Makefile (Python projects), npm scripts (Frontend)
- **Code quality**: ESLint, Prettier, TypeScript configs
- **Git**: .gitignore files ở mỗi component

## Những thay đổi chính:
1. **Thêm thư mục `ml_output/`**: Chứa kết quả từ ML pipeline
2. **Thêm thư mục `evaluation/`**: Code đánh giá model
3. **Dataset có metadata**: Cấu trúc dataset được mở rộng
4. **Frontend dependencies**: Thêm nhiều package mới như highlight.js, @firecms/neat