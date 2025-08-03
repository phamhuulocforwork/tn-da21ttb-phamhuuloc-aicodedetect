"""
AST (Abstract Syntax Tree) Analyzer for C/C++ Code
Phân tích cấu trúc cú pháp để trích xuất đặc trưng cho AI detection
"""

import re
import ast
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import Counter, defaultdict

@dataclass
class ASTFeatures:
    """Cấu trúc dữ liệu cho AST features"""
    # Structure features
    total_nodes: int = 0
    max_depth: int = 0
    avg_depth: float = 0.0
    branching_factor: float = 0.0
    
    # Control flow features
    if_statements: int = 0
    for_loops: int = 0
    while_loops: int = 0
    switch_statements: int = 0
    nested_control_depth: int = 0
    
    # Function features
    function_count: int = 0
    avg_function_length: float = 0.0
    max_function_length: int = 0
    recursive_functions: int = 0
    
    # Variable/naming features
    variable_count: int = 0
    unique_variable_names: int = 0
    avg_variable_name_length: float = 0.0
    camel_case_vars: int = 0
    snake_case_vars: int = 0
    single_char_vars: int = 0
    hungarian_notation: int = 0
    
    # Code pattern features
    magic_numbers: int = 0
    string_literals: int = 0
    include_count: int = 0
    macro_usage: int = 0
    
    # Style features
    indentation_consistency: float = 0.0
    brace_style_consistency: float = 0.0
    operator_spacing_consistency: float = 0.0

class CppASTAnalyzer:
    """
    Analyzer cho C/C++ code sử dụng pattern matching và static analysis
    (Vì C++ AST parsing phức tạp, ta sử dụng regex patterns và heuristics)
    """
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns cho C/C++ analysis"""
        # Control structures
        self.if_pattern = re.compile(r'\bif\s*\(', re.IGNORECASE)
        self.for_pattern = re.compile(r'\bfor\s*\(', re.IGNORECASE)
        self.while_pattern = re.compile(r'\bwhile\s*\(', re.IGNORECASE)
        self.switch_pattern = re.compile(r'\bswitch\s*\(', re.IGNORECASE)
        
        # Function patterns
        self.function_pattern = re.compile(r'\b(?:int|void|float|double|char|string|bool)\s+(\w+)\s*\([^)]*\)\s*\{', re.MULTILINE)
        self.main_pattern = re.compile(r'\bmain\s*\([^)]*\)\s*\{', re.MULTILINE)
        
        # Variable patterns
        self.variable_declaration = re.compile(r'\b(?:int|float|double|char|string|bool|auto)\s+(\w+)', re.MULTILINE)
        self.camel_case = re.compile(r'\b[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\b')
        self.snake_case = re.compile(r'\b[a-z]+_[a-z_0-9]*\b')
        self.single_char = re.compile(r'\b[a-z]\b')
        self.hungarian = re.compile(r'\b[a-z]{1,3}[A-Z][a-zA-Z0-9]*\b')  # strName, nCount, etc.
        
        # Code patterns
        self.magic_number = re.compile(r'\b\d{2,}\b')  # Numbers >= 10
        self.string_literal = re.compile(r'"[^"]*"')
        self.include_pattern = re.compile(r'#include\s*[<"][^>"]*[>"]')
        self.macro_pattern = re.compile(r'#define\s+\w+')
        
        # Style patterns
        self.indentation_spaces = re.compile(r'^( +)', re.MULTILINE)
        self.indentation_tabs = re.compile(r'^(\t+)', re.MULTILINE)
        self.brace_newline = re.compile(r'\{\s*\n')
        self.brace_sameline = re.compile(r'\S\s*\{')
        self.operator_spacing = re.compile(r'(\w+)\s*([=+\-*/])\s*(\w+)')
    
    def analyze_code(self, code: str, filename: str = "") -> ASTFeatures:
        """
        Phân tích code và trả về AST features
        """
        features = ASTFeatures()
        
        # Clean code
        clean_code = self._preprocess_code(code)
        lines = clean_code.split('\n')
        
        # Extract features
        features = self._extract_structure_features(clean_code, features)
        features = self._extract_control_flow_features(clean_code, features)
        features = self._extract_function_features(clean_code, features)
        features = self._extract_naming_features(clean_code, features)
        features = self._extract_pattern_features(clean_code, features)
        features = self._extract_style_features(lines, features)
        
        return features
    
    def _preprocess_code(self, code: str) -> str:
        """Tiền xử lý code để loại bỏ comments và normalize"""
        # Remove single-line comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        
        # Remove multi-line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        # Remove empty lines
        code = re.sub(r'\n\s*\n', '\n', code)
        
        return code
    
    def _extract_structure_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        """Trích xuất đặc trưng cấu trúc cơ bản"""
        lines = code.split('\n')
        features.total_nodes = len([l for l in lines if l.strip()])
        
        # Estimate depth from indentation
        max_indent = 0
        total_indent = 0
        indent_count = 0
        
        for line in lines:
            if line.strip():
                # Count leading spaces/tabs
                spaces = len(line) - len(line.lstrip())
                indent_level = spaces // 4  # Assume 4 spaces per level
                max_indent = max(max_indent, indent_level)
                total_indent += indent_level
                indent_count += 1
        
        features.max_depth = max_indent
        features.avg_depth = total_indent / indent_count if indent_count > 0 else 0
        
        # Branching factor (rough estimate)
        brace_open = code.count('{')
        features.branching_factor = brace_open / len(lines) if lines else 0
        
        return features
    
    def _extract_control_flow_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        """Trích xuất đặc trưng control flow"""
        features.if_statements = len(self.if_pattern.findall(code))
        features.for_loops = len(self.for_pattern.findall(code))
        features.while_loops = len(self.while_pattern.findall(code))
        features.switch_statements = len(self.switch_pattern.findall(code))
        
        # Estimate nested control depth
        max_nested = 0
        current_nested = 0
        
        for line in code.split('\n'):
            line = line.strip()
            if any(pattern.search(line) for pattern in [self.if_pattern, self.for_pattern, self.while_pattern]):
                current_nested += 1
                max_nested = max(max_nested, current_nested)
            elif line.startswith('}'):
                current_nested = max(0, current_nested - 1)
        
        features.nested_control_depth = max_nested
        return features
    
    def _extract_function_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        """Trích xuất đặc trưng functions"""
        functions = self.function_pattern.findall(code)
        features.function_count = len(functions)
        
        if features.function_count > 0:
            # Estimate function lengths
            function_blocks = re.split(r'\b(?:int|void|float|double|char|string|bool)\s+\w+\s*\([^)]*\)\s*\{', code)
            lengths = []
            
            for block in function_blocks[1:]:  # Skip first split
                # Count lines until matching brace
                brace_count = 1
                lines_count = 0
                for line in block.split('\n'):
                    if brace_count <= 0:
                        break
                    lines_count += 1
                    brace_count += line.count('{') - line.count('}')
                lengths.append(lines_count)
            
            if lengths:
                features.avg_function_length = sum(lengths) / len(lengths)
                features.max_function_length = max(lengths)
        
        # Check for recursive functions (basic heuristic)
        for func_name in functions:
            if code.count(func_name) > 1:  # Function name appears multiple times
                features.recursive_functions += 1
        
        return features
    
    def _extract_naming_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        """Trích xuất đặc trưng naming patterns"""
        # Find variable declarations
        variables = self.variable_declaration.findall(code)
        features.variable_count = len(variables)
        features.unique_variable_names = len(set(variables))
        
        if variables:
            features.avg_variable_name_length = sum(len(v) for v in variables) / len(variables)
        
        # Count naming patterns
        features.camel_case_vars = len(self.camel_case.findall(code))
        features.snake_case_vars = len(self.snake_case.findall(code))
        features.single_char_vars = len(self.single_char.findall(code))
        features.hungarian_notation = len(self.hungarian.findall(code))
        
        return features
    
    def _extract_pattern_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        """Trích xuất đặc trưng code patterns"""
        features.magic_numbers = len(self.magic_number.findall(code))
        features.string_literals = len(self.string_literal.findall(code))
        features.include_count = len(self.include_pattern.findall(code))
        features.macro_usage = len(self.macro_pattern.findall(code))
        
        return features
    
    def _extract_style_features(self, lines: List[str], features: ASTFeatures) -> ASTFeatures:
        """Trích xuất đặc trưng style consistency"""
        # Indentation consistency
        space_indents = 0
        tab_indents = 0
        
        for line in lines:
            if line.startswith(' '):
                space_indents += 1
            elif line.startswith('\t'):
                tab_indents += 1
        
        total_indents = space_indents + tab_indents
        if total_indents > 0:
            features.indentation_consistency = max(space_indents, tab_indents) / total_indents
        
        # Brace style consistency
        full_code = '\n'.join(lines)
        newline_braces = len(self.brace_newline.findall(full_code))
        sameline_braces = len(self.brace_sameline.findall(full_code))
        total_braces = newline_braces + sameline_braces
        
        if total_braces > 0:
            features.brace_style_consistency = max(newline_braces, sameline_braces) / total_braces
        
        # Operator spacing consistency
        operators = self.operator_spacing.findall(full_code)
        consistent_spacing = 0
        
        for before, op, after in operators:
            # Check if spacing is consistent (simplified check)
            if before and after:  # Both have spacing
                consistent_spacing += 1
        
        if operators:
            features.operator_spacing_consistency = consistent_spacing / len(operators)
        
        return features

# Utility functions
def analyze_code_file(file_path: str) -> ASTFeatures:
    """Phân tích một file code"""
    analyzer = CppASTAnalyzer()
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    
    return analyzer.analyze_code(code, file_path)

def batch_analyze_directory(directory: str, max_files: int = 100) -> List[Tuple[str, ASTFeatures]]:
    """Phân tích batch một directory"""
    results = []
    
    for file_path in Path(directory).rglob('*.c'):
        if len(results) >= max_files:
            break
        
        try:
            features = analyze_code_file(str(file_path))
            results.append((str(file_path), features))
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    for file_path in Path(directory).rglob('*.cpp'):
        if len(results) >= max_files:
            break
        
        try:
            features = analyze_code_file(str(file_path))
            results.append((str(file_path), features))
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    return results

if __name__ == "__main__":
    # Test the analyzer
    sample_code = '''
    #include <stdio.h>
    #include <stdlib.h>
    
    int calculateSum(int firstNumber, int secondNumber) {
        return firstNumber + secondNumber;
    }
    
    int main() {
        int userInput1, userInput2;
        printf("Enter numbers: ");
        scanf("%d %d", &userInput1, &userInput2);
        
        int result = calculateSum(userInput1, userInput2);
        printf("Result: %d", result);
        
        return 0;
    }
    '''
    
    analyzer = CppASTAnalyzer()
    features = analyzer.analyze_code(sample_code)
    print(f"Sample analysis: {features}")