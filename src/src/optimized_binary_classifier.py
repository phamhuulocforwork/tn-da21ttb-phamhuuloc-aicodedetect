#!/usr/bin/env python3
"""
Optimized Binary Classifier
Tối ưu hóa binary classification dựa trên feature analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging
import json
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ClassificationResult:
    """Kết quả classification"""
    prediction: str  # "AI" | "Human" | "Uncertain"
    confidence: float
    reasoning: List[str]
    feature_scores: Dict[str, float]
    method_used: str

class OptimizedBinaryClassifier:
    """
    Binary classifier được tối ưu dựa trên feature analysis
    Không sử dụng ML, chỉ dùng heuristic rules được tune từ data
    """
    
    def __init__(self, feature_analysis_csv: Optional[str] = None):
        self.feature_weights = {}
        self.thresholds = {}
        self.feature_stats = {}
        
        if feature_analysis_csv:
            self.load_feature_analysis(feature_analysis_csv)
        else:
            self.setup_default_weights()
    
    def load_feature_analysis(self, csv_path: str):
        """Load và phân tích data để tự động tính weights"""
        logger.info(f"Loading feature analysis từ {csv_path}")
        
        df = pd.read_csv(csv_path)
        df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
        
        ai_data = df[df['label'] == 'AI']
        human_data = df[df['label'] == 'Human']
        
        logger.info(f"AI samples: {len(ai_data)}, Human samples: {len(human_data)}")
        
        # Tính discriminative power cho từng feature
        discriminative_features = []
        
        numeric_features = df.select_dtypes(include=[np.number]).columns
        exclude_cols = ['file_size', 'detection_confidence']  # Loại bỏ meta features
        numeric_features = [f for f in numeric_features if f not in exclude_cols]
        
        for feature in numeric_features:
            try:
                ai_mean = ai_data[feature].mean()
                human_mean = human_data[feature].mean()
                ai_std = ai_data[feature].std()
                human_std = human_data[feature].std()
                
                # Tính Cohen's d
                pooled_std = np.sqrt(((len(ai_data) - 1) * ai_std**2 + 
                                    (len(human_data) - 1) * human_std**2) / 
                                   (len(ai_data) + len(human_data) - 2))
                
                if pooled_std > 0:
                    cohens_d = abs(ai_mean - human_mean) / pooled_std
                    
                    # Lưu feature stats
                    self.feature_stats[feature] = {
                        'ai_mean': float(ai_mean),
                        'human_mean': float(human_mean),
                        'ai_std': float(ai_std),
                        'human_std': float(human_std),
                        'cohens_d': float(cohens_d),
                        'ai_higher': bool(ai_mean > human_mean)
                    }
                    
                    discriminative_features.append((feature, cohens_d))
                
            except Exception as e:
                logger.warning(f"Error analyzing feature {feature}: {e}")
                continue
        
        # Sort by discriminative power
        discriminative_features.sort(key=lambda x: x[1], reverse=True)
        
        # Tạo weights dựa trên discriminative power
        self.setup_optimized_weights(discriminative_features[:15])  # Top 15 features
        
        logger.info(f"Setup {len(self.feature_weights)} feature weights")
    
    def setup_optimized_weights(self, top_features: List[Tuple[str, float]]):
        """Setup weights dựa trên data analysis"""
        
        # Normalize weights để tổng không quá 1.0
        total_discriminative_power = sum(score for _, score in top_features)
        
        self.feature_weights = {}
        
        for feature, score in top_features:
            # Weight proportional to discriminative power
            weight = (score / total_discriminative_power) * 0.8  # Scale down để tránh overfitting
            
            stats = self.feature_stats[feature]
            
            # Phân loại feature là AI-leaning hay Human-leaning
            if stats['ai_higher']:
                # AI có giá trị cao hơn
                self.feature_weights[f"ai_{feature}"] = weight
            else:
                # Human có giá trị cao hơn  
                self.feature_weights[f"human_{feature}"] = weight
        
        # Set thresholds dựa trên data distribution
        self.thresholds = {
            'ai_threshold': 0.55,    # Giảm threshold AI
            'human_threshold': 0.45, # Tăng threshold Human
            'uncertain_range': 0.10  # Khoảng uncertain
        }
        
        logger.info("Optimized weights based on data analysis:")
        for feature, weight in sorted(self.feature_weights.items(), key=lambda x: x[1], reverse=True)[:10]:
            logger.info(f"  {feature}: {weight:.4f}")
    
    def setup_default_weights(self):
        """Setup default weights nếu không có data analysis"""
        logger.info("Using default feature weights")
        
        # Updated weights dựa trên normalized features analysis
        self.feature_weights = {
            # AI-leaning features (features mà AI thường có giá trị cao hơn)
            'ai_comment_ratio': 0.056,                           # AI có comment structure tốt hơn
            'ai_naming_meaningful_names_score': 0.0096,          # AI naming có ý nghĩa hơn
            'ai_blank_ratio': 0.0388,                           # AI có blank line structure tốt
            'ai_complexity_maintainability_index': 0.04,        # AI code maintainable hơn
            'ai_naming_descriptive_var_ratio': 0.045,           # AI dùng tên biến descriptive
            'ai_ai_pattern_template_usage_score': 0.035,        # AI sử dụng templates
            'ai_ast_avg_variable_name_length': 0.031,           # AI dùng tên biến dài hơn
            'ai_ai_pattern_error_handling_score': 0.025,        # AI có error handling tốt
            'ai_naming_verb_function_ratio': 0.04,              # AI dùng verb functions
            
            # Human-leaning features (features mà Human thường có giá trị cao hơn)
            # CRITICAL: Sử dụng normalized features để tránh bias theo code length
            'human_naming_generic_var_ratio': 0.0555,           # Human dùng tên biến generic nhiều
            'human_ast_nested_control_depth': 0.0477,          # Human nested logic sâu hơn
            'human_ast_nodes_per_loc': 0.0461,                 # Human AST density cao hơn
            'human_ast_single_char_vars_ratio': 0.0436,        # Human single char ratio cao (NORMALIZED)
            'human_ast_max_function_length': 0.0397,           # Human functions dài hơn
            'human_ast_avg_function_length': 0.038,            # Human avg function length cao
            'human_redundancy_duplicate_line_ratio': 0.0377,   # Human có duplicate code nhiều
            'human_complexity_halstead_per_loc': 0.03,         # Human Halstead per LOC cao (NORMALIZED)
            'human_complexity_cognitive_per_loc': 0.025,       # Human cognitive per LOC cao (NORMALIZED)
            'human_ast_for_loops_per_loc': 0.02,               # Human for loops density cao (NORMALIZED)
        }
        
        # Cải thiện thresholds dựa trên pattern analysis
        self.thresholds = {
            'ai_threshold': 0.55,     # Giảm AI threshold để tăng sensitivity
            'human_threshold': 0.45,  # Tăng Human threshold để tăng precision  
            'uncertain_range': 0.10   # Thu nhỏ uncertain range
        }
    
    def extract_classifier_features(self, comprehensive_features: Dict[str, Any]) -> Dict[str, float]:
        """Trích xuất và normalize features cho classifier"""
        features = {}
        
        for weight_key in self.feature_weights.keys():
            # Parse feature name từ weight key
            if weight_key.startswith('ai_'):
                feature_name = weight_key[3:]  # Remove 'ai_' prefix
                direction = 'ai'
            elif weight_key.startswith('human_'):
                feature_name = weight_key[6:]  # Remove 'human_' prefix  
                direction = 'human'
            else:
                continue
            
            # Get raw feature value
            raw_value = float(comprehensive_features.get(feature_name, 0))
            
            # Normalize feature dựa trên training stats nếu có
            if feature_name in self.feature_stats:
                stats = self.feature_stats[feature_name]
                ai_mean = stats['ai_mean']
                human_mean = stats['human_mean']
                
                if direction == 'ai':
                    # Score cao nếu gần với AI mean
                    if ai_mean != human_mean:
                        score = max(0, (raw_value - human_mean) / (ai_mean - human_mean))
                    else:
                        score = 0.5
                else:
                    # Score cao nếu gần với Human mean
                    if ai_mean != human_mean:
                        score = max(0, (ai_mean - raw_value) / (ai_mean - human_mean))
                    else:
                        score = 0.5
                
                # Clamp score
                score = min(1.0, max(0.0, score))
                
            else:
                # Fallback normalization
                if feature_name == 'loc':
                    score = max(0, min(1, (80 - raw_value) / 60)) if direction == 'human' else 0
                elif feature_name == 'comment_ratio':
                    score = min(1, raw_value / 0.3) if direction == 'ai' else max(0, (0.3 - raw_value) / 0.3)
                else:
                    score = min(1, max(0, raw_value))
            
            features[weight_key] = score
        
        return features
    
    def classify(self, comprehensive_features: Dict[str, Any], 
                include_linting: bool = False) -> ClassificationResult:
        """Phân loại code dựa trên comprehensive features"""
        
        # Extract và normalize features
        classifier_features = self.extract_classifier_features(comprehensive_features)
        
        # Tính điểm
        ai_score = 0.5  # Base score
        contributions = {}
        reasoning = []
        
        for feature_key, feature_value in classifier_features.items():
            if feature_key in self.feature_weights:
                weight = self.feature_weights[feature_key]
                contribution = weight * feature_value
                
                if feature_key.startswith('ai_'):
                    ai_score += contribution
                    direction = "AI-leaning"
                else:
                    ai_score -= contribution  
                    direction = "Human-leaning"
                
                contributions[feature_key] = contribution
                
                if contribution > 0.01:  # Only significant contributions
                    feature_name = feature_key.split('_', 1)[1]
                    reasoning.append(f"{feature_name}: {direction} (+{contribution:.3f})")
        
        # Clamp final score
        ai_score = min(1.0, max(0.0, ai_score))
        
        # Classification decision với optimized thresholds
        if ai_score > self.thresholds['ai_threshold']:
            prediction = "AI"
            confidence = ai_score
        elif ai_score < self.thresholds['human_threshold']:
            prediction = "Human"
            confidence = 1.0 - ai_score
        else:
            prediction = "Uncertain"
            confidence = 0.5
        
        # Sort reasoning by contribution
        reasoning.sort(key=lambda x: float(x.split('(+')[1].split(')')[0]), reverse=True)
        
        return ClassificationResult(
            prediction=prediction,
            confidence=round(confidence, 3),
            reasoning=reasoning[:5],  # Top 5 reasons
            feature_scores=contributions,
            method_used="optimized-heuristic-v2"
        )
    
    def evaluate_on_dataset(self, csv_path: str) -> Dict[str, Any]:
        """Đánh giá classifier trên dataset"""
        df = pd.read_csv(csv_path)
        df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
        
        correct_predictions = 0
        total_predictions = 0
        
        ai_correct = 0
        ai_total = 0
        human_correct = 0
        human_total = 0
        
        confusion_matrix = {
            'ai_as_ai': 0,
            'ai_as_human': 0,
            'ai_as_uncertain': 0,
            'human_as_ai': 0,
            'human_as_human': 0,
            'human_as_uncertain': 0
        }
        
        for _, row in df.iterrows():
            features = row.to_dict()
            true_label = features['label']
            
            result = self.classify(features)
            prediction = result.prediction
            
            total_predictions += 1
            
            if true_label == 'AI':
                ai_total += 1
                if prediction == 'AI':
                    correct_predictions += 1
                    ai_correct += 1
                    confusion_matrix['ai_as_ai'] += 1
                elif prediction == 'Human':
                    confusion_matrix['ai_as_human'] += 1
                else:
                    confusion_matrix['ai_as_uncertain'] += 1
                    
            else:  # Human
                human_total += 1
                if prediction == 'Human':
                    correct_predictions += 1
                    human_correct += 1
                    confusion_matrix['human_as_human'] += 1
                elif prediction == 'AI':
                    confusion_matrix['human_as_ai'] += 1
                else:
                    confusion_matrix['human_as_uncertain'] += 1
        
        results = {
            'overall_accuracy': correct_predictions / total_predictions if total_predictions > 0 else 0,
            'ai_accuracy': ai_correct / ai_total if ai_total > 0 else 0,
            'human_accuracy': human_correct / human_total if human_total > 0 else 0,
            'total_samples': total_predictions,
            'ai_samples': ai_total,
            'human_samples': human_total,
            'confusion_matrix': confusion_matrix
        }
        
        return results
    
    def save_model(self, path: str):
        """Lưu classifier parameters"""
        model_data = {
            'feature_weights': self.feature_weights,
            'thresholds': self.thresholds,
            'feature_stats': self.feature_stats,
            'version': 'optimized-v2'
        }
        
        with open(path, 'w') as f:
            json.dump(model_data, f, indent=2)
        
        logger.info(f"Saved optimized classifier to {path}")
    
    def load_model(self, path: str):
        """Load classifier parameters"""
        with open(path, 'r') as f:
            model_data = json.load(f)
        
        self.feature_weights = model_data['feature_weights']
        self.thresholds = model_data['thresholds']
        self.feature_stats = model_data.get('feature_stats', {})
        
        logger.info(f"Loaded optimized classifier from {path}")

def main():
    """Test classifier"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Optimized Binary Classifier')
    parser.add_argument('--train-csv', type=str, help='CSV file for training/optimization')
    parser.add_argument('--test-csv', type=str, help='CSV file for testing')
    parser.add_argument('--save-model', type=str, help='Path to save trained model')
    parser.add_argument('--load-model', type=str, help='Path to load model')
    
    args = parser.parse_args()
    
    # Initialize classifier
    if args.load_model:
        classifier = OptimizedBinaryClassifier()
        classifier.load_model(args.load_model)
    elif args.train_csv:
        classifier = OptimizedBinaryClassifier(args.train_csv)
    else:
        classifier = OptimizedBinaryClassifier()
    
    # Save model if requested
    if args.save_model:
        classifier.save_model(args.save_model)
    
    # Evaluate on test set
    if args.test_csv:
        logger.info(f"Evaluating on {args.test_csv}")
        results = classifier.evaluate_on_dataset(args.test_csv)
        
        print(f"\n🎯 EVALUATION RESULTS:")
        print(f"Overall Accuracy: {results['overall_accuracy']:.3f}")
        print(f"AI Accuracy: {results['ai_accuracy']:.3f} ({results['confusion_matrix']['ai_as_ai']}/{results['ai_samples']})")
        print(f"Human Accuracy: {results['human_accuracy']:.3f} ({results['confusion_matrix']['human_as_human']}/{results['human_samples']})")
        print(f"\nConfusion Matrix:")
        print(f"  AI → AI: {results['confusion_matrix']['ai_as_ai']}")
        print(f"  AI → Human: {results['confusion_matrix']['ai_as_human']}")
        print(f"  AI → Uncertain: {results['confusion_matrix']['ai_as_uncertain']}")
        print(f"  Human → AI: {results['confusion_matrix']['human_as_ai']}")
        print(f"  Human → Human: {results['confusion_matrix']['human_as_human']}")
        print(f"  Human → Uncertain: {results['confusion_matrix']['human_as_uncertain']}")

if __name__ == "__main__":
    main()
