import sys
import tempfile
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# NOTE: Thêm src/src vào path để import ML components
current_dir = Path(__file__).parent
src_src_path = current_dir.parent.parent / "src"
sys.path.append(str(src_src_path))

try:
    from features.test_parser_sample import analyze_file, basic_metrics
    HAS_LIZARD = True
except ImportError:
    HAS_LIZARD = False
    print("Warning: Lizard not available. Using basic metrics only.")

class CodeAnalyzer:
    """
        Class phân tích code và trích xuất features
    """
    
    def __init__(self):
        self.has_advanced_features = HAS_LIZARD
    
    def extract_features(self, code: str, language: str, filename: Optional[str] = None) -> Dict:
        """
            Trích xuất các đặc trưng từ source code
            
            Returns:
                Dict chứa các metrics: loc, token_count, cyclomatic_avg, functions, comment_ratio, blank_ratio
        """
        try:
            if self.has_advanced_features:
                return self._extract_advanced_features(code, language)
            else:
                return self._extract_basic_features(code)
        except Exception as e:
            print(f"Error in feature extraction: {e}")
            return self._extract_minimal_features(code)
    
    def _extract_advanced_features(self, code: str, language: str) -> Dict:
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False) as f:
            f.write(code)
            temp_path = Path(f.name)
        
        try:
            metrics = analyze_file(temp_path)
            return {
                "loc": metrics.get("loc", 0),
                "token_count": metrics.get("token", None),
                "cyclomatic_avg": metrics.get("cyclomatic_avg", None),
                "functions": metrics.get("functions", None),
                "comment_ratio": self._calculate_comment_ratio(code),
                "blank_ratio": self._calculate_blank_ratio(code)
            }
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def _extract_basic_features(self, code: str) -> Dict:
        metrics = basic_metrics(code)
        return {
            "loc": metrics["loc"],
            "token_count": None,
            "cyclomatic_avg": None,
            "functions": None,
            "comment_ratio": metrics["comment_ratio"],
            "blank_ratio": metrics["blank_ratio"]
        }
    
    def _extract_minimal_features(self, code: str) -> Dict:
        lines = code.splitlines()
        return {
            "loc": len(lines),
            "token_count": None,
            "cyclomatic_avg": None,
            "functions": None,
            "comment_ratio": self._calculate_comment_ratio(code),
            "blank_ratio": self._calculate_blank_ratio(code)
        }
    
    def _calculate_comment_ratio(self, code: str) -> float:
        lines = code.splitlines()
        if not lines:
            return 0.0
        comment_lines = len([l for l in lines if l.strip().startswith("//") or "/*" in l])
        return comment_lines / len(lines)
    
    def _calculate_blank_ratio(self, code: str) -> float:
        lines = code.splitlines()
        if not lines:
            return 0.0
        blank_lines = len([l for l in lines if not l.strip()])
        return blank_lines / len(lines)

class AIDetector:
    """
        Class phát hiện AI-generated code sử dụng rule-based logic
    """
    
    def __init__(self):
        self.ai_patterns = [
            self._check_descriptive_naming,
            self._check_comment_patterns,
            self._check_include_patterns,
            self._check_structure_patterns,
            self._check_template_patterns,
            self._check_variable_patterns
        ]
        
        self.human_patterns = [
            self._check_short_code,
            self._check_single_char_vars,
            self._check_inconsistent_formatting
        ]
    
    def detect(self, code: str, features: Dict) -> Tuple[str, float, List[str]]:
        """
            Phát hiện AI vs Human code
            
            Returns:
                Tuple[prediction, confidence, reasoning]
        """
        ai_reasons = []
        human_reasons = []
        ai_score = 0.0
        
        # Áp dụng AI patterns
        for pattern_func in self.ai_patterns:
            score, reason = pattern_func(code, features)
            ai_score += score
            if reason:
                ai_reasons.append(f"[AI] {reason}")
        
        # Áp dụng Human patterns (giảm AI score)
        for pattern_func in self.human_patterns:
            score, reason = pattern_func(code, features)
            ai_score -= score  # Subtract for human indicators
            if reason:
                human_reasons.append(f"[Human] {reason}")
        
        # Normalize score
        ai_score = max(0.0, min(1.0, ai_score))
        
        # Make prediction với fixed reasoning logic
        if ai_score > 0.6:
            prediction = "AI-generated"
            confidence = ai_score
            # Chỉ hiển thị AI reasons khi prediction là AI-generated
            reasoning = ai_reasons if ai_reasons else ["Phân tích AI patterns"]
            if human_reasons:
                reasoning.append(f"Note: Found {len(human_reasons)} human indicators but AI score still high")
        elif ai_score < 0.4:
            prediction = "Human-written"
            confidence = 1.0 - ai_score
            # Chỉ hiển thị Human reasons khi prediction là Human-written
            reasoning = human_reasons if human_reasons else ["Phân tích Human patterns"] 
            if ai_reasons:
                reasoning.append(f"Note: Found {len(ai_reasons)} AI indicators but overall human-like")
        else:
            prediction = "Uncertain"
            confidence = 0.5
            # Hiển thị cả hai loại patterns khi uncertain
            reasoning = []
            if ai_reasons:
                reasoning.extend(ai_reasons)
            if human_reasons:
                reasoning.extend(human_reasons)
            reasoning.append("Kết quả không rõ ràng - cần thêm dữ liệu")
        
        if not reasoning:
            reasoning.append("Phân tích dựa trên các pattern cơ bản")
        
        return prediction, round(confidence, 3), reasoning
    
    def _check_descriptive_naming(self, code: str, features: Dict) -> Tuple[float, str]:
        camel_case = re.findall(r'\\b[a-zA-Z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\\b', code)
        snake_case = re.findall(r'\\b[a-z]+_[a-z]+\\b', code)
        
        descriptive_count = len(camel_case) + len(snake_case)
        
        if descriptive_count > 5:
            return 0.2, "Nhiều tên biến/hàm mô tả chi tiết"
        elif descriptive_count > 2:
            return 0.1, "Có tên biến/hàm mô tả"
        return 0.0, ""
    
    def _check_comment_patterns(self, code: str, features: Dict) -> Tuple[float, str]:
        comment_ratio = features.get("comment_ratio", 0)
        if comment_ratio > 0.15:  # >15% comment
            return 0.15, "Tỷ lệ comment cao (AI pattern)"
        elif comment_ratio > 0.08:  # >8% comment
            return 0.08, "Có comment giải thích"
        return 0.0, ""
    
    def _check_include_patterns(self, code: str, features: Dict) -> Tuple[float, str]:
        includes = re.findall(r'#include\\s*<[^>]+>', code)
        if len(includes) >= 3:
            return 0.1, "Sử dụng nhiều thư viện chuẩn"
        elif len(includes) >= 2:
            return 0.05, "Có include statements đầy đủ"
        return 0.0, ""
    
    def _check_structure_patterns(self, code: str, features: Dict) -> Tuple[float, str]:
        score = 0.0
        reasons = []
        
        if 'try' in code or 'catch' in code or ('if' in code and 'error' in code.lower()):
            score += 0.1
            reasons.append("error handling")
        
        cyclomatic_avg = features.get("cyclomatic_avg")
        if cyclomatic_avg and cyclomatic_avg < 3:
            score += 0.1
            reasons.append("độ phức tạp thấp")
        
        lines = code.split('\\n')
        indented_lines = [l for l in lines if l.startswith('    ') or l.startswith('\\t')]
        if len(indented_lines) > len(lines) * 0.3:
            score += 0.1
            reasons.append("formatting nhất quán")
        
        reason_text = "Code structure tốt: " + ", ".join(reasons) if reasons else ""
        return score, reason_text
    
    def _check_template_patterns(self, code: str, features: Dict) -> Tuple[float, str]:
        if 'int main()' in code and 'return 0' in code:
            return 0.05, "Sử dụng template chuẩn"
        return 0.0, ""
    
    def _check_variable_patterns(self, code: str, features: Dict) -> Tuple[float, str]:
        declarations = re.findall(r'\\b(int|float|double|char|string)\\s+\\w+', code)
        if len(declarations) > 3:
            return 0.05, "Khai báo biến rõ ràng"
        return 0.0, ""
    
    def _check_short_code(self, code: str, features: Dict) -> Tuple[float, str]:
        loc = features.get("loc", 0)
        if loc < 20:
            return 0.1, "Code ngắn (human pattern)"
        return 0.0, ""
    
    def _check_single_char_vars(self, code: str, features: Dict) -> Tuple[float, str]:
        single_vars = re.findall(r'\\b[a-z]\\b', code)
        if len(single_vars) > 3:
            return 0.15, "Nhiều biến 1 ký tự (human pattern)"
        elif len(single_vars) > 1:
            return 0.08, "Có biến 1 ký tự (human tendency)"
        return 0.0, ""
    
    def _check_inconsistent_formatting(self, code: str, features: Dict) -> Tuple[float, str]:
        lines = code.split('\\n')
        if not lines:
            return 0.0, ""
        
        space_indented = len([l for l in lines if l.startswith('    ')])
        tab_indented = len([l for l in lines if l.startswith('\\t')])
        
        if space_indented > 0 and tab_indented > 0:
            return 0.05, "Mixed indentation (human pattern)"
        
        inconsistent_spacing = re.findall(r'\\w+=[^=]|\\w+ = [^=]|\\w+=[^=]', code)
        if len(inconsistent_spacing) > 2:
            return 0.03, "Inconsistent spacing"
        
        return 0.0, ""

code_analyzer = CodeAnalyzer()
ai_detector = AIDetector()

def analyze_code_features(code: str, language: str, filename: Optional[str] = None) -> Dict:
    """
    Public function để trích xuất features
    """
    return code_analyzer.extract_features(code, language, filename)

def detect_ai_code(code: str, features: Dict) -> Tuple[str, float, List[str]]:
    """
    Public function để detect AI code
    """
    return ai_detector.detect(code, features)