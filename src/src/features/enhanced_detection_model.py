"""
Enhanced AI Code Detection Model với baseline-aware scoring
Dựa trên phân tích dataset để tạo ra detection model chính xác hơn
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import math
import numpy as np
from abc import ABC, abstractmethod

# Import base classes
try:
    from .detection_models import BaseDetector, DetectionResult
except ImportError:
    from dataclasses import dataclass
    @dataclass 
    class DetectionResult:
        prediction: str  # "AI-generated" | "Human-written" | "Uncertain"
        confidence: float  # 0.0 - 1.0
        reasoning: List[str]
        feature_importance: Dict[str, float]
        method_used: str

    class BaseDetector(ABC):
        @abstractmethod
        def detect(self, features: Dict[str, Any]) -> DetectionResult:
            pass
        
        @abstractmethod
        def get_name(self) -> str:
            pass

# Import baseline loader for dynamic stats loading
try:
    import sys
    from pathlib import Path
    
    # Try multiple possible paths for backend/app
    possible_backend_paths = [
        # From src/src/features/ to backend/app/
        Path(__file__).parent.parent.parent / "backend" / "app",
        # From project root
        Path(__file__).parent.parent.parent.parent / "src" / "backend" / "app",
        # Relative from current working directory
        Path("src/backend/app"),
        Path("backend/app"),
        # Direct path if running from project root
        Path("../backend/app"),
        Path("../../backend/app"),
    ]
    
    backend_path = None
    for path in possible_backend_paths:
        if path.exists() and (path / "baseline_loader.py").exists():
            backend_path = path
            break
    
    if backend_path and str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    
    from baseline_loader import get_baseline_loader
    HAS_BASELINE_LOADER = True
    print(f"Successfully imported baseline_loader from {backend_path}")
    
except ImportError as e:
    HAS_BASELINE_LOADER = False
    print(f"Warning: Could not import baseline_loader: {e}, using fallback stats")

@dataclass
class FallbackBaselineStats:
    """Fallback baseline stats when loader is not available"""
    
    # Minimal fallback stats - only the most critical ones
    ai_stats = {
        'comment_ratio': 0.066,
        'ast_indentation_consistency': 1.0,
        'naming_generic_var_ratio': 0.139,
        'ast_if_statements_per_loc': 0.007,
        'cyclomatic_complexity': 1.073,
        'human_style_overall_score': 0.212,
    }
    
    human_stats = {
        'comment_ratio': 0.006,
        'ast_indentation_consistency': 0.952,
        'naming_generic_var_ratio': 0.526,
        'ast_if_statements_per_loc': 0.052,
        'cyclomatic_complexity': 3.493,
        'human_style_overall_score': 0.697,
    }
    
    # Human baseline stats
    human_stats = {
        'comment_ratio': 0.006,
        'blank_ratio': 0.069,
        'ast_indentation_consistency': 0.952,
        'ast_operator_spacing_consistency': 0.907,
        'naming_descriptive_var_ratio': 0.448,
        'naming_generic_var_ratio': 0.526,
        'ast_avg_variable_name_length': 2.78,
        'ast_variable_uniqueness_ratio': 0.809,
        'ast_if_statements_per_loc': 0.052,
        'ast_for_loops_per_loc': 0.045,
        'ast_while_loops_per_loc': 0.006,
        'cyclomatic_complexity': 3.493,
        'complexity_maintainability_index': 95.37,
        'spacing_spacing_issues_ratio': 1.223,
        'indentation_indentation_issues_ratio': 0.249,
        'naming_inconsistency_naming_inconsistency_ratio': 1.311,
        'human_style_overall_score': 0.697,
        'redundancy_duplicate_line_ratio': 0.118,
        'ast_single_char_vars_ratio': 0.347,
        'ast_camel_case_ratio': 0.071,
        'ast_snake_case_ratio': 0.096,
        'naming_meaningful_names_score': 0.532,
        'complexity_cognitive_per_loc': 0.186,
    }

class EnhancedAIDetector(BaseDetector):
    """
    Enhanced AI Detection Model với baseline-aware scoring
    Sử dụng dynamic loading từ feature_stats.json
    """
    
    def __init__(self):
        # Load baseline stats dynamically
        if HAS_BASELINE_LOADER:
            try:
                self.baseline_loader = get_baseline_loader()
                self.baseline_stats = self.baseline_loader.get_baseline_stats()
                self.critical_features = self.baseline_loader.get_critical_features()
                print(f"Loaded {len(self.critical_features)} critical features from baseline stats")
            except Exception as e:
                print(f"Failed to load baseline stats: {e}, using fallback")
                self._use_fallback_stats()
        else:
            self._use_fallback_stats()
        
        # Thresholds cho classification
        self.ai_threshold = 0.65      # Confidence > 65% → AI
        self.human_threshold = 0.35   # Confidence < 35% → Human
    
    def _use_fallback_stats(self):
        """Use fallback stats when dynamic loading fails"""
        from types import SimpleNamespace
        
        fallback = FallbackBaselineStats()
        
        # Create a minimal baseline stats object
        self.baseline_stats = SimpleNamespace(
            ai_stats=fallback.ai_stats,
            human_stats=fallback.human_stats
        )
        
        # Create minimal critical features
        self.critical_features = {
            'ast_indentation_consistency': {'weight': 0.15, 'ai_better': True},
            'comment_ratio': {'weight': 0.12, 'ai_better': True},
            'naming_generic_var_ratio': {'weight': 0.12, 'ai_better': False},
            'ast_if_statements_per_loc': {'weight': 0.10, 'ai_better': False},
            'cyclomatic_complexity': {'weight': 0.08, 'ai_better': False},
            'human_style_overall_score': {'weight': 0.12, 'ai_better': False}
        }
        
    def _calculate_feature_score(self, feature_name: str, value: float) -> Tuple[float, str]:
        """
        Tính điểm cho một feature dựa trên baseline comparison
        Returns: (score, explanation)
        score: 0.0-1.0 where 1.0 = strongly AI-like, 0.0 = strongly Human-like
        """
        if feature_name not in self.baseline_stats.ai_stats or feature_name not in self.baseline_stats.human_stats:
            return 0.5, f"No baseline data for {feature_name}"
            
        ai_baseline = self.baseline_stats.ai_stats[feature_name]
        human_baseline = self.baseline_stats.human_stats[feature_name]
        
        # Handle edge cases
        if ai_baseline == human_baseline:
            return 0.5, f"{feature_name}: No difference between AI/Human baselines"
            
        # Calculate distance from each baseline (normalized)
        range_val = abs(ai_baseline - human_baseline)
        
        # Distance to AI baseline (0.0 = exactly AI-like)
        ai_distance = abs(value - ai_baseline) / range_val if range_val > 0 else 0
        
        # Distance to Human baseline (0.0 = exactly Human-like)  
        human_distance = abs(value - human_baseline) / range_val if range_val > 0 else 0
        
        # Convert to score (0.0 = Human-like, 1.0 = AI-like)
        if ai_distance < human_distance:
            # Closer to AI baseline
            similarity_to_ai = 1.0 - ai_distance
            score = 0.5 + (similarity_to_ai * 0.5)  # Map to [0.5, 1.0]
            explanation = f"Closer to AI baseline ({ai_baseline:.3f}) than Human ({human_baseline:.3f})"
        else:
            # Closer to Human baseline
            similarity_to_human = 1.0 - human_distance
            score = 0.5 - (similarity_to_human * 0.5)  # Map to [0.0, 0.5]
            explanation = f"Closer to Human baseline ({human_baseline:.3f}) than AI ({ai_baseline:.3f})"
            
        return max(0.0, min(1.0, score)), explanation
    
    def _calculate_perfection_score(self, features: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Tính điểm về sự hoàn hảo của code - AI code thường hoàn hảo hơn
        """
        perfection_indicators = []
        total_score = 0.0
        count = 0
        
        # Perfect indentation
        indentation_consistency = features.get('ast_indentation_consistency', 0.5)
        if indentation_consistency >= 0.99:
            perfection_indicators.append("Perfect indentation consistency (100%)")
            total_score += 1.0
        elif indentation_consistency >= 0.95:
            perfection_indicators.append(f"Very high indentation consistency ({indentation_consistency:.1%})")
            total_score += 0.7
        else:
            total_score += 0.0
        count += 1
        
        # Spacing consistency
        spacing_issues = features.get('spacing_spacing_issues_ratio', 1.0)
        if spacing_issues <= 0.1:
            perfection_indicators.append("Excellent spacing consistency")
            total_score += 1.0
        elif spacing_issues <= 0.5:
            perfection_indicators.append("Good spacing consistency")
            total_score += 0.6
        count += 1
        
        # Naming consistency
        naming_inconsistency = features.get('naming_inconsistency_naming_inconsistency_ratio', 1.0)
        if naming_inconsistency <= 0.2:
            perfection_indicators.append("Excellent naming consistency")
            total_score += 1.0
        elif naming_inconsistency <= 0.8:
            perfection_indicators.append("Good naming consistency")
            total_score += 0.6
        count += 1
        
        # Variable uniqueness (AI tends to avoid duplicate variable names)
        var_uniqueness = features.get('ast_variable_uniqueness_ratio', 0.5)
        if var_uniqueness >= 0.95:
            perfection_indicators.append(f"Very high variable uniqueness ({var_uniqueness:.1%})")
            total_score += 1.0
        elif var_uniqueness >= 0.8:
            perfection_indicators.append(f"High variable uniqueness ({var_uniqueness:.1%})")
            total_score += 0.6
        count += 1
        
        return total_score / count if count > 0 else 0.0, perfection_indicators
    
    def _calculate_simplicity_score(self, features: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Tính điểm về sự đơn giản của code - AI code thường đơn giản hơn
        """
        simplicity_indicators = []
        total_score = 0.0
        count = 0
        
        # Low cyclomatic complexity
        cyclomatic = features.get('cyclomatic_complexity', 5.0)
        if cyclomatic <= 2.0:
            simplicity_indicators.append(f"Very low complexity (CC={cyclomatic:.1f})")
            total_score += 1.0
        elif cyclomatic <= 4.0:
            simplicity_indicators.append(f"Low complexity (CC={cyclomatic:.1f})")
            total_score += 0.6
        count += 1
        
        # Few control structures
        if_density = features.get('ast_if_statements_per_loc', 0.05)
        for_density = features.get('ast_for_loops_per_loc', 0.05)
        
        if if_density <= 0.02 and for_density <= 0.02:
            simplicity_indicators.append("Very few control structures")
            total_score += 1.0
        elif if_density <= 0.04 and for_density <= 0.04:
            simplicity_indicators.append("Few control structures")
            total_score += 0.6
        count += 1
        
        # High maintainability
        maintainability = features.get('complexity_maintainability_index', 50)
        if maintainability >= 100:
            simplicity_indicators.append(f"Excellent maintainability ({maintainability:.0f})")
            total_score += 1.0
        elif maintainability >= 80:
            simplicity_indicators.append(f"Good maintainability ({maintainability:.0f})")
            total_score += 0.6
        count += 1
        
        return total_score / count if count > 0 else 0.0, simplicity_indicators
    
    def _calculate_human_chaos_score(self, features: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Tính điểm về sự 'chaos' đặc trưng của human code
        Score cao = nhiều human characteristics
        """
        chaos_indicators = []
        total_score = 0.0
        count = 0
        
        # Many generic variable names (i, j, k, temp, etc.)
        generic_ratio = features.get('naming_generic_var_ratio', 0.3)
        if generic_ratio >= 0.4:
            chaos_indicators.append(f"High use of generic variables ({generic_ratio:.1%})")
            total_score += 1.0
        elif generic_ratio >= 0.2:
            chaos_indicators.append(f"Moderate use of generic variables ({generic_ratio:.1%})")
            total_score += 0.6
        count += 1
        
        # Short variable names
        avg_var_length = features.get('ast_avg_variable_name_length', 4.0)
        if avg_var_length <= 2.5:
            chaos_indicators.append(f"Short variable names (avg={avg_var_length:.1f})")
            total_score += 1.0
        elif avg_var_length <= 3.5:
            chaos_indicators.append(f"Moderately short variable names (avg={avg_var_length:.1f})")
            total_score += 0.6
        count += 1
        
        # Spacing inconsistencies
        spacing_issues = features.get('spacing_spacing_issues_ratio', 0.5)
        if spacing_issues >= 1.0:
            chaos_indicators.append("Many spacing inconsistencies")
            total_score += 1.0
        elif spacing_issues >= 0.5:
            chaos_indicators.append("Some spacing inconsistencies") 
            total_score += 0.6
        count += 1
        
        # High single character variable usage
        single_char_ratio = features.get('ast_single_char_vars_ratio', 0.2)
        if single_char_ratio >= 0.3:
            chaos_indicators.append(f"Heavy use of single-char variables ({single_char_ratio:.1%})")
            total_score += 1.0
        elif single_char_ratio >= 0.15:
            chaos_indicators.append(f"Moderate use of single-char variables ({single_char_ratio:.1%})")
            total_score += 0.6
        count += 1
        
        return total_score / count if count > 0 else 0.0, chaos_indicators
    
    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        """
        Enhanced detection với baseline-aware scoring
        """
        feature_scores = {}
        reasoning = []
        
        # 1. Calculate baseline-aware scores for critical features
        baseline_score = 0.0
        baseline_weight_sum = 0.0
        
        for feature_name, config in self.critical_features.items():
            if feature_name in features:
                value = features[feature_name]
                score, explanation = self._calculate_feature_score(feature_name, value)
                weight = config['weight']
                
                feature_scores[f"baseline_{feature_name}"] = score * weight
                baseline_score += score * weight
                baseline_weight_sum += weight
                
                # Add reasoning
                if score > 0.6:
                    reasoning.append(f"AI-like {feature_name}: {explanation}")
                elif score < 0.4:
                    reasoning.append(f"Human-like {feature_name}: {explanation}")
        
        # Normalize baseline score
        baseline_score = baseline_score / baseline_weight_sum if baseline_weight_sum > 0 else 0.5
        
        # 2. Calculate advanced scoring
        perfection_score, perfection_indicators = self._calculate_perfection_score(features)
        simplicity_score, simplicity_indicators = self._calculate_simplicity_score(features)
        chaos_score, chaos_indicators = self._calculate_human_chaos_score(features)
        
        # Add advanced reasoning
        if perfection_score > 0.7:
            reasoning.extend(perfection_indicators[:2])  # Top 2
        if simplicity_score > 0.7:
            reasoning.extend(simplicity_indicators[:2])  # Top 2 
        if chaos_score > 0.7:
            reasoning.extend(chaos_indicators[:2])  # Top 2
        
        # 3. Combine scores với weighted approach
        weights = {
            'baseline': 0.60,    # Baseline comparison most important
            'perfection': 0.20,  # Code perfection
            'simplicity': 0.10,  # Code simplicity  
            'chaos': 0.10       # Human chaos (inverted)
        }
        
        # Final score calculation
        final_score = (
            baseline_score * weights['baseline'] +
            perfection_score * weights['perfection'] +
            simplicity_score * weights['simplicity'] +
            (1.0 - chaos_score) * weights['chaos']  # Invert chaos score
        )
        
        # Store feature importance
        feature_importance = {
            'baseline_comparison': round(baseline_score * weights['baseline'], 3),
            'code_perfection': round(perfection_score * weights['perfection'], 3),
            'code_simplicity': round(simplicity_score * weights['simplicity'], 3),
            'human_chaos_inverted': round((1.0 - chaos_score) * weights['chaos'], 3)
        }
        
        # 4. Make prediction with confidence
        if final_score >= self.ai_threshold:
            prediction = "AI-generated"
            confidence = final_score
            # Add confidence reasoning
            if final_score >= 0.8:
                reasoning.insert(0, f"Strong AI patterns detected (score: {final_score:.2f})")
            else:
                reasoning.insert(0, f"AI patterns detected (score: {final_score:.2f})")
                
        elif final_score <= self.human_threshold:
            prediction = "Human-written"
            confidence = 1.0 - final_score
            # Add confidence reasoning
            if final_score <= 0.2:
                reasoning.insert(0, f"Strong human patterns detected (score: {final_score:.2f})")
            else:
                reasoning.insert(0, f"Human patterns detected (score: {final_score:.2f})")
                
        else:
            prediction = "Uncertain"
            confidence = 0.5
            reasoning.insert(0, f"Mixed patterns - inconclusive (score: {final_score:.2f})")
        
        # Limit reasoning to top 8 items
        reasoning = reasoning[:8]
        
        return DetectionResult(
            prediction=prediction,
            confidence=round(confidence, 3),
            reasoning=reasoning,
            feature_importance=feature_importance,
            method_used="enhanced-baseline-aware"
        )
    
    def get_name(self) -> str:
        return "Enhanced Baseline-Aware AI Detector"

# Factory function updated
def create_enhanced_detector() -> BaseDetector:
    """Create enhanced detection model"""
    return EnhancedAIDetector()