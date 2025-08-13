#!/usr/bin/env python3
"""
Batch Feature Extraction Pipeline
Trích xuất đặc trưng từ toàn bộ dataset và xuất thành CSV để phân tích
"""

import os
import csv
import sys
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import asdict
import argparse
from tqdm import tqdm
import traceback

# Add src to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from features.advanced_features import AdvancedFeatureExtractor, ComprehensiveFeatures
    from features.detection_models import create_detector
    HAS_ADVANCED_FEATURES = True
except ImportError as e:
    print(f"Warning: Advanced features not available: {e}")
    HAS_ADVANCED_FEATURES = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('feature_extraction.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DatasetFeatureExtractor:
    """Pipeline để trích xuất đặc trưng từ toàn bộ dataset"""
    
    def __init__(self, dataset_root: str):
        self.dataset_root = Path(dataset_root)
        self.extractor = AdvancedFeatureExtractor() if HAS_ADVANCED_FEATURES else None
        self.detector = create_detector("heuristic") if HAS_ADVANCED_FEATURES else None
        
        # Verification
        if not self.dataset_root.exists():
            raise ValueError(f"Dataset path không tồn tại: {dataset_root}")
        
        logger.info(f"Khởi tạo DatasetFeatureExtractor với dataset: {dataset_root}")
        logger.info(f"Advanced features available: {HAS_ADVANCED_FEATURES}")
    
    def find_code_files(self) -> List[Tuple[str, str, str]]:
        """
        Tìm tất cả files code trong dataset
        Returns: List of (file_path, label, problem_id)
        """
        files = []
        
        # AI generated code
        ai_path = self.dataset_root / "code" / "c" / "ai"
        if ai_path.exists():
            for problem_dir in sorted(ai_path.iterdir()):
                if problem_dir.is_dir():
                    problem_id = problem_dir.name
                    for file_path in sorted(problem_dir.glob("*.c")):
                        files.append((str(file_path), "AI", problem_id))
                    for file_path in sorted(problem_dir.glob("*.cpp")):
                        files.append((str(file_path), "AI", problem_id))
        
        # Human written code  
        human_path = self.dataset_root / "code" / "c" / "human"
        if human_path.exists():
            for problem_dir in sorted(human_path.iterdir()):
                if problem_dir.is_dir():
                    problem_id = problem_dir.name
                    for file_path in sorted(problem_dir.glob("*.c")):
                        files.append((str(file_path), "Human", problem_id))
                    for file_path in sorted(problem_dir.glob("*.cpp")):
                        files.append((str(file_path), "Human", problem_id))
        
        # Shuffle để mix AI và Human files
        import random
        random.shuffle(files)
        
        logger.info(f"Tìm thấy {len(files)} files code")
        ai_count = len([f for f in files if f[1] == 'AI'])
        human_count = len([f for f in files if f[1] == 'Human'])
        logger.info(f"  - AI files: {ai_count}")
        logger.info(f"  - Human files: {human_count}")
        return files
    
    def extract_features_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Trích xuất features từ một file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            if not code.strip():
                logger.warning(f"File rỗng: {file_path}")
                return None
                
            # Extract comprehensive features
            if self.extractor:
                features = self.extractor.extract_all_features(code, file_path)
                feature_dict = features.to_dict()
                
                # Add detection result
                if self.detector:
                    detection = self.detector.detect(feature_dict)
                    feature_dict.update({
                        'detection_prediction': detection.prediction,
                        'detection_confidence': detection.confidence,
                        'detection_method': detection.method_used
                    })
                
                return feature_dict
            else:
                # Fallback to basic features
                lines = code.splitlines()
                return {
                    'loc': len(lines),
                    'comment_ratio': len([l for l in lines if l.strip().startswith('//') or '/*' in l]) / len(lines) if lines else 0,
                    'blank_ratio': len([l for l in lines if not l.strip()]) / len(lines) if lines else 0
                }
                
        except Exception as e:
            logger.error(f"Lỗi trích xuất features từ {file_path}: {e}")
            return None
    
    def process_dataset(self, max_files: Optional[int] = None, 
                       problems_limit: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Xử lý toàn bộ dataset và trích xuất features
        
        Args:
            max_files: Giới hạn số files xử lý (None = không giới hạn)
            problems_limit: Chỉ xử lý những problem cụ thể
        """
        files = self.find_code_files()
        
        # Filter by problems if specified
        if problems_limit:
            files = [(f, l, p) for f, l, p in files if p in problems_limit]
            logger.info(f"Lọc theo problems {problems_limit}: {len(files)} files")
        
        # Limit files if specified
        if max_files:
            files = files[:max_files]
            logger.info(f"Giới hạn {max_files} files đầu tiên")
        
        results = []
        
        logger.info(f"Bắt đầu xử lý {len(files)} files...")
        
        for file_path, label, problem_id in tqdm(files, desc="Extracting features"):
            try:
                features = self.extract_features_from_file(file_path)
                
                if features:
                    # Add metadata
                    features.update({
                        'file_path': file_path,
                        'filename': Path(file_path).name,
                        'label': label,
                        'problem_id': problem_id,
                        'file_extension': Path(file_path).suffix,
                        'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
                    })
                    
                    results.append(features)
                
            except Exception as e:
                logger.error(f"Lỗi xử lý file {file_path}: {e}")
                continue
        
        logger.info(f"Hoàn thành xử lý. Có {len(results)} kết quả hợp lệ")
        
        if not results:
            logger.warning("Không có kết quả nào được trích xuất!")
            return pd.DataFrame()
        
        return pd.DataFrame(results)
    
    def save_to_csv(self, df: pd.DataFrame, output_path: str):
        """Lưu DataFrame thành CSV"""
        try:
            df.to_csv(output_path, index=False, encoding='utf-8')
            logger.info(f"Đã lưu {len(df)} records vào {output_path}")
        except Exception as e:
            logger.error(f"Lỗi lưu CSV: {e}")
            raise
    
    def generate_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Tạo summary statistics"""
        stats = {}
        
        if df.empty:
            return stats
        
        # Basic counts
        stats['total_files'] = len(df)
        stats['ai_files'] = len(df[df['label'] == 'AI'])
        stats['human_files'] = len(df[df['label'] == 'Human'])
        stats['problems_count'] = df['problem_id'].nunique()
        
        # Feature statistics
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            if col in df.columns:
                stats[f'{col}_mean'] = df[col].mean()
                stats[f'{col}_std'] = df[col].std()
                stats[f'{col}_ai_mean'] = df[df['label'] == 'AI'][col].mean()
                stats[f'{col}_human_mean'] = df[df['label'] == 'Human'][col].mean()
        
        return stats

def main():
    parser = argparse.ArgumentParser(description='Extract features from code dataset')
    parser.add_argument('--dataset', type=str, default='dataset', 
                       help='Path to dataset directory')
    parser.add_argument('--output', type=str, default='extracted_features.csv',
                       help='Output CSV file path')
    parser.add_argument('--max-files', type=int, default=None,
                       help='Maximum number of files to process')
    parser.add_argument('--problems', type=str, nargs='*', default=None,
                       help='Specific problems to process (e.g. problem_1 problem_2)')
    parser.add_argument('--stats-output', type=str, default='feature_stats.json',
                       help='Output file for statistics')
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor
        extractor = DatasetFeatureExtractor(args.dataset)
        
        # Process dataset
        df = extractor.process_dataset(
            max_files=args.max_files,
            problems_limit=args.problems
        )
        
        if df.empty:
            logger.error("Không có dữ liệu để xuất!")
            return 1
        
        # Save results
        extractor.save_to_csv(df, args.output)
        
        # Generate and save statistics
        stats = extractor.generate_summary_stats(df)
        
        import json
        with open(args.stats_output, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Đã lưu statistics vào {args.stats_output}")
        
        # Print summary
        print(f"\n🎯 TỔNG KẾT:")
        print(f"📁 Tổng files: {stats['total_files']}")
        print(f"🤖 AI files: {stats['ai_files']}")
        print(f"👤 Human files: {stats['human_files']}")
        print(f"📊 Problems: {stats['problems_count']}")
        print(f"💾 Output: {args.output}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Lỗi chính: {e}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    exit(main())
