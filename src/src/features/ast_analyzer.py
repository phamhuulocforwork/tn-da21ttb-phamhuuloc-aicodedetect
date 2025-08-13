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
    # NOTE: Cấu trúc dữ liệu cho AST features - đã chuẩn hóa
    # Structure features
    total_nodes: int = 0
    nodes_per_loc: float = 0.0  # Normalized: total_nodes / loc
    max_depth: int = 0
    avg_depth: float = 0.0
    branching_factor: float = 0.0
    
    # Control flow features - normalized
    if_statements: int = 0
    if_statements_per_loc: float = 0.0  # Normalized
    for_loops: int = 0  
    for_loops_per_loc: float = 0.0  # Normalized
    while_loops: int = 0
    while_loops_per_loc: float = 0.0  # Normalized
    switch_statements: int = 0
    switch_statements_per_loc: float = 0.0  # Normalized
    nested_control_depth: int = 0
    
    # Function features
    function_count: int = 0
    functions_per_loc: float = 0.0  # Normalized
    avg_function_length: float = 0.0
    max_function_length: int = 0
    recursive_functions: int = 0
    recursive_functions_ratio: float = 0.0  # Normalized vs total functions
    
    # Variable/naming features - normalized
    variable_count: int = 0
    variables_per_loc: float = 0.0  # Normalized
    unique_variable_names: int = 0
    variable_uniqueness_ratio: float = 0.0  # unique_vars / total_vars
    avg_variable_name_length: float = 0.0
    camel_case_vars: int = 0
    camel_case_ratio: float = 0.0  # Normalized vs total vars
    snake_case_vars: int = 0
    snake_case_ratio: float = 0.0  # Normalized vs total vars
    single_char_vars: int = 0
    single_char_vars_ratio: float = 0.0  # Normalized vs total vars
    hungarian_notation: int = 0
    hungarian_notation_ratio: float = 0.0  # Normalized vs total vars
    
    # Code pattern features - normalized
    magic_numbers: int = 0
    magic_numbers_per_loc: float = 0.0  # Normalized
    string_literals: int = 0
    string_literals_per_loc: float = 0.0  # Normalized
    include_count: int = 0
    macro_usage: int = 0
    
    # Style features
    indentation_consistency: float = 0.0
    brace_style_consistency: float = 0.0
    operator_spacing_consistency: float = 0.0

class CppASTAnalyzer:
    # NOTE: Analyzer cho C/C++ code sử dụng pattern matching và static analysis
    # NOTE: Vì C++ AST parsing phức tạp, ta sử dụng regex patterns và heuristics
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        # NOTE: Setup regex patterns cho việc phân tích code C/C++
        # FIXME: Cần tối ưu chỗ này

        # Control structures
        self.if_pattern = re.compile(r'\bif\s*\(', re.IGNORECASE)
        self.for_pattern = re.compile(r'\bfor\s*\(', re.IGNORECASE)
        self.while_pattern = re.compile(r'\bwhile\s*\(', re.IGNORECASE)
        self.switch_pattern = re.compile(r'\bswitch\s*\(', re.IGNORECASE)
        
        # Function patterns - mở rộng cho C++
        self.function_pattern = re.compile(
            r'\b(?:int|void|float|double|char|string|bool|long|short|unsigned|signed|auto|const)\s*'
            r'(?:\*\s*)?'  # optional pointer
            r'(\w+)\s*\([^)]*\)\s*(?:const\s*)?\{', re.MULTILINE
        )
        self.main_pattern = re.compile(r'\bmain\s*\([^)]*\)\s*\{', re.MULTILINE)
        
        # Variable patterns - mở rộng cho C++
        self.variable_declaration = re.compile(
            r'\b(?:int|float|double|char|string|bool|auto|long|short|unsigned|signed|const|static)\s+'
            r'(?:\*\s*)?'  # optional pointer
            r'(\w+)(?:\s*=\s*[^;]+)?', re.MULTILINE
        )
        self.camel_case = re.compile(r'\b[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\b')
        self.snake_case = re.compile(r'\b[a-z]+_[a-z_0-9]*\b')
        self.single_char = re.compile(r'\b[a-z]\b')
        self.hungarian = re.compile(r'\b[a-z]{1,3}[A-Z][a-zA-Z0-9]*\b')  # strName, nCount, etc.
        
        # Code patterns
        self.magic_number = re.compile(r'\b\d{2,}\b') 
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
        # NOTE: Phân tích code và trả về AST features với normalization
        features = ASTFeatures()
        
        # Clean code
        clean_code = self._preprocess_code(code)
        lines = clean_code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        loc = len(non_empty_lines)
        
        # Extract features
        features = self._extract_structure_features(clean_code, features)
        features = self._extract_control_flow_features(clean_code, features)
        features = self._extract_function_features(clean_code, features)
        features = self._extract_naming_features(clean_code, features)
        features = self._extract_pattern_features(clean_code, features)
        features = self._extract_style_features(lines, features)
        
        # Normalize features theo LOC và các metrics khác
        features = self._normalize_features(features, loc)
        
        return features
    
    def _preprocess_code(self, code: str) -> str:
        # NOTE: Tiền xử lý code để loại bỏ comments và normalize
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'\n\s*\n', '\n', code)
        
        return code
    
    def _extract_structure_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        # NOTE: Trích xuất đặc trưng cấu trúc cơ bản
        lines = code.split('\n')
        non_empty_lines = len([l for l in lines if l.strip()])
        
        # Estimate total nodes: statements, expressions, declarations
        # Rough heuristic: count significant code elements
        statements = 0
        for line in lines:
            line = line.strip()
            if line and not line.startswith('//') and not line.startswith('/*'):
                # Count statements (lines ending with ; or { or })
                if line.endswith(';') or line.endswith('{') or line.endswith('}'):
                    statements += 1
                # Count declarations
                if any(keyword in line for keyword in ['int ', 'float ', 'double ', 'char ', 'void ']):
                    statements += 1
        
        features.total_nodes = max(statements, non_empty_lines)  # At least as many as LOC
        
        # NOTE: Ước lượng độ sâu từ indentation
        max_indent = 0
        total_indent = 0
        indent_count = 0
        
        for line in lines:
            if line.strip():
                # NOTE: Đếm số khoảng trắng/tab ở đầu dòng
                spaces = len(line) - len(line.lstrip())
                indent_level = spaces // 4  # NOTE: Giả sử 4 khoảng trắng cho mỗi level
                max_indent = max(max_indent, indent_level)
                total_indent += indent_level
                indent_count += 1
        
        features.max_depth = max_indent
        features.avg_depth = total_indent / indent_count if indent_count > 0 else 0
        
        # NOTE: Ước lượng branching factor (rough estimate)
        brace_open = code.count('{')
        features.branching_factor = brace_open / len(lines) if lines else 0
        
        return features
    
    def _extract_control_flow_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        # NOTE: Trích xuất đặc trưng control flow
        features.if_statements = len(self.if_pattern.findall(code))
        features.for_loops = len(self.for_pattern.findall(code))
        features.while_loops = len(self.while_pattern.findall(code))
        features.switch_statements = len(self.switch_pattern.findall(code))
        
        # NOTE: Ước lượng độ sâu lồng nhau của control flow
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
        # NOTE: Trích xuất đặc trưng functions
        functions = self.function_pattern.findall(code)
        features.function_count = len(functions)
        
        if features.function_count > 0:
            # NOTE: Ước lượng độ dài của các hàm
            function_blocks = re.split(r'\b(?:int|void|float|double|char|string|bool)\s+\w+\s*\([^)]*\)\s*\{', code)
            lengths = []
            
            for block in function_blocks[1:]:  # NOTE: Bỏ qua phần đầu tiên
                # NOTE: Đếm số dòng cho đến khi gặp dấu ngoặc nhọn
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
        
        # NOTE: Kiểm tra các hàm đệ quy (basic heuristic)
        for func_name in functions:
            if code.count(func_name) > 1:  # NOTE: Tên hàm xuất hiện nhiều lần
                features.recursive_functions += 1
        
        return features
    
    def _extract_naming_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        # NOTE: Trích xuất đặc trưng naming patterns
        variables = self.variable_declaration.findall(code)
        features.variable_count = len(variables)
        features.unique_variable_names = len(set(variables))
        
        if variables:
            features.avg_variable_name_length = sum(len(v) for v in variables) / len(variables)
        
        # NOTE: Đếm các patterns naming - tối ưu để tránh false positives
        features.camel_case_vars = len(self.camel_case.findall(code))
        features.snake_case_vars = len(self.snake_case.findall(code))
        
        # NOTE: Cải thiện detection single char vars - chỉ đếm declared variables
        single_char_vars = []
        for var in variables:
            if len(var) == 1 and var.isalpha():
                single_char_vars.append(var)
        
        # NOTE: Thêm common single char vars trong context (i, j, k trong loops)
        loop_context_chars = self._find_loop_variables(code)
        single_char_vars.extend(loop_context_chars)
        
        features.single_char_vars = len(set(single_char_vars))  # Unique count
        features.hungarian_notation = len(self.hungarian.findall(code))
        
        return features
    
    def _find_loop_variables(self, code: str) -> List[str]:
        """Tìm single-character variables trong context của loops"""
        loop_vars = []
        
        # Pattern for loop declarations: for(int i = 0; i < n; i++)
        for_loop_pattern = re.compile(r'for\s*\(\s*(?:int\s+)?([a-zA-Z])\s*[=;]', re.IGNORECASE)
        loop_declarations = for_loop_pattern.findall(code)
        
        # Chỉ lấy các single characters thực sự trong loops
        for var in loop_declarations:
            if len(var) == 1 and var.isalpha():
                loop_vars.append(var)
        
        return loop_vars

    def _extract_pattern_features(self, code: str, features: ASTFeatures) -> ASTFeatures:
        # NOTE: Trích xuất đặc trưng code patterns
        features.magic_numbers = len(self.magic_number.findall(code))
        features.string_literals = len(self.string_literal.findall(code))
        features.include_count = len(self.include_pattern.findall(code))
        features.macro_usage = len(self.macro_pattern.findall(code))
        
        return features
    
    def _extract_style_features(self, lines: List[str], features: ASTFeatures) -> ASTFeatures:
        # NOTE: Trích xuất đặc trưng style consistency
        # NOTE: Độ nhất quán của indentation
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
        
        # NOTE: Độ nhất quán của brace style
        full_code = '\n'.join(lines)
        newline_braces = len(self.brace_newline.findall(full_code))
        sameline_braces = len(self.brace_sameline.findall(full_code))
        total_braces = newline_braces + sameline_braces
        
        if total_braces > 0:
            features.brace_style_consistency = max(newline_braces, sameline_braces) / total_braces
        
        # NOTE: Độ nhất quán của operator spacing
        operators = self.operator_spacing.findall(full_code)
        consistent_spacing = 0
        
        for before, op, after in operators:
            # NOTE: Kiểm tra nếu khoảng cách là nhất quán (simplified check)
            if before and after:  # NOTE: Cả hai đều có khoảng cách
                consistent_spacing += 1
        
        if operators:
            features.operator_spacing_consistency = consistent_spacing / len(operators)
        
        return features
    
    def _normalize_features(self, features: ASTFeatures, loc: int) -> ASTFeatures:
        """Chuẩn hóa features theo LOC và các metrics khác"""
        
        # Avoid division by zero
        safe_loc = max(1, loc)
        safe_variable_count = max(1, features.variable_count)
        safe_function_count = max(1, features.function_count)
        
        # Normalize structure features - sử dụng LOC thực tế, không phải total_nodes
        features.nodes_per_loc = features.total_nodes / safe_loc
        
        # Normalize control flow features
        features.if_statements_per_loc = features.if_statements / safe_loc
        features.for_loops_per_loc = features.for_loops / safe_loc
        features.while_loops_per_loc = features.while_loops / safe_loc
        features.switch_statements_per_loc = features.switch_statements / safe_loc
        
        # Normalize function features
        features.functions_per_loc = features.function_count / safe_loc
        features.recursive_functions_ratio = features.recursive_functions / safe_function_count
        
        # Normalize variable features
        features.variables_per_loc = features.variable_count / safe_loc
        features.variable_uniqueness_ratio = features.unique_variable_names / safe_variable_count
        features.camel_case_ratio = features.camel_case_vars / safe_variable_count
        features.snake_case_ratio = features.snake_case_vars / safe_variable_count
        features.single_char_vars_ratio = features.single_char_vars / safe_variable_count
        features.hungarian_notation_ratio = features.hungarian_notation / safe_variable_count
        
        # Normalize pattern features
        features.magic_numbers_per_loc = features.magic_numbers / safe_loc
        features.string_literals_per_loc = features.string_literals / safe_loc
        
        return features

def analyze_code_file(file_path: str) -> ASTFeatures:
    # NOTE: Phân tích một file code
    analyzer = CppASTAnalyzer()
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read()
    
    return analyzer.analyze_code(code, file_path)

def batch_analyze_directory(directory: str, max_files: int = 100) -> List[Tuple[str, ASTFeatures]]:
    # NOTE: Phân tích batch một directory
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