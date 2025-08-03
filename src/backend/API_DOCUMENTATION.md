# AI Code Detection API Documentation

## Overview

API backend cho hệ thống phát hiện code AI-generated vs Human-written, được thiết kế đặc biệt cho code C/C++ trong môi trường giáo dục.

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Kiểm tra trạng thái hoạt động của API.

**Response:**
```json
{
  "status": "OK",
  "message": "AI Code Detection API is running",
  "timestamp": 1704067200.0,
  "ml_features_available": true,
  "uptime": 123.45
}
```

### 2. Root Endpoint
**GET** `/`

Thông tin cơ bản về API.

**Response:**
```json
{
  "message": "AI Code Detection API",
  "status": "OK",
  "docs": "/docs",
  "health": "/health",
  "timestamp": 1704067200.0
}
```

### 3. Analyze Code (Text Input)
**POST** `/analyze-code`

Phân tích source code để phát hiện AI-generated vs Human-written.

**Request Body:**
```json
{
  "code": "string (required) - Source code để phân tích",
  "language": "string (default: cpp) - Ngôn ngữ: c hoặc cpp",
  "filename": "string (optional) - Tên file"
}
```

**Response:**
```json
{
  "features": {
    "loc": 25.0,
    "token_count": 156,
    "cyclomatic_avg": 2.5,
    "functions": 3,
    "comment_ratio": 0.12,
    "blank_ratio": 0.08
  },
  "detection": {
    "prediction": "AI-generated",
    "confidence": 0.743,
    "reasoning": [
      "Nhiều tên biến/hàm mô tả chi tiết (AI pattern)",
      "Tỷ lệ comment cao (AI thường comment nhiều)",
      "Code structure tốt: formatting nhất quán"
    ]
  },
  "processing_time": 0.125
}
```

### 4. Analyze Code (File Upload)
**POST** `/analyze-code/file`

Phân tích code từ file upload.

**Request:**
- Content-Type: `multipart/form-data`
- File: C/C++ source file (.c, .cpp, .h, .hpp)

**Response:** Giống như `/analyze-code`

### 5. Submit Feedback
**POST** `/submit-feedback`

Thu thập feedback từ giảng viên để cải thiện model.

**Request Body:**
```json
{
  "code": "string (required) - Source code đã được phân tích",
  "predicted_label": "string (required) - Nhãn dự đoán: AI-generated/Human-written",
  "actual_label": "string (required) - Nhãn thực tế từ giảng viên",
  "feedback_notes": "string (optional) - Ghi chú từ giảng viên"
}
```

**Response:**
```json
{
  "message": "Feedback đã được ghi nhận",
  "status": "success", 
  "timestamp": 1704067200.0
}
```

## Features Extracted

### Code Metrics
- **LOC (Lines of Code)**: Tổng số dòng code
- **Token Count**: Số lượng token (chỉ khi có lizard)
- **Cyclomatic Complexity**: Độ phức tạp thuật toán (trung bình)
- **Functions**: Số lượng hàm/method
- **Comment Ratio**: Tỷ lệ dòng comment
- **Blank Ratio**: Tỷ lệ dòng trống

## Detection Logic

### AI-Generated Indicators
1. **Descriptive Naming**: Tên biến/hàm mô tả chi tiết (camelCase, snake_case)
2. **High Comment Ratio**: Tỷ lệ comment > 15%
3. **Multiple Includes**: Sử dụng nhiều thư viện chuẩn (≥3)
4. **Error Handling**: Có try/catch hoặc error checking
5. **Low Complexity**: Cyclomatic complexity < 3
6. **Consistent Formatting**: Indentation và spacing nhất quán
7. **Template Usage**: Follow template chuẩn (int main, return 0)
8. **Clear Declarations**: Khai báo biến rõ ràng

### Human-Written Indicators
1. **Short Code**: Code ngắn (<20 LOC)
2. **Single Char Variables**: Nhiều biến 1 ký tự (a, b, i, j)
3. **Inconsistent Formatting**: Mixed indentation, spacing

### Confidence Levels
- **> 0.6**: High confidence AI-generated
- **< 0.4**: High confidence Human-written  
- **0.4-0.6**: Uncertain, cần thêm analysis

## Error Codes

- **400 Bad Request**: Input validation failed
- **500 Internal Server Error**: Processing error

## Example Usage

### Python with requests
```python
import requests

# Analyze code
response = requests.post("http://localhost:8000/analyze-code", json={
    "code": "#include <stdio.h>\\nint main() { return 0; }",
    "language": "c"
})

result = response.json()
print(f"Prediction: {result['detection']['prediction']}")
print(f"Confidence: {result['detection']['confidence']}")
```

### cURL
```bash
# Health check
curl http://localhost:8000/health

# Analyze code
curl -X POST http://localhost:8000/analyze-code \\
  -H "Content-Type: application/json" \\
  -d '{
    "code": "#include <stdio.h>\\nint main() { return 0; }",
    "language": "c"
  }'

# Upload file
curl -X POST http://localhost:8000/analyze-code/file \\
  -F "file=@example.cpp"
```

## Development

### Start Development Server
```bash
cd src/backend
make setup  # First time only
make dev    # Start with hot reload
```

### Run Tests
```bash
cd src/backend
python test_api.py  # Manual API tests
```

### API Documentation
Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## Notes

- API hiện tại sử dụng rule-based detection
- Lizard package được sử dụng cho advanced metrics (optional)
- Feedback được log tạm thời, có thể extend để lưu database
- CORS được enable cho development (cần configure cho production)