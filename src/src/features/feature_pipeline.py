"""
Automated Feature Pipeline for AI Code Detection
Pipeline tự động cho trích xuất và xử lý features
"""

import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import concurrent.futures
from tqdm import tqdm
import logging

try:
    from .advanced_features import AdvancedFeatureExtractor, ComprehensiveFeatures
    from .detection_models import create_detector, DetectionResult
    HAS_ADVANCED_FEATURES = True
except ImportError:
    HAS_ADVANCED_FEATURES = False
    print("Warning: Advanced features not available.")

@dataclass
class ProcessingStats:
    """Statistics về quá trình processing"""
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    processing_time: float = 0.0
    ai_files: int = 0
    human_files: int = 0

@dataclass
class DatasetInfo:
    """Thông tin về dataset"""
    ai_directory: str
    human_directory: str
    output_directory: str
    max_files_per_class: int = 1000
    file_extensions: List[str] = None
    
    def __post_init__(self):
        if self.file_extensions is None:
            self.file_extensions = ['.c', '.cpp']

class FeaturePipeline:
    """
    Automated pipeline cho feature extraction và processing
    """
    
    def __init__(self, dataset_info: DatasetInfo, use_cache: bool = True):
        self.dataset_info = dataset_info
        self.use_cache = use_cache
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.feature_extractor = AdvancedFeatureExtractor() if HAS_ADVANCED_FEATURES else None
        self.detector = None
        
        # Create output directory
        os.makedirs(dataset_info.output_directory, exist_ok=True)
    
    def extract_features_from_dataset(self, parallel: bool = True, max_workers: int = 4) -> ProcessingStats:
        """
        Trích xuất features từ toàn bộ dataset
        """
        if not self.feature_extractor:
            raise ValueError("Advanced features not available")
        
        self.logger.info("Starting feature extraction from dataset...")
        
        # Collect all files
        ai_files = self._collect_files(self.dataset_info.ai_directory, "ai")
        human_files = self._collect_files(self.dataset_info.human_directory, "human")
        
        # Limit files per class
        ai_files = ai_files[:self.dataset_info.max_files_per_class]
        human_files = human_files[:self.dataset_info.max_files_per_class]
        
        all_files = ai_files + human_files
        
        self.logger.info(f"Found {len(ai_files)} AI files and {len(human_files)} human files")
        
        # Process files
        stats = ProcessingStats(
            total_files=len(all_files),
            ai_files=len(ai_files),
            human_files=len(human_files)
        )
        
        import time
        start_time = time.time()
        
        if parallel and len(all_files) > 10:
            results = self._parallel_feature_extraction(all_files, max_workers)
        else:
            results = self._sequential_feature_extraction(all_files)
        
        stats.processing_time = time.time() - start_time
        stats.successful = len([r for r in results if r is not None])
        stats.failed = stats.total_files - stats.successful
        
        # Save results
        self._save_extracted_features(results)
        
        self.logger.info(f"Feature extraction completed in {stats.processing_time:.2f}s")
        self.logger.info(f"Successful: {stats.successful}, Failed: {stats.failed}")
        
        return stats
    
    def _collect_files(self, directory: str, label: str) -> List[Tuple[str, str]]:
        """Collect files từ directory"""
        files = []
        
        for ext in self.dataset_info.file_extensions:
            pattern = f"**/*{ext}"
            for file_path in Path(directory).glob(pattern):
                if file_path.is_file():
                    files.append((str(file_path), label))
        
        return files
    
    def _parallel_feature_extraction(self, files: List[Tuple[str, str]], max_workers: int) -> List[Optional[Dict]]:
        """Parallel feature extraction"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._extract_features_from_file, file_path, label): (file_path, label)
                for file_path, label in files
            }
            
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(files), desc="Extracting features"):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    file_path, label = futures[future]
                    self.logger.error(f"Error processing {file_path}: {e}")
                    results.append(None)
        
        return results
    
    def _sequential_feature_extraction(self, files: List[Tuple[str, str]]) -> List[Optional[Dict]]:
        """Sequential feature extraction"""
        results = []
        
        for file_path, label in tqdm(files, desc="Extracting features"):
            try:
                result = self._extract_features_from_file(file_path, label)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                results.append(None)
        
        return results
    
    def _extract_features_from_file(self, file_path: str, label: str) -> Optional[Dict]:
        """Extract features từ một file"""
        try:
            # Check cache
            cache_path = self._get_cache_path(file_path)
            if self.use_cache and cache_path.exists():
                with open(cache_path, 'r') as f:
                    cached_data = json.load(f)
                    cached_data['label'] = label  # Update label
                    return cached_data
            
            # Read file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # Extract features
            features = self.feature_extractor.extract_all_features(code, file_path)
            
            # Convert to dict
            feature_dict = features.to_dict()
            feature_dict.update({
                'file_path': file_path,
                'label': label,
                'label_numeric': 1 if label == 'ai' else 0
            })
            
            # Cache result
            if self.use_cache:
                self._save_to_cache(cache_path, feature_dict)
            
            return feature_dict
            
        except Exception as e:
            self.logger.error(f"Failed to extract features from {file_path}: {e}")
            return None
    
    def _get_cache_path(self, file_path: str) -> Path:
        """Get cache path for file"""
        file_hash = hash(file_path)
        cache_dir = Path(self.dataset_info.output_directory) / "cache"
        cache_dir.mkdir(exist_ok=True)
        return cache_dir / f"{file_hash}.json"
    
    def _save_to_cache(self, cache_path: Path, data: Dict):
        """Save data to cache"""
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Failed to save cache {cache_path}: {e}")
    
    def _save_extracted_features(self, results: List[Optional[Dict]]):
        """Save extracted features to files"""
        # Filter out None results
        valid_results = [r for r in results if r is not None]
        
        if not valid_results:
            self.logger.warning("No valid results to save")
            return
        
        # Save as JSON
        json_path = Path(self.dataset_info.output_directory) / "features.json"
        with open(json_path, 'w') as f:
            json.dump(valid_results, f, indent=2)
        
        # Save as CSV
        df = pd.DataFrame(valid_results)
        csv_path = Path(self.dataset_info.output_directory) / "features.csv"
        df.to_csv(csv_path, index=False)
        
        # Save feature summary
        self._save_feature_summary(df)
        
        self.logger.info(f"Features saved to {json_path} and {csv_path}")
    
    def _save_feature_summary(self, df: pd.DataFrame):
        """Save feature summary statistics"""
        summary = {}
        
        # Basic statistics
        summary['total_samples'] = len(df)
        summary['ai_samples'] = len(df[df['label'] == 'ai'])
        summary['human_samples'] = len(df[df['label'] == 'human'])
        
        # Feature statistics
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        feature_stats = {}
        
        for col in numeric_columns:
            if col not in ['label_numeric']:
                feature_stats[col] = {
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'ai_mean': float(df[df['label'] == 'ai'][col].mean()) if 'ai' in df['label'].values else 0,
                    'human_mean': float(df[df['label'] == 'human'][col].mean()) if 'human' in df['label'].values else 0
                }
        
        summary['feature_statistics'] = feature_stats
        
        # Save summary
        summary_path = Path(self.dataset_info.output_directory) / "feature_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.logger.info(f"Feature summary saved to {summary_path}")
    
    def load_features(self) -> Optional[pd.DataFrame]:
        """Load extracted features từ file"""
        csv_path = Path(self.dataset_info.output_directory) / "features.csv"
        
        if not csv_path.exists():
            self.logger.warning(f"Features file not found: {csv_path}")
            return None
        
        try:
            df = pd.read_csv(csv_path)
            self.logger.info(f"Loaded {len(df)} feature samples")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load features: {e}")
            return None
    
    def train_detector(self, detector_type: str = "hybrid") -> bool:
        """
        Train detector với extracted features
        """
        # Load features
        df = self.load_features()
        if df is None:
            return False
        
        # Prepare data for ML
        feature_columns = [col for col in df.columns 
                          if col not in ['file_path', 'label', 'label_numeric'] 
                          and df[col].dtype in ['int64', 'float64']]
        
        X = df[feature_columns].fillna(0).values
        y = df['label_numeric'].values
        
        self.logger.info(f"Training detector with {len(feature_columns)} features and {len(X)} samples")
        
        # Create and train detector
        if detector_type == "ml":
            from .detection_models import MLDetector
            self.detector = MLDetector()
            self.detector.train(X, y, feature_columns)
            
            # Save trained model
            model_path = Path(self.dataset_info.output_directory) / "trained_model.pkl"
            self.detector.save_model(str(model_path))
            self.logger.info(f"Model saved to {model_path}")
            
        else:
            # Create hybrid detector (doesn't need training for rule-based part)
            self.detector = create_detector(detector_type)
        
        return True
    
    def evaluate_detector(self, test_files: Optional[List[Tuple[str, str]]] = None) -> Dict[str, Any]:
        """
        Evaluate detector performance
        """
        if not self.detector:
            raise ValueError("No detector available. Train or load a detector first.")
        
        # Use existing features if no test files provided
        if test_files is None:
            df = self.load_features()
            if df is None:
                raise ValueError("No features available for evaluation")
            
            # Use a sample for evaluation
            test_df = df.sample(min(100, len(df)))
            results = []
            
            for _, row in test_df.iterrows():
                features = row.drop(['file_path', 'label', 'label_numeric']).to_dict()
                prediction = self.detector.detect(features)
                
                results.append({
                    'file_path': row['file_path'],
                    'true_label': row['label'],
                    'predicted_label': prediction.prediction,
                    'confidence': prediction.confidence,
                    'method': prediction.method_used
                })
        
        else:
            # Evaluate on new test files
            results = []
            
            for file_path, true_label in test_files:
                try:
                    feature_dict = self._extract_features_from_file(file_path, true_label)
                    if feature_dict:
                        features = {k: v for k, v in feature_dict.items() 
                                   if k not in ['file_path', 'label', 'label_numeric']}
                        prediction = self.detector.detect(features)
                        
                        results.append({
                            'file_path': file_path,
                            'true_label': true_label,
                            'predicted_label': prediction.prediction,
                            'confidence': prediction.confidence,
                            'method': prediction.method_used
                        })
                except Exception as e:
                    self.logger.error(f"Evaluation error for {file_path}: {e}")
        
        # Calculate metrics
        evaluation_results = self._calculate_evaluation_metrics(results)
        
        # Save evaluation results
        eval_path = Path(self.dataset_info.output_directory) / "evaluation_results.json"
        with open(eval_path, 'w') as f:
            json.dump(evaluation_results, f, indent=2)
        
        self.logger.info(f"Evaluation results saved to {eval_path}")
        return evaluation_results
    
    def _calculate_evaluation_metrics(self, results: List[Dict]) -> Dict[str, Any]:
        """Calculate evaluation metrics"""
        if not results:
            return {'error': 'No results to evaluate'}
        
        # Convert predictions
        y_true = []
        y_pred = []
        confidences = []
        
        for result in results:
            true_label = 1 if result['true_label'] == 'ai' else 0
            
            if result['predicted_label'] == 'AI-generated':
                pred_label = 1
            elif result['predicted_label'] == 'Human-written':
                pred_label = 0
            else:  # Uncertain
                pred_label = 0.5  # Neutral for uncertain
            
            y_true.append(true_label)
            y_pred.append(pred_label)
            confidences.append(result['confidence'])
        
        # Calculate metrics
        y_pred_binary = [1 if p > 0.5 else 0 for p in y_pred]
        
        # Basic metrics
        correct = sum(1 for t, p in zip(y_true, y_pred_binary) if t == p)
        total = len(y_true)
        accuracy = correct / total if total > 0 else 0
        
        # Confusion matrix components
        tp = sum(1 for t, p in zip(y_true, y_pred_binary) if t == 1 and p == 1)
        tn = sum(1 for t, p in zip(y_true, y_pred_binary) if t == 0 and p == 0)
        fp = sum(1 for t, p in zip(y_true, y_pred_binary) if t == 0 and p == 1)
        fn = sum(1 for t, p in zip(y_true, y_pred_binary) if t == 1 and p == 0)
        
        # Precision, Recall, F1
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Average confidence
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'total_samples': total,
            'accuracy': round(accuracy, 3),
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'f1_score': round(f1, 3),
            'confusion_matrix': {
                'true_positive': tp,
                'true_negative': tn,
                'false_positive': fp,
                'false_negative': fn
            },
            'average_confidence': round(avg_confidence, 3),
            'detailed_results': results[:10]  # Save first 10 for inspection
        }

# Utility functions
def create_pipeline_from_config(config_path: str) -> FeaturePipeline:
    """Create pipeline từ config file"""
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    dataset_info = DatasetInfo(**config['dataset'])
    return FeaturePipeline(dataset_info, config.get('use_cache', True))

def run_full_pipeline(
    ai_directory: str,
    human_directory: str, 
    output_directory: str,
    max_files: int = 500,
    detector_type: str = "hybrid"
) -> Dict[str, Any]:
    """
    Run complete pipeline: extract features → train → evaluate
    """
    # Create dataset info
    dataset_info = DatasetInfo(
        ai_directory=ai_directory,
        human_directory=human_directory,
        output_directory=output_directory,
        max_files_per_class=max_files
    )
    
    # Create pipeline
    pipeline = FeaturePipeline(dataset_info)
    
    # Extract features
    print("🔍 Extracting features...")
    stats = pipeline.extract_features_from_dataset()
    
    # Train detector
    print("🧠 Training detector...")
    train_success = pipeline.train_detector(detector_type)
    
    # Evaluate
    print("📊 Evaluating detector...")
    eval_results = pipeline.evaluate_detector()
    
    return {
        'processing_stats': asdict(stats),
        'training_success': train_success,
        'evaluation_results': eval_results
    }

if __name__ == "__main__":
    # Example usage
    example_config = {
        'dataset': {
            'ai_directory': 'src/dataset/code/c/ai',
            'human_directory': 'src/dataset/code/c/human',
            'output_directory': 'src/features/output',
            'max_files_per_class': 100
        },
        'use_cache': True
    }
    
    # Save example config
    with open('pipeline_config.json', 'w') as f:
        json.dump(example_config, f, indent=2)
    
    print("Example config saved to pipeline_config.json")
    print("Run: python -m src.features.feature_pipeline")