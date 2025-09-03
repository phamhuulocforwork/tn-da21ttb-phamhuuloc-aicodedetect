# AI Code Detection System

## Nghiên cứu và phát triển hệ thống phát hiện mã nguồn do AI tạo

### 📚 Thông tin dự án

**Trường**: Trường Đại học Trà Vinh
**Khoa**: Khoa Kỹ thuật & Công nghệ
**Lớp**: DA21TTB
**Loại**: Khóa luận tốt nghiệp ngành Công nghệ thông tin
**Mã sinh viên**: DA21TTB-110120138
**Tên sinh viên**: Phạm Hữu Lộc
**Giảng viên hướng dẫn**: TS. Nguyễn Bảo Ân

---

## 🎯 Mục tiêu nghiên cứu

Hệ thống phân tích và phát hiện mã nguồn được tạo ra bởi các mô hình AI (như ChatGPT, GitHub Copilot) so với mã nguồn được viết bởi lập trình viên con người. Dự án tập trung vào:

- **Phân tích AST (Abstract Syntax Tree)**: Cấu trúc ngữ pháp và logic của mã
- **Phân tích phong cách coding**: Patterns đặc trưng của AI vs Human
- **So sánh baseline**: Điểm chuẩn từ dataset lớn
- **AI Detection Models**: Machine learning models để phân loại
- **Batch Analysis**: Phân tích nhiều files cùng lúc
- **Google Drive Integration**: Tích hợp OAuth2 để truy cập files

---

## 🛠️ Công nghệ sử dụng

- Frontend: `Next.js`, `TypeScript`, `TailwindCSS`, `Shadcn/UI`, `Monaco Editor`, `Recharts`, `Chart.js`, `next-themes`
- Backend: `FastAPI`, `Python 3.8+`, `Uvicorn`, `Google Gemini API`, `aiofiles`, `aiohttp`, `google-api-python-client`, `zipfile`, `rarfile`
- Analysis: `Feature Extractor`, `AST Analyzer`, `Human Style Analyzer`, `ML Classifiers`, `Baseline Comparison`
- DevOps: `Docker`, `Docker Compose`, `Turbopack`, `Swagger UI`, `ReDoc`

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống

- **Python**: 3.8+
- **Node.js**: 18+
- **Docker**: 20.10+ (optional)
- **Git**: Latest version

### 1. Sử dụng Docker

```bash
# Clone repository
git clone https://github.com/your-username/tn-da21ttb-phamhuuloc-aicodedetect.git
cd tn-da21ttb-phamhuuloc-aicodedetect
```

```bash
# Tạo env
cp .env.example .env
```

```bash
# Chạy development environment
docker-compose -f docker-compose.dev.yml up --build
```

```bash
# Hoặc chạy production
docker-compose up --build
```

### 2. Chạy cục bộ

#### Backend Setup

```bash
cd src/backend
```

```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

```bash
# Install dependencies
pip install -r requirements.txt
```

```bash
# Setup environment variables
cp .env.example .env
# Edit .env với API keys cần thiết
```

```bash
# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd src/frontend
```

```bash
# Install dependencies
npm install
```

```bash
# Setup environment
cp .env.local.example .env.local
# Edit .env.local với backend URL
```

```bash
# Run development server
npm run dev
```

### Option 3: Production Deployment

```bash
# Build frontend
cd src/frontend
npm run build
npm run start

# Build backend
cd ../backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🏗️ Cấu trúc dự án

```txt
tn-da21ttb-phamhuuloc-aicodedetect/
├── src/
│   ├── backend/                    # FastAPI backend
│   │   ├── app/
│   │   │   ├── main.py            # Main FastAPI app
│   │   │   └── baseline_loader.py # Baseline stats loader
│   │   ├── test_api.py            # API tests
│   │   ├── requirements.txt       # Python dependencies
│   │   └── Dockerfile             # Backend container
│   │
│   ├── frontend/                   # Next.js frontend
│   │   ├── app/                   # App router pages
│   │   ├── components/            # React components
│   │   ├── lib/                   # Utilities & API client
│   │   ├── styles/                # Global styles
│   │   └── package.json           # Node dependencies
│   │
│   └── src/                       # Python analysis modules
│       ├── features/              # Feature extractors
│       │   ├── advanced_features.py
│       │   ├── ast_analyzer.py
│       │   ├── human_style_analyzer.py
│       │   └── detection_models.py
│       ├── models/                # ML models
│       ├── dataset/               # Training data
│       ├── analysis_plots/        # Visualization
│       └── requirements.txt       # Analysis dependencies
│
├── thesis/                        # Documentation
├── docker-compose.yml             # Production setup
├── docker-compose.dev.yml         # Development setup
└── README.md                      # This file
```

## 🔐 Environment Variables

### Backend (.env)

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_DRIVE_API_KEY=your_drive_api_key

# Optional
ENVIRONMENT=development
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
MAX_FILE_SIZE=1048576
```

### Frontend (.env.local)

```bash
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_oauth_client_id

# Optional
NEXT_PUBLIC_ENABLE_CHARTS=true
NEXT_PUBLIC_MAX_CODE_LENGTH=50000
```

---
