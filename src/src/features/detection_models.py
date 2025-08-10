"""
Heuristic/static Detection Models for AI Code Detection
Chỉ sử dụng heuristic scoring + AST/style metrics (không ML/hybrid)
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import pickle
from abc import ABC, abstractmethod

# ML dependencies removed

try:
    from .advanced_features import AdvancedFeatureExtractor, ComprehensiveFeatures
    HAS_ADVANCED_FEATURES = True
except ImportError:
    HAS_ADVANCED_FEATURES = False
    print("Warning: Advanced features not available.")

@dataclass 
class DetectionResult:
    """Kết quả phát hiện"""
    prediction: str  # "AI-generated" | "Human-written" | "Uncertain"
    confidence: float  # 0.0 - 1.0
    reasoning: List[str]
    feature_importance: Dict[str, float]
    method_used: str  # "heuristic-static"

class BaseDetector(ABC):
    """Base class cho các detector"""
    
    @abstractmethod
    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class HeuristicScoringDetector(BaseDetector):
    """
    Heuristics-based static detector.
    - Aggregates multi-feature static signals (AST + style + naming + redundancy)
    - Produces a continuous score in [0, 1]
    - No ML dependency
    """

    def __init__(self):
        # Feature weights for AI-leaning (positive) and Human-leaning (negative)
        # The sum of absolute weights is <= 1.0 to keep score stable.
        self.ai_feature_weights = {
            # Basic/style
            'comment_ratio': 0.10,  # High comment ratio → AI tendency
            'ast_indentation_consistency': 0.08,
            'naming_naming_consistency_score': 0.07,

            # AI patterns
            'ai_pattern_template_usage_score': 0.12,
            'ai_pattern_boilerplate_ratio': 0.08,
            'ai_pattern_error_handling_score': 0.06,

            # Redundancy
            'redundancy_copy_paste_score': 0.08,
            'redundancy_duplicate_line_ratio': 0.05,

            # Structure/complexity
            'low_cyclomatic_complexity': 0.06,  # derived from cyclomatic_complexity
            'function_density': 0.04,           # derived: functions / max(loc, 1)
        }

        self.human_feature_weights = {
            'short_loc': 0.07,                       # derived from loc
            'naming_generic_var_ratio': 0.10,
            'ast_operator_spacing_inconsistency': 0.05,  # derived from ast_operator_spacing_consistency
            'ast_single_char_vars_density': 0.06,        # derived from ast_single_char_vars / max(variable_count, 1)
        }

        self.ai_threshold = 0.60
        self.human_threshold = 0.40

    # -------------------------- helpers --------------------------
    @staticmethod
    def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
        return max(low, min(high, value))

    @staticmethod
    def _normalize_high(value: float, low: float, high: float) -> float:
        """Normalize where higher values imply stronger signal."""
        if high <= low:
            return 0.0
        return HeuristicScoringDetector._clamp((value - low) / (high - low))

    @staticmethod
    def _normalize_low(value: float, low: float, high: float) -> float:
        """Normalize where lower values imply stronger signal (invert)."""
        if high <= low:
            return 0.0
        return HeuristicScoringDetector._clamp((high - value) / (high - low))

    # -------------------------- scoring --------------------------
    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        """Compute heuristic score and final prediction."""
        contributions: Dict[str, float] = {}
        reasons: List[str] = []

        # Positive contributions (AI-leaning)
        def add_ai(name: str, score: float, desc: str):
            if score <= 0:
                return
            weight = self.ai_feature_weights[name]
            contrib = weight * score
            contributions[name] = contrib
            reasons.append(f"{desc} (+{contrib:.3f})")

        # Negative contributions (Human-leaning)
        def add_human(name: str, score: float, desc: str):
            if score <= 0:
                return
            weight = self.human_feature_weights[name]
            contrib = weight * score
            contributions[name] = -contrib
            reasons.append(f"{desc} (-{contrib:.3f})")

        # Fetch raw metrics with safe defaults
        loc = float(features.get('loc', 0) or 0)
        functions = float(features.get('functions', 0) or 0)
        cyclomatic = float(features.get('cyclomatic_complexity', features.get('cyclomatic_avg', 0) or 0))

        comment_ratio = float(features.get('comment_ratio', 0) or 0)
        indentation_consistency = float(features.get('ast_indentation_consistency', 0) or 0)
        operator_spacing_consistency = float(features.get('ast_operator_spacing_consistency', 0) or 0)

        naming_consistency = float(features.get('naming_naming_consistency_score', 0) or 0)
        naming_generic_ratio = float(features.get('naming_generic_var_ratio', 0) or 0)

        template_usage = float(features.get('ai_pattern_template_usage_score', 0) or 0)
        boilerplate_ratio = float(features.get('ai_pattern_boilerplate_ratio', 0) or 0)
        error_handling_score = float(features.get('ai_pattern_error_handling_score', 0) or 0)

        copy_paste_score = float(features.get('redundancy_copy_paste_score', 0) or 0)
        duplicate_line_ratio = float(features.get('redundancy_duplicate_line_ratio', 0) or 0)

        ast_single_char_vars = float(features.get('ast_single_char_vars', 0) or 0)
        ast_variable_count = float(features.get('ast_variable_count', features.get('variable_count', 0) or 0))

        # Derived metrics
        function_density = functions / max(loc, 1.0)  # higher density in short code can be AI-ish

        # Normalize and add AI-leaning signals
        add_ai('comment_ratio', self._normalize_high(comment_ratio, 0.10, 0.35), 'High comment ratio')
        add_ai('ast_indentation_consistency', self._normalize_high(indentation_consistency, 0.6, 1.0), 'Consistent indentation style')
        add_ai('naming_naming_consistency_score', self._normalize_high(naming_consistency, 0.5, 1.0), 'Consistent naming style')

        add_ai('ai_pattern_template_usage_score', self._normalize_high(template_usage, 0.05, 0.30), 'Template/boilerplate patterns present')
        add_ai('ai_pattern_boilerplate_ratio', self._normalize_high(boilerplate_ratio, 0.05, 0.30), 'High boilerplate ratio')
        add_ai('ai_pattern_error_handling_score', self._normalize_high(error_handling_score, 0.02, 0.20), 'Explicit error-handling patterns')

        add_ai('redundancy_copy_paste_score', self._normalize_high(copy_paste_score, 0.05, 0.40), 'Copy-paste repetition detected')
        add_ai('redundancy_duplicate_line_ratio', self._normalize_high(duplicate_line_ratio, 0.02, 0.25), 'Duplicate lines present')

        # Lower cyclomatic complexity → AI-leaning
        add_ai('low_cyclomatic_complexity', self._normalize_low(cyclomatic, 1.0, 6.0), 'Low cyclomatic complexity')

        # More functions per LOC in short code → AI-leaning
        add_ai('function_density', self._normalize_high(function_density, 0.02, 0.12), 'High function density for code length')

        # Normalize and add Human-leaning signals
        add_human('short_loc', self._normalize_low(loc, 20.0, 80.0), 'Very short code')
        add_human('naming_generic_var_ratio', self._normalize_high(naming_generic_ratio, 0.20, 0.70), 'Generic variable names')

        # Operator spacing inconsistency (invert consistency)
        op_inconsistency = self._clamp(1.0 - operator_spacing_consistency)
        add_human('ast_operator_spacing_inconsistency', self._normalize_high(op_inconsistency, 0.20, 0.80), 'Inconsistent operator spacing')

        # Single-char var density
        scv_density = ast_single_char_vars / max(ast_variable_count, 1.0)
        add_human('ast_single_char_vars_density', self._normalize_high(scv_density, 0.10, 0.50), 'High single-character variable usage')

        # Aggregate score around 0.5 baseline
        total = 0.5
        for k, v in contributions.items():
            total += v
        total = self._clamp(total)

        if total > self.ai_threshold:
            prediction = "AI-generated"
            confidence = total
        elif total < self.human_threshold:
            prediction = "Human-written"
            confidence = 1.0 - total
        else:
            prediction = "Uncertain"
            confidence = 0.5

        # Sort reasons by absolute contribution and keep top 6
        sorted_items = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
        top_keys = set(k for k, _ in sorted_items[:6])
        filtered_reasons = [r for r in reasons if any(r.startswith(lbl) for lbl in [
            'High comment ratio', 'Consistent indentation style', 'Consistent naming style',
            'Template/boilerplate patterns present', 'High boilerplate ratio', 'Explicit error-handling patterns',
            'Copy-paste repetition detected', 'Duplicate lines present', 'Low cyclomatic complexity',
            'High function density for code length', 'Very short code', 'Generic variable names',
            'Inconsistent operator spacing', 'High single-character variable usage'])]

        feature_importance = {k: round(abs(v), 4) for k, v in contributions.items() if k in top_keys}

        return DetectionResult(
            prediction=prediction,
            confidence=round(confidence, 3),
            reasoning=filtered_reasons[:6],
            feature_importance=feature_importance,
            method_used="heuristic-static",
        )

    def get_name(self) -> str:
        return "Heuristic Scoring Detector"

# ML/Hybrid detectors removed

# Factory function
def create_detector(detector_type: str = "heuristic", model_path: Optional[str] = None) -> BaseDetector:
    """
    Factory function để tạo detector
    """
    # Map legacy names to heuristic detector
    if detector_type in ("heuristic", "rule", "rule-based", "static"):
        return HeuristicScoringDetector()
    elif detector_type == "ml":
        raise ValueError("ML detector removed from codebase")
    elif detector_type == "hybrid":
        raise ValueError("Hybrid detector removed from codebase")
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")

# Example usage and testing
if __name__ == "__main__":
    # Test với sample features
    sample_features = {
        'loc': 25,
        'comment_ratio': 0.2,
        'naming_descriptive_var_ratio': 0.8,
        'ast_indentation_consistency': 0.9,
        'ai_pattern_template_usage_score': 0.4,
        'ai_pattern_error_handling_score': 0.15,
        'cyclomatic_complexity': 2.5,
        'functions': 2
    }
    
    # Test rule-based detector
    detector = create_detector("rule")
    result = detector.detect(sample_features)
    
    print(f"Detector: {detector.get_name()}")
    print(f"Prediction: {result.prediction}")
    print(f"Confidence: {result.confidence}")
    print(f"Reasoning: {result.reasoning[:3]}")
    print(f"Method: {result.method_used}")