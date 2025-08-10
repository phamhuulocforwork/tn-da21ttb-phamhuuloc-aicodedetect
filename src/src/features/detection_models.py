from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import pickle
from abc import ABC, abstractmethod

try:
    from .advanced_features import AdvancedFeatureExtractor, ComprehensiveFeatures
    HAS_ADVANCED_FEATURES = True
except ImportError:
    HAS_ADVANCED_FEATURES = False

@dataclass 
class DetectionResult:
    prediction: str  # "AI-generated" | "Human-written" | "Uncertain"
    confidence: float  # 0.0 - 1.0
    reasoning: List[str]
    feature_importance: Dict[str, float]
    method_used: str  # "heuristic-static"

class BaseDetector(ABC):
    # NOTE: Base class cho các detector
    
    @abstractmethod
    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class HeuristicScoringDetector(BaseDetector):
    def __init__(self):
        # NOTE: Feature weights cho AI-leaning (positive) và Human-leaning (negative)
        # NOTE: Tổng các trọng số tuyệt đối <= 1.0 để giữ điểm ổn định
        self.ai_feature_weights = {
            # Basic/style
            'comment_ratio': 0.10,  # Tỷ lệ comment cao → AI-generated
            'ast_indentation_consistency': 0.08,
            'naming_naming_consistency_score': 0.07,

            # AI patterns
            'ai_pattern_template_usage_score': 0.12,
            'ai_pattern_boilerplate_ratio': 0.08,
            'ai_pattern_error_handling_score': 0.06,

            # Redundancy (copy-paste)
            'redundancy_copy_paste_score': 0.08,
            'redundancy_duplicate_line_ratio': 0.05,

            # Structure/complexity
            'low_cyclomatic_complexity': 0.06,  # Từ cyclomatic_complexity
            'function_density': 0.04,           # Từ functions / max(loc, 1)
        }

        self.human_feature_weights = {
            'short_loc': 0.07,                       # Từ loc
            'naming_generic_var_ratio': 0.10,
            'ast_operator_spacing_inconsistency': 0.05,  # Từ ast_operator_spacing_consistency
            'ast_single_char_vars_density': 0.06,        # Từ ast_single_char_vars / max(variable_count, 1)
        }

        self.ai_threshold = 0.60
        self.human_threshold = 0.40

    @staticmethod
    def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
        return max(low, min(high, value))

    @staticmethod
    def _normalize_high(value: float, low: float, high: float) -> float:
        # NOTE: Chuẩn hóa giá trị cao hơn
        if high <= low:
            return 0.0
        return HeuristicScoringDetector._clamp((value - low) / (high - low))

    @staticmethod
    def _normalize_low(value: float, low: float, high: float) -> float:
        # NOTE: Chuẩn hóa giá trị thấp hơn
        if high <= low:
            return 0.0
        return HeuristicScoringDetector._clamp((high - value) / (high - low))

    def detect(self, features: Dict[str, Any]) -> DetectionResult:
        # NOTE: Tính toán điểm heuristic -> đưa ra dự đoán
        contributions: Dict[str, float] = {}
        reasons: List[str] = []

        def add_ai(name: str, score: float, desc: str):
            if score <= 0:
                return
            weight = self.ai_feature_weights[name]
            contrib = weight * score
            contributions[name] = contrib
            reasons.append(f"{desc} (+{contrib:.3f})")

        def add_human(name: str, score: float, desc: str):
            if score <= 0:
                return
            weight = self.human_feature_weights[name]
            contrib = weight * score
            contributions[name] = -contrib
            reasons.append(f"{desc} (-{contrib:.3f})")

        # NOTE: Lấy các metrics raw với giá trị mặc định an toàn
        loc = float(features.get('loc', 0) or 0)
        functions = float(features.get('functions', 0) or 0)
        cyclomatic = float(features.get('cyclomatic_complexity', features.get('cyclomatic_avg', 0) or 0))

        comment_ratio = float(features.get('comment_ratio', 0) or 0)
        indentation_consistency = float(features.get('ast_indentation_consistency', 0) or 0)
        operator_spacing_consistency = float(features.get('ast_operator_spacing_consistency', 0) or 0)

        naming_consistency = float(features.get('naming_naming_consistency_score', 0) or 0)
        naming_generic_ratio = float(features.get('naming_generic_var_ratio', 0) or 0)

        template_usage = float(features.get('ai_pattern_template_usage_score', 0) or 0)
        boilerplate_ratio = float(features.get('ai_pattern_boilerplate_ratio', 0) or 0)
        error_handling_score = float(features.get('ai_pattern_error_handling_score', 0) or 0)

        copy_paste_score = float(features.get('redundancy_copy_paste_score', 0) or 0)
        duplicate_line_ratio = float(features.get('redundancy_duplicate_line_ratio', 0) or 0)

        ast_single_char_vars = float(features.get('ast_single_char_vars', 0) or 0)
        ast_variable_count = float(features.get('ast_variable_count', features.get('variable_count', 0) or 0))

        # NOTE: Các metrics dẫn xuất
        function_density = functions / max(loc, 1.0)  # NOTE: Mật độ cao hơn trong code ngắn thì có thể là AI-generated

        add_ai('comment_ratio', self._normalize_high(comment_ratio, 0.10, 0.35), 'Tỷ lệ comment cao')
        add_ai('ast_indentation_consistency', self._normalize_high(indentation_consistency, 0.6, 1.0), 'Cách thụt lề nhất quán')
        add_ai('naming_naming_consistency_score', self._normalize_high(naming_consistency, 0.5, 1.0), 'Cách đặt tên nhất quán')

        add_ai('ai_pattern_template_usage_score', self._normalize_high(template_usage, 0.05, 0.30), 'Tồn tại các mẫu/template/boilerplate')
        add_ai('ai_pattern_boilerplate_ratio', self._normalize_high(boilerplate_ratio, 0.05, 0.30), 'Tỷ lệ boilerplate cao')
        add_ai('ai_pattern_error_handling_score', self._normalize_high(error_handling_score, 0.02, 0.20), 'Có mẫu xử lý lỗi rõ ràng')

        add_ai('redundancy_copy_paste_score', self._normalize_high(copy_paste_score, 0.05, 0.40), 'Có lặp lại copy-paste')
        add_ai('redundancy_duplicate_line_ratio', self._normalize_high(duplicate_line_ratio, 0.02, 0.25), 'Có dòng trùng lặp')

        # NOTE: Độ phức tạp của code → AI-generated
        add_ai('low_cyclomatic_complexity', self._normalize_low(cyclomatic, 1.0, 6.0), 'Độ phức tạp cyclomatic thấp')

        # NOTE: Nhiều hàm trên mỗi LOC trong code ngắn → AI-generated
        add_ai('function_density', self._normalize_high(function_density, 0.02, 0.12), 'Mật độ hàm cao so với độ dài code')

        # NOTE: Chuẩn hóa và thêm tín hiệu nghiêng về code của người viết
        add_human('short_loc', self._normalize_low(loc, 20.0, 80.0), 'Code rất ngắn')
        add_human('naming_generic_var_ratio', self._normalize_high(naming_generic_ratio, 0.20, 0.70), 'Tên biến chung chung')

        # NOTE: Không nhất quán khoảng cách toán tử (đảo ngược tính nhất quán)  
        op_inconsistency = self._clamp(1.0 - operator_spacing_consistency)
        add_human('ast_operator_spacing_inconsistency', self._normalize_high(op_inconsistency, 0.20, 0.80), 'Khoảng cách toán tử không nhất quán')

        # NOTE: Mật độ biến ký tự đơn
        scv_density = ast_single_char_vars / max(ast_variable_count, 1.0)
        add_human('ast_single_char_vars_density', self._normalize_high(scv_density, 0.10, 0.50), 'Sử dụng biến ký tự đơn cao')

        # NOTE: Tổng hợp điểm xung quanh mốc 0.5
        total = 0.5
        for k, v in contributions.items():
            total += v
        total = self._clamp(total)

        if total > self.ai_threshold:
            prediction = "AI-generated"
            confidence = total
        elif total < self.human_threshold:
            prediction = "Human-written"
            confidence = 1.0 - total
        else:
            prediction = "Uncertain"
            confidence = 0.5

        # NOTE: Sắp xếp lý do theo đóng góp tuyệt đối và giữ lại top 6
        sorted_items = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
        top_keys = set(k for k, _ in sorted_items[:6])
        filtered_reasons = [r for r in reasons if any(r.startswith(lbl) for lbl in [
            'Tỷ lệ comment cao', 'Cách thụt lề nhất quán', 'Cách đặt tên nhất quán',
            'Tồn tại các mẫu/template/boilerplate', 'Tỷ lệ boilerplate cao', 'Có mẫu xử lý lỗi rõ ràng',
            'Có lặp lại copy-paste', 'Có dòng trùng lặp', 'Độ phức tạp cyclomatic thấp',
            'Mật độ hàm cao so với độ dài code', 'Code rất ngắn', 'Tên biến chung chung',
            'Khoảng cách toán tử không nhất quán', 'Sử dụng biến ký tự đơn cao'])]

        feature_importance = {k: round(abs(v), 4) for k, v in contributions.items() if k in top_keys}

        return DetectionResult(
            prediction=prediction,
            confidence=round(confidence, 3),
            reasoning=filtered_reasons[:6],
            feature_importance=feature_importance,
            method_used="heuristic-static",
        )

    def get_name(self) -> str:
        return "Heuristic Scoring Detector"

def create_detector(detector_type: str = "heuristic", model_path: Optional[str] = None) -> BaseDetector:
    # NOTE: Factory function để tạo detector
    # NOTE: Map legacy names to heuristic detector
    if detector_type in ("heuristic"):
        return HeuristicScoringDetector()
    else:
        raise ValueError(f"Unknown detector type: {detector_type}")