# AI Code Detection System - Tổng quan dự án

## Thông tin dự án

- **Tên dự án**: AI Code Detection System
- **Mục đích**: Phát hiện mã nguồn được tạo bởi AI (như ChatGPT, GitHub Copilot) so với mã nguồn viết bởi lập trình viên con người
- **Trường**: Trường Đại học Trà Vinh
- **Khoa**: Khoa Kỹ thuật & Công nghệ
- **Lớp**: DA21TTB
- **Loại**: Khóa luận tốt nghiệp ngành Công nghệ thông tin
- **Mã sinh viên**: DA21TTB-110121055
- **Tên sinh viên**: Phạm Hữu Lộc
- **Giảng viên hướng dẫn**: TS. Nguyễn Bảo Ân

## Mục tiêu nghiên cứu

Hệ thống phân tích và phát hiện mã nguồn được tạo ra bởi các mô hình AI so với mã nguồn được viết bởi lập trình viên con người, tập trung vào:

### Phân tích kỹ thuật chính:

1. **Phân tích AST (Abstract Syntax Tree)**: Cấu trúc ngữ pháp và logic của mã
2. **Phân tích phong cách coding**: Patterns đặc trưng của AI vs Human
3. **So sánh baseline**: Điểm chuẩn từ dataset lớn
4. **AI Detection Models**: Machine learning models để phân loại
5. **Batch Analysis**: Phân tích nhiều files cùng lúc
6. **Google Drive Integration**: Tích hợp OAuth2 để truy cập files

## Kiến trúc hệ thống

```
tn-da21ttb-phamhuuloc-aicodedetect/
├── src/
│   ├── backend/                    # FastAPI backend
│   ├── frontend/                   # Next.js frontend
│   └── src/                        # Python analysis modules
├── scripts/                        # Management scripts
├── docker-compose.yml             # Production setup
├── nginx/                         # Nginx configuration
└── thesis/                        # Documentation
```

## Các tính năng chính

- **Single File Analysis**: Phân tích một file code duy nhất
- **Batch Analysis**: Phân tích nhiều files từ ZIP, RAR hoặc Google Drive
- **AI Analysis**: Sử dụng Google Gemini AI để phân tích code patterns
- **Feature Extraction**: Trích xuất các đặc trưng từ AST và style analysis
- **Baseline Comparison**: So sánh với dataset baseline của AI và Human code
- **Real-time Analysis**: Phân tích real-time với progress tracking
- **OAuth2 Integration**: Kết nối với Google Drive để phân tích files
- **Visualization**: Charts và graphs để hiển thị kết quả phân tích

## Ngôn ngữ lập trình hỗ trợ

- C/C++ (chính)
- Python (analysis modules)
- TypeScript/JavaScript (frontend)
- Shell scripts (deployment)

## Đối tượng sử dụng

- Sinh viên và giảng viên ngành CNTT
- Nhà phát triển phần mềm
- Nhà nghiên cứu AI
- Các tổ chức cần kiểm tra tính xác thực của code
