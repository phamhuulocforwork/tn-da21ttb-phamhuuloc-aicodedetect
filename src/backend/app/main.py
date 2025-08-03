from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
import time
import tempfile
import os
import sys
from pathlib import Path

# Import ML integration modules
try:
    from .enhanced_ml_integration import analyze_code_with_enhanced_ml, get_enhanced_analyzer
    from .ml_integration import analyze_code_features, detect_ai_code, code_analyzer
    HAS_ENHANCED_ML = True
except ImportError:
    # Fallback if running as script or enhanced ML not available
    try:
        from enhanced_ml_integration import analyze_code_with_enhanced_ml, get_enhanced_analyzer
        from ml_integration import analyze_code_features, detect_ai_code, code_analyzer
        HAS_ENHANCED_ML = True
    except ImportError:
        from ml_integration import analyze_code_features, detect_ai_code, code_analyzer
        HAS_ENHANCED_ML = False
        print("Enhanced ML not available - using basic analysis")

app = FastAPI(
    title="AI Code Detection API",
    description="API for detecting AI-generated code vs Human-written code with enhanced ML features",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FIXME: Cấu hình cho production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Source code để phân tích")
    language: str = Field(default="cpp", description="Ngôn ngữ lập trình (c, cpp)")
    filename: Optional[str] = Field(default=None, description="Tên file (tùy chọn)")
    detector_type: str = Field(default="hybrid", description="Loại detector: rule, ml, hybrid")
    enhanced_analysis: bool = Field(default=True, description="Sử dụng enhanced analysis")

class BasicCodeFeatures(BaseModel):
    loc: float = Field(description="Lines of Code")
    token_count: Optional[float] = Field(description="Số lượng token")
    cyclomatic_complexity: Optional[float] = Field(description="Độ phức tạp cyclomatic trung bình")
    functions: Optional[int] = Field(description="Số lượng hàm")
    comment_ratio: Optional[float] = Field(description="Tỷ lệ comment")
    blank_ratio: Optional[float] = Field(description="Tỷ lệ dòng trống")

class EnhancedFeatures(BaseModel):
    ast_features: Optional[Dict] = Field(description="AST analysis features")
    redundancy_features: Optional[Dict] = Field(description="Code redundancy features")
    naming_patterns: Optional[Dict] = Field(description="Naming pattern features")
    complexity_features: Optional[Dict] = Field(description="Advanced complexity features")
    ai_patterns: Optional[Dict] = Field(description="AI-specific pattern features")

class DetectionResult(BaseModel):
    prediction: str = Field(description="AI-generated, Human-written, or Uncertain")
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

# Global variables for tracking
start_time = time.time()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Kiểm tra trạng thái hoạt động của backend API
    """
    ml_available = hasattr(code_analyzer, 'has_advanced_features') and code_analyzer.has_advanced_features if 'code_analyzer' in globals() else False
    
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
    """
    Root endpoint - chuyển hướng đến health check
    """
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
    Lấy thông tin về các detector có sẵn
    """
    if HAS_ENHANCED_ML:
        analyzer = get_enhanced_analyzer()
        return analyzer.get_detector_info()
    else:
        return DetectorInfoResponse(
            enhanced_ml_available=False,
            available_detectors=["basic-rule"],
            detector_details={
                "basic-rule": {
                    "name": "Basic Rule-based Detector",
                    "type": "rule",
                    "available": True
                }
            }
        )

@app.post("/analyze-code", response_model=EnhancedAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Phân tích code với enhanced ML features
    
    Workflow:
    1. Validate input
    2. Extract comprehensive features (nếu enhanced=True)
    3. Run detection với specified detector
    4. Return detailed results với performance metrics
    """
    try:
        # Validate input
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="Code không được để trống")
        
        if request.language not in ["c", "cpp"]:
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ ngôn ngữ C và C++")
        
        # Enhanced analysis
        if request.enhanced_analysis and HAS_ENHANCED_ML:
            result = analyze_code_with_enhanced_ml(
                code=request.code,
                language=request.language,
                filename=request.filename,
                detector_type=request.detector_type
            )
            
            # Convert to response format
            response = EnhancedAnalysisResponse(
                basic_features=BasicCodeFeatures(**result['basic_features']),
                enhanced_features=EnhancedFeatures(**result['enhanced_features']) if result['enhanced_features'] else None,
                detection=DetectionResult(**result['detection']),
                performance=PerformanceMetrics(**result['performance']),
                meta=AnalysisMetadata(**result['meta'])
            )
            
            return response
        
        # Fallback to basic analysis
        else:
            # Use existing basic analysis
            features_dict = analyze_code_features(request.code, request.language, request.filename)
            
            # Convert to basic features
            basic_features = BasicCodeFeatures(
                loc=features_dict.get("loc", 0),
                token_count=features_dict.get("token_count"),
                cyclomatic_complexity=features_dict.get("cyclomatic_avg"),
                functions=features_dict.get("functions"),
                comment_ratio=features_dict.get("comment_ratio", 0),
                blank_ratio=features_dict.get("blank_ratio", 0)
            )
            
            # Run basic detection
            prediction, confidence, reasoning = detect_ai_code(request.code, features_dict)
            
            detection = DetectionResult(
                prediction=prediction,
                confidence=confidence,
                reasoning=reasoning,
                method_used="basic-rule"
            )
            
            performance = PerformanceMetrics(
                feature_extraction_time=0.001,
                detection_time=0.001,
                total_time=0.002
            )
            
            meta = AnalysisMetadata(
                enhanced_analysis=False,
                detector_type="basic-rule",
                available_detectors=["basic-rule"],
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
                           detector_type: str = "hybrid",
                           enhanced_analysis: bool = True):
    """
    Phân tích code từ file upload
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename không hợp lệ")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in [".c", ".cpp", ".h", ".hpp"]:
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file C/C++ (.c, .cpp, .h, .hpp)")
        
        # Read file content
        content = await file.read()
        try:
            code = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File không thể đọc được (encoding issue)")
        
        # Determine language from extension
        language = "cpp" if file_ext in [".cpp", ".hpp"] else "c"
        
        # Create analysis request
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
    Phân tích batch nhiều code samples
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

@app.post("/benchmark-detectors")
async def benchmark_detectors(request: CodeAnalysisRequest):
    """
    Benchmark tất cả detectors trên code sample
    """
    if not HAS_ENHANCED_ML:
        raise HTTPException(status_code=501, detail="Enhanced ML required for benchmarking")
    
    try:
        analyzer = get_enhanced_analyzer()
        benchmark_results = analyzer.benchmark_detectors(request.code, request.language)
        
        return {
            "benchmark_results": benchmark_results,
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark failed: {str(e)}")

@app.post("/submit-feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Thu thập feedback từ giảng viên để cải thiện model
    """
    try:
        # TODO: Lưu feedback vào database hoặc file để training
        feedback_data = {
            "timestamp": time.time(),
            "code_hash": hash(feedback.code),
            "predicted_label": feedback.predicted_label,
            "actual_label": feedback.actual_label,
            "feedback_notes": feedback.feedback_notes,
            "code_length": len(feedback.code)
        }
        
        # Tạm thời log feedback (sau này có thể lưu vào DB)
        print(f"📝 Feedback received: {feedback_data}")
        
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