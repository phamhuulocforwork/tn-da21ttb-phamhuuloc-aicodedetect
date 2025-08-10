from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
import time
import tempfile
import os
import sys
from pathlib import Path

# Shared basic analysis (fallback)
from .basic_analysis import basic_analyze_code_features, basic_detect_ai_code

# NOTE: Kiểm tra enhanced static analyzer (không còn ML integration cũ)
try:
    from .enhanced_ml_integration import analyze_code_with_enhanced_ml, get_enhanced_analyzer
    HAS_ENHANCED_ML = True
except ImportError:
    try:
        from enhanced_ml_integration import analyze_code_with_enhanced_ml, get_enhanced_analyzer
        HAS_ENHANCED_ML = True
    except ImportError:
        HAS_ENHANCED_ML = False
        print("Enhanced static analyzer not available - using basic fallback")

# Basic fallback functions are provided by basic_analysis module

app = FastAPI(
    title="AI Code Detection API",
    description="API for detecting AI-generated code vs Human-written code with enhanced static analysis (no ML)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FIXME: Cấu hình cho production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Source code để phân tích")
    language: str = Field(default="cpp", description="Ngôn ngữ lập trình (c, cpp)")
    filename: Optional[str] = Field(default=None, description="Tên file (tùy chọn)")
    detector_type: str = Field(default="heuristic", description="Loại detector: heuristic (mặc định)")
    enhanced_analysis: bool = Field(default=True, description="Sử dụng enhanced static analysis (không ML)")

class BasicCodeFeatures(BaseModel):
    loc: float = Field(description="Lines of Code")
    token_count: Optional[float] = Field(description="Số lượng token")
    cyclomatic_complexity: Optional[float] = Field(description="Độ phức tạp cyclomatic trung bình")
    functions: Optional[int] = Field(description="Số lượng hàm")
    comment_ratio: Optional[float] = Field(description="Tỷ lệ comment")
    blank_ratio: Optional[float] = Field(description="Tỷ lệ dòng trống")

class EnhancedFeatures(BaseModel):
    ast_features: Optional[Dict] = Field(description="Các features AST")
    redundancy_features: Optional[Dict] = Field(description="Các features redundancy")
    naming_patterns: Optional[Dict] = Field(description="Các features naming pattern")
    complexity_features: Optional[Dict] = Field(description="Các features complexity")
    ai_patterns: Optional[Dict] = Field(description="Các features AI-specific pattern")

class DetectionResult(BaseModel):
    prediction: str = Field(description="AI-generated, Human-written, or Uncertain (chưa xác định)")
    confidence: float = Field(description="Độ tin cậy (0-1)")
    reasoning: List[str] = Field(description="Lý do phán đoán")
    method_used: str = Field(description="Phương pháp sử dụng")

class PerformanceMetrics(BaseModel):
    feature_extraction_time: float = Field(description="Thời gian trích xuất features (s)")
    detection_time: float = Field(description="Thời gian phát hiện (s)")
    total_time: float = Field(description="Tổng thời gian xử lý (s)")

class AnalysisMetadata(BaseModel):
    enhanced_analysis: bool = Field(description="Có sử dụng enhanced analysis không")
    detector_type: str = Field(description="Loại detector đã sử dụng")
    available_detectors: List[str] = Field(description="Các detector có sẵn")
    feature_count: int = Field(description="Số lượng features đã trích xuất")
    fallback_reason: Optional[str] = Field(description="Lý do fallback (nếu có)")

class EnhancedAnalysisResponse(BaseModel):
    basic_features: BasicCodeFeatures
    enhanced_features: Optional[EnhancedFeatures]
    detection: DetectionResult
    performance: PerformanceMetrics
    meta: AnalysisMetadata

class FeedbackRequest(BaseModel):
    code: str = Field(..., description="Source code đã được phân tích")
    predicted_label: str = Field(..., description="Nhãn dự đoán từ hệ thống")
    actual_label: str = Field(..., description="Nhãn thực tế từ giảng viên")
    feedback_notes: Optional[str] = Field(default="", description="Ghi chú từ giảng viên")

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: float
    ml_features_available: bool
    enhanced_ml_available: bool
    uptime: float

class DetectorInfoResponse(BaseModel):
    enhanced_ml_available: bool
    available_detectors: List[str]
    detector_details: Dict[str, Dict]

start_time = time.time()

# Removed ML model path resolution (no ML in codebase)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
        API kiểm tra server
    """
    ml_available = HAS_ENHANCED_ML
    
    return HealthResponse(
        status="OK",
        message="AI Code Detection API is running",
        timestamp=time.time(),
        ml_features_available=ml_available,
        enhanced_ml_available=HAS_ENHANCED_ML,
        uptime=time.time() - start_time
    )

@app.get("/")
async def root():
    return {
        "message": "AI Code Detection API v2.0",
        "status": "OK", 
        "enhanced_ml": HAS_ENHANCED_ML,
        "docs": "/docs",
        "health": "/health",
        "timestamp": time.time()
    }

@app.get("/detectors", response_model=DetectorInfoResponse)
async def get_detector_info():
    """
        API lấy thông tin của các detector
    """
    if HAS_ENHANCED_ML:
        # ML is deprecated; create only heuristic detector info
        analyzer = get_enhanced_analyzer(None)
        return analyzer.get_detector_info()
    else:
        return DetectorInfoResponse(
            enhanced_ml_available=False,
            available_detectors=["heuristic"],
            detector_details={
                "heuristic": {
                    "name": "Heuristic Scoring Detector",
                    "type": "heuristic",
                    "available": True
                }
            }
        )

@app.post("/analyze-code", response_model=EnhancedAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
        API phân tích code với enhanced ML features
        
        Workflow:
        1. Kiểm tra đầu vào
        2. Trích xuất các features (nếu enhanced=True)
        3. Chạy kiểm tra đầu vào bằng detector đã chọn
        4. Trả về kết quả chi tiết với các metrics
    """
    try:
        # NOTE: Kiểm tra đầu vào
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="Code không được để trống")
        
        if request.language not in ["c", "cpp"]:
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ ngôn ngữ C và C++")
        
        if request.enhanced_analysis and HAS_ENHANCED_ML:
            result = analyze_code_with_enhanced_ml(
                code=request.code,
                language=request.language,
                filename=request.filename,
                detector_type=request.detector_type,
                model_path=None
            )
            
            # Trả đúng định dạng
            response = EnhancedAnalysisResponse(
                basic_features=BasicCodeFeatures(**result['basic_features']),
                enhanced_features=EnhancedFeatures(**result['enhanced_features']) if result['enhanced_features'] else None,
                detection=DetectionResult(**result['detection']),
                performance=PerformanceMetrics(**result['performance']),
                meta=AnalysisMetadata(**result['meta'])
            )
            
            return response
        
        # NOTE: Fallback to basic analysis
        else:
            # NOTE: Sử dụng phân tích cơ bản (fallback nội bộ)
            features_dict = basic_analyze_code_features(request.code)
            
            # NOTE: Chuyển đổi sang định dạng cơ bản
            basic_features = BasicCodeFeatures(
                loc=features_dict.get("loc", 0),
                token_count=features_dict.get("token_count"),
                cyclomatic_complexity=features_dict.get("cyclomatic_complexity"),
                functions=features_dict.get("functions"),
                comment_ratio=features_dict.get("comment_ratio", 0),
                blank_ratio=features_dict.get("blank_ratio", 0)
            )
            
            detection_dict = basic_detect_ai_code(request.code, features_dict)
            
            detection = DetectionResult(**detection_dict)
            
            performance = PerformanceMetrics(
                feature_extraction_time=0.001,
                detection_time=0.001,
                total_time=0.002
            )
            
            meta = AnalysisMetadata(
                enhanced_analysis=False,
                detector_type="heuristic",
                available_detectors=["heuristic"],
                feature_count=len(features_dict),
                fallback_reason="Enhanced ML not available or disabled"
            )
            
            return EnhancedAnalysisResponse(
                basic_features=basic_features,
                enhanced_features=None,
                detection=detection,
                performance=performance,
                meta=meta
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")

@app.post("/analyze-code/file")
async def analyze_code_file(file: UploadFile = File(...), 
                           detector_type: str = "heuristic",
                           enhanced_analysis: bool = True):
    """
        API phân tích code từ file upload
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename không hợp lệ")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in [".c", ".cpp", ".h", ".hpp"]:
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file C/C++ (.c, .cpp, .h, .hpp)")
        
        content = await file.read()
        try:
            code = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File không thể đọc được (encoding issue)")
        
        language = "cpp" if file_ext in [".cpp", ".hpp"] else "c"
        
        request = CodeAnalysisRequest(
            code=code,
            language=language,
            filename=file.filename,
            detector_type=detector_type,
            enhanced_analysis=enhanced_analysis
        )
        
        return await analyze_code(request)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý file: {str(e)}")

@app.post("/analyze-code/batch")
async def analyze_code_batch(requests: List[CodeAnalysisRequest]):
    """
        API phân tích batch nhiều code samples
    """
    if len(requests) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 samples per batch")
    
    results = []
    
    for i, request in enumerate(requests):
        try:
            result = await analyze_code(request)
            results.append({
                "index": i,
                "result": result,
                "status": "success"
            })
        except Exception as e:
            results.append({
                "index": i,
                "error": str(e),
                "status": "failed"
            })
    
    return {
        "batch_results": results,
        "total_samples": len(requests),
        "successful": len([r for r in results if r["status"] == "success"]),
        "failed": len([r for r in results if r["status"] == "failed"])
    }

@app.post("/submit-feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
        API thu thập feedback
    """
    try:
        feedback_data = {
            "timestamp": time.time(),
            "code_hash": hash(feedback.code),
            "predicted_label": feedback.predicted_label,
            "actual_label": feedback.actual_label,
            "feedback_notes": feedback.feedback_notes,
            "code_length": len(feedback.code)
        }
        
        # TODO: Lưu feedback vào database hoặc file để training
        print({feedback_data})
        
        return {
            "message": "Feedback đã được ghi nhận",
            "status": "success",
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi lưu feedback: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)