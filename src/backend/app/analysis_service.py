#!/usr/bin/env python3
"""
Code Analysis Service
Service class để xử lý phân tích code và trả về kết quả cho frontend
"""

import sys
import logging
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np

# Add src/src to path for imports
current_dir = Path(__file__).parent
src_src_path = current_dir.parent.parent / "src"
sys.path.append(str(src_src_path))

try:
    from features.advanced_features import AdvancedFeatureExtractor
    from optimized_binary_classifier import OptimizedBinaryClassifier, ClassificationResult
    from super_linter_integration import SuperLinterIntegration
    HAS_ADVANCED_FEATURES = True
except ImportError as e:
    print(f"Warning: Advanced features not available: {e}")
    HAS_ADVANCED_FEATURES = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FeatureComparisonData:
    """Data structure cho feature comparison"""
    feature_name: str
    user_value: float
    ai_baseline: float
    difference: float
    difference_percentage: float
    category: str  # 'ast', 'naming', 'complexity', 'ai_pattern', etc.
    interpretation: str  # 'Higher than AI', 'Lower than AI', 'Similar to AI'

@dataclass
class CodeAnalysisResult:
    """Kết quả phân tích code hoàn chỉnh"""
    # Basic info
    code_info: Dict[str, Any]
    
    # Classification result
    classification: Dict[str, Any]
    
    # All extracted features
    features: Dict[str, float]
    
    # Feature comparison với AI baseline
    feature_comparison: List[FeatureComparisonData]
    
    # Top discriminative features
    top_features: List[Dict[str, Any]]
    
    # Code quality metrics
    quality_metrics: Dict[str, Any]
    
    # Charts data for frontend
    charts_data: Dict[str, Any]

class CodeAnalysisService:
    """Service chính để phân tích code"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.feature_extractor = AdvancedFeatureExtractor() if HAS_ADVANCED_FEATURES else None
        self.linter = SuperLinterIntegration()
        
        # Load classifier
        self.classifier = OptimizedBinaryClassifier()
        if model_path and Path(model_path).exists():
            self.classifier.load_model(model_path)
            logger.info(f"Loaded trained model from {model_path}")
        else:
            logger.warning("Using default classifier weights")
        
        # Load AI baseline data
        self.ai_baseline = self._load_ai_baseline()
        
        # Define feature categories - updated với normalized features
        self.feature_categories = {
            'ast': ['ast_total_nodes', 'ast_nodes_per_loc', 'ast_max_depth', 'ast_avg_depth', 'ast_branching_factor',
                   'ast_if_statements', 'ast_if_statements_per_loc', 'ast_for_loops', 'ast_for_loops_per_loc', 
                   'ast_while_loops', 'ast_while_loops_per_loc', 'ast_function_count', 'ast_functions_per_loc',
                   'ast_variable_count', 'ast_variables_per_loc', 'ast_camel_case_vars', 'ast_camel_case_ratio',
                   'ast_snake_case_vars', 'ast_snake_case_ratio', 'ast_single_char_vars', 'ast_single_char_vars_ratio',
                   'ast_avg_variable_name_length'],
            
            'naming': ['naming_descriptive_var_ratio', 'naming_generic_var_ratio',
                      'naming_meaningful_names_score', 'naming_verb_function_ratio',
                      'naming_descriptive_function_ratio', 'naming_naming_consistency_score'],
            
            'complexity': ['complexity_halstead_complexity', 'complexity_halstead_per_loc',
                          'complexity_cognitive_complexity', 'complexity_cognitive_per_loc',
                          'complexity_maintainability_index', 'complexity_code_to_comment_ratio',
                          'cyclomatic_complexity'],
            
            'ai_pattern': ['ai_pattern_template_usage_score', 'ai_pattern_boilerplate_ratio',
                          'ai_pattern_error_handling_score', 'ai_pattern_defensive_programming_score',
                          'ai_pattern_over_engineering_score'],
            
            'redundancy': ['redundancy_duplicate_lines', 'redundancy_duplicate_line_ratio',
                          'redundancy_repeated_patterns', 'redundancy_repeated_patterns_per_loc', 
                          'redundancy_copy_paste_score'],
            
            'basic': ['loc', 'comment_ratio', 'blank_ratio', 'token_count', 'functions']
        }
        
        # Define top discriminative features (từ training results)
        self.top_discriminative_features = [
            'naming_verb_function_ratio',
            'naming_meaningful_names_score', 
            'blank_ratio',
            'complexity_maintainability_index',
            'naming_descriptive_var_ratio',
            'comment_ratio',
            'ai_pattern_template_usage_score',
            'ast_total_nodes',
            'complexity_cognitive_complexity',
            'naming_naming_consistency_score'
        ]
    
    def _load_ai_baseline(self) -> Dict[str, float]:
        """Load AI baseline features từ trained data"""
        # Updated AI baseline values (từ analysis results và tối ưu)
        ai_baseline = {
            # Naming features
            'naming_verb_function_ratio': 0.4512,
            'naming_meaningful_names_score': 0.7234,
            'naming_descriptive_var_ratio': 0.6789,
            'naming_generic_var_ratio': 0.25,
            'naming_naming_consistency_score': 0.8456,
            'naming_abbreviation_usage': 0.15,
            
            # Basic features
            'blank_ratio': 0.1456,
            'comment_ratio': 0.2134,
            'loc': 35.5,
            'functions': 2.1,
            'token_count': 120.5,
            
            # AST features - normalized values
            'ast_total_nodes': 45.6,  # Keep absolute for comparison
            'ast_nodes_per_loc': 1.28,  # Normalized: ~45.6 / ~35.5 LOC
            'ast_avg_variable_name_length': 6.8,
            
            # Variable features - normalized
            'ast_camel_case_vars': 3.2,  # Keep absolute
            'ast_camel_case_ratio': 0.32,  # Normalized: ~3.2 / ~10 vars
            'ast_snake_case_vars': 1.2,
            'ast_snake_case_ratio': 0.12,  # Normalized
            'ast_single_char_vars': 2.1,  # Keep absolute
            'ast_single_char_vars_ratio': 0.21,  # Normalized: critical metric
            
            # Control flow - normalized  
            'ast_for_loops': 1.3,
            'ast_for_loops_per_loc': 0.037,  # Normalized: ~1.3 / ~35.5
            'ast_while_loops': 0.7,
            'ast_while_loops_per_loc': 0.020,  # Normalized
            'ast_if_statements': 2.8,
            'ast_if_statements_per_loc': 0.079,  # Normalized
            
            # Function features
            'ast_function_count': 2.1,
            'ast_functions_per_loc': 0.059,  # Normalized: ~2.1 / ~35.5
            'ast_avg_function_length': 14.0,
            'ast_max_function_length': 18.0,
            'ast_nested_control_depth': 1.8,
            'ast_branching_factor': 0.12,
            
            # Complexity features - normalized
            'complexity_maintainability_index': 85.2,  # Already normalized (0-100)
            'complexity_cognitive_complexity': 3.2,
            'complexity_cognitive_per_loc': 0.090,  # Normalized: ~3.2 / ~35.5
            'complexity_halstead_complexity': 156.7,
            'complexity_halstead_per_loc': 4.41,  # Normalized: ~156.7 / ~35.5
            'complexity_code_to_comment_ratio': 5.0,  # Already a ratio
            'cyclomatic_complexity': 2.8,
            
            # AI pattern features
            'ai_pattern_template_usage_score': 0.1234,
            'ai_pattern_boilerplate_ratio': 0.15,
            'ai_pattern_error_handling_score': 0.11,
            'ai_pattern_defensive_programming_score': 0.11,
            'ai_pattern_over_engineering_score': 0.05,
            
            # Redundancy features - normalized
            'redundancy_copy_paste_score': 0.08,  # Already normalized (0-1 scale)
            'redundancy_duplicate_lines': 0.8,
            'redundancy_duplicate_line_ratio': 0.02,  # Already normalized
            'redundancy_repeated_patterns': 1.2,
            'redundancy_repeated_patterns_per_loc': 0.034,  # Normalized: ~1.2 / ~35.5
            'redundancy_similar_function_ratio': 0.1  # Already normalized
        }
        
        # Try to load from file if exists
        baseline_file = current_dir / "features" / "ai_baseline_features.json"
        if baseline_file.exists():
            try:
                with open(baseline_file, 'r') as f:
                    loaded_baseline = json.load(f)
                    ai_baseline.update(loaded_baseline)
                    logger.info(f"Loaded AI baseline from {baseline_file}")
            except Exception as e:
                logger.warning(f"Could not load AI baseline: {e}")
        
        return ai_baseline
    
    def analyze_code(self, code: str, filename: str = "code.c", 
                    include_linting: bool = True) -> CodeAnalysisResult:
        """Phân tích code và trả về kết quả hoàn chỉnh"""
        
        logger.info(f"Analyzing code: {filename}")
        
        # 1. Basic code info
        lines = code.splitlines()
        code_info = {
            'filename': filename,
            'language': self._detect_language(filename),
            'size_bytes': len(code),
            'lines_of_code': len(lines),
            'non_empty_lines': len([l for l in lines if l.strip()]),
            'comment_lines': len([l for l in lines if l.strip().startswith('//') or '/*' in l])
        }
        
        # 2. Extract comprehensive features
        if not self.feature_extractor:
            raise ValueError("Feature extractor not available")
        
        features = self.feature_extractor.extract_all_features(code, filename)
        feature_dict = features.to_dict()
        
        # 3. Run classification
        classification_result = self.classifier.classify(feature_dict, include_linting)
        classification = {
            'prediction': classification_result.prediction,
            'confidence': classification_result.confidence,
            'reasoning': classification_result.reasoning,
            'method': classification_result.method_used,
            'feature_importance': classification_result.feature_scores
        }
        
        # 4. Quality metrics
        quality_metrics = {}
        if include_linting:
            lint_results = self.linter.comprehensive_lint(code, filename)
            quality_metrics = {
                'total_issues': lint_results['total_issues'],
                'errors': lint_results['total_errors'],
                'warnings': lint_results['total_warnings'],
                'style_issues': lint_results['total_style_issues'],
                'complexity_score': lint_results['avg_complexity'],
                'tools_used': lint_results['total_tools_used']
            }
        
        # 5. Feature comparison với AI baseline
        feature_comparison = self._create_feature_comparison(feature_dict)
        
        # 6. Top features analysis
        top_features = self._analyze_top_features(feature_dict, classification_result)
        
        # 7. Charts data for frontend
        charts_data = self._prepare_charts_data(feature_dict, feature_comparison, top_features)
        
        return CodeAnalysisResult(
            code_info=code_info,
            classification=classification,
            features=feature_dict,
            feature_comparison=feature_comparison,
            top_features=top_features,
            quality_metrics=quality_metrics,
            charts_data=charts_data
        )
    
    def _detect_language(self, filename: str) -> str:
        """Detect programming language từ filename"""
        ext = Path(filename).suffix.lower()
        if ext in ['.c']:
            return 'c'
        elif ext in ['.cpp', '.cc', '.cxx']:
            return 'cpp'
        else:
            return 'unknown'
    
    def _create_feature_comparison(self, features: Dict[str, float]) -> List[FeatureComparisonData]:
        """Tạo feature comparison với AI baseline"""
        comparisons = []
        
        for feature_name, user_value in features.items():
            if feature_name in self.ai_baseline:
                ai_baseline = self.ai_baseline[feature_name]
                difference = user_value - ai_baseline
                
                # Calculate percentage difference
                if ai_baseline != 0:
                    difference_percentage = (difference / ai_baseline) * 100
                else:
                    difference_percentage = 0
                
                # Determine interpretation
                if abs(difference_percentage) < 10:
                    interpretation = "Similar to AI"
                elif difference > 0:
                    interpretation = "Higher than AI"
                else:
                    interpretation = "Lower than AI"
                
                # Find category
                category = "other"
                for cat, feature_list in self.feature_categories.items():
                    if feature_name in feature_list:
                        category = cat
                        break
                
                comparison = FeatureComparisonData(
                    feature_name=feature_name,
                    user_value=round(user_value, 4),
                    ai_baseline=round(ai_baseline, 4),
                    difference=round(difference, 4),
                    difference_percentage=round(difference_percentage, 2),
                    category=category,
                    interpretation=interpretation
                )
                
                comparisons.append(comparison)
        
        # Sort by absolute difference percentage
        comparisons.sort(key=lambda x: abs(x.difference_percentage), reverse=True)
        
        return comparisons
    
    def _analyze_top_features(self, features: Dict[str, float], 
                            classification: ClassificationResult) -> List[Dict[str, Any]]:
        """Phân tích top discriminative features"""
        top_features = []
        
        for feature_name in self.top_discriminative_features[:8]:  # Top 8
            if feature_name in features:
                user_value = features[feature_name]
                ai_baseline = self.ai_baseline.get(feature_name, 0)
                
                # Feature importance from classification
                importance = 0
                for key, value in classification.feature_scores.items():
                    if feature_name in key:
                        importance = abs(value)
                        break
                
                top_features.append({
                    'name': feature_name,
                    'display_name': self._get_feature_display_name(feature_name),
                    'user_value': round(user_value, 4),
                    'ai_baseline': round(ai_baseline, 4),
                    'importance': round(importance, 4),
                    'category': self._get_feature_category(feature_name)
                })
        
        return top_features
    
    def _get_feature_display_name(self, feature_name: str) -> str:
        """Convert feature name to display-friendly name"""
        display_names = {
            'naming_verb_function_ratio': 'Verb Function Ratio',
            'naming_meaningful_names_score': 'Meaningful Names Score',
            'blank_ratio': 'Blank Line Ratio',
            'complexity_maintainability_index': 'Maintainability Index',
            'naming_descriptive_var_ratio': 'Descriptive Variable Ratio',
            'comment_ratio': 'Comment Ratio',
            'ai_pattern_template_usage_score': 'Template Usage Score',
            'ast_total_nodes': 'AST Total Nodes',
            'complexity_cognitive_complexity': 'Cognitive Complexity',
            'naming_naming_consistency_score': 'Naming Consistency'
        }
        
        return display_names.get(feature_name, feature_name.replace('_', ' ').title())
    
    def _get_feature_category(self, feature_name: str) -> str:
        """Get category of a feature"""
        for category, features in self.feature_categories.items():
            if feature_name in features:
                return category
        return 'other'
    
    def _prepare_charts_data(self, features: Dict[str, float], 
                           comparisons: List[FeatureComparisonData],
                           top_features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare data for frontend charts"""
        
        # 1. Radar chart data cho top features
        radar_data = {
            'labels': [f['display_name'] for f in top_features],
            'user_values': [f['user_value'] for f in top_features],
            'ai_baseline': [f['ai_baseline'] for f in top_features],
            'max_values': [max(f['user_value'], f['ai_baseline']) * 1.2 for f in top_features]
        }
        
        # 2. Bar chart data cho feature comparison
        significant_comparisons = [c for c in comparisons if abs(c.difference_percentage) > 5][:10]
        bar_data = {
            'labels': [self._get_feature_display_name(c.feature_name) for c in significant_comparisons],
            'user_values': [c.user_value for c in significant_comparisons],
            'ai_baseline': [c.ai_baseline for c in significant_comparisons],
            'differences': [c.difference_percentage for c in significant_comparisons]
        }
        
        # 3. Category breakdown
        category_data = {}
        for category in self.feature_categories.keys():
            category_features = [c for c in comparisons if c.category == category]
            if category_features:
                avg_diff = np.mean([abs(c.difference_percentage) for c in category_features])
                category_data[category] = {
                    'avg_difference': round(avg_diff, 2),
                    'feature_count': len(category_features),
                    'significant_features': len([c for c in category_features if abs(c.difference_percentage) > 10])
                }
        
        # 4. Distribution data
        all_diffs = [c.difference_percentage for c in comparisons]
        distribution_data = {
            'mean_difference': round(np.mean(all_diffs), 2),
            'std_difference': round(np.std(all_diffs), 2),
            'higher_than_ai': len([d for d in all_diffs if d > 10]),
            'lower_than_ai': len([d for d in all_diffs if d < -10]),
            'similar_to_ai': len([d for d in all_diffs if abs(d) <= 10])
        }
        
        return {
            'radar_chart': radar_data,
            'bar_chart': bar_data,
            'category_breakdown': category_data,
            'distribution': distribution_data
        }
    
    def get_ai_baseline_summary(self) -> Dict[str, Any]:
        """Get summary của AI baseline data"""
        return {
            'total_features': len(self.ai_baseline),
            'categories': {
                category: {
                    'feature_count': len([f for f in features if f in self.ai_baseline]),
                    'avg_value': round(np.mean([self.ai_baseline[f] for f in features if f in self.ai_baseline]), 4)
                }
                for category, features in self.feature_categories.items()
            },
            'top_discriminative': [
                {
                    'name': feature,
                    'display_name': self._get_feature_display_name(feature),
                    'baseline_value': self.ai_baseline.get(feature, 0),
                    'category': self._get_feature_category(feature)
                }
                for feature in self.top_discriminative_features[:10]
                if feature in self.ai_baseline
            ]
        }
