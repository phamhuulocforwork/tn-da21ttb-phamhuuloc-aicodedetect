# AI Code Detection System

## Nghiên cứu và phát triển hệ thống phát hiện mã nguồn do AI tạo

### 📚 Thông tin dự án

**Trường**: Trường Đại học Trà Vinh<br>
**Khoa**: Khoa Kỹ thuật & Công nghệ<br>
**Lớp**: DA21TTB<br>
**Loại**: Khóa luận tốt nghiệp ngành Công nghệ thông tin<br>
**Mã sinh viên**: DA21TTB-110121055<br>
**Tên sinh viên**: Phạm Hữu Lộc<br>
**Giảng viên hướng dẫn**: TS. Nguyễn Bảo Ân<br>
**Năm bảo vệ**: 2025

---

## 🎯 Mục tiêu nghiên cứu

**Tên đề tài**: Xây dựng cơ chế phát hiện AI-generated code trong bài tập lập trình sinh viên

Hệ thống phân tích và phát hiện mã nguồn được tạo ra bởi các mô hình AI (như ChatGPT, GitHub Copilot, Claude) so với mã nguồn được viết bởi lập trình viên con người. Dự án tập trung vào việc xây dựng một công cụ toàn diện với **4 phương pháp phân tích** và **100+ đặc trưng** để hỗ trợ giảng viên và nhà phát triển đánh giá tính xác thực của code.

### Mục tiêu chính:

- **Xây dựng hệ thống phân tích mã nguồn toàn diện** sử dụng nhiều phương pháp tiếp cận khác nhau
- **Phát triển 4 module phân tích chuyên biệt** với tổng cộng hơn 100 đặc trưng
- **Tạo giao diện web thân thiện** với khả năng hiển thị kết quả phân tích chi tiết
- **Đánh giá hiệu quả** của hệ thống trong việc phát hiện code AI-generated

### Các phương pháp phân tích chính:

#### 1. **Phân tích tổng hợp** (100+ đặc trưng)

- Kết hợp tất cả các module phân tích
- Đưa ra kết quả toàn diện nhất

#### 2. **Phân tích AST (Abstract Syntax Tree)** (25+ đặc trưng)

- Cấu trúc ngữ pháp và logic của mã
- Patterns đặc trưng của AI vs Human
- Sử dụng regex pattern matching thay vì parser truyền thống

#### 3. **Phân tích phong cách Human** (39+ đặc trưng)

- Phát hiện "không nhất quán tự nhiên" của code con người
- Phân tích spacing, indentation, naming conventions
- Tính điểm overall_human_score (0-1 scale)

#### 4. **AI Analysis với Google Gemini** (Phân tích thông minh)

- Tích hợp Google Gemini 2.0 Flash API
- Phân tích với khả năng lập luận và giải thích
- Output format MDX có cấu trúc

---

## 🛠️ Công nghệ sử dụng

- **Frontend**: `Next.js 15.3.5`, `TypeScript 5`, `React 19.0.0`, `TailwindCSS 4`, `Shadcn/UI`, `Radix UI`, `Monaco Editor`, `Chart.js 4.5.0`, `Recharts 2.15.4`, `ECharts 6.0.0`, `Lucide React`, `Framer Motion`, `next-themes`

- **Backend**: `FastAPI`, `Python 3.8+`, `Uvicorn`, `Google Gemini 2.0 Flash API`, `aiohttp`, `aiofiles`, `zipfile`, `rarfile`, `google-api-python-client`

- **Analysis Modules (Python Core)**: AST Analyzer (25+ đặc trưng), Human Style Analyzer (39+ đặc trưng), Advanced Features (32+ đặc trưng), Detection Models (Heuristic & binary classifiers), Baseline Comparison (dataset statistics & feature normalization)

- **DevOps & Infrastructure**: `Docker 20.10+`, `Docker Compose`, `Nginx`, `Let's Encrypt`, Reverse Proxy (load balancing, static file serving)

---

## 📊 Các đặc trưng phân tích (100+ features)

### 🎯 AST Analyzer Module (25+ đặc trưng)

#### Nhóm cấu trúc (Structure Features)

- `total_nodes`: Tổng số node ước lượng trong AST
- `nodes_per_loc`: Mật độ node trên mỗi dòng code
- `max_depth`: Độ sâu tối đa của AST
- `branching_factor`: Hệ số phân nhánh

#### Nhóm luồng điều khiển (Control Flow)

- `if_statements`, `for_loops`, `while_loops`, `switch_statements`
- `nested_control_depth`: Độ sâu lồng nhau tối đa
- `*_per_loc`: Mật độ trên mỗi dòng code

#### Nhóm hàm và biến (Functions & Variables)

- `function_count`, `avg_function_length`, `recursive_functions`
- `variable_count`, `camel_case_ratio`, `snake_case_ratio`
- `single_char_vars_ratio`: Tỷ lệ biến 1 ký tự

#### Nhóm patterns (Code Patterns)

- `magic_numbers`, `string_literals`, `include_count`
- `indentation_consistency`, `brace_style_consistency`

### 🎨 Human Style Analyzer Module (39+ đặc trưng)

#### Nhóm vấn đề khoảng trắng (Spacing Issues)

- `missing_space_before/after_operator`
- `extra_space_before/after_operator`
- `space_after_opening_paren`, `space_before_closing_paren`
- `trailing_spaces`, `spacing_issues_ratio`

#### Nhóm vấn đề thụt lề (Indentation Issues)

- `mixed_tabs_spaces`, `inconsistent_indentation`
- `unusual_indent_size`, `indentation_issues_ratio`

#### Nhóm bất nhất quán đặt tên (Naming Inconsistency)

- `mixed_camel_snake`, `unclear_abbreviations`
- `naming_inconsistency_ratio`

#### Nhóm vấn đề định dạng (Formatting Issues)

- `inconsistent_brace_style`, `poor_comment_formatting`
- `formatting_issues_ratio`

**Điểm tổng thể**: `overall_human_score` (0-1 scale)

### 🔬 Advanced Features Module (32+ đặc trưng)

#### Nhóm đặc trưng cơ bản

- `loc`, `token_count`, `cyclomatic_complexity`
- `comment_ratio`, `blank_ratio`

#### Nhóm redundancy

- `duplicate_lines`, `copy_paste_score`
- `repeated_patterns`, `similar_function_ratio`

#### Nhóm complexity

- `halstead_complexity`, `cognitive_complexity`
- `maintainability_index`

#### Nhóm AI patterns

- `template_usage_score`, `boilerplate_ratio`
- `error_handling_score`, `over_engineering_score`

### 🤖 AI Analysis Module (Google Gemini)

**Output format MDX có cấu trúc:**

```markdown
# Phân tích Code AI Detection

## Kết quả dự đoán

**Dự đoán:** [AI-generated/Human-written]
**Độ tin cậy:** [0-100]%
**Xác suất AI:** [0-100]%
**Xác suất Human:** [0-100]%

## Phân tích chi tiết

### Phong cách mã nguồn

### Cấu trúc code

### Patterns cú pháp

### Documentation

## Chỉ số quan trọng

### Patterns AI phát hiện

### Patterns Human phát hiện

## Lý do chính (3 lý do)

## Giải thích độ tin cậy

## Ghi chú bổ sung
```

---

## 🏗️ Kiến trúc hệ thống

### Frontend (Next.js)

```
src/frontend/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Route groups
│   ├── api/               # API routes
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── ui/               # Shadcn/UI components
│   ├── forms/            # Form components
│   ├── charts/           # Chart components
│   └── analysis/         # Analysis-specific components
├── lib/                  # Utilities
│   ├── api.ts            # API client
│   ├── utils.ts          # Utility functions
│   └── validations.ts    # Form validations
├── hooks/                # Custom React hooks
└── types/                # TypeScript definitions
```

### Backend (FastAPI)

```
src/backend/app/
├── main.py               # FastAPI application
├── baseline_loader.py    # Baseline statistics
├── chart_helpers.py      # Chart generation
└── __init__.py
```

### Analysis Modules (Python Core)

```
src/src/
├── features/             # Feature extractors
│   ├── ast_analyzer.py          # 25+ AST features
│   ├── human_style_analyzer.py  # 39+ style features
│   ├── advanced_features.py     # 32+ advanced features
│   └── detection_models.py      # ML classifiers
├── models/               # ML models & baseline
├── dataset/              # Training datasets
├── analysis_plots/       # Visualization utilities
└── requirements.txt      # Analysis dependencies
```

### Production Infrastructure

```
tn-da21ttb-phamhuuloc-aicodedetect/
├── docker-compose.yml         # Production stack
├── docker-compose.dev.yml     # Development stack
├── nginx/                     # Reverse proxy config
│   ├── nginx.conf
│   ├── conf.d/
│   └── ssl/
├── scripts/                   # Management scripts
│   ├── deploy.sh             # Auto deployment
│   ├── manage.sh             # Service management
│   └── setup-vps.sh          # VPS setup
└── src/                      # Application source
```

---

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống

- **Python**: 3.8+
- **Node.js**: 18+
- **Docker**: 20.10+ (optional)
- **Git**: Latest version

### 1. Triển khai với Docker (Khuyến nghị cho Production)

#### Chuẩn bị VPS Ubuntu 22.04

```bash
# 1. Setup VPS tự động (chạy với root)
sudo ./scripts/setup-vps.sh

# 2. Chuyển sang user appuser
su - appuser

# 3. Clone repository
git clone https://github.com/your-username/tn-da21ttb-phamhuuloc-aicodedetect.git app
cd app
```

#### Cấu hình Environment

```bash
# Copy file cấu hình mẫu
cp env.example .env

# Chỉnh sửa file .env với thông tin thực tế
nano .env

# Các biến quan trọng cần cấu hình:
# - GEMINI_API_KEY: API key từ Google AI Studio
# - GOOGLE_DRIVE_API_KEY: API key cho Google Drive integration
# - SSL_DOMAIN: Domain của bạn (để có HTTPS)
# - SSL_EMAIL: Email để nhận thông báo SSL
```

#### Triển khai ứng dụng

```bash
# Chạy script deploy tự động
./scripts/deploy.sh

# Hoặc chạy thủ công
docker-compose up --build -d
```

#### Kiểm tra trạng thái

```bash
# Xem trạng thái services
./scripts/manage.sh status

# Xem logs
./scripts/manage.sh logs

# Kiểm tra health
./scripts/manage.sh health
```

### 2. Quản lý ứng dụng

#### Các lệnh quản lý thường dùng

```bash
# Restart services
./scripts/manage.sh restart

# Xem logs của service cụ thể
./scripts/manage.sh logs nginx
./scripts/manage.sh logs backend

# Backup dữ liệu
./scripts/manage.sh backup

# Mở shell trong container
./scripts/manage.sh shell backend

# Kiểm tra SSL certificate
./scripts/manage.sh ssl-status

# Renew SSL certificate
./scripts/manage.sh ssl-renew
```

### 3. Cấu trúc Production

```
tn-da21ttb-phamhuuloc-aicodedetect/
├── docker-compose.yml          # Cấu hình chính
├── docker-compose.override.yml # Cấu hình production
├── env.example                 # Template environment
├── nginx/                      # Nginx configuration
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── conf.d/
│   ├── init-ssl.sh
│   └── docker-entrypoint.sh
├── scripts/                    # Management scripts
│   ├── deploy.sh              # Auto deployment
│   ├── manage.sh              # Service management
│   └── setup-vps.sh           # VPS setup
└── src/                       # Application source
```

### 4. SSL và Domain Configuration

#### Thiết lập Domain

1. Trỏ domain về IP VPS của bạn
2. Cập nhật `SSL_DOMAIN` trong file `.env`
3. Chạy `./scripts/deploy.sh` để áp dụng thay đổi

#### SSL Certificate tự động

- Hệ thống tự động tạo SSL certificate từ Let's Encrypt
- Certificate được renew tự động mỗi 90 ngày
- Sử dụng `SSL_STAGING=true` trong `.env` để test SSL

### 5. Monitoring và Logs

#### Xem logs real-time

```bash
# Tất cả services
docker-compose logs -f

# Service cụ thể
docker-compose logs -f nginx
```

#### Health checks

```bash
# Kiểm tra health của tất cả services
./scripts/manage.sh health

# Kiểm tra từng service
curl http://localhost/health
curl http://localhost/api/health
```

### 6. Backup và Recovery

#### Tự động backup

```bash
# Tạo backup
./scripts/manage.sh backup

# Backup sẽ được lưu trong thư mục backup_YYYYMMDD_HHMMSS/
```

#### Khôi phục từ backup

```bash
# Dừng services
docker-compose down

# Khôi phục volumes
docker run --rm -v $(pwd):/backup \
  -v nginx_logs:/nginx_logs \
  -v nginx_ssl:/nginx_ssl \
  -v letsencrypt:/letsencrypt \
  alpine tar xzf /backup/backup_dir/volumes.tar.gz

# Khởi động lại
docker-compose up -d
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
