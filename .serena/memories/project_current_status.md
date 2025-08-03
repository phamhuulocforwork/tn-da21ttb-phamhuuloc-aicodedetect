# Trạng thái hiện tại của dự án AI Code Detection

## Cập nhật ngày: 2025-01-27

### Tình trạng tổng quan
Dự án AI Code Detection đã có những tiến bộ đáng kể trong việc phát triển và đánh giá các model Machine Learning để phân biệt code được viết bởi AI và con người.

### Kết quả Model Machine Learning hiện tại

#### 1. Kết quả Training (từ final_pipeline_report.json - 29/07/2025):

**Rule-Based Model:**
- Accuracy: 75.5%
- Precision: 2% ⚠️ (cực kỳ thấp)
- Recall: 100%
- F1-score: 0.0392 ⚠️ (cực kỳ thấp)
- Specificity: 75.38%
- AUC Score: 1.0
- True Positives: 1, True Negatives: 150
- False Positives: 49, False Negatives: 0

**Hybrid Model:**
- Có kết quả hoàn toàn giống với Rule-Based Model
- Cho thấy cần review lại cách kết hợp các phương pháp

#### 2. Vấn đề nghiêm trọng cần giải quyết:
- **Precision quá thấp (2%)**: Model có xu hướng classify hầu hết code là AI-generated
- **F1-score cực thấp (0.039)**: Dưới ngưỡng chấp nhận được (< 60%)
- **High False Positive Rate**: 49/50 cases bị misclassify
- **Model bias**: Có thể do dataset imbalance hoặc feature selection không phù hợp

### Cấu trúc Output mới được tạo:

```
src/src/ml_output/
├── comparison/       # So sánh performance giữa các model
├── models/          # Trained model files (.pkl)
├── features/        # Extracted features data
├── evaluation/      # Chi tiết evaluation results
└── final_pipeline_report.json  # Báo cáo tổng kết
```

### Cấu trúc thư mục chính:
```
├── .serena/         # Serena MCP configuration
├── src/
│   ├── src/         # Core ML component với dataset và model
│   ├── backend/     # FastAPI backend
│   └── frontend/    # Next.js frontend
├── thesis/          # Luận văn documentation
├── progress-report/ # Báo cáo tiến độ
└── README.md
```

### Recommendations từ hệ thống:
1. ⚠️ **URGENT**: Review feature selection do F1-score quá thấp (0.039)
2. ⚠️ **URGENT**: Cần fix data imbalance issue
3. ✅ Kết hợp multiple detectors để cải thiện performance
4. 📊 Monitor performance trên new data thường xuyên
5. 🔄 Retrain model khi có thêm balanced data

### Công việc cần ưu tiên:
1. **Data Analysis**: Phân tích dataset balance và feature distribution
2. **Feature Engineering**: Review và cải thiện feature extraction
3. **Model Tuning**: Thử các hyperparameter khác
4. **Data Augmentation**: Tăng cường dataset để balance hơn
5. **Evaluation**: Test trên external dataset để validate

### Tech Stack hiện tại:
- **ML/Data**: Python, Pandas, Jupyter Notebook
- **Backend**: FastAPI đã setup sẵn
- **Frontend**: Next.js 15, React 19, TailwindCSS 4
- **Environment**: WSL2 Linux