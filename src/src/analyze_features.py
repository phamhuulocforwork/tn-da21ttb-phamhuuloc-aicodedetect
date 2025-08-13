#!/usr/bin/env python3
"""
Feature Analysis & Visualization Script
Phân tích và tạo charts từ CSV features đã trích xuất
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
import logging
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set style
plt.style.use('default')
sns.set_palette("husl")

class FeatureAnalyzer:
    """Phân tích và visualize đặc trưng từ CSV"""
    
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.df = None
        self.numeric_features = []
        self.categorical_features = []
        
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file không tồn tại: {csv_path}")
        
        self.load_data()
    
    def load_data(self):
        """Load và preprocess data"""
        logger.info(f"Loading data từ {self.csv_path}")
        
        self.df = pd.read_csv(self.csv_path)
        logger.info(f"Loaded {len(self.df)} records")
        
        # Phân loại features
        self.numeric_features = []
        self.categorical_features = []
        
        for col in self.df.columns:
            if col in ['file_path', 'filename', 'label', 'problem_id']:
                self.categorical_features.append(col)
            elif self.df[col].dtype in ['int64', 'float64']:
                self.numeric_features.append(col)
            else:
                self.categorical_features.append(col)
        
        logger.info(f"Numeric features: {len(self.numeric_features)}")
        logger.info(f"Categorical features: {len(self.categorical_features)}")
        
        # Clean data
        self.df = self.df.replace([np.inf, -np.inf], np.nan)
        
        # Fill NaN values
        for col in self.numeric_features:
            self.df[col] = self.df[col].fillna(0)
    
    def basic_statistics(self) -> Dict:
        """Tính toán thống kê cơ bản"""
        stats = {}
        
        # Overall stats
        stats['total_samples'] = len(self.df)
        stats['ai_samples'] = len(self.df[self.df['label'] == 'AI'])
        stats['human_samples'] = len(self.df[self.df['label'] == 'Human'])
        stats['problems'] = self.df['problem_id'].nunique()
        
        logger.info(f"📊 THỐNG KÊ CƠ BẢN:")
        logger.info(f"  Tổng samples: {stats['total_samples']}")
        logger.info(f"  AI samples: {stats['ai_samples']}")
        logger.info(f"  Human samples: {stats['human_samples']}")
        logger.info(f"  Problems: {stats['problems']}")
        
        return stats
    
    def find_discriminative_features(self, top_n: int = 15) -> List[Tuple[str, float]]:
        """Tìm đặc trưng phân biệt mạnh nhất giữa AI và Human"""
        discriminative_scores = []
        
        ai_data = self.df[self.df['label'] == 'AI']
        human_data = self.df[self.df['label'] == 'Human']
        
        for feature in self.numeric_features:
            try:
                ai_mean = ai_data[feature].mean()
                human_mean = human_data[feature].mean()
                ai_std = ai_data[feature].std()
                human_std = human_data[feature].std()
                
                # Cohen's d effect size
                pooled_std = np.sqrt(((len(ai_data) - 1) * ai_std**2 + 
                                    (len(human_data) - 1) * human_std**2) / 
                                   (len(ai_data) + len(human_data) - 2))
                
                if pooled_std > 0:
                    cohens_d = abs(ai_mean - human_mean) / pooled_std
                    discriminative_scores.append((feature, cohens_d))
                
            except Exception as e:
                continue
        
        # Sort by discriminative power
        discriminative_scores.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"🎯 TOP {top_n} ĐẶC TRƯNG PHÂN BIỆT MẠNH NHẤT:")
        for i, (feature, score) in enumerate(discriminative_scores[:top_n]):
            logger.info(f"  {i+1:2d}. {feature:<35} (Cohen's d: {score:.3f})")
        
        return discriminative_scores[:top_n]
    
    def create_comparison_plots(self, output_dir: str = "plots"):
        """Tạo plots so sánh AI vs Human"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Get top discriminative features
        top_features = self.find_discriminative_features(12)
        feature_names = [f[0] for f in top_features]
        
        # 1. Distribution comparison for top features
        fig, axes = plt.subplots(3, 4, figsize=(20, 15))
        axes = axes.flatten()
        
        for i, feature in enumerate(feature_names):
            if i >= 12:
                break
                
            ax = axes[i]
            
            # Plot distributions
            ai_data = self.df[self.df['label'] == 'AI'][feature]
            human_data = self.df[self.df['label'] == 'Human'][feature]
            
            bins = np.linspace(
                min(ai_data.min(), human_data.min()), 
                max(ai_data.max(), human_data.max()), 
                30
            )
            
            ax.hist(ai_data, bins=bins, alpha=0.7, label='AI', color='red', density=True)
            ax.hist(human_data, bins=bins, alpha=0.7, label='Human', color='blue', density=True)
            
            ax.set_title(f'{feature}\n(Cohen\'s d: {top_features[i][1]:.3f})', fontsize=10)
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / "feature_distributions.png", dpi=300, bbox_inches='tight')
        logger.info(f"💾 Saved feature distributions to {output_path}/feature_distributions.png")
        plt.close()
        
        # 2. Mean comparison chart
        fig, ax = plt.subplots(figsize=(14, 8))
        
        ai_means = []
        human_means = []
        feature_labels = []
        
        for feature, _ in top_features[:10]:
            ai_mean = self.df[self.df['label'] == 'AI'][feature].mean()
            human_mean = self.df[self.df['label'] == 'Human'][feature].mean()
            
            ai_means.append(ai_mean)
            human_means.append(human_mean)
            feature_labels.append(feature.replace('_', ' ').title())
        
        x = np.arange(len(feature_labels))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, ai_means, width, label='AI-generated', color='red', alpha=0.7)
        bars2 = ax.bar(x + width/2, human_means, width, label='Human-written', color='blue', alpha=0.7)
        
        ax.set_xlabel('Features')
        ax.set_ylabel('Mean Values')
        ax.set_title('AI vs Human: Mean Feature Values Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(feature_labels, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / "mean_comparison.png", dpi=300, bbox_inches='tight')
        logger.info(f"💾 Saved mean comparison to {output_path}/mean_comparison.png")
        plt.close()
        
        # 3. Correlation matrix for top features
        correlation_features = feature_names[:8]  # Top 8 để matrix dễ đọc
        corr_matrix = self.df[correlation_features].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, fmt='.2f', ax=ax)
        ax.set_title('Feature Correlation Matrix (Top Discriminative Features)')
        
        plt.tight_layout()
        plt.savefig(output_path / "correlation_matrix.png", dpi=300, bbox_inches='tight')
        logger.info(f"💾 Saved correlation matrix to {output_path}/correlation_matrix.png")
        plt.close()
        
        # 4. Box plots for key features
        key_features = feature_names[:6]
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, feature in enumerate(key_features):
            ax = axes[i]
            
            data_to_plot = [
                self.df[self.df['label'] == 'AI'][feature],
                self.df[self.df['label'] == 'Human'][feature]
            ]
            
            box_plot = ax.boxplot(data_to_plot, labels=['AI', 'Human'], patch_artist=True)
            box_plot['boxes'][0].set_facecolor('red')
            box_plot['boxes'][1].set_facecolor('blue')
            
            ax.set_title(f'{feature.replace("_", " ").title()}')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / "boxplots_comparison.png", dpi=300, bbox_inches='tight')
        logger.info(f"💾 Saved box plots to {output_path}/boxplots_comparison.png")
        plt.close()
    
    def analyze_detection_accuracy(self):
        """Phân tích độ chính xác của detection hiện tại"""
        if 'detection_prediction' not in self.df.columns:
            logger.warning("Không có detection prediction data")
            return
        
        # Confusion matrix
        ai_predicted_as_ai = len(self.df[(self.df['label'] == 'AI') & 
                                        (self.df['detection_prediction'] == 'AI-generated')])
        ai_predicted_as_human = len(self.df[(self.df['label'] == 'AI') & 
                                           (self.df['detection_prediction'] == 'Human-written')])
        human_predicted_as_ai = len(self.df[(self.df['label'] == 'Human') & 
                                           (self.df['detection_prediction'] == 'AI-generated')])
        human_predicted_as_human = len(self.df[(self.df['label'] == 'Human') & 
                                              (self.df['detection_prediction'] == 'Human-written')])
        
        total_ai = len(self.df[self.df['label'] == 'AI'])
        total_human = len(self.df[self.df['label'] == 'Human'])
        
        if total_ai > 0:
            ai_accuracy = ai_predicted_as_ai / total_ai
        else:
            ai_accuracy = 0
            
        if total_human > 0:
            human_accuracy = human_predicted_as_human / total_human
        else:
            human_accuracy = 0
        
        overall_accuracy = (ai_predicted_as_ai + human_predicted_as_human) / len(self.df)
        
        logger.info(f"🎯 DETECTION ACCURACY:")
        logger.info(f"  AI detection accuracy: {ai_accuracy:.3f} ({ai_predicted_as_ai}/{total_ai})")
        logger.info(f"  Human detection accuracy: {human_accuracy:.3f} ({human_predicted_as_human}/{total_human})")
        logger.info(f"  Overall accuracy: {overall_accuracy:.3f}")
        
        return {
            'ai_accuracy': ai_accuracy,
            'human_accuracy': human_accuracy, 
            'overall_accuracy': overall_accuracy,
            'confusion_matrix': {
                'ai_as_ai': ai_predicted_as_ai,
                'ai_as_human': ai_predicted_as_human,
                'human_as_ai': human_predicted_as_ai,
                'human_as_human': human_predicted_as_human
            }
        }
    
    def generate_feature_ranking_report(self, output_file: str = "feature_ranking.txt"):
        """Tạo báo cáo ranking đặc trưng"""
        discriminative_features = self.find_discriminative_features(20)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("FEATURE RANKING REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Dataset: {self.csv_path}\n")
            f.write(f"Total samples: {len(self.df)}\n")
            f.write(f"AI samples: {len(self.df[self.df['label'] == 'AI'])}\n")
            f.write(f"Human samples: {len(self.df[self.df['label'] == 'Human'])}\n\n")
            
            f.write("TOP DISCRIMINATIVE FEATURES (Cohen's d):\n")
            f.write("-" * 50 + "\n")
            
            for i, (feature, score) in enumerate(discriminative_features):
                ai_mean = self.df[self.df['label'] == 'AI'][feature].mean()
                human_mean = self.df[self.df['label'] == 'Human'][feature].mean()
                
                f.write(f"{i+1:2d}. {feature:<40} | Cohen's d: {score:.3f}\n")
                f.write(f"    AI mean: {ai_mean:.4f}, Human mean: {human_mean:.4f}\n")
                f.write(f"    {'AI > Human' if ai_mean > human_mean else 'Human > AI'}\n\n")
        
        logger.info(f"💾 Saved feature ranking report to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze extracted features from dataset')
    parser.add_argument('--csv', type=str, required=True, help='Path to CSV file with extracted features')
    parser.add_argument('--plots-dir', type=str, default='plots', help='Directory to save plots')
    parser.add_argument('--report', type=str, default='feature_ranking.txt', help='Feature ranking report file')
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = FeatureAnalyzer(args.csv)
        
        # Basic statistics
        stats = analyzer.basic_statistics()
        
        # Find discriminative features
        top_features = analyzer.find_discriminative_features()
        
        # Create visualizations
        analyzer.create_comparison_plots(args.plots_dir)
        
        # Analyze detection accuracy
        analyzer.analyze_detection_accuracy()
        
        # Generate report
        analyzer.generate_feature_ranking_report(args.report)
        
        logger.info("✅ Analysis completed successfully!")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    exit(main())
