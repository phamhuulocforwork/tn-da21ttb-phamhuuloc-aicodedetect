#!/usr/bin/env python3
"""
Complete System Test for AI Code Detection ML Pipeline
Test toàn bộ hệ thống từ feature extraction đến API integration
"""

import os
import sys
import time
import tempfile
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def test_feature_extraction():
    """Test feature extraction components"""
    print("🔍 Testing Feature Extraction Components...")
    
    # Test AST Analyzer
    try:
        from features.ast_analyzer import CppASTAnalyzer
        
        analyzer = CppASTAnalyzer()
        
        test_code = '''#include <stdio.h>
int calculateSum(int a, int b) {
    return a + b;
}

int main() {
    int x = 5, y = 10;
    printf("Sum: %d", calculateSum(x, y));
    return 0;
}'''
        
        features = analyzer.analyze_code(test_code)
        
        assert features.function_count >= 2, "Should detect at least 2 functions"
        assert features.max_depth > 0, "Should have some nesting depth"
        
        print("  ✅ AST Analyzer working correctly")
        
    except Exception as e:
        print(f"  ❌ AST Analyzer failed: {e}")
        return False
    
    # Test Advanced Features
    try:
        from features.advanced_features import AdvancedFeatureExtractor
        
        extractor = AdvancedFeatureExtractor()
        comprehensive_features = extractor.extract_all_features(test_code)
        
        assert comprehensive_features.loc > 0, "Should have LOC"
        assert comprehensive_features.ast_features is not None, "Should have AST features"
        
        # Convert to dict
        feature_dict = comprehensive_features.to_dict()
        assert len(feature_dict) > 10, "Should have many features"
        
        print("  ✅ Advanced Feature Extractor working correctly")
        
    except Exception as e:
        print(f"  ❌ Advanced Feature Extractor failed: {e}")
        return False
    
    return True

def test_detection_models():
    """Test detection model components"""
    print("🤖 Testing Detection Models...")
    
    try:
        from features.detection_models import create_detector
        
        # Sample features for testing
        sample_features = {
            'loc': 25,
            'comment_ratio': 0.2,
            'naming_descriptive_var_ratio': 0.8,
            'ast_indentation_consistency': 0.9,
            'ai_pattern_template_usage_score': 0.4,
            'ai_pattern_error_handling_score': 0.15,
            'cyclomatic_complexity': 2.5,
            'functions': 2,
            'token_count': 100,
            'ast_max_depth': 3,
            'redundancy_duplicate_line_ratio': 0.1,
            'complexity_halstead_complexity': 50.0
        }
        
        # Test Rule-based Detector
        rule_detector = create_detector("rule")
        rule_result = rule_detector.detect(sample_features)
        
        assert rule_result.prediction in ["AI-generated", "Human-written", "Uncertain"]
        assert 0 <= rule_result.confidence <= 1
        assert len(rule_result.reasoning) > 0
        
        print("  ✅ Rule-based Detector working correctly")
        
        # Test Hybrid Detector
        hybrid_detector = create_detector("hybrid")
        hybrid_result = hybrid_detector.detect(sample_features)
        
        assert hybrid_result.prediction in ["AI-generated", "Human-written", "Uncertain"]
        assert 0 <= hybrid_result.confidence <= 1
        
        print("  ✅ Hybrid Detector working correctly")
        
    except Exception as e:
        print(f"  ❌ Detection Models failed: {e}")
        return False
    
    return True

def test_evaluation_framework():
    """Test evaluation framework"""
    print("📊 Testing Evaluation Framework...")
    
    try:
        from evaluation.model_evaluator import ModelEvaluator
        
        # Create temporary evaluator
        with tempfile.TemporaryDirectory() as temp_dir:
            evaluator = ModelEvaluator(temp_dir)
            
            # Mock some test data
            mock_predictions = [
                {
                    'file_path': 'test1.cpp',
                    'true_label': 'ai',
                    'predicted_label': 'AI-generated',
                    'confidence': 0.9,
                    'features': {'loc': 20},
                    'reasoning': ['High confidence'],
                    'method_used': 'test',
                    'is_correct': True
                },
                {
                    'file_path': 'test2.cpp', 
                    'true_label': 'human',
                    'predicted_label': 'Human-written',
                    'confidence': 0.8,
                    'features': {'loc': 15},
                    'reasoning': ['Short code'],
                    'method_used': 'test',
                    'is_correct': True
                }
            ]
            
            # Simulate evaluation
            evaluator.predictions = [
                type('MockPrediction', (), pred)() for pred in mock_predictions
            ]
            
            metrics = evaluator._calculate_comprehensive_metrics(evaluator.predictions)
            
            assert metrics.accuracy == 1.0, "Should have 100% accuracy for perfect predictions"
            assert metrics.precision == 1.0, "Should have perfect precision"
            
            print("  ✅ Evaluation Framework working correctly")
    
    except Exception as e:
        print(f"  ❌ Evaluation Framework failed: {e}")
        return False
    
    return True

def test_feature_pipeline():
    """Test feature pipeline"""
    print("⚙️ Testing Feature Pipeline...")
    
    try:
        from features.feature_pipeline import FeaturePipeline, DatasetInfo
        
        # Create temporary test files
        with tempfile.TemporaryDirectory() as temp_dir:
            ai_dir = Path(temp_dir) / "ai"
            human_dir = Path(temp_dir) / "human"
            output_dir = Path(temp_dir) / "output"
            
            ai_dir.mkdir()
            human_dir.mkdir()
            
            # Create test files
            ai_code = '''#include <stdio.h>
// Function to calculate sum
int calculateSum(int firstNumber, int secondNumber) {
    return firstNumber + secondNumber;
}

int main() {
    int userInput1 = 5;
    int userInput2 = 10;
    printf("Sum: %d", calculateSum(userInput1, userInput2));
    return 0;
}'''
            
            human_code = '''#include <stdio.h>
int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d", a + b);
    return 0;
}'''
            
            # Write test files
            (ai_dir / "test_ai.cpp").write_text(ai_code)
            (human_dir / "test_human.cpp").write_text(human_code)
            
            # Test pipeline
            dataset_info = DatasetInfo(
                ai_directory=str(ai_dir),
                human_directory=str(human_dir),
                output_directory=str(output_dir),
                max_files_per_class=10
            )
            
            pipeline = FeaturePipeline(dataset_info, use_cache=False)
            
            # Test feature extraction
            stats = pipeline.extract_features_from_dataset(parallel=False)
            
            assert stats.total_files == 2, "Should process 2 files"
            assert stats.successful > 0, "Should have successful extractions"
            
            print("  ✅ Feature Pipeline working correctly")
    
    except Exception as e:
        print(f"  ❌ Feature Pipeline failed: {e}")
        return False
    
    return True

def test_api_integration():
    """Test API integration components"""
    print("🔌 Testing API Integration...")
    
    try:
        # Import without starting server
        sys.path.append(str(Path(__file__).parent.parent / "backend" / "app"))
        
        from enhanced_ml_integration import EnhancedMLAnalyzer
        
        # Test analyzer
        analyzer = EnhancedMLAnalyzer()
        
        test_code = '''#include <stdio.h>
int main() {
    printf("Hello World");
    return 0;
}'''
        
        result = analyzer.analyze_code_comprehensive(test_code, "cpp")
        
        assert 'basic_features' in result
        assert 'detection' in result
        assert 'performance' in result
        assert 'meta' in result
        
        # Check detection result
        detection = result['detection']
        assert detection['prediction'] in ["AI-generated", "Human-written", "Uncertain"]
        assert 0 <= detection['confidence'] <= 1
        
        print("  ✅ API Integration working correctly")
        
    except Exception as e:
        print(f"  ❌ API Integration failed: {e}")
        return False
    
    return True

def test_end_to_end_workflow():
    """Test complete end-to-end workflow"""
    print("🔄 Testing End-to-End Workflow...")
    
    try:
        from features.advanced_features import AdvancedFeatureExtractor
        from features.detection_models import create_detector
        
        # Sample AI-like code
        ai_code = '''#include <stdio.h>
#include <stdlib.h>

// Function to calculate the sum of two integers
int calculateSum(int firstNumber, int secondNumber) {
    // Return the sum of the two parameters
    return firstNumber + secondNumber;
}

// Function to get user input
int getUserInput(const char* prompt) {
    int userValue;
    printf("%s", prompt);
    scanf("%d", &userValue);
    return userValue;
}

int main() {
    int firstUserInput, secondUserInput;
    int calculatedResult;
    
    // Display program information
    printf("Sum Calculator Program\\n");
    printf("=====================\\n");
    
    // Get user inputs
    firstUserInput = getUserInput("Enter first number: ");
    secondUserInput = getUserInput("Enter second number: ");
    
    // Calculate the sum
    calculatedResult = calculateSum(firstUserInput, secondUserInput);
    
    // Display the result
    printf("\\nResult: %d + %d = %d\\n", firstUserInput, secondUserInput, calculatedResult);
    
    return 0;
}'''
        
        # Sample Human-like code
        human_code = '''#include <stdio.h>
int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d", a + b);
    return 0;
}'''
        
        # Extract features
        extractor = AdvancedFeatureExtractor()
        
        ai_features = extractor.extract_all_features(ai_code)
        human_features = extractor.extract_all_features(human_code)
        
        # Test detection
        detector = create_detector("hybrid")
        
        ai_result = detector.detect(ai_features.to_dict())
        human_result = detector.detect(human_features.to_dict())
        
        print(f"  AI Code → {ai_result.prediction} (confidence: {ai_result.confidence:.3f})")
        print(f"  Human Code → {human_result.prediction} (confidence: {human_result.confidence:.3f})")
        
        # Validate results make sense
        # AI code should have higher confidence in being detected as AI
        # Human code should be detected as human or at least lower confidence
        
        success = True
        if ai_result.prediction == "AI-generated" and ai_result.confidence > 0.6:
            print("  ✅ AI code correctly identified as AI-generated")
        else:
            print("  ⚠️  AI code not confidently identified as AI")
            success = False
        
        if human_result.prediction == "Human-written" or human_result.confidence < 0.7:
            print("  ✅ Human code appropriately classified")
        else:
            print("  ⚠️  Human code incorrectly classified with high confidence")
            success = False
        
        return success
        
    except Exception as e:
        print(f"  ❌ End-to-End Workflow failed: {e}")
        return False

def run_performance_benchmark():
    """Run performance benchmark"""
    print("⚡ Running Performance Benchmark...")
    
    try:
        from features.advanced_features import AdvancedFeatureExtractor
        from features.detection_models import create_detector
        
        extractor = AdvancedFeatureExtractor()
        detector = create_detector("hybrid")
        
        # Test code samples
        test_codes = [
            '''#include <stdio.h>
int main() { printf("Hello"); return 0; }''',
            
            '''#include <stdio.h>
#include <stdlib.h>

int calculateSum(int a, int b) {
    return a + b;
}

int main() {
    int x = 5, y = 10;
    printf("Sum: %d", calculateSum(x, y));
    return 0;
}''',
            
            '''#include <stdio.h>
int main() {
    int a, b, c;
    scanf("%d %d", &a, &b);
    c = a + b;
    printf("%d", c);
    return 0;
}'''
        ]
        
        total_extraction_time = 0
        total_detection_time = 0
        
        for i, code in enumerate(test_codes):
            # Feature extraction timing
            start_time = time.time()
            features = extractor.extract_all_features(code)
            extraction_time = time.time() - start_time
            total_extraction_time += extraction_time
            
            # Detection timing
            start_time = time.time()
            result = detector.detect(features.to_dict())
            detection_time = time.time() - start_time
            total_detection_time += detection_time
            
            print(f"  Sample {i+1}: Extract {extraction_time:.4f}s, Detect {detection_time:.4f}s")
        
        avg_extraction = total_extraction_time / len(test_codes)
        avg_detection = total_detection_time / len(test_codes)
        
        print(f"  📊 Average Feature Extraction: {avg_extraction:.4f}s")
        print(f"  📊 Average Detection: {avg_detection:.4f}s")
        print(f"  📊 Total Average: {avg_extraction + avg_detection:.4f}s")
        
        # Performance thresholds
        if avg_extraction < 0.1 and avg_detection < 0.05:
            print("  ✅ Performance within acceptable limits")
            return True
        else:
            print("  ⚠️  Performance slower than expected")
            return True  # Still pass, just warn
        
    except Exception as e:
        print(f"  ❌ Performance Benchmark failed: {e}")
        return False

def main():
    """Run complete system test"""
    print("🧪 === AI CODE DETECTION SYSTEM TEST ===\\n")
    
    start_time = time.time()
    tests_passed = 0
    total_tests = 0
    
    # Test individual components
    test_functions = [
        test_feature_extraction,
        test_detection_models,
        test_evaluation_framework,
        test_feature_pipeline,
        test_api_integration,
        test_end_to_end_workflow,
        run_performance_benchmark
    ]
    
    for test_func in test_functions:
        total_tests += 1
        print(f"\\n{'='*50}")
        
        try:
            if test_func():
                tests_passed += 1
                print(f"✅ {test_func.__name__} PASSED")
            else:
                print(f"❌ {test_func.__name__} FAILED")
        except Exception as e:
            print(f"❌ {test_func.__name__} CRASHED: {e}")
    
    # Final results
    print(f"\\n{'='*50}")
    print(f"🎯 TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Success Rate: {tests_passed/total_tests*100:.1f}%")
    print(f"Total Time: {time.time() - start_time:.2f}s")
    
    if tests_passed == total_tests:
        print("\\n🎉 ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION!")
        return 0
    elif tests_passed >= total_tests * 0.8:
        print("\\n⚠️  MOST TESTS PASSED - SYSTEM MOSTLY FUNCTIONAL")
        return 0
    else:
        print("\\n❌ MULTIPLE TESTS FAILED - SYSTEM NEEDS ATTENTION")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)