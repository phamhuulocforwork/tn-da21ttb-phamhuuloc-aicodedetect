"""
Advanced Feature Extraction System for AI Code Detection
Hệ thống trích xuất đặc trưng nâng cao cho phát hiện code AI
"""

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
    print("Warning: Some dependencies not available. Using fallback mode.")

@dataclass
class CodeRedundancyFeatures:
    """Đặc trưng về code redundancy và repetition"""
    duplicate_lines: int = 0
    duplicate_line_ratio: float = 0.0
    repeated_patterns: int = 0
    copy_paste_score: float = 0.0
    similar_function_ratio: float = 0.0

@dataclass
class NamingPatternFeatures:
    """Đặc trưng về naming patterns chi tiết"""
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
    """Đặc trưng về độ phức tạp code"""
    halstead_complexity: float = 0.0
    cognitive_complexity: float = 0.0
    maintainability_index: float = 0.0
    code_to_comment_ratio: float = 0.0
    
@dataclass
class AIPatternFeatures:
    """Đặc trưng đặc trưng của AI-generated code"""
    template_usage_score: float = 0.0
    boilerplate_ratio: float = 0.0
    error_handling_score: float = 0.0
    defensive_programming_score: float = 0.0
    over_engineering_score: float = 0.0

@dataclass
class ComprehensiveFeatures:
    """Tập hợp đầy đủ tất cả features"""
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
        """Convert to dictionary for ML processing"""
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
    """
    Hệ thống trích xuất đặc trưng nâng cao
    """
    
    def __init__(self):
        self.ast_analyzer = CppASTAnalyzer() if 'CppASTAnalyzer' in globals() else None
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns for analysis"""
        # Common templates and boilerplate patterns
        self.template_patterns = [
            r'#include\s*<stdio\.h>',
            r'#include\s*<iostream>',
            r'int\s+main\s*\(\s*\)',
            r'return\s+0\s*;',
            r'using\s+namespace\s+std\s*;'
        ]
        
        # Generic variable names
        self.generic_vars = {
            'i', 'j', 'k', 'n', 'm', 'x', 'y', 'z', 'a', 'b', 'c', 
            'temp', 'tmp', 'val', 'value', 'data', 'item', 'var'
        }
        
        # Descriptive naming patterns
        self.descriptive_patterns = [
            r'[a-z]+[A-Z][a-z]*',  # camelCase
            r'[a-z]+_[a-z_]+',      # snake_case
            r'\w{4,}',              # Long names
        ]
        
        # AI-typical patterns
        self.ai_patterns = [
            r'//\s*[A-Z][a-z].*',  # Comments starting with capital
            r'printf\s*\(\s*".*:"',  # Descriptive printf
            r'scanf\s*\(\s*".*",',  # Input prompts
            r'if\s*\(.*!=.*\)',     # Error checking
        ]
    
    def extract_all_features(self, code: str, filename: str = "") -> ComprehensiveFeatures:
        """
        Trích xuất tất cả features từ source code
        """
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
        """Trích xuất basic features (tương thích với existing system)"""
        lines = code.splitlines()
        features.loc = len(lines)
        
        # Comment ratio
        comment_lines = len([l for l in lines if l.strip().startswith('//') or '/*' in l])
        features.comment_ratio = comment_lines / len(lines) if lines else 0
        
        # Blank ratio
        blank_lines = len([l for l in lines if not l.strip()])
        features.blank_ratio = blank_lines / len(lines) if lines else 0
        
        # Try to get advanced metrics if available
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
        """Trích xuất features về code redundancy"""
        features = CodeRedundancyFeatures()
        
        lines = [l.strip() for l in code.splitlines() if l.strip()]
        
        if not lines:
            return features
        
        # Duplicate lines
        line_counts = Counter(lines)
        duplicates = sum(count - 1 for count in line_counts.values() if count > 1)
        features.duplicate_lines = duplicates
        features.duplicate_line_ratio = duplicates / len(lines)
        
        # Repeated patterns (look for similar code blocks)
        patterns = []
        for i, line in enumerate(lines):
            # Create 3-gram patterns
            if i + 2 < len(lines):
                pattern = (lines[i], lines[i+1], lines[i+2])
                patterns.append(pattern)
        
        pattern_counts = Counter(patterns)
        repeated = sum(1 for count in pattern_counts.values() if count > 1)
        features.repeated_patterns = repeated
        
        # Copy-paste score (heuristic based on identical sequences)
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
        """Trích xuất features về naming patterns"""
        features = NamingPatternFeatures()
        
        # Find all identifiers
        identifiers = re.findall(r'\\b[a-zA-Z_][a-zA-Z0-9_]*\\b', code)
        variables = re.findall(r'\\b(?:int|float|double|char|string|bool)\\s+([a-zA-Z_][a-zA-Z0-9_]*)\\b', code)
        functions = re.findall(r'\\b(?:int|void|float|double|char|string|bool)\\s+([a-zA-Z_][a-zA-Z0-9_]*)\\s*\\(', code)
        
        if not identifiers:
            return features
        
        # Descriptive vs generic variables
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
        
        # Function naming patterns
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
        
        # Meaningful names score (heuristic)
        meaningful_score = 0
        for identifier in set(identifiers):
            if len(identifier) >= 3 and identifier not in self.generic_vars:
                # Check for vowels (meaningful words usually have vowels)
                vowel_ratio = sum(1 for c in identifier.lower() if c in 'aeiou') / len(identifier)
                if vowel_ratio > 0.2:
                    meaningful_score += 1
        
        features.meaningful_names_score = meaningful_score / len(set(identifiers)) if identifiers else 0
        
        # Naming consistency (camelCase vs snake_case consistency)
        camel_case_count = len(re.findall(r'\\b[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\\b', code))
        snake_case_count = len(re.findall(r'\\b[a-z]+_[a-z_0-9]*\\b', code))
        
        total_naming = camel_case_count + snake_case_count
        if total_naming > 0:
            features.naming_consistency_score = max(camel_case_count, snake_case_count) / total_naming
        
        return features
    
    def _extract_complexity_features(self, code: str) -> CodeComplexityFeatures:
        """Trích xuất features về complexity"""
        features = CodeComplexityFeatures()
        
        lines = code.splitlines()
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('//')]
        comment_lines = [l for l in lines if l.strip().startswith('//') or '/*' in l]
        
        # Code to comment ratio
        if comment_lines:
            features.code_to_comment_ratio = len(code_lines) / len(comment_lines)
        else:
            # Use a high but finite value instead of infinity to avoid ML training issues
            features.code_to_comment_ratio = 999.0 if code_lines else 0
        
        # Simplified Halstead complexity
        operators = re.findall(r'[+\\-*/=<>!&|]+', code)
        operands = re.findall(r'\\b[a-zA-Z_][a-zA-Z0-9_]*\\b', code)
        
        unique_operators = len(set(operators))
        unique_operands = len(set(operands))
        total_operators = len(operators)
        total_operands = len(operands)
        
        if unique_operators > 0 and unique_operands > 0:
            vocabulary = unique_operators + unique_operands
            length = total_operators + total_operands
            
            if vocabulary > 0 and length > 0:
                features.halstead_complexity = length * math.log2(vocabulary)
        
        # Cognitive complexity (simplified)
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
        
        # Maintainability index (simplified)
        if features.halstead_complexity > 0 and len(code_lines) > 0:
            features.maintainability_index = max(0, 171 - 5.2 * math.log(features.halstead_complexity) - 0.23 * 1 - 16.2 * math.log(len(code_lines)))
        
        return features
    
    def _extract_ai_pattern_features(self, code: str) -> AIPatternFeatures:
        """Trích xuất features đặc trưng của AI-generated code"""
        features = AIPatternFeatures()
        
        lines = code.splitlines()
        code_content = ' '.join(lines)
        
        # Template usage score
        template_matches = 0
        for pattern in self.template_patterns:
            template_matches += len(re.findall(pattern, code, re.IGNORECASE))
        
        features.template_usage_score = template_matches / len(lines) if lines else 0
        
        # Boilerplate ratio
        boilerplate_lines = 0
        for line in lines:
            line = line.strip()
            if (line.startswith('#include') or 
                line.startswith('using namespace') or
                line == 'return 0;' or
                line == '{' or line == '}'):
                boilerplate_lines += 1
        
        features.boilerplate_ratio = boilerplate_lines / len(lines) if lines else 0
        
        # Error handling score
        error_patterns = ['if', '!=', 'NULL', 'errno', 'error', 'exception', 'try', 'catch']
        error_score = 0
        
        for pattern in error_patterns:
            error_score += code_content.lower().count(pattern.lower())
        
        features.error_handling_score = error_score / len(lines) if lines else 0
        
        # Defensive programming score
        defensive_patterns = ['assert', 'check', 'validate', 'verify', 'bounds']
        defensive_score = 0
        
        for pattern in defensive_patterns:
            defensive_score += code_content.lower().count(pattern.lower())
        
        features.defensive_programming_score = defensive_score / len(lines) if lines else 0
        
        # Over-engineering score (too many functions for simple tasks)
        function_count = len(re.findall(r'\\b(?:int|void|float|double|char|string|bool)\\s+\\w+\\s*\\(', code))
        if function_count > 1 and len(lines) < 50:  # Many functions in short code
            features.over_engineering_score = function_count / len(lines)
        
        return features

# Test and utility functions
def analyze_sample_codes():
    """Test function để so sánh AI vs Human code"""
    extractor = AdvancedFeatureExtractor()
    
    ai_code = '''#include <stdio.h>
#include <stdlib.h>

// Function to calculate the sum of two numbers
int calculateSum(int firstNumber, int secondNumber) {
    // Return the sum of both parameters
    return firstNumber + secondNumber;
}

int main() {
    int userInput1, userInput2;
    int resultSum;
    
    // Get input from user
    printf("Enter first number: ");
    scanf("%d", &userInput1);
    
    printf("Enter second number: ");
    scanf("%d", &userInput2);
    
    // Calculate the sum
    resultSum = calculateSum(userInput1, userInput2);
    
    // Display the result
    printf("The sum is: %d\\n", resultSum);
    
    return 0;
}'''

    human_code = '''#include <stdio.h>
int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d", a + b);
    return 0;
}'''
    
    print("=== AI Code Analysis ===")
    ai_features = extractor.extract_all_features(ai_code)
    print(f"LOC: {ai_features.loc}")
    print(f"Comment ratio: {ai_features.comment_ratio:.3f}")
    if ai_features.naming_patterns:
        print(f"Descriptive variables: {ai_features.naming_patterns.descriptive_var_ratio:.3f}")
    if ai_features.ai_patterns:
        print(f"Template usage: {ai_features.ai_patterns.template_usage_score:.3f}")
    
    print("\\n=== Human Code Analysis ===")
    human_features = extractor.extract_all_features(human_code)
    print(f"LOC: {human_features.loc}")
    print(f"Comment ratio: {human_features.comment_ratio:.3f}")
    if human_features.naming_patterns:
        print(f"Generic variables: {human_features.naming_patterns.generic_var_ratio:.3f}")

if __name__ == "__main__":
    analyze_sample_codes()