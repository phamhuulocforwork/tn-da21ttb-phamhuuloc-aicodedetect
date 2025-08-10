import re
import math
import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict
from pathlib import Path

# Import existing modules
try:
    from .ast_analyzer import CppASTAnalyzer, ASTFeatures
    from .test_parser_sample import analyze_file, basic_metrics
    HAS_LIZARD = True
except ImportError:
    HAS_LIZARD = False

@dataclass
class CodeRedundancyFeatures:
    # NOTE: Đặc trưng về code redundancy và repetition
    duplicate_lines: int = 0
    duplicate_line_ratio: float = 0.0
    repeated_patterns: int = 0
    copy_paste_score: float = 0.0
    similar_function_ratio: float = 0.0

@dataclass
class NamingPatternFeatures:
    # NOTE: Đặc trưng về naming patterns chi tiết
    # Variable naming
    descriptive_var_ratio: float = 0.0
    generic_var_ratio: float = 0.0
    meaningful_names_score: float = 0.0
    
    # Function naming
    verb_function_ratio: float = 0.0
    descriptive_function_ratio: float = 0.0
    
    # Naming consistency
    naming_consistency_score: float = 0.0
    abbreviation_usage: float = 0.0

@dataclass
class CodeComplexityFeatures:
    # NOTE: Đặc trưng về độ phức tạp code
    halstead_complexity: float = 0.0
    cognitive_complexity: float = 0.0
    maintainability_index: float = 0.0
    code_to_comment_ratio: float = 0.0
    
@dataclass
class AIPatternFeatures:
    # NOTE: Đặc trưng đặc trưng của AI-generated code
    template_usage_score: float = 0.0
    boilerplate_ratio: float = 0.0
    error_handling_score: float = 0.0
    defensive_programming_score: float = 0.0
    over_engineering_score: float = 0.0

@dataclass
class ComprehensiveFeatures:
    # NOTE: Tập hợp đầy đủ tất cả features
    # Basic features (từ existing system)
    loc: int = 0
    token_count: Optional[int] = None
    cyclomatic_complexity: Optional[float] = None
    functions: Optional[int] = None
    comment_ratio: float = 0.0
    blank_ratio: float = 0.0
    
    # AST features
    ast_features: Optional[ASTFeatures] = None
    
    # Advanced features
    redundancy: CodeRedundancyFeatures = None
    naming_patterns: NamingPatternFeatures = None
    complexity: CodeComplexityFeatures = None
    ai_patterns: AIPatternFeatures = None
    
    def to_dict(self) -> Dict:
        # NOTE: Convert to dictionary for ML processing
        result = {}
        
        # Basic features
        result.update({
            'loc': self.loc,
            'token_count': self.token_count or 0,
            'cyclomatic_complexity': self.cyclomatic_complexity or 0,
            'functions': self.functions or 0,
            'comment_ratio': self.comment_ratio,
            'blank_ratio': self.blank_ratio
        })
        
        # AST features
        if self.ast_features:
            ast_dict = asdict(self.ast_features)
            result.update({f'ast_{k}': v for k, v in ast_dict.items()})
        
        # Advanced features
        if self.redundancy:
            red_dict = asdict(self.redundancy)
            result.update({f'redundancy_{k}': v for k, v in red_dict.items()})
            
        if self.naming_patterns:
            naming_dict = asdict(self.naming_patterns)
            result.update({f'naming_{k}': v for k, v in naming_dict.items()})
            
        if self.complexity:
            comp_dict = asdict(self.complexity)
            result.update({f'complexity_{k}': v for k, v in comp_dict.items()})
            
        if self.ai_patterns:
            ai_dict = asdict(self.ai_patterns)
            result.update({f'ai_pattern_{k}': v for k, v in ai_dict.items()})
        
        return result

class AdvancedFeatureExtractor:
    # NOTE: Hệ thống trích xuất đặc trưng nâng cao
    
    def __init__(self):
        self.ast_analyzer = CppASTAnalyzer() if 'CppASTAnalyzer' in globals() else None
        self.setup_patterns()
    
    def setup_patterns(self):
        # NOTE: Setup regex patterns cho việc phân tích code
        self.template_patterns = [
            r'#include\s*<stdio\.h>',
            r'#include\s*<iostream>',
            r'int\s+main\s*\(\s*\)',
            r'return\s+0\s*;',
            r'using\s+namespace\s+std\s*;'
        ]
        
        # NOTE: Tên biến chung chung
        self.generic_vars = {
            'i', 'j', 'k', 'n', 'm', 'x', 'y', 'z', 'a', 'b', 'c', 
            'temp', 'tmp', 'val', 'value', 'data', 'item', 'var'
        }
        
        # NOTE: Tên biến có ý nghĩa
        self.descriptive_patterns = [
            r'[a-z]+[A-Z][a-z]*',  # camelCase  
            r'[a-z]+_[a-z_]+',      # snake_case
            r'\w{4,}',              # Long names
        ]
        
        # NOTE: Các patterns thường gặp của AI
        self.ai_patterns = [
            r'//\s*[A-Z][a-z].*',  # Comments bắt đầu bằng chữ cái viết hoa
            r'printf\s*\(\s*".*":',  # printf có ý nghĩa
            r'scanf\s*\(\s*".*",',  # scanf có ý nghĩa
            r'if\s*\(.*!=.*\)',     # if có ý nghĩa
        ]
    
    def extract_all_features(self, code: str, filename: str = "") -> ComprehensiveFeatures:
        # NOTE: Trích xuất tất cả features từ source code
        features = ComprehensiveFeatures()
        
        # Basic features
        features = self._extract_basic_features(code, features)
        
        # AST features
        if self.ast_analyzer:
            features.ast_features = self.ast_analyzer.analyze_code(code, filename)
        
        # Advanced features
        features.redundancy = self._extract_redundancy_features(code)
        features.naming_patterns = self._extract_naming_features(code)
        features.complexity = self._extract_complexity_features(code)
        features.ai_patterns = self._extract_ai_pattern_features(code)
        
        return features

    def _extract_basic_features(self, code: str, features: ComprehensiveFeatures) -> ComprehensiveFeatures:
        # NOTE: Trích xuất basic features
        lines = code.splitlines()
        features.loc = len(lines)
        
        # NOTE: Tỷ lệ comment
        comment_lines = len([l for l in lines if l.strip().startswith('//') or '/*' in l])
        features.comment_ratio = comment_lines / len(lines) if lines else 0
        
        # NOTE: Tỷ lệ dòng trống
        blank_lines = len([l for l in lines if not l.strip()])
        features.blank_ratio = blank_lines / len(lines) if lines else 0
        
        # NOTE: Trích xuất các metrics nâng cao nếu có
        if HAS_LIZARD:
            try:
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                    f.write(code)
                    temp_path = f.name
                
                try:
                    metrics = analyze_file(Path(temp_path))
                    features.token_count = metrics.get('token', None)
                    features.cyclomatic_complexity = metrics.get('cyclomatic_avg', None)
                    features.functions = metrics.get('functions', None)
                finally:
                    if Path(temp_path).exists():
                        Path(temp_path).unlink()
            except Exception:
                pass
        
        return features
    
    def _extract_redundancy_features(self, code: str) -> CodeRedundancyFeatures:
        # NOTE: Trích xuất features về code redundancy
        features = CodeRedundancyFeatures()
        
        lines = [l.strip() for l in code.splitlines() if l.strip()]
        
        if not lines:
            return features
        
        # NOTE: Dòng trùng lặp
        line_counts = Counter(lines)
        duplicates = sum(count - 1 for count in line_counts.values() if count > 1)
        features.duplicate_lines = duplicates
        features.duplicate_line_ratio = duplicates / len(lines)
        
        # NOTE: Các patterns lặp lại (tìm kiếm các khối code tương tự)
        patterns = []
        for i, line in enumerate(lines):
            # Create 3-gram patterns
            if i + 2 < len(lines):
                pattern = (lines[i], lines[i+1], lines[i+2])
                patterns.append(pattern)
        
        pattern_counts = Counter(patterns)
        repeated = sum(1 for count in pattern_counts.values() if count > 1)
        features.repeated_patterns = repeated
        
        # NOTE: Điểm copy-paste (heuristic dựa trên các chuỗi giống hệt nhau)
        max_sequence = 0
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                seq_len = 0
                while (i + seq_len < len(lines) and 
                       j + seq_len < len(lines) and 
                       lines[i + seq_len] == lines[j + seq_len]):
                    seq_len += 1
                max_sequence = max(max_sequence, seq_len)
        
        features.copy_paste_score = max_sequence / len(lines) if lines else 0
        
        return features
    
    def _extract_naming_features(self, code: str) -> NamingPatternFeatures:
        # NOTE: Trích xuất features về naming patterns
        features = NamingPatternFeatures()
        
        # NOTE: Tìm tất cả các identifiers
        # FIXME: Cần tối ưu chỗ này
        identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
        variables = re.findall(r'\b(?:int|float|double|char|string|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', code)
        functions = re.findall(r'\b(?:int|void|float|double|char|string|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
        
        if not identifiers:
            return features
        
        # NOTE: Tên biến có ý nghĩa vs tên biến chung chung
        descriptive_vars = 0
        generic_vars = 0
        
        for var in variables:
            if var.lower() in self.generic_vars or len(var) <= 2:
                generic_vars += 1
            elif len(var) >= 4 or any(re.match(pattern, var) for pattern in self.descriptive_patterns):
                descriptive_vars += 1
        
        total_vars = len(variables)
        if total_vars > 0:
            features.descriptive_var_ratio = descriptive_vars / total_vars
            features.generic_var_ratio = generic_vars / total_vars
        
        # NOTE: Tên hàm có ý nghĩa vs tên hàm chung chung
        verb_functions = 0
        descriptive_functions = 0
        
        verb_patterns = ['get', 'set', 'calculate', 'compute', 'process', 'handle', 'create', 'delete', 'update']
        
        for func in functions:
            if func.lower() != 'main':
                if any(func.lower().startswith(verb) for verb in verb_patterns):
                    verb_functions += 1
                if len(func) >= 6:
                    descriptive_functions += 1
        
        total_funcs = len([f for f in functions if f.lower() != 'main'])
        if total_funcs > 0:
            features.verb_function_ratio = verb_functions / total_funcs
            features.descriptive_function_ratio = descriptive_functions / total_funcs
        
        # NOTE: Điểm tên biến có ý nghĩa (heuristic)
        meaningful_score = 0
        for identifier in set(identifiers):
            if len(identifier) >= 3 and identifier not in self.generic_vars:
                vowel_ratio = sum(1 for c in identifier.lower() if c in 'aeiou') / len(identifier)
                if vowel_ratio > 0.2:
                    meaningful_score += 1
        
        features.meaningful_names_score = meaningful_score / len(set(identifiers)) if identifiers else 0
        
        # NOTE: Độ nhất quán của naming (camelCase vs snake_case consistency)
        camel_case_count = len(re.findall(r'\b[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\b', code))
        snake_case_count = len(re.findall(r'\b[a-z]+_[a-z_0-9]*\b', code))
        
        total_naming = camel_case_count + snake_case_count
        if total_naming > 0:
            features.naming_consistency_score = max(camel_case_count, snake_case_count) / total_naming
        
        return features
    
    def _extract_complexity_features(self, code: str) -> CodeComplexityFeatures:
        # NOTE: Trích xuất features về complexity
        features = CodeComplexityFeatures()
        
        lines = code.splitlines()
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('//')]
        comment_lines = [l for l in lines if l.strip().startswith('//') or '/*' in l]
        
        # NOTE: Tỷ lệ code to comment
        if comment_lines:
            features.code_to_comment_ratio = len(code_lines) / len(comment_lines)
        else:
            # NOTE: Sử dụng một giá trị cao nhưng hữu hạn để tránh vấn đề với ML training
            features.code_to_comment_ratio = 999.0 if code_lines else 0
        
        operators = re.findall(r'[+\-*/=<>!&|]+', code)
        operands = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
        
        unique_operators = len(set(operators))
        unique_operands = len(set(operands))
        total_operators = len(operators)
        total_operands = len(operands)
        
        if unique_operators > 0 and unique_operands > 0:
            vocabulary = unique_operators + unique_operands
            length = total_operators + total_operands
            
            if vocabulary > 0 and length > 0:
                features.halstead_complexity = length * math.log2(vocabulary)
        
        nesting_score = 0
        current_depth = 0
        
        for line in code_lines:
            line = line.strip()
            if any(keyword in line for keyword in ['if', 'for', 'while', 'switch']):
                current_depth += 1
                nesting_score += current_depth
            elif line.startswith('}'):
                current_depth = max(0, current_depth - 1)
        
        features.cognitive_complexity = nesting_score
        
        if features.halstead_complexity > 0 and len(code_lines) > 0:
            features.maintainability_index = max(0, 171 - 5.2 * math.log(features.halstead_complexity) - 0.23 * 1 - 16.2 * math.log(len(code_lines)))
        
        return features
    
    def _extract_ai_pattern_features(self, code: str) -> AIPatternFeatures:
        # NOTE: Trích xuất features đặc trưng của AI-generated code
        features = AIPatternFeatures()
        
        lines = code.splitlines()
        code_content = ' '.join(lines)
        
        # NOTE: Điểm sử dụng template
        template_matches = 0
        for pattern in self.template_patterns:
            template_matches += len(re.findall(pattern, code, re.IGNORECASE))
        
        features.template_usage_score = template_matches / len(lines) if lines else 0
        
        # NOTE: Tỷ lệ boilerplate
        boilerplate_lines = 0
        for line in lines:
            line = line.strip()
            if (line.startswith('#include') or 
                line.startswith('using namespace') or
                line == 'return 0;' or
                line == '{' or line == '}'):
                boilerplate_lines += 1
        
        features.boilerplate_ratio = boilerplate_lines / len(lines) if lines else 0
        
        # NOTE: Điểm xử lý lỗi
        error_patterns = ['if', '!=', 'NULL', 'errno', 'error', 'exception', 'try', 'catch']
        error_score = 0
        
        for pattern in error_patterns:
            error_score += code_content.lower().count(pattern.lower())
        
        features.error_handling_score = error_score / len(lines) if lines else 0
        
        # NOTE: Điểm defensive programming
        defensive_patterns = ['assert', 'check', 'validate', 'verify', 'bounds']
        defensive_score = 0
        
        for pattern in defensive_patterns:
            defensive_score += code_content.lower().count(pattern.lower())
        
        features.defensive_programming_score = defensive_score / len(lines) if lines else 0
        
        # NOTE: Điểm over-engineering (quá nhiều hàm cho các tác vụ đơn giản)
        function_count = len(re.findall(r'\b(?:int|void|float|double|char|string|bool)\s+\w+\s*\(', code))
        if function_count > 1 and len(lines) < 50:  # NOTE: Nhiều hàm trong code ngắn
            features.over_engineering_score = function_count / len(lines)
        
        return features