"""
Baseline Statistics Loader
Automatically loads baseline stats từ feature_stats.json
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class BaselineStats:
    """Container for AI vs Human baseline statistics"""
    ai_stats: Dict[str, float]
    human_stats: Dict[str, float]
    
    def get_feature_baseline(self, feature_name: str) -> Optional[Tuple[float, float]]:
        """
        Get AI and Human baseline values for a feature
        Returns: (ai_value, human_value) or None if not found
        """
        if feature_name in self.ai_stats and feature_name in self.human_stats:
            return self.ai_stats[feature_name], self.human_stats[feature_name]
        return None
    
    def get_feature_difference(self, feature_name: str) -> Optional[float]:
        """
        Get absolute difference between AI and Human baselines
        """
        baseline = self.get_feature_baseline(feature_name)
        if baseline:
            ai_val, human_val = baseline
            return abs(ai_val - human_val)
        return None

class BaselineLoader:
    """
    Loads and manages baseline statistics from feature_stats.json
    """
    
    def __init__(self, stats_file_path: Optional[str] = None):
        """
        Initialize baseline loader
        
        Args:
            stats_file_path: Path to feature_stats.json. If None, auto-detect from project structure
        """
        self.stats_file_path = stats_file_path
        self._baseline_stats: Optional[BaselineStats] = None
        self._load_baseline_stats()
    
    def _auto_detect_stats_file(self) -> str:
        """Auto-detect feature_stats.json path from backend"""
        # Try different possible paths from backend
        current_dir = Path(__file__).parent.absolute()
        
        possible_paths = [
            # From backend/app/ to src/
            current_dir.parent.parent / "src" / "feature_stats.json",
            # From project root
            current_dir.parent.parent.parent / "src" / "src" / "feature_stats.json",
            # Relative paths
            Path("../../src/feature_stats.json"),
            Path("../../../src/src/feature_stats.json"),
        ]
        
        for path in possible_paths:
            if path.exists():
                logger.info(f"Found feature_stats.json at: {path}")
                return str(path.resolve())
        
        raise FileNotFoundError(f"Could not find feature_stats.json. Tried paths: {[str(p) for p in possible_paths]}")
    
    def _load_baseline_stats(self) -> None:
        """Load baseline statistics from JSON file"""
        try:
            if not self.stats_file_path:
                self.stats_file_path = self._auto_detect_stats_file()
            
            with open(self.stats_file_path, 'r', encoding='utf-8') as f:
                stats_data = json.load(f)
            
            # Extract AI and Human stats
            ai_stats = {}
            human_stats = {}
            
            for key, value in stats_data.items():
                if key.endswith('_ai_mean'):
                    # Convert 'feature_name_ai_mean' -> 'feature_name'
                    feature_name = key.replace('_ai_mean', '')
                    ai_stats[feature_name] = float(value)
                elif key.endswith('_human_mean'):
                    # Convert 'feature_name_human_mean' -> 'feature_name'
                    feature_name = key.replace('_human_mean', '')
                    human_stats[feature_name] = float(value)
            
            self._baseline_stats = BaselineStats(
                ai_stats=ai_stats,
                human_stats=human_stats
            )
            
            logger.info(f"Loaded baseline stats: {len(ai_stats)} AI features, {len(human_stats)} Human features")
            
        except Exception as e:
            logger.error(f"Failed to load baseline stats: {e}")
            # Fallback to minimal stats
            self._baseline_stats = BaselineStats(ai_stats={}, human_stats={})
    
    def get_baseline_stats(self) -> BaselineStats:
        """Get loaded baseline statistics"""
        if self._baseline_stats is None:
            self._load_baseline_stats()
        return self._baseline_stats
    
    def reload_stats(self) -> None:
        """Reload statistics from file"""
        self._baseline_stats = None
        self._load_baseline_stats()
    
    def get_critical_features(self) -> Dict[str, Dict]:
        """
        Determine critical features based on effect size between AI and Human baselines
        
        Returns:
            Dictionary mapping feature names to their config (weight, direction)
        """
        baseline_stats = self.get_baseline_stats()
        critical_features = {}
        
        # Calculate effect sizes for all available features
        feature_effects = []
        
        for feature_name in baseline_stats.ai_stats.keys():
            if feature_name in baseline_stats.human_stats:
                ai_val = baseline_stats.ai_stats[feature_name]
                human_val = baseline_stats.human_stats[feature_name]
                
                # Calculate effect size (Cohen's d approximation)
                diff = abs(ai_val - human_val)
                avg_val = (ai_val + human_val) / 2
                
                # Avoid division by zero
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
        
        # Sort by effect size (highest first)
        feature_effects.sort(key=lambda x: x['effect_size'], reverse=True)
        
        # Select top features and assign weights
        top_features = feature_effects[:15]  # Top 15 most distinctive features
        
        # Assign weights based on ranking
        for i, feature_info in enumerate(top_features):
            # Higher effect size = higher weight
            weight = max(0.05, 0.20 - (i * 0.01))  # Weights from 0.20 down to 0.05
            
            critical_features[feature_info['name']] = {
                'weight': weight,
                'ai_better': feature_info['ai_higher'],
                'effect_size': feature_info['effect_size']
            }
        
        logger.info(f"Identified {len(critical_features)} critical features")
        return critical_features
    
    def get_feature_stats_summary(self) -> Dict:
        """Get summary of loaded statistics"""
        baseline_stats = self.get_baseline_stats()
        critical_features = self.get_critical_features()
        
        return {
            'total_ai_features': len(baseline_stats.ai_stats),
            'total_human_features': len(baseline_stats.human_stats),
            'critical_features_count': len(critical_features),
            'stats_file_path': self.stats_file_path,
            'top_critical_features': list(critical_features.keys())[:5]
        }

# Global instance for backend
_baseline_loader: Optional[BaselineLoader] = None

def get_baseline_loader() -> BaselineLoader:
    """Get singleton baseline loader instance"""
    global _baseline_loader
    if _baseline_loader is None:
        _baseline_loader = BaselineLoader()
    return _baseline_loader

def reload_baseline_stats():
    """Reload baseline statistics (useful for development)"""
    global _baseline_loader
    if _baseline_loader:
        _baseline_loader.reload_stats()
    else:
        _baseline_loader = BaselineLoader()