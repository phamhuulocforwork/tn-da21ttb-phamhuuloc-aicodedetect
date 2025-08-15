#!/usr/bin/env python3
"""
AI Code Detection Backend API
Main FastAPI application with analysis endpoints
"""

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

# Import baseline loader for dynamic stats management
try:
    from baseline_loader import get_baseline_loader, reload_baseline_stats
    BASELINE_LOADER_AVAILABLE = True
except ImportError:
    BASELINE_LOADER_AVAILABLE = False
    print("Warning: baseline_loader not available")

# Add the ML pipeline to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir.parent.parent / "src"
sys.path.insert(0, str(src_dir))

# Import analysis modules
try:
    from features.advanced_features import AdvancedFeatureExtractor, ComprehensiveFeatures
    from features.ast_analyzer import CppASTAnalyzer, ASTFeatures
    from features.human_style_analyzer import HumanStyleAnalyzer, HumanStyleFeatures
    from features.detection_models import create_detector
    ANALYSIS_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import analysis modules: {e}")
    ANALYSIS_MODULES_AVAILABLE = False
    # Create dummy classes for development
    class AdvancedFeatureExtractor:
        def extract_all_features(self, code: str, filename: str = "") -> Dict:
            return {"error": "Analysis modules not available"}
    
    class CppASTAnalyzer:
        def analyze_code(self, code: str, filename: str = "") -> Dict:
            return {"error": "AST analyzer not available"}
    
    class HumanStyleAnalyzer:
        def analyze_code(self, code: str, filename: str = "") -> Dict:
            return {"error": "Human style analyzer not available"}

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Detection API",
    description="API for analyzing code to detect AI-generated vs human-written patterns",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Initialize analysis modules
if ANALYSIS_MODULES_AVAILABLE:
    advanced_extractor = AdvancedFeatureExtractor()
    ast_analyzer = CppASTAnalyzer()
    human_style_analyzer = HumanStyleAnalyzer()
    # Use enhanced detection model by default
    detection_model = create_detector("enhanced")
else:
    advanced_extractor = AdvancedFeatureExtractor()
    ast_analyzer = CppASTAnalyzer()
    human_style_analyzer = HumanStyleAnalyzer()
    detection_model = None

# Pydantic models
class CodeAnalysisRequest(BaseModel):
    """Request model for code analysis"""
    code: str = Field(..., min_length=1, max_length=50000, description="Source code to analyze")
    filename: Optional[str] = Field("code.c", description="Filename for context")
    language: str = Field("c", description="Programming language")
    
    @validator('code')
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError("Code cannot be empty")
        return v
    
    @validator('language')
    def validate_language(cls, v):
        supported_languages = ["c", "cpp", "c++"]
        if v.lower() not in supported_languages:
            raise ValueError(f"Language must be one of: {supported_languages}")
        return v.lower()

class FeatureInfo(BaseModel):
    """Individual feature information"""
    name: str
    value: float
    normalized: bool
    interpretation: str
    weight: float = 1.0

class FeatureGroup(BaseModel):
    """Group of related features"""
    group_name: str
    description: str
    features: List[FeatureInfo]
    group_score: float
    visualization_type: str  # 'bar', 'radar', 'boxplot', 'line'

class AssessmentResult(BaseModel):
    """Overall assessment result"""
    overall_score: float = Field(..., ge=0, le=1, description="0=human-like, 1=AI-like")
    confidence: float = Field(..., ge=0, le=1, description="Confidence level")
    key_indicators: List[str]
    summary: str

class CodeInfo(BaseModel):
    """Basic code information"""
    filename: str
    language: str
    loc: int
    file_size: int

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    success: bool
    analysis_id: str
    timestamp: str
    code_info: CodeInfo
    feature_groups: Dict[str, FeatureGroup]
    assessment: AssessmentResult
    raw_features: Optional[Dict[str, float]] = None

# Helper functions
def generate_analysis_id() -> str:
    """Generate unique analysis ID"""
    return f"analysis_{uuid.uuid4().hex[:12]}"

def calculate_file_size(code: str) -> int:
    """Calculate code size in bytes"""
    return len(code.encode('utf-8'))

def interpret_feature(feature_name: str, value: float, normalized: bool = True) -> str:
    """Generate interpretation for a feature value"""
    interpretations = {
        # Structure metrics
        "loc": f"{'Small' if value < 50 else 'Medium' if value < 200 else 'Large'} codebase ({value} lines)",
        "nodes_per_loc": f"{'Simple' if value < 2 else 'Complex'} AST structure ({value:.2f} nodes/line)",
        "max_depth": f"{'Shallow' if value < 5 else 'Deep'} nesting ({value} levels)",
        "cyclomatic_complexity": f"{'Low' if value < 5 else 'Medium' if value < 15 else 'High'} complexity ({value:.1f})",
        
        # Style metrics  
        "spacing_issues_ratio": f"{'Good' if value < 0.1 else 'Poor'} spacing consistency ({value:.1%} issues)",
        "indentation_issues_ratio": f"{'Consistent' if value < 0.1 else 'Inconsistent'} indentation ({value:.1%} issues)",
        "naming_inconsistency_ratio": f"{'Consistent' if value < 0.2 else 'Inconsistent'} naming ({value:.1%} issues)",
        
        # AI detection metrics
        "template_usage_score": f"{'Low' if value < 0.1 else 'High'} template usage ({value:.1%})",
        "boilerplate_ratio": f"{value:.1%} boilerplate code",
        "error_handling_score": f"{'Minimal' if value < 0.05 else 'Extensive'} error handling ({value:.1%})",
    }
    
    return interpretations.get(feature_name, f"Value: {value:.3f}")

def create_feature_groups(features_dict: Dict[str, float]) -> Dict[str, FeatureGroup]:
    """Group features into logical categories for visualization"""
    
    # Define feature groupings
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
                features.append(FeatureInfo(
                    name=fname,
                    value=value,
                    normalized=True,  # Most features are normalized
                    interpretation=interpret_feature(fname, value),
                    weight=1.0
                ))
                group_values.append(value)
        
        # Calculate group score (mean of available features, normalized to [0, 1])
        group_score = sum(group_values) / len(group_values) if group_values else 0.0
        group_score = max(0.0, min(1.0, group_score))  # Normalize to [0, 1] range
        
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
            "Code structure, complexity and control flow analysis",
            structure_features,
            "bar"
        ),
        "style_metrics": create_group(
            "Style Metrics", 
            "Coding style, formatting and human-like patterns",
            style_features,
            "radar"
        ),
        "complexity_metrics": create_group(
            "Complexity Metrics",
            "Code complexity, maintainability and cognitive load",
            complexity_features,
            "line"
        ),
        "ai_detection_metrics": create_group(
            "AI Detection Metrics",
            "Patterns typically associated with AI-generated code",
            ai_detection_features,
            "boxplot"
        )
    }

def calculate_assessment(feature_groups: Dict[str, FeatureGroup], raw_features: Dict[str, float] = None) -> AssessmentResult:
    """Calculate overall assessment using advanced detection model"""
    
    # Use detection model if available and we have raw features
    if ANALYSIS_MODULES_AVAILABLE and detection_model and raw_features:
        try:
            detection_result = detection_model.detect(raw_features)
            
            # Convert detection result to assessment format
            if detection_result.prediction == "AI-generated":
                overall_score = detection_result.confidence
            elif detection_result.prediction == "Human-written":
                overall_score = 1.0 - detection_result.confidence
            else:  # Uncertain
                overall_score = 0.5
            
            # Extract key indicators from reasoning
            key_indicators = []
            for reason in detection_result.reasoning[:4]:  # Top 4 reasons
                if "→ AI" in reason:
                    key_indicators.append(f"AI pattern: {reason.split(':')[0]}")
                elif "→ Human" in reason:
                    key_indicators.append(f"Human pattern: {reason.split(':')[0]}")
            
            # Add confidence-based indicators
            if detection_result.confidence > 0.8:
                key_indicators.append("High confidence prediction")
            elif detection_result.confidence < 0.6:
                key_indicators.append("Low confidence - mixed patterns")
            
            # Generate summary based on prediction
            if detection_result.prediction == "AI-generated":
                if detection_result.confidence > 0.8:
                    summary = f"Strong AI patterns detected with {detection_result.confidence:.1%} confidence"
                else:
                    summary = f"Likely AI-generated with {detection_result.confidence:.1%} confidence"
            elif detection_result.prediction == "Human-written":
                if detection_result.confidence > 0.8:
                    summary = f"Strong human patterns detected with {detection_result.confidence:.1%} confidence"
                else:
                    summary = f"Likely human-written with {detection_result.confidence:.1%} confidence"
            else:
                summary = "Mixed characteristics - manual review recommended"
            
            return AssessmentResult(
                overall_score=round(overall_score, 3),
                confidence=round(detection_result.confidence, 3),
                key_indicators=key_indicators if key_indicators else ["Analysis completed successfully"],
                summary=summary
            )
            
        except Exception as e:
            print(f"Detection model error: {e}")
            # Fall back to old method
    
    # Fallback to old assessment method
    weights = {
        "structure_metrics": 0.2,
        "style_metrics": 0.4,      # Human style is very important
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
            
            # Add key indicators based on significant scores
            if group_name == "style_metrics" and group.group_score > 0.3:
                key_indicators.append("High human-style inconsistencies detected")
            elif group_name == "ai_detection_metrics" and group.group_score > 0.4:
                key_indicators.append("AI-typical patterns found")
            elif group_name == "complexity_metrics" and group.group_score < 0.2:
                key_indicators.append("Unusually simple structure")
    
    # Normalize score and clamp to [0, 1] range
    overall_score = weighted_score / total_weight if total_weight > 0 else 0.5
    overall_score = max(0.0, min(1.0, overall_score))  # Clamp to [0, 1]
    
    # Calculate confidence based on feature availability and consistency
    confidence = min(0.9, total_weight)  # Higher confidence with more features
    
    # Generate summary
    if overall_score < 0.3:
        summary = "Code shows strong human-like characteristics with natural inconsistencies"
    elif overall_score < 0.6:
        summary = "Code shows mixed characteristics, manual review recommended"
    else:
        summary = "Code shows patterns commonly associated with AI generation"
    
    if not key_indicators:
        key_indicators = ["Analysis completed successfully"]
    
    return AssessmentResult(
        overall_score=overall_score,
        confidence=confidence,
        key_indicators=key_indicators,
        summary=summary
    )

# API Routes

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Code Detection API",
        "status": "running",
        "version": "1.0.0",
        "analysis_modules": ANALYSIS_MODULES_AVAILABLE
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "advanced_features": ANALYSIS_MODULES_AVAILABLE,
            "ast_analyzer": ANALYSIS_MODULES_AVAILABLE,
            "human_style_analyzer": ANALYSIS_MODULES_AVAILABLE
        }
    }

@app.post("/api/analysis/combined-analysis", response_model=AnalysisResponse)
async def analyze_code_combined(request: CodeAnalysisRequest):
    """
    Comprehensive code analysis using all available methods
    Returns complete feature analysis with grouped results
    """
    try:
        if not ANALYSIS_MODULES_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Analysis modules not available. Please check server configuration."
            )
        
        # Generate analysis metadata
        analysis_id = generate_analysis_id()
        timestamp = datetime.now().isoformat()
        
        # Perform comprehensive analysis
        features = advanced_extractor.extract_all_features(request.code, request.filename)
        
        # Convert to dictionary if needed
        if hasattr(features, 'to_dict'):
            features_dict = features.to_dict()
        else:
            features_dict = features
        
        # Create code info
        code_info = CodeInfo(
            filename=request.filename,
            language=request.language,
            loc=features_dict.get('loc', len(request.code.splitlines())),
            file_size=calculate_file_size(request.code)
        )
        
        # Group features for visualization
        feature_groups = create_feature_groups(features_dict)
        
        # Calculate overall assessment
        assessment = calculate_assessment(feature_groups, features_dict)
        
        # Build response
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
        # Log the error (in production, use proper logging)
        print(f"Analysis error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/api/analysis/ast-analysis")
async def analyze_ast_only(request: CodeAnalysisRequest):
    """
    AST-only analysis endpoint
    Returns structure, control flow, functions, and naming features
    """
    try:
        if not ANALYSIS_MODULES_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Analysis modules not available"
            )
        
        analysis_id = generate_analysis_id()
        timestamp = datetime.now().isoformat()
        
        # Perform AST analysis only
        ast_features = ast_analyzer.analyze_code(request.code, request.filename)
        
        # Convert to dict if needed
        if hasattr(ast_features, '__dict__'):
            features_dict = ast_features.__dict__
        else:
            features_dict = ast_features
        
        # Create simplified response for single analysis type
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
            "summary": f"AST analysis completed with {len(features_dict)} features extracted"
        }
        
        return response
        
    except Exception as e:
        print(f"AST analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AST analysis failed: {str(e)}")

@app.post("/api/analysis/human-style")  
async def analyze_human_style_only(request: CodeAnalysisRequest):
    """
    Human style analysis endpoint
    Returns spacing, indentation, naming inconsistency, and formatting features
    """
    try:
        if not ANALYSIS_MODULES_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Analysis modules not available"
            )
        
        analysis_id = generate_analysis_id()
        timestamp = datetime.now().isoformat()
        
        # Perform human style analysis only
        style_features = human_style_analyzer.analyze_code(request.code, request.filename)
        
        # Convert to dict
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
            "summary": f"Human style analysis completed with {len(features_dict)} features extracted"
        }
        
        return response
        
    except Exception as e:
        print(f"Human style analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Human style analysis failed: {str(e)}")

@app.post("/api/analysis/advanced-features")
async def analyze_advanced_features_only(request: CodeAnalysisRequest):
    """
    Advanced features analysis endpoint  
    Returns redundancy, complexity, and AI patterns features (excluding AST and human style)
    """
    try:
        if not ANALYSIS_MODULES_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="Analysis modules not available"
            )
        
        analysis_id = generate_analysis_id()
        timestamp = datetime.now().isoformat()
        
        # Get comprehensive features but filter for advanced only
        all_features = advanced_extractor.extract_all_features(request.code, request.filename)
        
        if hasattr(all_features, 'to_dict'):
            all_features_dict = all_features.to_dict()
        else:
            all_features_dict = all_features
        
        # Filter for advanced features only (exclude AST and human style features)
        advanced_feature_prefixes = [
            'redundancy_', 'complexity_', 'ai_pattern_', 'naming_', 
            'halstead', 'cognitive', 'maintainability', 'copy_paste'
        ]
        
        advanced_features = {}
        for key, value in all_features_dict.items():
            if any(key.startswith(prefix) for prefix in advanced_feature_prefixes):
                advanced_features[key] = value
            # Also include some basic metrics
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
            "summary": f"Advanced features analysis completed with {len(advanced_features)} features extracted"
        }
        
        return response
        
    except Exception as e:
        print(f"Advanced features analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Advanced features analysis failed: {str(e)}")

@app.post("/api/analysis/upload-file")
async def analyze_uploaded_file(
    file: UploadFile = File(...),
    analysis_type: str = Form("combined"),
    language: str = Form("c")
):
    """
    File upload endpoint for code analysis
    Supports .c, .cpp, .txt files up to 1MB
    """
    try:
        # Validate file size (1MB = 1024*1024 bytes)
        MAX_FILE_SIZE = 1024 * 1024
        
        # Read file content
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB"
            )
        
        # Validate file extension
        allowed_extensions = ['.c', '.cpp', '.cc', '.cxx', '.txt']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Decode content
        try:
            code_content = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File must be valid UTF-8 encoded text"
            )
        
        # Validate content
        if not code_content.strip():
            raise HTTPException(
                status_code=400,
                detail="File cannot be empty"
            )
        
        # Create analysis request
        analysis_request = CodeAnalysisRequest(
            code=code_content,
            filename=file.filename,
            language=language
        )
        
        # Route to appropriate analysis endpoint based on type
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
                detail="Invalid analysis_type. Must be: combined, ast, human-style, or advanced"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"File upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"File analysis failed: {str(e)}"
        )

@app.get("/api/analysis/methods")
async def get_analysis_methods():
    """
    Get available analysis methods and their descriptions
    """
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
    """
    Get baseline statistics summary
    """
    if not BASELINE_LOADER_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Baseline loader not available"
        )
    
    try:
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
            detail=f"Failed to get baseline stats: {str(e)}"
        )

@app.post("/api/baseline/reload")
async def reload_baseline():
    """
    Reload baseline statistics from feature_stats.json
    """
    if not BASELINE_LOADER_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Baseline loader not available"
        )
    
    try:
        reload_baseline_stats()
        
        # Reinitialize detection model with new stats
        global detection_model
        if ANALYSIS_MODULES_AVAILABLE:
            detection_model = create_detector("enhanced")
        
        return {
            "success": True,
            "message": "Baseline statistics reloaded successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reload baseline stats: {str(e)}"
        )

@app.get("/api/baseline/critical-features")
async def get_critical_features():
    """
    Get critical features identified from baseline analysis
    """
    if not BASELINE_LOADER_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Baseline loader not available"
        )
    
    try:
        baseline_loader = get_baseline_loader()
        critical_features = baseline_loader.get_critical_features()
        
        # Format for frontend display
        formatted_features = []
        for feature_name, config in critical_features.items():
            formatted_features.append({
                "name": feature_name,
                "weight": config["weight"],
                "ai_favored": config["ai_better"],
                "effect_size": config.get("effect_size", 0),
                "description": _get_feature_description(feature_name)
            })
        
        # Sort by weight (most important first)
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
            detail=f"Failed to get critical features: {str(e)}"
        )

def _get_feature_description(feature_name: str) -> str:
    """Get human-readable description for feature"""
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
    return descriptions.get(feature_name, f"Feature: {feature_name}")

@app.post("/api/analysis/test-sample")
async def test_sample_analysis(
    sample_name: str = Form(...),
    expected_result: str = Form(...)  # "ai" or "human"
):
    """
    Test analysis with a known sample for validation
    """
    try:
        # For now, we'll use the test.cpp content provided by user
        test_code = '''#include <stdio.h>
#include <stdlib.h>

// Hàm tính tổng số chẵn trên đường chéo chính
int tongChanCheoChinh(int *arr, int m) {
    int sum = 0;
    for (int i = 0; i < m; i++) {
        int val = *(arr + i * m + i); // a[i][i] qua con trỏ
        if (val % 2 == 0) {
            sum += val;
        }
    }
    return sum;
}

int main() {
    int m;
    scanf("%d", &m);

    // Cấp phát động mảng m x m
    int *arr = (int *)malloc(m * m * sizeof(int));
    if (arr == NULL) {
        printf("Khong the cap phat bo nho!\n");
        return 1;
    }

    // Nhập mảng
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            scanf("%d", (arr + i * m + j));
        }
    }

    // Gọi hàm và in kết quả
    int result = tongChanCheoChinh(arr, m);
    printf("%d\n", result);

    // Giải phóng bộ nhớ
    free(arr);
    return 0;
}'''
        
        # Create analysis request
        analysis_request = CodeAnalysisRequest(
            code=test_code,
            filename=f"{sample_name}.c",
            language="c"
        )
        
        # Run analysis
        analysis_result = await analyze_code_combined(analysis_request)
        
        # Extract prediction info
        prediction = analysis_result.assessment.overall_score
        confidence = analysis_result.assessment.confidence
        
        # Determine predicted class
        if prediction > 0.6:
            predicted_class = "ai"
        elif prediction < 0.4:
            predicted_class = "human"
        else:
            predicted_class = "uncertain"
        
        # Check if prediction matches expected
        correct = predicted_class == expected_result.lower()
        
        return {
            "success": True,
            "sample_name": sample_name,
            "expected_result": expected_result,
            "predicted_class": predicted_class,
            "prediction_score": prediction,
            "confidence": confidence,
            "correct_prediction": correct,
            "analysis_summary": analysis_result.assessment.summary,
            "key_indicators": analysis_result.assessment.key_indicators
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Test analysis failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )