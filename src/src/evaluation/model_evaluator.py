"""
Model Evaluation Framework for AI Code Detection
Framework đánh giá hiệu quả của các phương pháp phát hiện
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import json
from collections import defaultdict

try:
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, classification_report, roc_curve, auc,
        precision_recall_curve, average_precision_score
    )
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("Warning: scikit-learn not available. Limited evaluation metrics.")

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOTTING = True
except ImportError:
    HAS_PLOTTING = False
    print("Warning: matplotlib/seaborn not available. No plots will be generated.")

@dataclass
class EvaluationMetrics:
    """Comprehensive evaluation metrics"""
    # Basic metrics
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    
    # Advanced metrics
    specificity: float
    sensitivity: float  # Same as recall
    balanced_accuracy: float
    
    # Confidence metrics
    avg_confidence: float
    confidence_calibration: float
    
    # Confusion matrix
    true_positives: int
    true_negatives: int
    false_positives: int
    false_negatives: int
    
    # ROC/AUC metrics (if available)
    auc_score: Optional[float] = None
    avg_precision_score: Optional[float] = None

@dataclass
class DetailedPrediction:
    """Chi tiết prediction cho analysis"""
    file_path: str
    true_label: str
    predicted_label: str
    confidence: float
    features: Dict[str, Any]
    reasoning: List[str]
    method_used: str
    is_correct: bool

class ModelEvaluator:
    """
    Comprehensive model evaluator với multiple metrics và visualization
    """
    
    def __init__(self, output_dir: str = "evaluation_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Store evaluation data
        self.predictions: List[DetailedPrediction] = []
        self.metrics: Optional[EvaluationMetrics] = None
        
    def evaluate_detector(self, detector, test_data: List[Tuple[Dict, str]], 
                         method_name: str = "detector") -> EvaluationMetrics:
        """
        Evaluate detector trên test data
        """
        predictions = []
        
        print(f"🔍 Evaluating {method_name} on {len(test_data)} samples...")
        
        for features, true_label in test_data:
            try:
                # Get prediction
                detection_result = detector.detect(features)
                
                # Convert labels
                true_binary = 1 if true_label.lower() == 'ai' else 0
                pred_binary = 1 if detection_result.prediction == 'AI-generated' else 0
                
                # Store detailed prediction
                detailed_pred = DetailedPrediction(
                    file_path=features.get('file_path', 'unknown'),
                    true_label=true_label,
                    predicted_label=detection_result.prediction,
                    confidence=detection_result.confidence,
                    features=features,
                    reasoning=detection_result.reasoning,
                    method_used=detection_result.method_used,
                    is_correct=(true_binary == pred_binary)
                )
                
                predictions.append(detailed_pred)
                
            except Exception as e:
                print(f"Error evaluating sample: {e}")
                continue
        
        self.predictions = predictions
        
        # Calculate metrics
        self.metrics = self._calculate_comprehensive_metrics(predictions)
        
        # Save results
        self._save_evaluation_results(method_name)
        
        return self.metrics
    
    def _calculate_comprehensive_metrics(self, predictions: List[DetailedPrediction]) -> EvaluationMetrics:
        """Calculate comprehensive evaluation metrics"""
        
        if not predictions:
            raise ValueError("No predictions to evaluate")
        
        # Convert to binary arrays
        y_true = []
        y_pred = []
        y_scores = []  # Confidence scores
        confidences = []
        
        for pred in predictions:
            true_binary = 1 if pred.true_label.lower() == 'ai' else 0
            
            if pred.predicted_label == 'AI-generated':
                pred_binary = 1
                score = pred.confidence
            elif pred.predicted_label == 'Human-written':
                pred_binary = 0
                score = 1.0 - pred.confidence
            else:  # Uncertain
                pred_binary = 0  # Treat uncertain as human for evaluation
                score = 0.5
            
            y_true.append(true_binary)
            y_pred.append(pred_binary)
            y_scores.append(score)
            confidences.append(pred.confidence)
        
        # Basic confusion matrix components
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
        tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
        
        # Basic metrics
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Advanced metrics
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        sensitivity = recall  # Same as recall
        balanced_accuracy = (sensitivity + specificity) / 2
        
        # Confidence metrics
        avg_confidence = np.mean(confidences) if confidences else 0
        
        # Confidence calibration (how well confidence correlates with accuracy)
        confidence_calibration = 0
        if len(confidences) > 10:
            correct_predictions = [pred.is_correct for pred in predictions]
            correlation = np.corrcoef(confidences, correct_predictions)[0, 1]
            confidence_calibration = max(0, correlation) if not np.isnan(correlation) else 0
        
        # ROC/AUC metrics (if sklearn available)
        auc_score = None
        avg_precision_score = None
        
        if HAS_SKLEARN and len(set(y_true)) > 1:  # Need both classes for ROC
            try:
                fpr, tpr, _ = roc_curve(y_true, y_scores)
                auc_score = auc(fpr, tpr)
                avg_precision_score = average_precision_score(y_true, y_scores)
            except Exception as e:
                print(f"Warning: Could not calculate AUC metrics: {e}")
        
        return EvaluationMetrics(
            accuracy=round(accuracy, 4),
            precision=round(precision, 4),
            recall=round(recall, 4),
            f1_score=round(f1, 4),
            specificity=round(specificity, 4),
            sensitivity=round(sensitivity, 4),
            balanced_accuracy=round(balanced_accuracy, 4),
            avg_confidence=round(avg_confidence, 4),
            confidence_calibration=round(confidence_calibration, 4),
            true_positives=tp,
            true_negatives=tn,
            false_positives=fp,
            false_negatives=fn,
            auc_score=round(auc_score, 4) if auc_score else None,
            avg_precision_score=round(avg_precision_score, 4) if avg_precision_score else None
        )
    
    def _save_evaluation_results(self, method_name: str):
        """Save evaluation results to files"""
        
        # Save metrics
        metrics_dict = {
            'method_name': method_name,
            'total_samples': len(self.predictions),
            'correct_predictions': sum(1 for p in self.predictions if p.is_correct),
            'metrics': self.metrics.__dict__ if self.metrics else {},
            'confusion_matrix': {
                'tp': self.metrics.true_positives if self.metrics else 0,
                'tn': self.metrics.true_negatives if self.metrics else 0,
                'fp': self.metrics.false_positives if self.metrics else 0,
                'fn': self.metrics.false_negatives if self.metrics else 0
            }
        }
        
        metrics_path = self.output_dir / f"{method_name}_metrics.json"
        with open(metrics_path, 'w') as f:
            json.dump(metrics_dict, f, indent=2)
        
        # Save detailed predictions
        predictions_data = []
        for pred in self.predictions:
            pred_dict = {
                'file_path': pred.file_path,
                'true_label': pred.true_label,
                'predicted_label': pred.predicted_label,
                'confidence': pred.confidence,
                'method_used': pred.method_used,
                'is_correct': pred.is_correct,
                'reasoning': pred.reasoning[:3]  # Top 3 reasons
            }
            predictions_data.append(pred_dict)
        
        predictions_path = self.output_dir / f"{method_name}_predictions.json"
        with open(predictions_path, 'w') as f:
            json.dump(predictions_data, f, indent=2)
        
        # Save as CSV for easy analysis
        df = pd.DataFrame(predictions_data)
        csv_path = self.output_dir / f"{method_name}_predictions.csv"
        df.to_csv(csv_path, index=False)
        
        print(f"📊 Evaluation results saved to {self.output_dir}")
    
    def generate_evaluation_report(self, method_name: str = "detector") -> str:
        """Generate comprehensive evaluation report"""
        
        if not self.metrics or not self.predictions:
            return "No evaluation data available"
        
        report = f"""
# AI Code Detection Evaluation Report
## Method: {method_name}

### Summary Statistics
- **Total Samples**: {len(self.predictions)}
- **Correct Predictions**: {sum(1 for p in self.predictions if p.is_correct)}
- **Overall Accuracy**: {self.metrics.accuracy:.2%}

### Performance Metrics
- **Precision**: {self.metrics.precision:.3f} (Of predicted AI, how many are actually AI)
- **Recall (Sensitivity)**: {self.metrics.recall:.3f} (Of actual AI, how many detected)
- **F1-Score**: {self.metrics.f1_score:.3f} (Harmonic mean of precision & recall)
- **Specificity**: {self.metrics.specificity:.3f} (Of actual Human, how many correctly identified)
- **Balanced Accuracy**: {self.metrics.balanced_accuracy:.3f} (Average of sensitivity & specificity)

### Confidence Analysis
- **Average Confidence**: {self.metrics.avg_confidence:.3f}
- **Confidence Calibration**: {self.metrics.confidence_calibration:.3f} (How well confidence correlates with correctness)

### Confusion Matrix
```
                 Predicted
                AI    Human
Actual   AI   {self.metrics.true_positives:4d}    {self.metrics.false_negatives:4d}
        Human {self.metrics.false_positives:4d}    {self.metrics.true_negatives:4d}
```

### Error Analysis
"""
        
        # Add error analysis
        errors = [p for p in self.predictions if not p.is_correct]
        
        if errors:
            report += f"\\n#### Common Error Patterns ({len(errors)} errors)\\n"
            
            # False Positives (Human predicted as AI)
            false_positives = [p for p in errors if p.true_label.lower() == 'human' and p.predicted_label == 'AI-generated']
            if false_positives:
                report += f"\\n**False Positives** ({len(false_positives)}): Human code predicted as AI\\n"
                for fp in false_positives[:3]:  # Show first 3
                    report += f"- {Path(fp.file_path).name}: {fp.reasoning[0] if fp.reasoning else 'No reason given'}\\n"
            
            # False Negatives (AI predicted as Human)
            false_negatives = [p for p in errors if p.true_label.lower() == 'ai' and p.predicted_label == 'Human-written']
            if false_negatives:
                report += f"\\n**False Negatives** ({len(false_negatives)}): AI code predicted as Human\\n"
                for fn in false_negatives[:3]:  # Show first 3
                    report += f"- {Path(fn.file_path).name}: {fn.reasoning[0] if fn.reasoning else 'No reason given'}\\n"
        
        # Add AUC metrics if available
        if self.metrics.auc_score:
            report += f"\\n### Advanced Metrics\\n"
            report += f"- **AUC-ROC**: {self.metrics.auc_score:.3f}\\n"
            report += f"- **Average Precision**: {self.metrics.avg_precision_score:.3f}\\n"
        
        # Save report
        report_path = self.output_dir / f"{method_name}_evaluation_report.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        return report
    
    def plot_evaluation_charts(self, method_name: str = "detector"):
        """Generate evaluation charts"""
        
        if not HAS_PLOTTING or not self.predictions:
            print("Plotting not available or no data")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Evaluation Charts - {method_name}', fontsize=16)
        
        # 1. Confusion Matrix Heatmap
        cm = np.array([[self.metrics.true_negatives, self.metrics.false_positives],
                      [self.metrics.false_negatives, self.metrics.true_positives]])
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Human', 'AI'], yticklabels=['Human', 'AI'],
                   ax=axes[0, 0])
        axes[0, 0].set_title('Confusion Matrix')
        axes[0, 0].set_xlabel('Predicted')
        axes[0, 0].set_ylabel('Actual')
        
        # 2. Confidence Distribution
        confidences = [p.confidence for p in self.predictions]
        correct_confidences = [p.confidence for p in self.predictions if p.is_correct]
        incorrect_confidences = [p.confidence for p in self.predictions if not p.is_correct]
        
        axes[0, 1].hist(correct_confidences, alpha=0.7, label='Correct', bins=20, color='green')
        axes[0, 1].hist(incorrect_confidences, alpha=0.7, label='Incorrect', bins=20, color='red')
        axes[0, 1].set_title('Confidence Distribution')
        axes[0, 1].set_xlabel('Confidence')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].legend()
        
        # 3. Metrics Bar Chart
        metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Specificity']
        metrics_values = [self.metrics.accuracy, self.metrics.precision, 
                         self.metrics.recall, self.metrics.f1_score, self.metrics.specificity]
        
        bars = axes[1, 0].bar(metrics_names, metrics_values, color=['skyblue', 'lightgreen', 'lightcoral', 'gold', 'plum'])
        axes[1, 0].set_title('Performance Metrics')
        axes[1, 0].set_ylabel('Score')
        axes[1, 0].set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, value in zip(bars, metrics_values):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                           f'{value:.3f}', ha='center', va='bottom')
        
        # 4. ROC Curve (if data available)
        if HAS_SKLEARN and self.metrics.auc_score:
            y_true = [1 if p.true_label.lower() == 'ai' else 0 for p in self.predictions]
            y_scores = [p.confidence if p.predicted_label == 'AI-generated' else 1-p.confidence 
                       for p in self.predictions]
            
            fpr, tpr, _ = roc_curve(y_true, y_scores)
            axes[1, 1].plot(fpr, tpr, color='darkorange', lw=2, 
                           label=f'ROC curve (AUC = {self.metrics.auc_score:.3f})')
            axes[1, 1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
            axes[1, 1].set_xlabel('False Positive Rate')
            axes[1, 1].set_ylabel('True Positive Rate')
            axes[1, 1].set_title('ROC Curve')
            axes[1, 1].legend()
        else:
            # Show prediction distribution instead
            ai_predictions = [p for p in self.predictions if p.true_label.lower() == 'ai']
            human_predictions = [p for p in self.predictions if p.true_label.lower() == 'human']
            
            ai_confidences = [p.confidence for p in ai_predictions]
            human_confidences = [p.confidence for p in human_predictions]
            
            axes[1, 1].hist(ai_confidences, alpha=0.7, label='True AI', bins=15, color='red')
            axes[1, 1].hist(human_confidences, alpha=0.7, label='True Human', bins=15, color='blue')
            axes[1, 1].set_title('Confidence by True Label')
            axes[1, 1].set_xlabel('Confidence')
            axes[1, 1].set_ylabel('Frequency')
            axes[1, 1].legend()
        
        plt.tight_layout()
        
        # Save plot
        plot_path = self.output_dir / f"{method_name}_evaluation_charts.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 Evaluation charts saved to {plot_path}")

def compare_detectors(detectors: Dict[str, Any], test_data: List[Tuple[Dict, str]], 
                     output_dir: str = "comparison_output") -> Dict[str, EvaluationMetrics]:
    """
    Compare multiple detectors trên cùng test data
    """
    results = {}
    
    for name, detector in detectors.items():
        print(f"\\n🔍 Evaluating {name}...")
        
        evaluator = ModelEvaluator(f"{output_dir}/{name}")
        metrics = evaluator.evaluate_detector(detector, test_data, name)
        evaluator.generate_evaluation_report(name)
        evaluator.plot_evaluation_charts(name)
        
        results[name] = metrics
    
    # Generate comparison report
    _generate_comparison_report(results, output_dir)
    
    return results

def _generate_comparison_report(results: Dict[str, EvaluationMetrics], output_dir: str):
    """Generate comparison report for multiple detectors"""
    
    comparison = {
        'summary': {},
        'detailed_metrics': {}
    }
    
    for name, metrics in results.items():
        comparison['detailed_metrics'][name] = metrics.__dict__
        comparison['summary'][name] = {
            'accuracy': metrics.accuracy,
            'f1_score': metrics.f1_score,
            'precision': metrics.precision,
            'recall': metrics.recall
        }
    
    # Save comparison
    comparison_path = Path(output_dir) / "detector_comparison.json"
    comparison_path.parent.mkdir(exist_ok=True)
    
    with open(comparison_path, 'w') as f:
        json.dump(comparison, f, indent=2)
    
    # Generate comparison table
    df = pd.DataFrame(comparison['summary']).T
    csv_path = Path(output_dir) / "detector_comparison.csv"
    df.to_csv(csv_path)
    
    print(f"\\n📊 Comparison results saved to {output_dir}")
    print("\\n📈 Performance Summary:")
    print(df.round(3))

if __name__ == "__main__":
    print("Model Evaluator module ready!")
    print("Use: evaluator = ModelEvaluator() to start evaluation")