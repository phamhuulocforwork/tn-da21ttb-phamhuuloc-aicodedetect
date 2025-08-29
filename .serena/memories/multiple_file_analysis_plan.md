# Kế hoạch triển khai tính năng phân tích nhiều file

## Tổng quan yêu cầu
- **API Backend**: Xử lý upload file nén (zip/rar) và Google Drive links
- **Frontend**: Page với 3 steps sử dụng stepper, data-table và scroller
- **Tính năng chính**: So sánh với baseline và hiển thị radial chart kết quả

## Kiến trúc Backend

### 1. API Endpoints mới cần tạo
- `POST /api/analysis/batch/upload-zip` - Upload và phân tích file nén
- `POST /api/analysis/batch/google-drive` - Phân tích từ Google Drive link
- `GET /api/analysis/batch/{batch_id}/status` - Theo dõi tiến trình phân tích
- `GET /api/analysis/batch/{batch_id}/results` - Lấy kết quả phân tích

### 2. Models dữ liệu
```python
class BatchAnalysisRequest(BaseModel):
    source_type: str  # "zip" or "google_drive"
    source_url: Optional[str] = None
    file: Optional[UploadFile] = None
    
class FileAnalysisResult(BaseModel):
    filename: str
    filepath: str
    language: str
    loc: int
    file_size: int
    ai_similarity: float
    human_similarity: float
    confidence: float
    analysis_id: str
    status: str  # "success", "error", "processing"
    error_message: Optional[str] = None

class BatchAnalysisResponse(BaseModel):
    batch_id: str
    total_files: int
    processed_files: int
    success_count: int
    error_count: int
    results: List[FileAnalysisResult]
    status: str  # "processing", "completed", "error"
```

### 3. Xử lý file nén
- Sử dụng `zipfile` và `rarfile` để extract files
- Validate file extensions (.c, .cpp, .h, .hpp)
- Recursive extraction cho nested folders
- Temporary storage cho extracted files

### 4. Google Drive Integration
- Parse Google Drive share link để lấy file/folder ID
- Sử dụng Google Drive API để download files
- Xử lý nested folders và large files
- Authentication với service account

## Kiến trúc Frontend

### 1. Step 1: Upload Options
- Toggle giữa "Upload File" và "Google Drive Link"
- Drag & drop area cho file upload
- Input field cho Google Drive URL
- Validation cho file types và URL format

### 2. Step 2: File List Table
- Sử dụng `DataTable` component từ Dice UI
- Columns: Filename, Path, Size, Status, Actions
- Row selection và bulk operations
- Filtering và sorting capabilities

### 3. Step 3: Results Display
- Danh sách file với `Scroller` component
- Radial chart cho mỗi file (AI vs Human similarity)
- Nút "Xem chi tiết" link đến analysis page
- Summary statistics

## Component Structure

```
src/frontend/components/features/analysis_multiple/
├── step1-upload-options.tsx
├── step2-file-list.tsx  
├── step3-results-display.tsx
├── file-table.tsx
├── radial-chart.tsx
└── google-drive-input.tsx
```

## API Integration

### Frontend API calls:
```typescript
// Upload file nén
const response = await fetch('/api/analysis/batch/upload-zip', {
  method: 'POST',
  body: formData
});

// Google Drive analysis
const response = await fetch('/api/analysis/batch/google-drive', {
  method: 'POST', 
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({ url: driveUrl })
});

// Check status
const status = await fetch(`/api/analysis/batch/${batchId}/status`);

// Get results
const results = await fetch(`/api/analysis/batch/${batchId}/results`);
```

## Data Flow

1. **Upload Phase**: User uploads file hoặc nhập Google Drive URL
2. **Processing Phase**: Backend extracts/processes files, chạy analysis cho từng file
3. **Results Phase**: Frontend hiển thị danh sách file với kết quả analysis
4. **Detail View**: Click vào file để xem chi tiết analysis

## Error Handling

- File validation errors
- Google Drive access errors  
- Analysis processing errors
- Network connectivity issues
- Large file size limits

## Performance Considerations

- Batch processing để tránh overload
- Progress tracking cho large uploads
- Caching cho repeated analyses
- Pagination cho large result sets
- Memory management cho file processing