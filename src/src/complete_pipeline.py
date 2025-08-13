#!/usr/bin/env python3
"""
Complete AI Code Detection Pipeline
Pipeline hoàn chỉnh cho phân tích và phân loại mã nguồn AI vs Human
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

# Import our modules
try:
    from features.advanced_features import AdvancedFeatureExtractor
    from optimized_binary_classifier import OptimizedBinaryClassifier
    from super_linter_integration import SuperLinterIntegration
    from batch_feature_extraction import DatasetFeatureExtractor
    HAS_ADVANCED_FEATURES = True
except ImportError as e:
    print(f"Warning: Some modules not available: {e}")
    HAS_ADVANCED_FEATURES = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AICodeDetectionPipeline:
    """Pipeline hoàn chỉnh cho phân tích mã nguồn"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.feature_extractor = AdvancedFeatureExtractor() if HAS_ADVANCED_FEATURES else None
        self.linter = SuperLinterIntegration()
        
        # Load hoặc initialize classifier
        self.classifier = OptimizedBinaryClassifier()
        if model_path and Path(model_path).exists():
            self.classifier.load_model(model_path)
            logger.info(f"Loaded trained model từ {model_path}")
        else:
            logger.info("Using default classifier weights")
    
    def analyze_single_code(self, code: str, filename: str = "code.c", 
                           include_linting: bool = True) -> Dict[str, Any]:
        """Phân tích một đoạn code"""
        
        result = {
            'filename': filename,
            'code_length': len(code),
            'lines_of_code': len(code.splitlines())
        }
        
        try:
            # 1. Feature extraction
            if self.feature_extractor:
                logger.info("Extracting comprehensive features...")
                features = self.feature_extractor.extract_all_features(code, filename)
                feature_dict = features.to_dict()
                result['features'] = feature_dict
            else:
                logger.warning("Advanced feature extraction not available")
                result['features'] = {}
            
            # 2. Linting analysis
            if include_linting:
                logger.info("Running linting analysis...")
                lint_results = self.linter.comprehensive_lint(code, filename)
                result['linting'] = {
                    'total_issues': lint_results['total_issues'],
                    'errors': lint_results['total_errors'],
                    'warnings': lint_results['total_warnings'],
                    'style_issues': lint_results['total_style_issues'],
                    'avg_complexity': lint_results['avg_complexity'],
                    'tools_used': lint_results['total_tools_used']
                }
            
            # 3. Classification
            logger.info("Running classification...")
            classification = self.classifier.classify(
                result['features'], 
                include_linting=include_linting
            )
            
            result['classification'] = {
                'prediction': classification.prediction,
                'confidence': classification.confidence,
                'reasoning': classification.reasoning,
                'method': classification.method_used
            }
            
            # 4. Summary
            result['summary'] = self._generate_summary(result)
            
        except Exception as e:
            logger.error(f"Error analyzing code: {e}")
            result['error'] = str(e)
        
        return result
    
    def analyze_file(self, file_path: str, include_linting: bool = True) -> Dict[str, Any]:
        """Phân tích một file code"""
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File không tồn tại: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            return self.analyze_single_code(code, str(file_path), include_linting)
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    def batch_analyze_directory(self, directory: str, pattern: str = "*.c", 
                               max_files: int = 100, include_linting: bool = False) -> List[Dict[str, Any]]:
        """Phân tích batch một directory"""
        
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"Directory không tồn tại: {directory}")
        
        # Find files
        files = list(directory.rglob(pattern))[:max_files]
        logger.info(f"Found {len(files)} files matching pattern {pattern}")
        
        results = []
        
        for file_path in files:
            try:
                result = self.analyze_file(str(file_path), include_linting)
                results.append(result)
                
                logger.info(f"✅ {file_path.name}: {result['classification']['prediction']} "
                           f"({result['classification']['confidence']:.3f})")
                
            except Exception as e:
                logger.error(f"❌ Error analyzing {file_path}: {e}")
                continue
        
        return results
    
    def train_on_dataset(self, dataset_path: str, max_files: int = 1000, 
                        save_model: Optional[str] = None) -> Dict[str, Any]:
        """Train classifier trên dataset"""
        
        logger.info(f"Training classifier on dataset: {dataset_path}")
        
        # Extract features từ dataset
        extractor = DatasetFeatureExtractor(dataset_path)
        df = extractor.process_dataset(max_files=max_files)
        
        if df.empty:
            raise ValueError("No data extracted from dataset")
        
        # Save extracted features
        features_csv = "training_features.csv"
        extractor.save_to_csv(df, features_csv)
        
        # Initialize optimized classifier
        self.classifier = OptimizedBinaryClassifier(features_csv)
        
        # Evaluate performance
        evaluation = self.classifier.evaluate_on_dataset(features_csv)
        
        # Save trained model
        if save_model:
            self.classifier.save_model(save_model)
            logger.info(f"Saved trained model to {save_model}")
        
        return {
            'training_samples': len(df),
            'ai_samples': len(df[df['label'] == 'AI']),
            'human_samples': len(df[df['label'] == 'Human']),
            'evaluation': evaluation,
            'features_csv': features_csv,
            'model_path': save_model
        }
    
    def _generate_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo summary cho kết quả phân tích"""
        
        summary = {
            'file_info': {
                'filename': result['filename'],
                'size_bytes': result['code_length'],
                'lines': result['lines_of_code']
            }
        }
        
        # Classification summary
        if 'classification' in result:
            cls = result['classification']
            summary['prediction'] = {
                'label': cls['prediction'],
                'confidence': cls['confidence'],
                'top_reasons': cls['reasoning'][:3]
            }
        
        # Feature highlights
        if 'features' in result:
            features = result['features']
            summary['code_characteristics'] = {
                'complexity': features.get('complexity_cognitive_complexity', 0),
                'comment_ratio': features.get('comment_ratio', 0),
                'functions': features.get('functions', 0),
                'variables': features.get('ast_variable_count', 0)
            }
        
        # Quality metrics
        if 'linting' in result:
            lint = result['linting']
            summary['quality_metrics'] = {
                'total_issues': lint['total_issues'],
                'error_rate': lint['errors'] / max(result['lines_of_code'], 1),
                'complexity_score': lint['avg_complexity']
            }
        
        return summary

def main():
    parser = argparse.ArgumentParser(description='AI Code Detection Pipeline')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze single file
    analyze_parser = subparsers.add_parser('analyze', help='Analyze single file')
    analyze_parser.add_argument('file', help='Path to code file')
    analyze_parser.add_argument('--model', help='Path to trained model')
    analyze_parser.add_argument('--no-linting', action='store_true', help='Skip linting analysis')
    analyze_parser.add_argument('--output', help='Output JSON file')
    
    # Batch analyze directory
    batch_parser = subparsers.add_parser('batch', help='Batch analyze directory')
    batch_parser.add_argument('directory', help='Directory to analyze')
    batch_parser.add_argument('--pattern', default='*.c', help='File pattern (default: *.c)')
    batch_parser.add_argument('--max-files', type=int, default=100, help='Maximum files to analyze')
    batch_parser.add_argument('--model', help='Path to trained model')
    batch_parser.add_argument('--output', help='Output JSON file')
    
    # Train on dataset
    train_parser = subparsers.add_parser('train', help='Train classifier on dataset')
    train_parser.add_argument('dataset', help='Path to dataset directory')
    train_parser.add_argument('--max-files', type=int, default=1000, help='Maximum files for training')
    train_parser.add_argument('--save-model', help='Path to save trained model')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Initialize pipeline
        model_path = getattr(args, 'model', None)
        pipeline = AICodeDetectionPipeline(model_path)
        
        if args.command == 'analyze':
            logger.info(f"Analyzing file: {args.file}")
            
            result = pipeline.analyze_file(
                args.file, 
                include_linting=not args.no_linting
            )
            
            # Print summary
            summary = result['summary']
            print(f"\n🔍 ANALYSIS RESULTS for {summary['file_info']['filename']}")
            print(f"📊 Prediction: {summary['prediction']['label']} "
                  f"(confidence: {summary['prediction']['confidence']:.3f})")
            print(f"📝 File: {summary['file_info']['lines']} lines, "
                  f"{summary['file_info']['size_bytes']} bytes")
            
            if 'quality_metrics' in summary:
                qm = summary['quality_metrics']
                print(f"🔧 Quality: {qm['total_issues']} issues, "
                      f"complexity: {qm['complexity_score']:.1f}")
            
            print(f"💡 Top reasons:")
            for reason in summary['prediction']['top_reasons']:
                print(f"   • {reason}")
            
            # Save detailed results
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"💾 Detailed results saved to {args.output}")
        
        elif args.command == 'batch':
            logger.info(f"Batch analyzing directory: {args.directory}")
            
            results = pipeline.batch_analyze_directory(
                args.directory,
                pattern=args.pattern,
                max_files=args.max_files,
                include_linting=False  # Skip linting for batch to speed up
            )
            
            # Summary statistics
            total = len(results)
            ai_count = len([r for r in results if r['classification']['prediction'] == 'AI'])
            human_count = len([r for r in results if r['classification']['prediction'] == 'Human'])
            uncertain_count = len([r for r in results if r['classification']['prediction'] == 'Uncertain'])
            
            print(f"\n📊 BATCH ANALYSIS SUMMARY")
            print(f"Total files analyzed: {total}")
            print(f"AI-generated: {ai_count} ({ai_count/total*100:.1f}%)")
            print(f"Human-written: {human_count} ({human_count/total*100:.1f}%)")
            print(f"Uncertain: {uncertain_count} ({uncertain_count/total*100:.1f}%)")
            
            # Save results
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"💾 Results saved to {args.output}")
        
        elif args.command == 'train':
            logger.info(f"Training on dataset: {args.dataset}")
            
            training_result = pipeline.train_on_dataset(
                args.dataset,
                max_files=args.max_files,
                save_model=args.save_model
            )
            
            eval_result = training_result['evaluation']
            
            print(f"\n🎯 TRAINING RESULTS")
            print(f"Training samples: {training_result['training_samples']}")
            print(f"AI samples: {training_result['ai_samples']}")
            print(f"Human samples: {training_result['human_samples']}")
            print(f"\n📊 EVALUATION")
            print(f"Overall Accuracy: {eval_result['overall_accuracy']:.3f}")
            print(f"AI Accuracy: {eval_result['ai_accuracy']:.3f}")
            print(f"Human Accuracy: {eval_result['human_accuracy']:.3f}")
            
            if args.save_model:
                print(f"💾 Model saved to {args.save_model}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    exit(main())
