import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

current_dir = Path(__file__).parent
src_src_path = current_dir.parent.parent / "src"
sys.path.append(str(src_src_path))

from .basic_analysis import basic_analyze_code_features, basic_detect_ai_code

# NOTE: Kiểm tra features và detectors
try:
    from features.advanced_features import AdvancedFeatureExtractor, ComprehensiveFeatures
    from features.detection_models import create_detector, DetectionResult
    HAS_ADVANCED_FEATURES = True
except ImportError as e:
    HAS_ADVANCED_FEATURES = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedMLAnalyzer:
    # NOTE: Phân tích với toàn bộ các feat được trích xuất và các detectors
    # NOTE: Nếu không có features, sẽ fallback về basic analysis

    def __init__(self, model_path: Optional[str] = None):
        self.has_enhanced_features = HAS_ADVANCED_FEATURES
        
        if self.has_enhanced_features:
            self.feature_extractor = AdvancedFeatureExtractor()
            
            self.detectors = {}
            self._initialize_detectors(model_path)
        else:
            logger.warning("Không có công cụ phân tích nâng cao - sử dụng phân tích cơ bản")
    
    def _initialize_detectors(self, model_path: Optional[str] = None):        
        try:
            self.detectors['heuristic'] = create_detector("heuristic")
            logger.info("Sử dụng detector heuristic")
        except Exception as e:
            logger.error(f"Không thể khởi tạo detector heuristic: {e}")
    
    def analyze_code_comprehensive(self, code: str, language: str = "cpp", 
                                 filename: Optional[str] = None,
                                 detector_type: str = "heuristic") -> Dict[str, Any]:
        
        if not self.has_enhanced_features:
            # NOTE: Fallback sử dụng phân tích cơ bản
            return self._basic_analysis_fallback(code, language)
        
        try:
            # NOTE: Trích xuất các features
            start_time = self._get_time()
            features = self.feature_extractor.extract_all_features(code, filename or f"temp.{language}")
            feature_extraction_time = self._get_time() - start_time
            
            # NOTE: Chuyển đổi features sang dict để detection
            feature_dict = features.to_dict()
            
            detection_start = self._get_time()
            detection_result = self._run_detection(feature_dict, detector_type)
            detection_time = self._get_time() - detection_start
            
            response = {
                'basic_features': {
                    'loc': features.loc,
                    'token_count': features.token_count,
                    'cyclomatic_complexity': features.cyclomatic_complexity,
                    'functions': features.functions,
                    'comment_ratio': features.comment_ratio,
                    'blank_ratio': features.blank_ratio
                },
                
                'enhanced_features': {
                    'ast_features': features.ast_features.__dict__ if features.ast_features else None,
                    'redundancy_features': features.redundancy.__dict__ if features.redundancy else None,
                    'naming_patterns': features.naming_patterns.__dict__ if features.naming_patterns else None,
                    'complexity_features': features.complexity.__dict__ if features.complexity else None,
                    'ai_patterns': features.ai_patterns.__dict__ if features.ai_patterns else None
                },
                
                'detection': {
                    'prediction': detection_result.prediction,
                    'confidence': detection_result.confidence,
                    'reasoning': detection_result.reasoning,
                    'method_used': detection_result.method_used
                },
                
                'performance': {
                    'feature_extraction_time': round(feature_extraction_time, 4),
                    'detection_time': round(detection_time, 4),
                    'total_time': round(feature_extraction_time + detection_time, 4)
                },
                
                'meta': {
                    'enhanced_analysis': True,
                    'detector_type': detector_type,
                    'available_detectors': list(self.detectors.keys()),
                    'feature_count': len(feature_dict),
                    'fallback_reason': None
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Phân tích không thành công: {e}")
            return self._basic_analysis_fallback(code, language, error=str(e))
    
    def _run_detection(self, features: Dict[str, Any], detector_type: str) -> DetectionResult:
        # NOTE: Chạy detection với detector đã chọn
        
        detector = self.detectors.get(detector_type)
        
        if not detector:
            # NOTE: Fallback: sử dụng detector heuristic
            if self.detectors:
                detector = self.detectors.get('heuristic') or next(iter(self.detectors.values()))
                logger.warning("Không tồn tại detector này, sử dụng detector mặc định - heuristic")
            else:
                raise ValueError("Không tìm thấy detector nào")
        
        result = detector.detect(features)
        return result
    
    def _basic_analysis_fallback(self, code: str, language: str, error: Optional[str] = None) -> Dict[str, Any]:
        # NOTE: Fallback sử dụng phân tích cơ bản
        basic_features = basic_analyze_code_features(code)
        detection = basic_detect_ai_code(code, basic_features)

        return {
            'basic_features': basic_features,
            'enhanced_features': None,
            'detection': detection,
            'performance': {
                'feature_extraction_time': 0.001,
                'detection_time': 0.001,
                'total_time': 0.002
            },
            'meta': {
                'enhanced_analysis': False,
                'detector_type': 'fallback',
                'available_detectors': [],
                'feature_count': len(basic_features),
                'fallback_reason': error or "Không có công cụ phân tích nâng cao"
            }
        }
    
    def get_detector_info(self) -> Dict[str, Any]:
        # NOTE: Lấy thông tin về các detectors
        
        info = {
            'enhanced_ml_available': self.has_enhanced_features,
            'available_detectors': list(self.detectors.keys()),
            'detector_details': {}
        }
        
        for name, detector in self.detectors.items():
            info['detector_details'][name] = {
                'name': detector.get_name(),
                'type': name,
                'available': True
            }
        
        return info
    
    def run_batch_analysis(self, code_samples: List[Tuple[str, str]], 
                          detector_type: str = "heuristic") -> List[Dict[str, Any]]:
        
        results = []
        
        for code, language in code_samples:
            try:
                result = self.analyze_code_comprehensive(code, language, detector_type=detector_type)
                results.append(result)
            except Exception as e:
                logger.error(f"Lỗi phân tích batch: {e}")
                results.append({
                    'error': str(e),
                    'code_length': len(code),
                    'language': language
                })
        
        return results
    
    def _get_time(self) -> float:
        import time
        return time.time()

# Global instance
enhanced_analyzer = None

def get_enhanced_analyzer(model_path: Optional[str] = None) -> EnhancedMLAnalyzer:
    global enhanced_analyzer
    
    if enhanced_analyzer is None:
        enhanced_analyzer = EnhancedMLAnalyzer(model_path)
    
    return enhanced_analyzer

def analyze_code_with_enhanced_ml(code: str, language: str = "cpp", 
                                filename: Optional[str] = None,
                                detector_type: str = "heuristic",
                                model_path: Optional[str] = None) -> Dict[str, Any]:
    
    analyzer = get_enhanced_analyzer(model_path)
    return analyzer.analyze_code_comprehensive(code, language, filename, detector_type)