# Trạng thái hiện tại của dự án AI Code Detection

## Cập nhật ngày: 2025-01-27

### Tiến độ phát triển chính
Dự án đã có những tiến bộ đáng kể từ lần onboarding trước:

#### 1. Phát triển Model Machine Learning
- **Đã hoàn thành**: Xây dựng và đánh giá các model ML
- **Thư mục mới**: `src/src/ml_output/` chứa output từ quá trình training
- **Kết quả training**: Có file `final_pipeline_report.json` với kết quả đánh giá model

#### 2. Kết quả Model hiện tại (ngày 29/07/2025):
- **Rule-Based Model**: 
  - Accuracy: 75.5%
  - Precision: 2% (rất thấp)
  - Recall: 100%
  - F1-score: 0.039 (rất thấp)
  - AUC: 1.0

- **Hybrid Model**: Kết quả tương tự Rule-Based

#### 3. Vấn đề cần giải quyết:
- **Precision và F1-score quá thấp** (dưới 60%)
- Model có xu hướng predict tất cả là AI-generated (false positive cao)
- Cần review lại feature selection và data balancing

#### 4. Cấu trúc dữ liệu output mới:
```
src/src/ml_output/
├── comparison/     # So sánh giữa các model
├── models/         # Trained model files  
├── features/       # Extracted features
├── evaluation/     # Evaluation results
└── final_pipeline_report.json  # Báo cáo tổng kết
```

#### 5. Cấu trúc thư mục mới được thêm:
- `src/src/evaluation/` - Chứa code evaluation (hiện có __pycache__)
- `src/src/ml_output/` - Output từ ML pipeline

### Recommendations từ hệ thống:
1. ⚠️ Review feature selection do F1-score thấp
2. ✅ Kết hợp multiple detectors để cải thiện performance  
3. 📊 Monitor performance trên new data thường xuyên
4. 🔄 Retrain model khi có thêm data

### Frontend cập nhật:
- Dependencies đã được cập nhật với các package mới như @firecms/neat, highlight.js
- Vẫn duy trì Next.js 15, React 19, TailwindCSS 4

### Backend: 
- Giữ nguyên FastAPI stack cũ

### Dataset:
- Cấu trúc vẫn giữ nguyên với code/c/ai và code/c/human
- Có metadata được generate