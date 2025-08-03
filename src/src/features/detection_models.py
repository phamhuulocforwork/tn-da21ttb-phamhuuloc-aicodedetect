"""
Enhanced Detection Models for AI Code Detection
Mô hình phát hiện nâng cao kết hợp rule-based và machine learning
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import pickle
from abc import ABC, abstractmethod

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("Warning: scikit-learn not available. ML models disabled.")

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
    method_used: str  # "rule-based" | "ml" | "hybrid"

class BaseDetector(ABC):
    """Base class cho các detector"""
    
    @abstractmethod
    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class EnhancedRuleBasedDetector(BaseDetector):
    """
    Enhanced Rule-based Detector với sophisticated thresholds
    """
    
    def __init__(self):
        self.setup_rules()
    
    def setup_rules(self):
        """Setup detection rules với weights và thresholds"""
        
        # AI Indicators (positive score = more likely AI)
        self.ai_rules = {
            # Basic features
            'high_comment_ratio': {
                'threshold': 0.15,
                'weight': 0.2,
                'description': 'Tỷ lệ comment cao (>15%)'
            },
            'descriptive_naming': {
                'threshold': 0.6,
                'weight': 0.25,
                'description': 'Tên biến mô tả chi tiết'
            },
            'consistent_formatting': {
                'threshold': 0.8,
                'weight': 0.15,
                'description': 'Formatting nhất quán'
            },
            'template_usage': {
                'threshold': 0.3,
                'weight': 0.2,
                'description': 'Sử dụng template chuẩn'
            },
            'error_handling': {
                'threshold': 0.1,
                'weight': 0.15,
                'description': 'Có error handling'
            },
            'boilerplate_code': {
                'threshold': 0.2,
                'weight': 0.1,
                'description': 'Nhiều boilerplate code'
            },
            
            # AST features
            'low_complexity': {
                'threshold': 3.0,
                'weight': 0.1,
                'description': 'Độ phức tạp thấp'
            },
            'structured_code': {
                'threshold': 0.5,
                'weight': 0.1,
                'description': 'Code có cấu trúc tốt'
            }
        }
        
        # Human Indicators (negative score = more likely Human)
        self.human_rules = {
            'short_code': {
                'threshold': 30,
                'weight': -0.15,
                'description': 'Code ngắn (<30 LOC)'
            },
            'generic_variables': {
                'threshold': 0.5,
                'weight': -0.2,
                'description': 'Nhiều biến generic (a,b,i,j)'
            },
            'minimal_comments': {
                'threshold': 0.05,
                'weight': -0.1,
                'description': 'Ít comment (<5%)'
            },
            'inconsistent_style': {
                'threshold': 0.3,
                'weight': -0.15,
                'description': 'Style không nhất quán'
            },
            'pragmatic_approach': {
                'threshold': 0.7,
                'weight': -0.1,
                'description': 'Approach thực dụng'
            }
        }
        
        # Thresholds for final decision
        self.decision_thresholds = {
            'ai_threshold': 0.6,      # > 0.6 = AI-generated
            'human_threshold': 0.4,   # < 0.4 = Human-written
            'uncertainty_zone': (0.4, 0.6)  # Between = Uncertain
        }
    
    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        """
        Phát hiện sử dụng enhanced rule-based approach
        """
        reasoning = []
        feature_importance = {}
        total_score = 0.0
        
        # Apply AI rules
        for rule_name, rule_config in self.ai_rules.items():
            score = self._evaluate_rule(rule_name, rule_config, features)
            if score > 0:
                total_score += score
                feature_importance[rule_name] = score
                reasoning.append(f"{rule_config['description']} (score: +{score:.3f})")
        
        # Apply Human rules  
        for rule_name, rule_config in self.human_rules.items():
            score = self._evaluate_rule(rule_name, rule_config, features)
            if score < 0:
                total_score += score
                feature_importance[rule_name] = abs(score)
                reasoning.append(f"{rule_config['description']} (score: {score:.3f})")
        
        # Normalize score to 0-1 range
        normalized_score = max(0.0, min(1.0, (total_score + 1.0) / 2.0))
        
        # Make decision
        if normalized_score > self.decision_thresholds['ai_threshold']:
            prediction = "AI-generated"
            confidence = normalized_score
        elif normalized_score < self.decision_thresholds['human_threshold']:
            prediction = "Human-written"
            confidence = 1.0 - normalized_score
        else:
            prediction = "Uncertain"
            confidence = 0.5
            reasoning.append("Score in uncertainty zone - cần thêm analysis")
        
        return DetectionResult(
            prediction=prediction,
            confidence=round(confidence, 3),
            reasoning=reasoning[:5],  # Top 5 reasons
            feature_importance=feature_importance,
            method_used="rule-based"
        )
    
    def _evaluate_rule(self, rule_name: str, rule_config: Dict, features: Dict) -> float:
        """Evaluate a single rule"""
        
        # Basic feature rules
        if rule_name == 'high_comment_ratio':
            comment_ratio = features.get('comment_ratio', 0)
            if comment_ratio > rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'descriptive_naming':
            descriptive_ratio = features.get('naming_descriptive_var_ratio', 0)
            if descriptive_ratio > rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'consistent_formatting':
            consistency = features.get('ast_indentation_consistency', 0)
            if consistency > rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'template_usage':
            template_score = features.get('ai_pattern_template_usage_score', 0)
            if template_score > rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'error_handling':
            error_score = features.get('ai_pattern_error_handling_score', 0)
            if error_score > rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'boilerplate_code':
            boilerplate = features.get('ai_pattern_boilerplate_ratio', 0)
            if boilerplate > rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'low_complexity':
            complexity = features.get('cyclomatic_complexity', 10)
            if complexity < rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'structured_code':
            structure_score = features.get('ast_branching_factor', 0)
            if structure_score > rule_config['threshold']:
                return rule_config['weight']
        
        # Human indicator rules
        elif rule_name == 'short_code':
            loc = features.get('loc', 100)
            if loc < rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'generic_variables':
            generic_ratio = features.get('naming_generic_var_ratio', 0)
            if generic_ratio > rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'minimal_comments':
            comment_ratio = features.get('comment_ratio', 0)
            if comment_ratio < rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'inconsistent_style':
            consistency = features.get('ast_indentation_consistency', 1.0)
            if consistency < rule_config['threshold']:
                return rule_config['weight']
        
        elif rule_name == 'pragmatic_approach':
            # Heuristic: short code với ít functions
            loc = features.get('loc', 100)
            functions = features.get('functions', 1)
            if loc < 30 and functions <= 1:
                return rule_config['weight']
        
        return 0.0
    
    def get_name(self) -> str:
        return "Enhanced Rule-Based Detector"

class MLDetector(BaseDetector):
    """
    Machine Learning Detector sử dụng Random Forest và Logistic Regression
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.models = {}
        self.scalers = {}
        self.feature_names = []
        self.is_trained = False
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
    
    def train(self, X: np.ndarray, y: np.ndarray, feature_names: List[str]):
        """
        Train ML models
        """
        if not HAS_SKLEARN:
            raise ValueError("scikit-learn not available for ML training")
        
        self.feature_names = feature_names
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        self.scalers['scaler'] = StandardScaler()
        X_train_scaled = self.scalers['scaler'].fit_transform(X_train)
        X_test_scaled = self.scalers['scaler'].transform(X_test)
        
        # Train Random Forest
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.models['random_forest'].fit(X_train_scaled, y_train)
        
        # Train Logistic Regression
        self.models['logistic'] = LogisticRegression(random_state=42)
        self.models['logistic'].fit(X_train_scaled, y_train)
        
        # Evaluate models
        self._evaluate_models(X_test_scaled, y_test)
        
        self.is_trained = True
    
    def _evaluate_models(self, X_test: np.ndarray, y_test: np.ndarray):
        """Evaluate trained models"""
        for name, model in self.models.items():
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"{name} accuracy: {accuracy:.3f}")
    
    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        """
        Phát hiện sử dụng ML models
        """
        if not self.is_trained:
            raise ValueError("Models not trained yet")
        
        # Convert features to array
        feature_vector = np.array([features.get(name, 0) for name in self.feature_names]).reshape(1, -1)
        feature_vector_scaled = self.scalers['scaler'].transform(feature_vector)
        
        # Get predictions from both models
        rf_pred = self.models['random_forest'].predict(feature_vector_scaled)[0]
        rf_proba = self.models['random_forest'].predict_proba(feature_vector_scaled)[0]
        
        lr_pred = self.models['logistic'].predict(feature_vector_scaled)[0]
        lr_proba = self.models['logistic'].predict_proba(feature_vector_scaled)[0]
        
        # Ensemble prediction (average probabilities)
        avg_proba = (rf_proba + lr_proba) / 2
        final_pred = 1 if avg_proba[1] > 0.5 else 0
        confidence = max(avg_proba)
        
        # Get feature importance
        rf_importance = dict(zip(self.feature_names, self.models['random_forest'].feature_importances_))
        top_features = sorted(rf_importance.items(), key=lambda x: x[1], reverse=True)[:5]
        
        prediction = "AI-generated" if final_pred == 1 else "Human-written"
        reasoning = [f"Feature '{name}' importance: {score:.3f}" for name, score in top_features]
        
        return DetectionResult(
            prediction=prediction,
            confidence=round(confidence, 3),
            reasoning=reasoning,
            feature_importance=rf_importance,
            method_used="ml"
        )
    
    def save_model(self, path: str):
        """Save trained models"""
        model_data = {
            'models': self.models,
            'scalers': self.scalers,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, path: str):
        """Load trained models"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.models = model_data['models']
        self.scalers = model_data['scalers']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
    
    def get_name(self) -> str:
        return "ML Detector (Random Forest + Logistic Regression)"

class HybridDetector(BaseDetector):
    """
    Hybrid Detector kết hợp rule-based và ML
    """
    
    def __init__(self, ml_model_path: Optional[str] = None):
        self.rule_detector = EnhancedRuleBasedDetector()
        self.ml_detector = MLDetector(ml_model_path) if HAS_SKLEARN else None
        self.use_ml = self.ml_detector and self.ml_detector.is_trained
    
    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        """
        Phát hiện sử dụng hybrid approach
        """
        # Always get rule-based result
        rule_result = self.rule_detector.detect(features)
        
        if not self.use_ml:
            # Fallback to rule-based only
            rule_result.method_used = "hybrid-rule-only"
            return rule_result
        
        # Get ML result
        ml_result = self.ml_detector.detect(features)
        
        # Combine results với weighted voting
        rule_weight = 0.4
        ml_weight = 0.6
        
        # Convert predictions to numeric scores
        rule_score = self._prediction_to_score(rule_result.prediction, rule_result.confidence)
        ml_score = self._prediction_to_score(ml_result.prediction, ml_result.confidence)
        
        # Weighted average
        combined_score = rule_weight * rule_score + ml_weight * ml_score
        
        # Convert back to prediction
        if combined_score > 0.6:
            final_prediction = "AI-generated"
            final_confidence = combined_score
        elif combined_score < 0.4:
            final_prediction = "Human-written"
            final_confidence = 1.0 - combined_score
        else:
            final_prediction = "Uncertain"
            final_confidence = 0.5
        
        # Combine reasoning
        combined_reasoning = []
        combined_reasoning.extend([f"Rule: {r}" for r in rule_result.reasoning[:3]])
        combined_reasoning.extend([f"ML: {r}" for r in ml_result.reasoning[:2]])
        
        # Combine feature importance
        combined_importance = {}
        for feature, importance in rule_result.feature_importance.items():
            combined_importance[f"rule_{feature}"] = importance * rule_weight
        
        for feature, importance in ml_result.feature_importance.items():
            combined_importance[f"ml_{feature}"] = importance * ml_weight
        
        return DetectionResult(
            prediction=final_prediction,
            confidence=round(final_confidence, 3),
            reasoning=combined_reasoning,
            feature_importance=combined_importance,
            method_used="hybrid"
        )
    
    def _prediction_to_score(self, prediction: str, confidence: float) -> float:
        """Convert prediction to numeric score (0=Human, 1=AI)"""
        if prediction == "AI-generated":
            return confidence
        elif prediction == "Human-written":
            return 1.0 - confidence
        else:  # Uncertain
            return 0.5
    
    def get_name(self) -> str:
        return "Hybrid Detector (Rule-based + ML)"

# Factory function
def create_detector(detector_type: str = "hybrid", model_path: Optional[str] = None) -> BaseDetector:
    """
    Factory function để tạo detector
    """
    if detector_type == "rule":
        return EnhancedRuleBasedDetector()
    elif detector_type == "ml":
        if not HAS_SKLEARN:
            raise ValueError("scikit-learn not available for ML detector")
        return MLDetector(model_path)
    elif detector_type == "hybrid":
        return HybridDetector(model_path)
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