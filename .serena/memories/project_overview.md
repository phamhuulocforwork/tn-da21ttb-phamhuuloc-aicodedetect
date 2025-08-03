# AI Code Detection Project - Dự án Phát hiện Code AI

## Thông tin cơ bản
- **Tác giả**: Phạm Hữu Lộc 
- **Mã số**: TN-DA21TTB
- **Loại**: Luận văn tốt nghiệp
- **Chủ đề**: "AI Code Detection" - Phát hiện code được sinh bởi AI
- **Environment**: WSL2 Linux, workspace tại `/home/huuloc/Github/tn-da21ttb-phamhuuloc-aicodedetect-ml-py`

## Mục đích dự án
Phát triển hệ thống phân biệt code C/C++ được viết bởi AI vs con người thông qua:
- Xây dựng dataset code C/C++ từ cả con người và AI generators
- Phân tích và trích xuất đặc trưng từ code structure
- Phát triển Machine Learning models để classification
- Xây dựng web application để demo và test kết quả

## Tình trạng hiện tại (2025-01-27)
### ✅ Đã hoàn thành:
- Dataset C/C++ với code từ human và AI (Gemini)
- Feature extraction pipeline
- Rule-based và Hybrid model training
- Cấu trúc project hoàn chỉnh (ML, Backend, Frontend)

### ⚠️ Vấn đề nghiêm trọng:
- **Model performance kém**: F1-score chỉ 0.039 (< 60% standard)
- **Precision cực thấp**: 2% (high false positive rate)
- Model có bias classify hầu hết code là AI-generated

### 🎯 Cần ưu tiên:
1. Fix model performance issues
2. Review feature selection và data balance
3. Improve evaluation methodology

## Cấu trúc chính
```
├── src/src/         # Core ML: dataset, features, models, evaluation
├── src/backend/     # FastAPI API server
├── src/frontend/    # Next.js web interface  
├── thesis/          # Luận văn documentation
└── progress-report/ # Báo cáo tiến độ
```

## Tech Stack
- **ML/Data Science**: Python, Pandas, Jupyter Notebook, scikit-learn
- **Backend API**: FastAPI, Python 3, uvicorn
- **Frontend**: Next.js 15, React 19, TypeScript, TailwindCSS 4
- **AI Integration**: Google Gemini API (code generation)
- **Development**: WSL2, VS Code với Cursor

## Output quan trọng
- **Dataset**: `src/src/dataset/code/c/` (ai/ và human/ folders)
- **Models**: `src/src/ml_output/models/` (trained .pkl files)
- **Results**: `src/src/ml_output/final_pipeline_report.json`
- **Evaluation**: Chi tiết metrics và comparison results

## Mục tiêu tiếp theo
1. Cải thiện model performance lên F1-score > 60%
2. Balance dataset và feature engineering
3. Hoàn thiện web application demo
4. Viết luận văn final với kết quả cải thiện