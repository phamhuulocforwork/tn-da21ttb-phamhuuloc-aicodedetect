# AI Code Detection Project Overview

## Project Purpose

Hệ thống phân tích và phát hiện mã nguồn AI-generated vs human-written cho ngôn ngữ C/C++. Dự án bao gồm:

- **Feature extraction** từ source code (80+ features)
- **Machine learning models** để classification
- **Web interface** để interactive analysis
- **API backend** cho integration

## Architecture Components

### 1. Core ML Engine (`src/src/`)

- **Python-based** với data science stack
- **Feature extractors**: AST, human style, advanced patterns
- **Model training pipeline** với dataset management
- **Batch processing** cho large-scale analysis

### 2. Backend API (`src/backend/`)

- **FastAPI framework** với comprehensive endpoints
- **Real-time analysis** với multiple methods
- **File upload support** và validation
- **Structured responses** cho frontend integration

### 3. Frontend Interface (`src/frontend/`)

- **Next.js 15** với modern React patterns
- **Interactive code editor** (Monaco Editor)
- **Data visualization** (Recharts, Chart.js)
- **Responsive design** với dark/light themes

## Key Features

- **Multi-method analysis**: Combined, AST-only, Style-only, Advanced
- **Real-time processing**: 1-5 seconds analysis time
- **Interactive visualizations**: Charts, metrics, detailed reports
- **File upload support**: .c, .cpp, .txt files (max 1MB)
- **Export functionality**: JSON reports và raw data
- **API-first design**: RESTful endpoints với comprehensive docs

## Tech Stack Summary

- **Languages**: Python, TypeScript, C/C++ (analysis target)
- **Frameworks**: FastAPI, Next.js, React
- **ML Libraries**: NumPy, Pandas, custom feature extractors
- **UI Components**: Shadcn/UI, Radix primitives
- **Development**: Docker support, comprehensive Makefiles
