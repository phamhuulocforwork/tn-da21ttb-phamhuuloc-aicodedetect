import sys
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import tempfile
import pickle

# NOTE: Thêm src/src vào path để import ML components
current_dir = Path(__file__).parent
src_src_path = current_dir.parent.parent / "src"
sys.path.append(str(src_src_path))

try:
    from features.advanced_features import AdvancedFeatureExtractor, ComprehensiveFeatures
    from features.detection_models import create_detector, DetectionResult
    HAS_ENHANCED_ML = True
    print("✅ Enhanced ML components imported successfully")
except ImportError as e:
    HAS_ENHANCED_ML = False
    print(f"⚠️  Enhanced ML components not available: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedMLAnalyzer:
    # NOTE: Enhanced ML Analyzer với toàn bộ các đặc trưng được trích xuất + các detectors
    
    def __init__(self, model_path: Optional[str] = None):
        self.has_enhanced_features = HAS_ENHANCED_ML
        
        if self.has_enhanced_features:
            self.feature_extractor = AdvancedFeatureExtractor()
            
            self.detectors = {}
            self._initialize_detectors(model_path)
        else:
            logger.warning("Enhanced ML features not available - using basic analysis only")
    
    def _initialize_detectors(self, model_path: Optional[str] = None):        
        try:
            # NOTE: Rule-based detector (luôn sử dụng)
            self.detectors['rule_based'] = create_detector("rule")
            logger.info("✅ Rule-based detector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize rule-based detector: {e}")
        
        try:
            # NOTE: ML detector (nếu có)
            if model_path and Path(model_path).exists():
                self.detectors['ml'] = create_detector("ml", model_path)
                logger.info("✅ ML detector initialized")
            else:
                logger.info("📝 ML detector not available (no trained model)")
        except Exception as e:
            logger.error(f"Failed to initialize ML detector: {e}")
        
        try:
            # NOTE: Sử dụng cả 2 detector rule-based và ml
            hybrid_model_path = model_path if model_path and Path(model_path).exists() else None
            self.detectors['hybrid'] = create_detector("hybrid", hybrid_model_path)
            logger.info("✅ Hybrid detector initialized")
        except Exception as e:
            logger.error(f"Failed to initialize hybrid detector: {e}")
    
    def analyze_code_comprehensive(self, code: str, language: str = "cpp", 
                                 filename: Optional[str] = None,
                                 detector_type: str = "hybrid") -> Dict[str, Any]:
        # NOTE: Phân tích code với enhanced features và detection
        
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
            
            # NOTE: Chạy detection với detector đã chọn
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
            logger.error(f"Enhanced analysis failed: {e}")
            return self._basic_analysis_fallback(code, language, error=str(e))
    
    def _run_detection(self, features: Dict[str, Any], detector_type: str) -> DetectionResult:
        # NOTE: Chạy detection với detector đã chọn
        
        detector = self.detectors.get(detector_type)
        
        if not detector:
            # NOTE: Fallback sử dụng detector nào có sẵn
            if self.detectors:
                detector_type = list(self.detectors.keys())[0]
                detector = self.detectors[detector_type]
                logger.warning(f"Requested detector not available, using {detector_type}")
            else:
                raise ValueError("No detectors available")
        
        # Run detection
        result = detector.detect(features)
        return result
    
    def _basic_analysis_fallback(self, code: str, language: str, error: Optional[str] = None) -> Dict[str, Any]:
        # NOTE: Fallback sử dụng phân tích cơ bản
        
        lines = code.splitlines()
        
        basic_features = {
            'loc': len(lines),
            'comment_ratio': len([l for l in lines if l.strip().startswith('//')]) / len(lines) if lines else 0,
            'blank_ratio': len([l for l in lines if not l.strip()]) / len(lines) if lines else 0,
            'token_count': None,
            'cyclomatic_complexity': None,
            'functions': None
        }
        
        detection = self._simple_rule_detection(basic_features, code)
        
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
                'fallback_reason': error or "Enhanced features not available"
            }
        }
    
    def _simple_rule_detection(self, features: Dict[str, Any], code: str) -> Dict[str, Any]:        
        score = 0.0
        reasoning = []
        
        if features['comment_ratio'] > 0.15:
            score += 0.3
            reasoning.append("High comment ratio (AI tendency)")
        
        import re
        descriptive_names = len(re.findall(r'\\b[a-zA-Z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\\b', code))
        if descriptive_names > 3:
            score += 0.2
            reasoning.append("Descriptive variable names")
        
        if '#include' in code and 'int main()' in code and 'return 0' in code:
            score += 0.2
            reasoning.append("Standard template usage")
        
        if features['loc'] < 20:
            score -= 0.2
            reasoning.append("Short code (human tendency)")
        
        if score > 0.5:
            prediction = "AI-generated"
            confidence = min(0.95, score)
        elif score < 0.3:
            prediction = "Human-written"
            confidence = min(0.95, 1.0 - score)
        else:
            prediction = "Uncertain"
            confidence = 0.5
        
        return {
            'prediction': prediction,
            'confidence': round(confidence, 3),
            'reasoning': reasoning[:3],
            'method_used': 'simple-rule-fallback'
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
                          detector_type: str = "hybrid") -> List[Dict[str, Any]]:
        
        results = []
        
        for code, language in code_samples:
            try:
                result = self.analyze_code_comprehensive(code, language, detector_type=detector_type)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch analysis error: {e}")
                results.append({
                    'error': str(e),
                    'code_length': len(code),
                    'language': language
                })
        
        return results
    
    def _get_time(self) -> float:
        """Get current time for performance measurement"""
        import time
        return time.time()

# Global instance
enhanced_analyzer = None

def get_enhanced_analyzer(model_path: Optional[str] = None) -> EnhancedMLAnalyzer:
    """Get global enhanced analyzer instance"""
    global enhanced_analyzer
    
    if enhanced_analyzer is None:
        enhanced_analyzer = EnhancedMLAnalyzer(model_path)
    
    return enhanced_analyzer

def analyze_code_with_enhanced_ml(code: str, language: str = "cpp", 
                                filename: Optional[str] = None,
                                detector_type: str = "hybrid",
                                model_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function cho enhanced code analysis
    """
    analyzer = get_enhanced_analyzer(model_path)
    return analyzer.analyze_code_comprehensive(code, language, filename, detector_type)

# Test function
def test_enhanced_integration():
    """Test function để verify enhanced integration"""
    
    test_code = '''#include <stdio.h>
#include <stdlib.h>

// Function to calculate the sum of two numbers
int calculateSum(int firstNumber, int secondNumber) {
    // Return the sum of both parameters
    return firstNumber + secondNumber;
}

int main() {
    int userInput1, userInput2;
    int resultSum;
    
    // Get input from user
    printf("Enter first number: ");
    scanf("%d", &userInput1);
    
    printf("Enter second number: ");
    scanf("%d", &userInput2);
    
    // Calculate the sum
    resultSum = calculateSum(userInput1, userInput2);
    
    // Display the result
    printf("The sum is: %d\\n", resultSum);
    
    return 0;
}'''
    
    print("🧪 Testing Enhanced ML Integration...")
    
    # Test basic analysis
    result = analyze_code_with_enhanced_ml(test_code, "cpp")
    
    print(f"✅ Analysis completed:")
    print(f"   Enhanced features: {result['meta']['enhanced_analysis']}")
    print(f"   Prediction: {result['detection']['prediction']}")
    print(f"   Confidence: {result['detection']['confidence']}")
    print(f"   Method: {result['detection']['method_used']}")
    print(f"   Processing time: {result['performance']['total_time']}s")
    
    return result

if __name__ == "__main__":
    test_enhanced_integration()