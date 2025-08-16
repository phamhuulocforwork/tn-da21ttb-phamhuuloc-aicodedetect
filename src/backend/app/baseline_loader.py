import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

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
        current_dir = Path(__file__).parent.absolute()
        
        possible_paths = [
            current_dir.parent.parent / "src" / "feature_stats.json",
            current_dir.parent.parent.parent / "src" / "src" / "feature_stats.json",
            Path("../../src/feature_stats.json"),
            Path("../../../src/src/feature_stats.json"),
        ]
        
        for path in possible_paths:
            if path.exists():
                logger.info(f"Found feature_stats.json at: {path}")
                return str(path.resolve())
        
        raise FileNotFoundError(f"Could not find feature_stats.json. Tried paths: {[str(p) for p in possible_paths]}")
    
    def _load_baseline_stats(self) -> None:
        try:
            if not self.stats_file_path:
                self.stats_file_path = self._auto_detect_stats_file()
            
            with open(self.stats_file_path, 'r', encoding='utf-8') as f:
                stats_data = json.load(f)
            
            ai_stats = {}
            human_stats = {}
            
            for key, value in stats_data.items():
                if key.endswith('_ai_mean'):
                    feature_name = key.replace('_ai_mean', '')
                    ai_stats[feature_name] = float(value)
                elif key.endswith('_human_mean'):
                    feature_name = key.replace('_human_mean', '')
                    human_stats[feature_name] = float(value)
            
            self._baseline_stats = BaselineStats(
                ai_stats=ai_stats,
                human_stats=human_stats
            )
            
            logger.info(f"Loaded baseline stats: {len(ai_stats)} AI features, {len(human_stats)} Human features")
            
        except Exception as e:
            logger.error(f"Failed to load baseline stats: {e}")
            self._baseline_stats = BaselineStats(ai_stats={}, human_stats={})
    
    def get_baseline_stats(self) -> BaselineStats:
        if self._baseline_stats is None:
            self._load_baseline_stats()
        return self._baseline_stats
    
    def reload_stats(self) -> None:
        self._baseline_stats = None
        self._load_baseline_stats()
    
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