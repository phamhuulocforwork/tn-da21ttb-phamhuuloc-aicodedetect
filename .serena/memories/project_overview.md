# AI Code Detection System - Project Overview

## Mục đích dự án

Hệ thống phát hiện code được tạo bởi AI, phân biệt giữa code được viết bởi con người và AI. Dự án này là luận văn tốt nghiệp với chủ đề "AI Code Detection".

## Kiến trúc hệ thống

Dự án bao gồm 3 thành phần chính:

### 1. Machine Learning Pipeline (`src/src/`)

- **Feature Extraction**: Trích xuất đặc trung từ code (AST, complexity, style metrics)
- **Model Training**: Training binary classifier để phân loại AI vs Human code
- **Analysis Tools**: Công cụ phân tích và visualization các features

### 2. Backend API (`src/backend/`)

- **Framework**: FastAPI
- **Chức năng**: REST API để phân tích code, trả về prediction và confidence score
- **Static Analysis**: Sử dụng lizard và các công cụ khác để phân tích code

### 3. Frontend Web Interface (`src/frontend/`)

- **Framework**: Next.js với TypeScript
- **UI**: Modern interface với dark/light theme, code editor
- **Features**: Upload code, xem kết quả analysis, charts và visualizations

## Dataset

- **Vị trí**: `src/src/dataset/code/c/`
- **Cấu trúc**:
  - `human/`: Code samples được viết bởi con người
  - `ai/`: Code samples được generate bởi AI
- **Metadata**: Thông tin chi tiết về dataset trong `ithub_oj_metadata.md`

## Tech Stack

- **Backend**: Python 3.12, FastAPI, Uvicorn
- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **ML/Analysis**: NumPy, Pandas, Matplotlib, Seaborn
- **Static Analysis**: Lizard, AST analysis
- **Development**: Make, Virtual environments
