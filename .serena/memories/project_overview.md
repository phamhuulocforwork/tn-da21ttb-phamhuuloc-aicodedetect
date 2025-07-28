# AI Code Detection Project - Dự án Phát hiện Code AI

## Mục đích dự án
Đây là dự án luận văn của Phạm Hữu Lộc (TN-DA21TTB) về "AI Code Detection" - Phát hiện code được sinh bởi AI. Dự án nhằm:
- Xây dựng dataset code C/C++ từ cả con người và AI  
- Phân tích và trích xuất đặc trưng từ code
- Phát triển model Machine Learning để phân biệt code AI vs Human
- Xây dựng web application để demo kết quả

## Cấu trúc dự án
```
├── src/
│   ├── src/           # Core ML components và dataset processing
│   ├── backend/       # FastAPI backend server  
│   └── frontend/      # Next.js React frontend
├── thesis/           # Tài liệu luận văn
├── progress-report/  # Báo cáo tiến độ
└── README.md
```

## Tech stack chính
- **ML/Data Science**: Python, Pandas, Jupyter Notebook
- **Backend**: FastAPI, Python 3, uvicorn
- **Frontend**: Next.js 15, React 19, TypeScript, TailwindCSS 4
- **AI Integration**: Google Gemini API (để sinh code AI)
- **Development**: WSL2 trên Windows