import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
import logging
import time
from functools import lru_cache

logger = logging.getLogger(__name__)

# Configuration for stats file paths
STATS_FILE_CONFIG = {
    'docker_paths': [
        Path('/src/feature_stats.json'),  # Docker volume mount
        Path('/app/../src/feature_stats.json'),
    ],
    'dev_paths': [
        Path(__file__).parent.parent.parent / "src" / "feature_stats.json",
        Path(__file__).parent.parent.parent.parent / "src" / "src" / "feature_stats.json",
        Path("../../src/feature_stats.json"),
        Path("../../../src/src/feature_stats.json"),
        Path("src/src/feature_stats.json"),
        Path("../src/src/feature_stats.json"),
    ]
}

@dataclass
class BaselineStats:
    ai_stats: Dict[str, float]
    human_stats: Dict[str, float]
    
    def get_feature_baseline(self, feature_name: str) -> Optional[Tuple[float, float]]:
        if feature_name in self.ai_stats and feature_name in self.human_stats:
            return self.ai_stats[feature_name], self.human_stats[feature_name]
        return None
    
    def get_feature_difference(self, feature_name: str) -> Optional[float]:
        baseline = self.get_feature_baseline(feature_name)
        if baseline:
            ai_val, human_val = baseline
            return abs(ai_val - human_val)
        return None

class BaselineLoader:
    
    def __init__(self, stats_file_path: Optional[str] = None):
        self.stats_file_path = stats_file_path
        self._baseline_stats: Optional[BaselineStats] = None
        self._load_baseline_stats()
    
    def _auto_detect_stats_file(self) -> str:
        """Auto-detect feature_stats.json file with optimized path resolution"""
        # First try Docker-specific paths (more efficient in containerized environment)
        for path in STATS_FILE_CONFIG['docker_paths']:
            if path.exists():
                logger.info(f"Found feature_stats.json at Docker path: {path}")
                return str(path.resolve())

        # Then try development paths
        for path in STATS_FILE_CONFIG['dev_paths']:
            if path.exists():
                logger.info(f"Found feature_stats.json at dev path: {path}")
                return str(path.resolve())

        # If no file found, provide detailed error with all attempted paths
        all_paths = STATS_FILE_CONFIG['docker_paths'] + STATS_FILE_CONFIG['dev_paths']
        error_msg = f"Could not find feature_stats.json. Searched {len(all_paths)} locations:\n"
        for i, path in enumerate(all_paths, 1):
            error_msg += f"  {i}. {path} {'✓' if path.exists() else '✗'}\n"

        raise FileNotFoundError(error_msg)
    
    @lru_cache(maxsize=1)
    def _load_baseline_stats(self) -> None:
        """Load baseline stats with caching and improved error handling"""
        try:
            if not self.stats_file_path:
                self.stats_file_path = self._auto_detect_stats_file()

            # Check file modification time to detect changes
            file_path = Path(self.stats_file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Stats file not found: {self.stats_file_path}")

            # Load and parse JSON data
            with open(self.stats_file_path, 'r', encoding='utf-8') as f:
                stats_data = json.load(f)

            if not isinstance(stats_data, dict):
                raise ValueError(f"Invalid stats file format: expected dict, got {type(stats_data)}")

            ai_stats = {}
            human_stats = {}

            # Parse features with validation
            for key, value in stats_data.items():
                if not isinstance(key, str) or not isinstance(value, (int, float)):
                    logger.warning(f"Skipping invalid entry: {key} = {value}")
                    continue

                if key.endswith('_ai_mean'):
                    feature_name = key.replace('_ai_mean', '')
                    ai_stats[feature_name] = float(value)
                elif key.endswith('_human_mean'):
                    feature_name = key.replace('_human_mean', '')
                    human_stats[feature_name] = float(value)

            if not ai_stats and not human_stats:
                raise ValueError("No valid AI or human stats found in file")

            self._baseline_stats = BaselineStats(
                ai_stats=ai_stats,
                human_stats=human_stats
            )

            logger.info(f"Successfully loaded baseline stats: {len(ai_stats)} AI features, {len(human_stats)} Human features from {self.stats_file_path}")

        except Exception as e:
            logger.error(f"Failed to load baseline stats: {e}")
            # Create minimal fallback stats to prevent system failure
            self._baseline_stats = self._create_fallback_stats()

    def _create_fallback_stats(self) -> BaselineStats:
        """Create minimal fallback stats when file loading fails"""
        logger.warning("Using fallback baseline stats")
        return BaselineStats(
            ai_stats={
                'comment_ratio': 0.05,
                'cyclomatic_complexity': 1.2,
                'loc': 25.0
            },
            human_stats={
                'comment_ratio': 0.15,
                'cyclomatic_complexity': 1.0,
                'loc': 20.0
            }
        )
    
    def get_baseline_stats(self) -> BaselineStats:
        if self._baseline_stats is None:
            self._load_baseline_stats()
        return self._baseline_stats
    
    def reload_stats(self) -> None:
        """Reload baseline stats from file, clearing cache"""
        self._load_baseline_stats.cache_clear()  # Clear LRU cache
        self._baseline_stats = None
        self._load_baseline_stats()

    def validate_stats_integrity(self) -> Dict[str, any]:
        """Validate the integrity of loaded baseline stats"""
        if self._baseline_stats is None:
            return {"valid": False, "errors": ["No baseline stats loaded"]}

        errors = []
        warnings = []

        ai_count = len(self._baseline_stats.ai_stats)
        human_count = len(self._baseline_stats.human_stats)

        if ai_count == 0:
            errors.append("No AI baseline features found")
        if human_count == 0:
            errors.append("No human baseline features found")

        if ai_count != human_count:
            warnings.append(f"AI features ({ai_count}) != Human features ({human_count})")

        # Check for common features
        common_features = set(self._baseline_stats.ai_stats.keys()) & set(self._baseline_stats.human_stats.keys())
        if len(common_features) < min(ai_count, human_count):
            warnings.append(f"Only {len(common_features)} features have both AI and human baselines")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "ai_features_count": ai_count,
            "human_features_count": human_count,
            "common_features_count": len(common_features),
            "file_path": self.stats_file_path
        }
    
    def get_critical_features(self) -> Dict[str, Dict]:
        baseline_stats = self.get_baseline_stats()
        critical_features = {}
        
        feature_effects = []
        
        for feature_name in baseline_stats.ai_stats.keys():
            if feature_name in baseline_stats.human_stats:
                ai_val = baseline_stats.ai_stats[feature_name]
                human_val = baseline_stats.human_stats[feature_name]
                
                diff = abs(ai_val - human_val)
                avg_val = (ai_val + human_val) / 2
                
                if avg_val != 0:
                    effect_size = diff / abs(avg_val)
                else:
                    effect_size = diff
                
                feature_effects.append({
                    'name': feature_name,
                    'effect_size': effect_size,
                    'ai_val': ai_val,
                    'human_val': human_val,
                    'ai_higher': ai_val > human_val
                })
        
        feature_effects.sort(key=lambda x: x['effect_size'], reverse=True)
        
        
        for i, feature_info in enumerate(top_features):
            
            critical_features[feature_info['name']] = {
                'weight': weight,
                'ai_better': feature_info['ai_higher'],
                'effect_size': feature_info['effect_size']
            }
        
        logger.info(f"Identified {len(critical_features)} critical features")
        return critical_features
    
    def get_feature_stats_summary(self) -> Dict:
        baseline_stats = self.get_baseline_stats()
        critical_features = self.get_critical_features()
        
        return {
            'total_ai_features': len(baseline_stats.ai_stats),
            'total_human_features': len(baseline_stats.human_stats),
            'critical_features_count': len(critical_features),
            'stats_file_path': self.stats_file_path,
            'top_critical_features': list(critical_features.keys())[:5]
        }

_baseline_loader: Optional[BaselineLoader] = None

def get_baseline_loader() -> BaselineLoader:
    global _baseline_loader
    if _baseline_loader is None:
        _baseline_loader = BaselineLoader()
    return _baseline_loader

def reload_baseline_stats():
    global _baseline_loader
    if _baseline_loader:
        _baseline_loader.reload_stats()
    else:
        _baseline_loader = BaselineLoader()