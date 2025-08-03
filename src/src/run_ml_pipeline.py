#!/usr/bin/env python3
"""
Main Script to Run Complete ML Pipeline for AI Code Detection
Script chính để chạy toàn bộ ML pipeline cho dự án phát hiện code AI
"""

import os
import sys
import argparse
import json
import time
from pathlib import Path
from typing import Dict, Any

# Add src to path để import modules
sys.path.append(str(Path(__file__).parent))

try:
    from features.feature_pipeline import FeaturePipeline, DatasetInfo, run_full_pipeline
    from features.detection_models import create_detector
    from evaluation.model_evaluator import ModelEvaluator, compare_detectors
    print("✅ All ML modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed")
    sys.exit(1)

def setup_directories(output_base: str = "ml_output") -> Dict[str, str]:
    """Setup thư mục output cho pipeline"""
    
    base_path = Path(output_base)
    directories = {
        'base': str(base_path),
        'features': str(base_path / "features"),
        'models': str(base_path / "models"), 
        'evaluation': str(base_path / "evaluation"),
        'comparison': str(base_path / "comparison")
    }
    
    # Tạo directories
    for dir_path in directories.values():
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    return directories

def validate_dataset_paths(ai_dir: str, human_dir: str) -> bool:
    """Validate dataset paths và kiểm tra có files không"""
    
    ai_path = Path(ai_dir)
    human_path = Path(human_dir)
    
    if not ai_path.exists():
        print(f"❌ AI dataset directory not found: {ai_dir}")
        return False
    
    if not human_path.exists():
        print(f"❌ Human dataset directory not found: {human_dir}")
        return False
    
    # Count files
    ai_files = list(ai_path.rglob('*.c')) + list(ai_path.rglob('*.cpp'))
    human_files = list(human_path.rglob('*.c')) + list(human_path.rglob('*.cpp'))
    
    print(f"📁 Found {len(ai_files)} AI files and {len(human_files)} human files")
    
    if len(ai_files) == 0:
        print(f"⚠️  No AI files found in {ai_dir}")
        return False
    
    if len(human_files) == 0:
        print(f"⚠️  No human files found in {human_dir}")
        return False
    
    if len(ai_files) < 10 or len(human_files) < 10:
        print(f"⚠️  Warning: Very few files found. Need at least 10 files per class for meaningful evaluation")
    
    return True

def run_feature_extraction(ai_dir: str, human_dir: str, output_dir: str, 
                          max_files: int = 100, use_parallel: bool = True) -> bool:
    """Run feature extraction pipeline"""
    
    print("\n🔍 === PHASE 1: FEATURE EXTRACTION ===")
    
    dataset_info = DatasetInfo(
        ai_directory=ai_dir,
        human_directory=human_dir,
        output_directory=output_dir,
        max_files_per_class=max_files
    )
    
    pipeline = FeaturePipeline(dataset_info, use_cache=True)
    
    try:
        start_time = time.time()
        stats = pipeline.extract_features_from_dataset(parallel=use_parallel, max_workers=4)
        end_time = time.time()
        
        print(f"✅ Feature extraction completed in {end_time - start_time:.2f}s")
        print(f"   Total files: {stats.total_files}")
        print(f"   Successful: {stats.successful}")
        print(f"   Failed: {stats.failed}")
        print(f"   AI files: {stats.ai_files}")
        print(f"   Human files: {stats.human_files}")
        
        if stats.successful < 20:
            print("⚠️  Warning: Very few successful extractions. Check dataset quality.")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Feature extraction failed: {e}")
        return False

def run_model_training(features_dir: str, models_dir: str) -> Dict[str, Any]:
    """Train and save models"""
    
    print("\n🧠 === PHASE 2: MODEL TRAINING ===")
    
    # Load features
    dataset_info = DatasetInfo(
        ai_directory="dummy",  # Not used for loading
        human_directory="dummy",
        output_directory=features_dir
    )
    
    pipeline = FeaturePipeline(dataset_info)
    
    results = {}
    
    try:
        # Try to train ML model
        print("🔬 Training ML models...")
        ml_success = pipeline.train_detector("ml")
        
        if ml_success:
            print("✅ ML model training successful")
            
            # Move trained model to models directory
            model_source = Path(features_dir) / "trained_model.pkl"
            model_dest = Path(models_dir) / "ml_model.pkl"
            
            if model_source.exists():
                import shutil
                shutil.copy2(model_source, model_dest)
                print(f"📁 ML model saved to {model_dest}")
            
            results['ml_model'] = str(model_dest)
        else:
            print("❌ ML model training failed")
            
    except Exception as e:
        print(f"⚠️  ML training error: {e}")
        
    # Rule-based model doesn't need training
    print("✅ Rule-based detector ready (no training needed)")
    results['rule_based'] = "ready"
    
    # Hybrid model  
    print("✅ Hybrid detector ready")
    results['hybrid'] = "ready"
    
    return results

def run_model_evaluation(features_dir: str, models_dir: str, evaluation_dir: str,
                        model_results: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate trained models"""
    
    print("\n📊 === PHASE 3: MODEL EVALUATION ===")
    
    # Load test data
    dataset_info = DatasetInfo(
        ai_directory="dummy",
        human_directory="dummy", 
        output_directory=features_dir
    )
    
    pipeline = FeaturePipeline(dataset_info)
    df = pipeline.load_features()
    
    if df is None:
        print("❌ Could not load features for evaluation")
        return {}
    
    # Prepare test data
    feature_columns = [col for col in df.columns 
                      if col not in ['file_path', 'label', 'label_numeric']
                      and df[col].dtype in ['int64', 'float64']]
    
    # Take sample for evaluation (to avoid memory issues)
    sample_size = min(200, len(df))
    test_df = df.sample(sample_size, random_state=42)
    
    test_data = []
    for _, row in test_df.iterrows():
        features = row[feature_columns].fillna(0).to_dict()
        features['file_path'] = row.get('file_path', 'unknown')
        label = row['label']
        test_data.append((features, label))
    
    print(f"🧪 Evaluating on {len(test_data)} test samples")
    
    # Create detectors for evaluation
    detectors = {}
    
    # Rule-based detector
    try:
        detectors['Rule-Based'] = create_detector("rule")
        print("✅ Rule-based detector created")
    except Exception as e:
        print(f"❌ Rule-based detector error: {e}")
    
    # ML detector (if available)
    ml_model_path = model_results.get('ml_model')
    if ml_model_path and Path(ml_model_path).exists():
        try:
            detectors['ML'] = create_detector("ml", ml_model_path)
            print("✅ ML detector loaded")
        except Exception as e:
            print(f"❌ ML detector error: {e}")
    
    # Hybrid detector
    try:
        hybrid_model_path = ml_model_path if ml_model_path and Path(ml_model_path).exists() else None
        detectors['Hybrid'] = create_detector("hybrid", hybrid_model_path)
        print("✅ Hybrid detector created")
    except Exception as e:
        print(f"❌ Hybrid detector error: {e}")
    
    if not detectors:
        print("❌ No detectors available for evaluation")
        return {}
    
    # Run comparison evaluation
    print(f"🔬 Comparing {len(detectors)} detectors...")
    
    try:
        comparison_results = compare_detectors(detectors, test_data, evaluation_dir)
        
        print("\\n📈 EVALUATION RESULTS:")
        for name, metrics in comparison_results.items():
            print(f"\\n{name}:")
            print(f"  Accuracy: {metrics.accuracy:.3f}")
            print(f"  Precision: {metrics.precision:.3f}")
            print(f"  Recall: {metrics.recall:.3f}")
            print(f"  F1-Score: {metrics.f1_score:.3f}")
        
        return {name: metrics.__dict__ for name, metrics in comparison_results.items()}
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        return {}

def generate_final_report(directories: Dict[str, str], model_results: Dict[str, Any], 
                         evaluation_results: Dict[str, Any]):
    """Generate final comprehensive report"""
    
    print("\\n📋 === GENERATING FINAL REPORT ===")
    
    report = {
        'pipeline_summary': {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'directories': directories,
            'model_training_results': model_results,
            'evaluation_results': evaluation_results
        },
        'best_performer': None,
        'recommendations': []
    }
    
    # Find best performing model
    if evaluation_results:
        best_f1 = 0
        best_model = None
        
        for model_name, metrics in evaluation_results.items():
            f1_score = metrics.get('f1_score', 0)
            if f1_score > best_f1:
                best_f1 = f1_score
                best_model = model_name
        
        if best_model:
            report['best_performer'] = {
                'model': best_model,
                'f1_score': best_f1,
                'metrics': evaluation_results[best_model]
            }
    
    # Generate recommendations
    recommendations = []
    
    if not evaluation_results:
        recommendations.append("❌ No evaluation results available - check pipeline errors")
    else:
        # Performance-based recommendations
        for model_name, metrics in evaluation_results.items():
            accuracy = metrics.get('accuracy', 0)
            f1_score = metrics.get('f1_score', 0)
            
            if accuracy < 0.7:
                recommendations.append(f"⚠️  {model_name} accuracy ({accuracy:.3f}) below 70% - consider more training data")
            
            if f1_score < 0.6:
                recommendations.append(f"⚠️  {model_name} F1-score ({f1_score:.3f}) below 60% - review feature selection")
        
        # General recommendations
        recommendations.append("✅ Consider combining multiple detectors for better performance")
        recommendations.append("📊 Monitor performance on new data regularly")
        recommendations.append("🔄 Retrain models as more data becomes available")
    
    report['recommendations'] = recommendations
    
    # Save final report
    report_path = Path(directories['base']) / "final_pipeline_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Generate summary
    summary_path = Path(directories['base']) / "PIPELINE_SUMMARY.md"
    with open(summary_path, 'w') as f:
        f.write("# AI Code Detection ML Pipeline Results\\n\\n")
        
        if report['best_performer']:
            f.write(f"## 🏆 Best Performing Model: {report['best_performer']['model']}\\n")
            f.write(f"- **F1-Score**: {report['best_performer']['f1_score']:.3f}\\n")
            f.write(f"- **Accuracy**: {report['best_performer']['metrics']['accuracy']:.3f}\\n")
            f.write(f"- **Precision**: {report['best_performer']['metrics']['precision']:.3f}\\n")
            f.write(f"- **Recall**: {report['best_performer']['metrics']['recall']:.3f}\\n\\n")
        
        f.write("## 📝 Recommendations\\n")
        for rec in recommendations:
            f.write(f"- {rec}\\n")
        
        f.write(f"\\n## 📁 Output Files\\n")
        f.write(f"- Features: `{directories['features']}/`\\n")
        f.write(f"- Models: `{directories['models']}/`\\n") 
        f.write(f"- Evaluation: `{directories['evaluation']}/`\\n")
        f.write(f"- Full Report: `{report_path}`\\n")
    
    print(f"✅ Final report saved to {report_path}")
    print(f"📋 Summary available at {summary_path}")

def main():
    """Main function to run complete ML pipeline"""
    
    parser = argparse.ArgumentParser(description="AI Code Detection ML Pipeline")
    parser.add_argument("--ai-dir", default="dataset/code/c/ai", 
                       help="Directory containing AI-generated code")
    parser.add_argument("--human-dir", default="dataset/code/c/human",
                       help="Directory containing human-written code")
    parser.add_argument("--output-dir", default="ml_output",
                       help="Base output directory")
    parser.add_argument("--max-files", type=int, default=100,
                       help="Maximum files per class to process")
    parser.add_argument("--no-parallel", action="store_true",
                       help="Disable parallel processing")
    parser.add_argument("--skip-extraction", action="store_true",
                       help="Skip feature extraction (use existing)")
    parser.add_argument("--skip-training", action="store_true", 
                       help="Skip model training")
    parser.add_argument("--evaluation-only", action="store_true",
                       help="Run evaluation only")
    
    args = parser.parse_args()
    
    print("🚀 === AI CODE DETECTION ML PIPELINE ===")
    print(f"AI Directory: {args.ai_dir}")
    print(f"Human Directory: {args.human_dir}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Max Files per Class: {args.max_files}")
    
    # Setup directories
    directories = setup_directories(args.output_dir)
    
    # Validate dataset
    if not args.evaluation_only and not args.skip_extraction:
        if not validate_dataset_paths(args.ai_dir, args.human_dir):
            print("❌ Dataset validation failed")
            return 1
    
    model_results = {}
    evaluation_results = {}
    
    try:
        # Phase 1: Feature Extraction
        if not args.skip_extraction and not args.evaluation_only:
            success = run_feature_extraction(
                args.ai_dir, args.human_dir, directories['features'],
                args.max_files, not args.no_parallel
            )
            if not success:
                print("❌ Feature extraction failed")
                return 1
        
        # Phase 2: Model Training  
        if not args.skip_training and not args.evaluation_only:
            model_results = run_model_training(directories['features'], directories['models'])
        
        # Phase 3: Model Evaluation
        evaluation_results = run_model_evaluation(
            directories['features'], directories['models'], 
            directories['evaluation'], model_results
        )
        
        # Generate final report
        generate_final_report(directories, model_results, evaluation_results)
        
        print("\\n🎉 === PIPELINE COMPLETED SUCCESSFULLY ===")
        print(f"📁 All results saved to: {directories['base']}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\\n⚠️  Pipeline interrupted by user")
        return 1
    except Exception as e:
        print(f"\\n❌ Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)