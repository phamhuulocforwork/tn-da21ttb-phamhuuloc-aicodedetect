import os
import sys
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import tempfile

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uvicorn

try:
    from baseline_loader import get_baseline_loader, reload_baseline_stats
    BASELINE_LOADER_AVAILABLE = True
except ImportError as e:
    BASELINE_LOADER_AVAILABLE = False

if BASELINE_LOADER_AVAILABLE:
    try:
        test_loader = get_baseline_loader()
        test_stats = test_loader.get_feature_stats_summary()
    except Exception as e:
        BASELINE_LOADER_AVAILABLE = False

current_dir = Path(__file__).parent.absolute()
src_dir = current_dir.parent.parent / "src"
sys.path.insert(0, str(src_dir))

try:
    from features.advanced_features import AdvancedFeatureExtractor, ComprehensiveFeatures
    from features.ast_analyzer import CppASTAnalyzer, ASTFeatures
    from features.human_style_analyzer import HumanStyleAnalyzer, HumanStyleFeatures
    from features.detection_models import create_detector
    ANALYSIS_MODULES_AVAILABLE = True
except ImportError as e:
    ANALYSIS_MODULES_AVAILABLE = False
    class AdvancedFeatureExtractor:
        def extract_all_features(self, code: str, filename: str = "") -> Dict:
            return {"error": "Module phân tích không khả dụng"}
    
    class CppASTAnalyzer:
        def analyze_code(self, code: str, filename: str = "") -> Dict:
            return {"error": "AST analyzer không khả dụng"}
    
    class HumanStyleAnalyzer:
        def analyze_code(self, code: str, filename: str = "") -> Dict:
            return {"error": "Human style analyzer không khả dụng"}

app = FastAPI(
    title="API Phân tích phát hiện mã AI",
    description="API để phân tích mã nhằm phát hiện mẫu do AI tạo vs mẫu viết bởi con người",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #FIXME: Tạm thời cho phép tất cả origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

if ANALYSIS_MODULES_AVAILABLE:
    advanced_extractor = AdvancedFeatureExtractor()
    ast_analyzer = CppASTAnalyzer()
    human_style_analyzer = HumanStyleAnalyzer()
    try:
        detection_model = create_detector("enhanced")
    except Exception as e:
        detection_model = create_detector("heuristic")
else:
    advanced_extractor = AdvancedFeatureExtractor()
    ast_analyzer = CppASTAnalyzer()
    human_style_analyzer = HumanStyleAnalyzer()
    detection_model = None

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000, description="Mã nguồn")
    filename: Optional[str] = Field("code.c", description="Tên file")
    language: str = Field("c", description="Ngôn ngữ")
    
    @validator('code')
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError("Mã không thể để trống")
        return v
    
    @validator('language')
    def validate_language(cls, v):
        supported_languages = ["c", "cpp", "c++"]
        if v.lower() not in supported_languages:
            raise ValueError(f"Ngôn ngữ phải là một trong: {supported_languages}")
        return v.lower()

class BaselineComparison(BaseModel): 
    ai_baseline: float
    human_baseline: float
    current_value: float
    deviation_from_ai: float  
    deviation_from_human: float  
    ai_similarity: float  
    human_similarity: float  
    verdict: str  
    confidence: float  
    explanation: str

class FeatureInfo(BaseModel):
    name: str
    value: float
    normalized: bool
    interpretation: str
    weight: float = 1.0
    baseline_comparison: Optional[BaselineComparison] = None

class FeatureGroup(BaseModel):
    group_name: str
    description: str
    features: List[FeatureInfo]
    group_score: float
    visualization_type: str  

class BaselineSummary(BaseModel):
    total_features_compared: int
    ai_like_features: int
    human_like_features: int
    neutral_features: int
    strongest_ai_indicators: List[str]  
    strongest_human_indicators: List[str]  
    overall_ai_similarity: float
    overall_human_similarity: float

class AssessmentResult(BaseModel):
    overall_score: float = Field(..., ge=0, le=1, description="0=giống human, 1=giống AI")
    confidence: float = Field(..., ge=0, le=1, description="Mức độ tin cậy")
    key_indicators: List[str]
    summary: str
    baseline_summary: Optional[BaselineSummary] = None

class CodeInfo(BaseModel):
    filename: str
    language: str
    loc: int
    file_size: int

class AnalysisResponse(BaseModel):
    success: bool
    analysis_id: str
    timestamp: str
    code_info: CodeInfo
    feature_groups: Dict[str, FeatureGroup]
    assessment: AssessmentResult
    raw_features: Optional[Dict[str, float]] = None


def generate_analysis_id() -> str:
    return f"analysis_{uuid.uuid4().hex[:12]}"

def calculate_file_size(code: str) -> int:
    return len(code.encode('utf-8'))

def calculate_baseline_comparison(feature_name: str, current_value: float) -> Optional[BaselineComparison]:
    try:
        from baseline_loader import get_baseline_loader
        baseline_loader = get_baseline_loader()
        baseline_stats = baseline_loader.get_baseline_stats()
        baseline = baseline_stats.get_feature_baseline(feature_name)
        if not baseline:
            available_features = list(baseline_stats.ai_stats.keys())[:10]
            return None
            
        ai_baseline, human_baseline = baseline
        
        baseline_range = abs(ai_baseline - human_baseline)
        if baseline_range == 0:
            return None
        ai_distance = abs(current_value - ai_baseline)
        human_distance = abs(current_value - human_baseline)
        ai_distance_norm = min(ai_distance / baseline_range, 2.0) if baseline_range > 0 else 0
        human_distance_norm = min(human_distance / baseline_range, 2.0) if baseline_range > 0 else 0
        
        ai_similarity = max(0, 1.0 - ai_distance_norm)
        human_similarity = max(0, 1.0 - human_distance_norm)
        if ai_baseline < human_baseline:
            deviation_from_ai = (current_value - ai_baseline) / baseline_range
            deviation_from_human = (current_value - human_baseline) / baseline_range
        else:
            deviation_from_ai = (ai_baseline - current_value) / baseline_range
            deviation_from_human = (human_baseline - current_value) / baseline_range
        deviation_from_ai = max(-2.0, min(2.0, deviation_from_ai))
        deviation_from_human = max(-2.0, min(2.0, deviation_from_human))
        if ai_similarity > human_similarity + 0.1:
            verdict = "ai-like"
            confidence = min(0.95, ai_similarity)
        elif human_similarity > ai_similarity + 0.1:
            verdict = "human-like"
            confidence = min(0.95, human_similarity)
        else:
            verdict = "neutral"
            confidence = 0.5
        if verdict == "ai-like":
            explanation = f"Gần baseline AI ({ai_baseline:.3f}) hơn baseline Human ({human_baseline:.3f})"
        elif verdict == "human-like":
            explanation = f"Gần baseline Human ({human_baseline:.3f}) hơn baseline AI ({ai_baseline:.3f})"
        else:
            explanation = f"Nằm giữa baseline AI ({ai_baseline:.3f}) và baseline Human ({human_baseline:.3f})"
        
        return BaselineComparison(
            ai_baseline=ai_baseline,
            human_baseline=human_baseline,
            current_value=current_value,
            deviation_from_ai=deviation_from_ai,
            deviation_from_human=deviation_from_human,
            ai_similarity=ai_similarity,
            human_similarity=human_similarity,
            verdict=verdict,
            confidence=confidence,
            explanation=explanation
        )
        
    except Exception as e:
        print(f"⚠️ Lỗi tính toán so sánh baseline cho {feature_name}: {e}")
        return None

def interpret_feature(feature_name: str, value: float, normalized: bool = True) -> str:
    interpretations = {
        "loc": f"{'Small' if value < 50 else 'Medium' if value < 200 else 'Large'} codebase ({value} lines)",
        "nodes_per_loc": f"{'Simple' if value < 2 else 'Complex'} AST structure ({value:.2f} nodes/line)",
        "max_depth": f"{'Shallow' if value < 5 else 'Deep'} nesting ({value} levels)",
        "cyclomatic_complexity": f"{'Thấp' if value < 5 else 'Trung bình' if value < 15 else 'Cao'} độ phức tạp ({value:.1f})",  
        "spacing_issues_ratio": f"{'Tốt' if value < 0.1 else 'Kém'} tính nhất quán khoảng cách ({value:.1%} lỗi)",
        "indentation_issues_ratio": f"{'Nhất quán' if value < 0.1 else 'Không nhất quán'} thụt lề ({value:.1%} lỗi)",
        "naming_inconsistency_ratio": f"{'Nhất quán' if value < 0.2 else 'Không nhất quán'} đặt tên ({value:.1%} lỗi)",
        "template_usage_score": f"{'Thấp' if value < 0.1 else 'Cao'} sử dụng template ({value:.1%})",
        "boilerplate_ratio": f"{value:.1%} mã boilerplate",
        "error_handling_score": f"{'Tối thiểu' if value < 0.05 else 'Mở rộng'} xử lý lỗi ({value:.1%})",
    }
    
    return interpretations.get(feature_name, f"Giá trị: {value:.3f}")

def create_feature_groups(features_dict: Dict[str, float]) -> Dict[str, FeatureGroup]:
    structure_features = [
        "loc", "nodes_per_loc", "max_depth", "avg_depth", "branching_factor",
        "if_statements_per_loc", "for_loops_per_loc", "while_loops_per_loc",
        "functions_per_loc", "cyclomatic_complexity"
    ]
    
    style_features = [
        "spacing_issues_ratio", "indentation_issues_ratio", "naming_inconsistency_ratio",
        "formatting_issues_ratio", "human_style_overall_score", "indentation_consistency",
        "brace_style_consistency", "operator_spacing_consistency"
    ]
    
    complexity_features = [
        "halstead_complexity", "halstead_per_loc", "cognitive_complexity", 
        "cognitive_per_loc", "maintainability_index", "code_to_comment_ratio",
        "variable_uniqueness_ratio", "avg_function_length"
    ]
    
    ai_detection_features = [
        "template_usage_score", "boilerplate_ratio", "error_handling_score",
        "defensive_programming_score", "over_engineering_score", "copy_paste_score",
        "redundancy_duplicate_line_ratio", "ai_pattern_template_usage_score"
    ]
    
    def create_group(group_name: str, description: str, feature_names: List[str], viz_type: str) -> FeatureGroup:
        features = []
        group_values = []
        
        for fname in feature_names:
            if fname in features_dict:
                value = features_dict[fname]
                
                baseline_comparison = calculate_baseline_comparison(fname, value)
                if baseline_comparison:
                    print(f"✓ So sánh baseline cho {fname}: {baseline_comparison.verdict}")
                else:
                    print(f"❌ Không có so sánh baseline cho {fname}")
                
                features.append(FeatureInfo(
                    name=fname,
                    value=value,
                    normalized=True,
                    interpretation=interpret_feature(fname, value),
                    weight=1.0,
                    baseline_comparison=baseline_comparison
                ))
                group_values.append(value)
        
        group_score = sum(group_values) / len(group_values) if group_values else 0.0
        group_score = max(0.0, min(1.0, group_score))
        
        return FeatureGroup(
            group_name=group_name,
            description=description,
            features=features,
            group_score=group_score,
            visualization_type=viz_type
        )
    
    return {
        "structure_metrics": create_group(
            "Structure Metrics",
            "Cấu trúc mã, độ phức tạp và phân tích luồng điều khiển",
            structure_features,
            "bar"
        ),
        "style_metrics": create_group(
            "Style Metrics", 
            "Phong cách mã, định dạng và mẫu giống human",
            style_features,
            "radar"
        ),
        "complexity_metrics": create_group(
            "Complexity Metrics",
            "Độ phức tạp mã, khả năng bảo trì và tải nhận thức",
            complexity_features,
            "line"
        ),
        "ai_detection_metrics": create_group(
            "AI Detection Metrics",
            "Mẫu thường liên quan đến mã do AI tạo",
            ai_detection_features,
            "boxplot"
        )
    }

def calculate_baseline_summary(feature_groups: Dict[str, FeatureGroup]) -> Optional[BaselineSummary]:
    try:
        ai_like_features = []
        human_like_features = []
        neutral_features = []
        ai_similarities = []
        human_similarities = []
        for group in feature_groups.values():
            for feature in group.features:
                if feature.baseline_comparison:
                    comparison = feature.baseline_comparison
                    if comparison.verdict == "ai-like":
                        ai_like_features.append((feature.name, comparison.confidence))
                    elif comparison.verdict == "human-like":
                        human_like_features.append((feature.name, comparison.confidence))
                    else:
                        neutral_features.append(feature.name)
                    ai_similarities.append(comparison.ai_similarity)
                    human_similarities.append(comparison.human_similarity)
        overall_ai_similarity = sum(ai_similarities) / len(ai_similarities) if ai_similarities else 0
        overall_human_similarity = sum(human_similarities) / len(human_similarities) if human_similarities else 0
        ai_like_features.sort(key=lambda x: x[1], reverse=True)
        human_like_features.sort(key=lambda x: x[1], reverse=True)
        
        strongest_ai_indicators = [name for name, _ in ai_like_features[:3]]
        strongest_human_indicators = [name for name, _ in human_like_features[:3]]
        
        return BaselineSummary(
            total_features_compared=len(ai_similarities),
            ai_like_features=len(ai_like_features),
            human_like_features=len(human_like_features),
            neutral_features=len(neutral_features),
            strongest_ai_indicators=strongest_ai_indicators,
            strongest_human_indicators=strongest_human_indicators,
            overall_ai_similarity=round(overall_ai_similarity, 3),
            overall_human_similarity=round(overall_human_similarity, 3)
        )
        
    except Exception as e:
        print(f"Lỗi tính toán tổng quan baseline: {e}")
        return None

def calculate_assessment(feature_groups: Dict[str, FeatureGroup], raw_features: Dict[str, float] = None) -> AssessmentResult:

    if ANALYSIS_MODULES_AVAILABLE and detection_model and raw_features:
        try:
            detection_result = detection_model.detect(raw_features)
            if detection_result.prediction == "AI-generated":
                overall_score = detection_result.confidence
            elif detection_result.prediction == "Human-written":
                overall_score = 1.0 - detection_result.confidence
            else:
                overall_score = 0.5
            key_indicators = []
            for reason in detection_result.reasoning[:4]:
                if "→ AI" in reason:
                    key_indicators.append(f"Mẫu AI: {reason.split(':')[0]}")
                elif "→ Human" in reason:
                    key_indicators.append(f"Mẫu Human: {reason.split(':')[0]}")
            if detection_result.confidence > 0.8:
                key_indicators.append("Dự đoán tin cậy cao")
            elif detection_result.confidence < 0.6:
                key_indicators.append("Tin cậy thấp - mẫu hỗn hợp")
            if detection_result.prediction == "AI-generated":
                if detection_result.confidence > 0.8:
                    summary = f"Phát hiện mẫu AI rõ rệt với độ tin cậy {detection_result.confidence:.1%}"
                else:
                    summary = f"Có thể do AI tạo với độ tin cậy {detection_result.confidence:.1%}"
            elif detection_result.prediction == "Human-written":
                if detection_result.confidence > 0.8:
                    summary = f"Phát hiện mẫu human rõ rệt với độ tin cậy {detection_result.confidence:.1%}"
                else:
                    summary = f"Có thể do human viết với độ tin cậy {detection_result.confidence:.1%}"
            else:
                summary = "Đặc điểm hỗn hợp - cần xem xét thủ công"
            baseline_summary = calculate_baseline_summary(feature_groups)
            
            return AssessmentResult(
                overall_score=round(overall_score, 3),
                confidence=round(detection_result.confidence, 3),
                key_indicators=key_indicators if key_indicators else ["Phân tích hoàn tất thành công"],
                summary=summary,
                baseline_summary=baseline_summary
            )
            
        except Exception as e:
                print(f"Lỗi model phát hiện: {e}")
    weights = {
        "structure_metrics": 0.2,
        "style_metrics": 0.4,
        "complexity_metrics": 0.2,
        "ai_detection_metrics": 0.2
    }
    
    weighted_score = 0.0
    total_weight = 0.0
    key_indicators = []
    
    for group_name, group in feature_groups.items():
        if group_name in weights:
            weight = weights[group_name]
            weighted_score += group.group_score * weight
            total_weight += weight
            if group_name == "style_metrics" and group.group_score > 0.3:
                key_indicators.append("Phát hiện nhiều điểm không nhất quán kiểu human")
            elif group_name == "ai_detection_metrics" and group.group_score > 0.4:
                key_indicators.append("Tìm thấy mẫu đặc trưng AI")
            elif group_name == "complexity_metrics" and group.group_score < 0.2:
                key_indicators.append("Cấu trúc đơn giản bất thường")
    overall_score = weighted_score / total_weight if total_weight > 0 else 0.5
    overall_score = max(0.0, min(1.0, overall_score))
    
    confidence = min(0.9, total_weight)
    if overall_score < 0.3:
        summary = "Mã thể hiện đặc điểm human mạnh mẽ với sự không nhất quán tự nhiên"
    elif overall_score < 0.6:
        summary = "Mã thể hiện đặc điểm hỗn hợp, cần xem xét thủ công"
    else:
        summary = "Mã thể hiện mẫu thường liên quan đến việc AI tạo"
    
    if not key_indicators:
        key_indicators = ["Phân tích hoàn tất thành công"]
    
    baseline_summary = calculate_baseline_summary(feature_groups)
    
    return AssessmentResult(
        overall_score=overall_score,
        confidence=confidence,
        key_indicators=key_indicators,
        summary=summary,
        baseline_summary=baseline_summary
    )

@app.get("/")
async def root():
    return {
        "message": "API Phân tích phát hiện mã AI",
        "status": "đang chạy",
        "version": "1.0.0",
        "analysis_modules": ANALYSIS_MODULES_AVAILABLE
    }

@app.get("/health")
async def health_check():
    return {
        "status": "khỏe mạnh",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "advanced_features": ANALYSIS_MODULES_AVAILABLE,
            "ast_analyzer": ANALYSIS_MODULES_AVAILABLE,
            "human_style_analyzer": ANALYSIS_MODULES_AVAILABLE
        }
    }

@app.post("/api/analysis/combined-analysis", response_model=AnalysisResponse)
async def analyze_code_combined(request: CodeAnalysisRequest):
    try:
        if not ANALYSIS_MODULES_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Module phân tích không khả dụng. Vui lòng kiểm tra cấu hình server."
            )
        
        analysis_id = generate_analysis_id()
        timestamp = datetime.now().isoformat()
        features = advanced_extractor.extract_all_features(request.code, request.filename)
        if hasattr(features, 'to_dict'):
            features_dict = features.to_dict()
        else:
            features_dict = features
        code_info = CodeInfo(
            filename=request.filename,
            language=request.language,
            loc=features_dict.get('loc', len(request.code.splitlines())),
            file_size=calculate_file_size(request.code)
        )
        
        feature_groups = create_feature_groups(features_dict)
        assessment = calculate_assessment(feature_groups, features_dict)
        response = AnalysisResponse(
            success=True,
            analysis_id=analysis_id,
            timestamp=timestamp,
            code_info=code_info,
            feature_groups=feature_groups,
            assessment=assessment,
            raw_features=features_dict
        )
        
        return response
        
    except Exception as e:
        print(f"Lỗi phân tích: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Phân tích thất bại: {str(e)}"
        )

@app.post("/api/analysis/ast-analysis")
async def analyze_ast_only(request: CodeAnalysisRequest):
    try:
        if not ANALYSIS_MODULES_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Module phân tích không khả dụng"
            )
        
        analysis_id = generate_analysis_id()
        timestamp = datetime.now().isoformat()
        ast_features = ast_analyzer.analyze_code(request.code, request.filename)
        if hasattr(ast_features, '__dict__'):
            features_dict = ast_features.__dict__
        else:
            features_dict = ast_features
        response = {
            "success": True,
            "analysis_id": analysis_id,
            "timestamp": timestamp,
            "analysis_type": "ast_only",
            "code_info": {
                "filename": request.filename,
                "language": request.language,
                "loc": features_dict.get('total_nodes', len(request.code.splitlines())),
                "file_size": calculate_file_size(request.code)
            },
            "features": features_dict,
            "summary": f"Phân tích AST hoàn tất với {len(features_dict)} đặc trưng được trích xuất"
        }
        
        return response
        
    except Exception as e:
        print(f"Lỗi phân tích AST: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Phân tích AST thất bại: {str(e)}")

@app.post("/api/analysis/human-style")  
async def analyze_human_style_only(request: CodeAnalysisRequest):
    try:
        if not ANALYSIS_MODULES_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Module phân tích không khả dụng"
            )
        
        analysis_id = generate_analysis_id()
        timestamp = datetime.now().isoformat()
        style_features = human_style_analyzer.analyze_code(request.code, request.filename)
        if hasattr(style_features, 'to_dict'):
            features_dict = style_features.to_dict()
        elif hasattr(style_features, '__dict__'):
            features_dict = style_features.__dict__
        else:
            features_dict = style_features
        
        response = {
            "success": True,
            "analysis_id": analysis_id,
            "timestamp": timestamp,
            "analysis_type": "human_style_only",
            "code_info": {
                "filename": request.filename,
                "language": request.language,
                "loc": len(request.code.splitlines()),
                "file_size": calculate_file_size(request.code)
            },
            "features": features_dict,
            "summary": f"Phân tích phong cách Human hoàn tất với {len(features_dict)} đặc trưng được trích xuất"
        }
        
        return response
        
    except Exception as e:
        print(f"Lỗi phân tích phong cách Human: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Phân tích phong cách Human thất bại: {str(e)}")

@app.post("/api/analysis/advanced-features")
async def analyze_advanced_features_only(request: CodeAnalysisRequest):
    try:
        if not ANALYSIS_MODULES_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Module phân tích không khả dụng"
            )
        
        analysis_id = generate_analysis_id()
        timestamp = datetime.now().isoformat()
        all_features = advanced_extractor.extract_all_features(request.code, request.filename)
        
        if hasattr(all_features, 'to_dict'):
            all_features_dict = all_features.to_dict()
        else:
            all_features_dict = all_features
        advanced_feature_prefixes = [
            'redundancy_', 'complexity_', 'ai_pattern_', 'naming_', 
            'halstead', 'cognitive', 'maintainability', 'copy_paste'
        ]
        
        advanced_features = {}
        for key, value in all_features_dict.items():
            if any(key.startswith(prefix) for prefix in advanced_feature_prefixes):
                advanced_features[key] = value
            elif key in ['loc', 'token_count', 'cyclomatic_complexity', 'functions', 'comment_ratio', 'blank_ratio']:
                advanced_features[key] = value
        
        response = {
            "success": True,
            "analysis_id": analysis_id,
            "timestamp": timestamp,
            "analysis_type": "advanced_features_only",
            "code_info": {
                "filename": request.filename,
                "language": request.language,
                "loc": advanced_features.get('loc', len(request.code.splitlines())),
                "file_size": calculate_file_size(request.code)
            },
            "features": advanced_features,
            "summary": f"Phân tích đặc trưng nâng cao hoàn tất với {len(advanced_features)} đặc trưng được trích xuất"
        }
        
        return response
        
    except Exception as e:
        print(f"Lỗi phân tích đặc trưng nâng cao: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Phân tích tính năng nâng cao thất bại: {str(e)}")

@app.post("/api/analysis/upload-file")
async def analyze_uploaded_file(
    file: UploadFile = File(...),
    analysis_type: str = Form("combined"),
    language: str = Form("c")
):
    try:
        MAX_FILE_SIZE = 1024 * 1024
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File quá lớn. Kích thước tối đa là {MAX_FILE_SIZE/1024/1024}MB"
            )
        
        allowed_extensions = ['.c', '.cpp', '.cc', '.cxx', '.txt']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Định dạng file không được hỗ trợ. Cho phép: {', '.join(allowed_extensions)}"
            )
        

        try:
            code_content = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File phải được mã hóa UTF-8 hợp lệ"
            )
        

        if not code_content.strip():
            raise HTTPException(
                status_code=400,
                detail="File không thể để trống"
            )
        

        analysis_request = CodeAnalysisRequest(
            code=code_content,
            filename=file.filename,
            language=language
        )
        

        if analysis_type == "combined":
            return await analyze_code_combined(analysis_request)
        elif analysis_type == "ast":
            return await analyze_ast_only(analysis_request)
        elif analysis_type == "human-style":
            return await analyze_human_style_only(analysis_request)
        elif analysis_type == "advanced":
            return await analyze_advanced_features_only(analysis_request)
        else:
            raise HTTPException(
                status_code=400,
                detail="Loại phân tích không hợp lệ. Phải là: combined, ast, human-style, hoặc advanced"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Lỗi tải lên file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Phân tích file thất bại: {str(e)}"
        )

@app.get("/api/analysis/methods")
async def get_analysis_methods():
    return {
        "methods": [
            {
                "id": "combined",
                "name": "Combined Analysis",
                "description": "Comprehensive analysis using all available methods (80+ features)",
                "features": ["AST Analysis", "Human Style", "Advanced Features", "AI Detection"],
                "estimated_time": "2-5 seconds"
            },
            {
                "id": "ast",
                "name": "AST Analysis",
                "description": "Code structure, control flow, and naming pattern analysis",
                "features": ["Structure metrics", "Control flow", "Function analysis", "Variable naming"],
                "estimated_time": "1-2 seconds"
            },
            {
                "id": "human-style", 
                "name": "Human Style Analysis",
                "description": "Coding style and human-like inconsistency detection",
                "features": ["Spacing issues", "Indentation consistency", "Naming patterns", "Formatting"],
                "estimated_time": "1-2 seconds"
            },
            {
                "id": "advanced",
                "name": "Advanced Features",
                "description": "Code complexity, redundancy, and AI pattern detection",
                "features": ["Complexity metrics", "Code redundancy", "AI patterns", "Maintainability"],
                "estimated_time": "2-3 seconds"
            }
        ],
        "supported_languages": ["c", "cpp", "c++"],
        "supported_extensions": [".c", ".cpp", ".cc", ".cxx", ".txt"],
        "max_file_size": "1MB",
        "max_code_length": 50000
    }

@app.get("/api/baseline/stats")
async def get_baseline_stats():
    try:
        from baseline_loader import get_baseline_loader
        baseline_loader = get_baseline_loader()
        stats_summary = baseline_loader.get_feature_stats_summary()
        
        return {
            "success": True,
            "baseline_stats": stats_summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Không thể lấy thống kê baseline: {str(e)}"
        )

@app.post("/api/baseline/reload")
async def reload_baseline():
    try:
        from baseline_loader import reload_baseline_stats
        reload_baseline_stats()
        

        global detection_model
        if ANALYSIS_MODULES_AVAILABLE:
            detection_model = create_detector("enhanced")
        
        return {
            "success": True,
            "message": "Thống kê baseline đã được tải lại thành công",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Không thể tải lại thống kê baseline: {str(e)}"
        )

@app.get("/api/baseline/critical-features")
async def get_critical_features():
    try:
        from baseline_loader import get_baseline_loader
        baseline_loader = get_baseline_loader()
        critical_features = baseline_loader.get_critical_features()
        

        formatted_features = []
        for feature_name, config in critical_features.items():
            formatted_features.append({
                "name": feature_name,
                "weight": config["weight"],
                "ai_favored": config["ai_better"],
                "effect_size": config.get("effect_size", 0),
                "description": _get_feature_description(feature_name)
            })
        

        formatted_features.sort(key=lambda x: x["weight"], reverse=True)
        
        return {
            "success": True,
            "critical_features": formatted_features,
            "total_features": len(formatted_features),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Không thể lấy danh sách tính năng quan trọng: {str(e)}"
        )

def _get_feature_description(feature_name: str) -> str:
    descriptions = {
        'comment_ratio': 'Ratio of comment lines to total lines',
        'ast_indentation_consistency': 'Consistency of code indentation',
        'naming_generic_var_ratio': 'Ratio of generic variable names (i, j, temp, etc.)',
        'ast_if_statements_per_loc': 'Number of if statements per line of code',
        'ast_for_loops_per_loc': 'Number of for loops per line of code',
        'cyclomatic_complexity': 'Cyclomatic complexity of the code',
        'human_style_overall_score': 'Overall human-like style score',
        'naming_descriptive_var_ratio': 'Ratio of descriptive variable names',
        'ast_avg_variable_name_length': 'Average length of variable names',
        'blank_ratio': 'Ratio of blank lines to total lines',
        'spacing_spacing_issues_ratio': 'Ratio of spacing inconsistencies'
    }
    return descriptions.get(feature_name, f"Đặc trưng: {feature_name}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )