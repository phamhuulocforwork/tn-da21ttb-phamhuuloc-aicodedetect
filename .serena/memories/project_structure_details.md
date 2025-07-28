# Project Structure Details - Cấu trúc dự án chi tiết

## Root Level
```
tn-da21ttb-phamhuuloc-aicodedetect-ml-py/
├── .serena/          # Serena configuration
├── src/              # Source code components  
├── thesis/           # Luận văn documentation
├── progress-report/  # Báo cáo tiến độ
└── README.md         # Project overview (hiện tại trống)
```

## Core ML Component (src/src/)
```
src/src/
├── dataset/          # Dataset files và metadata
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
├── index.ipynb       # Main Jupyter notebook
├── requirements.txt  # Python dependencies (pandas)
├── Makefile         # Setup commands
└── .env.example     # Environment template
```

## Backend API (src/backend/)
```
src/backend/
├── app/
│   └── main.py      # FastAPI application entry point
├── requirements.txt # FastAPI, uvicorn, python-multipart
├── Makefile        # Development commands
└── .gitignore      # Python gitignore
```

## Frontend Web App (src/frontend/)
```
src/frontend/
├── app/            # Next.js App Router pages
├── components/     # React components  
├── lib/            # Utility libraries
├── styles/         # CSS và styling
├── public/         # Static assets
├── package.json    # Dependencies và scripts
├── tsconfig.json   # TypeScript configuration
├── next.config.ts  # Next.js configuration
├── tailwind.config # TailwindCSS setup
├── eslint.config.mjs # ESLint rules
├── .prettierrc.cjs # Prettier formatting
└── node_modules/   # Installed packages
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