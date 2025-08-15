#!/usr/bin/env python3
"""
Human Style Analyzer
Phân tích các patterns đặc trưng của code do con người viết mà AI thường không mắc phải
Bao gồm: spacing, indentation, naming inconsistency, formatting issues
"""

import re
import math
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict

@dataclass
class SpacingIssues:
    """Các vấn đề về khoảng trắng"""
    # Khoảng trắng xung quanh operators
    missing_space_before_operator: int = 0
    missing_space_after_operator: int = 0
    extra_space_before_operator: int = 0
    extra_space_after_operator: int = 0
    
    # Khoảng trắng xung quanh dấu phẩy và chấm phẩy
    missing_space_after_comma: int = 0
    missing_space_after_semicolon: int = 0
    extra_space_before_comma: int = 0
    extra_space_before_semicolon: int = 0
    
    # Khoảng trắng trong ngoặc
    space_after_opening_paren: int = 0
    space_before_closing_paren: int = 0
    missing_space_before_opening_paren: int = 0
    
    # Trailing spaces và line ending issues
    trailing_spaces: int = 0
    empty_lines_with_spaces: int = 0
    
    # Tỷ lệ các issues so với tổng số dòng
    spacing_issues_ratio: float = 0.0

@dataclass
class IndentationIssues:
    """Các vấn đề về indentation"""
    # Tab vs Space inconsistency
    mixed_tabs_spaces: int = 0
    inconsistent_indentation: int = 0
    
    # Indentation depth issues
    unusual_indent_size: int = 0  # Không phải 2, 4, 8 spaces
    over_indented_lines: int = 0
    under_indented_lines: int = 0
    
    # Alignment issues
    poor_continuation_alignment: int = 0
    
    # Tỷ lệ các issues
    indentation_issues_ratio: float = 0.0

@dataclass
class NamingInconsistency:
    """Các vấn đề về naming convention không nhất quán"""
    # Mixed naming styles
    mixed_camel_snake: int = 0
    inconsistent_variable_naming: int = 0
    inconsistent_function_naming: int = 0
    
    # Poor naming choices
    unclear_abbreviations: int = 0
    inconsistent_abbreviations: int = 0
    magic_numbers_without_constants: int = 0
    
    # Global variable misuse
    excessive_global_vars: int = 0
    uncontrolled_global_usage: int = 0
    
    # Tỷ lệ naming issues
    naming_inconsistency_ratio: float = 0.0

@dataclass
class FormattingIssues:
    """Các vấn đề về formatting tổng thể"""
    # Brace placement inconsistency
    inconsistent_brace_style: int = 0
    unnecessary_nested_braces: int = 0
    
    # Line breaks and structure
    inappropriate_line_breaks: int = 0
    too_long_lines: int = 0
    too_short_logical_blocks: int = 0
    
    # Comments formatting
    poor_comment_formatting: int = 0
    inconsistent_comment_style: int = 0
    
    # Tỷ lệ formatting issues
    formatting_issues_ratio: float = 0.0

@dataclass
class HumanStyleFeatures:
    """Tập hợp đầy đủ các features về style đặc trưng của con người"""
    spacing: SpacingIssues
    indentation: IndentationIssues  
    naming: NamingInconsistency
    formatting: FormattingIssues
    
    # Overall human-likeness score
    overall_human_score: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary cho ML processing"""
        result = {}
        
        # Spacing features
        spacing_dict = asdict(self.spacing)
        result.update({f'spacing_{k}': v for k, v in spacing_dict.items()})
        
        # Indentation features
        indent_dict = asdict(self.indentation)
        result.update({f'indentation_{k}': v for k, v in indent_dict.items()})
        
        # Naming features  
        naming_dict = asdict(self.naming)
        result.update({f'naming_inconsistency_{k}': v for k, v in naming_dict.items()})
        
        # Formatting features
        format_dict = asdict(self.formatting)
        result.update({f'formatting_{k}': v for k, v in format_dict.items()})
        
        # Overall score
        result['human_style_overall_score'] = self.overall_human_score
        
        return result

class HumanStyleAnalyzer:
    """Analyzer cho human-specific coding patterns"""
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns cho các vấn đề phổ biến"""
        
        # Operator spacing patterns
        self.operators = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '&', '|']
        
        # Common poor naming patterns
        self.poor_naming_patterns = [
            r'\b[a-z]+\d+\b',  # var1, temp2, etc.
            r'\b[a-z]{1,2}\b',  # Very short names
            r'\btemp\w*\b',    # temp variables
            r'\bvar\w*\b',     # var variables
            r'\bfoo\w*\b',     # foo variables
            r'\bbar\w*\b',     # bar variables
        ]
        
        # Global variable patterns
        self.global_patterns = [
            r'^\s*(?:int|float|double|char|string)\s+[a-zA-Z_]\w*\s*[=;]',
            r'^\s*(?:extern|static)\s+',
        ]
        
        # Magic number patterns (literals that should be constants)ư
        self.magic_number_patterns = [
            r'\b(?:[1-9]\d{2,}|[2-9]\d)\b',  # Numbers > 9 (excluding 0, 1)
            r'\b0x[0-9a-fA-F]{3,}\b',         # Large hex numbers
        ]
        
        # Function call patterns for spacing analysis
        self.function_call_pattern = re.compile(r'\w+\s*\([^)]*\)')
        
        # Control structure patterns
        self.control_structures = ['if', 'for', 'while', 'switch', 'do']
    
    def analyze_code(self, code: str, filename: str = "") -> HumanStyleFeatures:
        """Phân tích code và trả về human style features"""
        
        lines = code.splitlines()
        
        # Analyze từng khía cạnh
        spacing = self._analyze_spacing_issues(lines, code)
        indentation = self._analyze_indentation_issues(lines)
        naming = self._analyze_naming_inconsistency(code)
        formatting = self._analyze_formatting_issues(lines, code)
        
        # Calculate overall human-likeness score
        overall_score = self._calculate_human_score(spacing, indentation, naming, formatting)
        
        return HumanStyleFeatures(
            spacing=spacing,
            indentation=indentation,
            naming=naming,
            formatting=formatting,
            overall_human_score=overall_score
        )
    
    def _analyze_spacing_issues(self, lines: List[str], code: str) -> SpacingIssues:
        """Phân tích các vấn đề về spacing"""
        issues = SpacingIssues()
        
        for line_num, line in enumerate(lines):
            if not line.strip():
                # Check empty lines with spaces
                if line and not line.isspace():
                    issues.empty_lines_with_spaces += 1
                continue
            
            # Check trailing spaces
            if line.endswith(' ') or line.endswith('\t'):
                issues.trailing_spaces += 1
            
            # Check operator spacing
            for op in self.operators:
                # Missing space before operator: var+1, x=5
                pattern_before = re.compile(rf'\w{re.escape(op)}')
                if pattern_before.search(line):
                    issues.missing_space_before_operator += len(pattern_before.findall(line))
                
                # Missing space after operator: x+ 1, y =5
                pattern_after = re.compile(rf'{re.escape(op)}\w')
                if pattern_after.search(line):
                    issues.missing_space_after_operator += len(pattern_after.findall(line))
                
                # Extra spaces: x  +  1, y   =   5
                pattern_extra_before = re.compile(rf'\w\s{{2,}}{re.escape(op)}')
                if pattern_extra_before.search(line):
                    issues.extra_space_before_operator += len(pattern_extra_before.findall(line))
                
                pattern_extra_after = re.compile(rf'{re.escape(op)}\s{{2,}}\w')
                if pattern_extra_after.search(line):
                    issues.extra_space_after_operator += len(pattern_extra_after.findall(line))
            
            # Check comma and semicolon spacing
            # Missing space after comma: func(a,b,c)
            if re.search(r',\w', line):
                issues.missing_space_after_comma += len(re.findall(r',\w', line))
            
            # Extra space before comma: func(a , b , c)
            if re.search(r'\w\s+,', line):
                issues.extra_space_before_comma += len(re.findall(r'\w\s+,', line))
            
            # Missing space after semicolon in for loops: for(i=0;i<n;i++)
            if re.search(r';\w', line):
                issues.missing_space_after_semicolon += len(re.findall(r';\w', line))
            
            # Extra space before semicolon: for(i=0 ; i<n ; i++)
            if re.search(r'\w\s+;', line):
                issues.extra_space_before_semicolon += len(re.findall(r'\w\s+;', line))
            
            # Check parentheses spacing
            # Space after opening paren: func( a, b)
            if re.search(r'\(\s+\w', line):
                issues.space_after_opening_paren += len(re.findall(r'\(\s+\w', line))
            
            # Space before closing paren: func(a, b )
            if re.search(r'\w\s+\)', line):
                issues.space_before_closing_paren += len(re.findall(r'\w\s+\)', line))
            
            # Missing space before opening paren in control structures: if(condition)
            for ctrl in self.control_structures:
                pattern = rf'\b{ctrl}\('
                if re.search(pattern, line):
                    issues.missing_space_before_opening_paren += len(re.findall(pattern, line))
        
        # Calculate spacing issues ratio
        total_lines = len([l for l in lines if l.strip()])
        if total_lines > 0:
            total_spacing_issues = (
                issues.missing_space_before_operator + issues.missing_space_after_operator +
                issues.extra_space_before_operator + issues.extra_space_after_operator +
                issues.missing_space_after_comma + issues.extra_space_before_comma +
                issues.missing_space_after_semicolon + issues.extra_space_before_semicolon +
                issues.space_after_opening_paren + issues.space_before_closing_paren +
                issues.missing_space_before_opening_paren + issues.trailing_spaces +
                issues.empty_lines_with_spaces
            )
            issues.spacing_issues_ratio = total_spacing_issues / total_lines
        
        return issues
    
    def _analyze_indentation_issues(self, lines: List[str]) -> IndentationIssues:
        """Phân tích các vấn đề về indentation"""
        issues = IndentationIssues()
        
        tab_lines = 0
        space_lines = 0
        indent_sizes = []
        prev_indent = 0
        
        for line_num, line in enumerate(lines):
            if not line.strip():
                continue
            
            # Check for leading whitespace
            leading_whitespace = len(line) - len(line.lstrip())
            if leading_whitespace == 0:
                continue
            
            # Check for mixed tabs and spaces
            leading_part = line[:leading_whitespace]
            has_tabs = '\t' in leading_part
            has_spaces = ' ' in leading_part
            
            if has_tabs and has_spaces:
                issues.mixed_tabs_spaces += 1
            elif has_tabs:
                tab_lines += 1
            elif has_spaces:
                space_lines += 1
                
                # Analyze space-based indentation
                space_count = len(leading_part)
                indent_sizes.append(space_count)
                
                # Check for unusual indent sizes
                if space_count % 2 != 0 and space_count % 4 != 0 and space_count % 8 != 0:
                    issues.unusual_indent_size += 1
            
            # Check for inconsistent indentation changes
            current_indent = leading_whitespace
            indent_change = current_indent - prev_indent
            
            # Detect poor indentation patterns
            if abs(indent_change) > 8:  # Very large indent changes
                issues.over_indented_lines += 1
            elif indent_change < 0 and abs(indent_change) not in [2, 4, 8]:  # Poor unindent
                issues.under_indented_lines += 1
            
            prev_indent = current_indent
        
        # Check for mixed indentation styles (both tabs and spaces used)
        if tab_lines > 0 and space_lines > 0:
            issues.inconsistent_indentation = min(tab_lines, space_lines)
        
        # Analyze space indentation consistency
        if indent_sizes:
            # Find most common indent increment
            indent_diffs = []
            for i in range(1, len(indent_sizes)):
                diff = abs(indent_sizes[i] - indent_sizes[i-1])
                if diff > 0:
                    indent_diffs.append(diff)
            
            if indent_diffs:
                common_indent = Counter(indent_diffs).most_common(1)[0][0]
                # Count lines that don't follow the common pattern
                for diff in indent_diffs:
                    if diff != common_indent and diff % common_indent != 0:
                        issues.inconsistent_indentation += 1
        
        # Calculate indentation issues ratio
        total_indented_lines = len([l for l in lines if l.strip() and (len(l) - len(l.lstrip())) > 0])
        if total_indented_lines > 0:
            total_indent_issues = (
                issues.mixed_tabs_spaces + issues.inconsistent_indentation +
                issues.unusual_indent_size + issues.over_indented_lines +
                issues.under_indented_lines + issues.poor_continuation_alignment
            )
            issues.indentation_issues_ratio = total_indent_issues / total_indented_lines
        
        return issues
    
    def _analyze_naming_inconsistency(self, code: str) -> NamingInconsistency:
        """Phân tích naming convention inconsistency"""
        issues = NamingInconsistency()
        
        # Extract all identifiers
        identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
        variables = re.findall(r'\b(?:int|float|double|char|string|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b', code)
        functions = re.findall(r'\b(?:int|void|float|double|char|string|bool)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
        
        # Analyze naming style consistency
        camel_case_count = 0
        snake_case_count = 0
        
        for var in variables:
            if re.match(r'^[a-z][a-zA-Z0-9]*[A-Z]', var):  # camelCase
                camel_case_count += 1
            elif '_' in var and var.islower():  # snake_case
                snake_case_count += 1
        
        # Mixed camelCase and snake_case in same code
        if camel_case_count > 0 and snake_case_count > 0:
            issues.mixed_camel_snake = min(camel_case_count, snake_case_count)
        
        # Inconsistent variable naming patterns
        if len(variables) > 1:
            naming_patterns = []
            for var in variables:
                if re.match(r'^[a-z][a-zA-Z0-9]*[A-Z]', var):
                    naming_patterns.append('camel')
                elif '_' in var:
                    naming_patterns.append('snake')
                elif var.islower():
                    naming_patterns.append('lower')
                elif var.isupper():
                    naming_patterns.append('upper')
                else:
                    naming_patterns.append('mixed')
            
            pattern_counts = Counter(naming_patterns)
            if len(pattern_counts) > 2:  # More than 2 different patterns
                issues.inconsistent_variable_naming = len(pattern_counts) - 1
        
        # Poor naming choices
        for pattern in self.poor_naming_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            issues.unclear_abbreviations += len(matches)
        
        # Check for magic numbers
        magic_numbers = []
        for pattern in self.magic_number_patterns:
            magic_numbers.extend(re.findall(pattern, code))
        
        issues.magic_numbers_without_constants = len(magic_numbers)
        
        # Calculate naming inconsistency ratio
        total_identifiers = len(set(identifiers))
        if total_identifiers > 0:
            total_naming_issues = (
                issues.mixed_camel_snake + issues.inconsistent_variable_naming +
                issues.inconsistent_function_naming + issues.unclear_abbreviations +
                issues.inconsistent_abbreviations + issues.magic_numbers_without_constants +
                issues.excessive_global_vars + issues.uncontrolled_global_usage
            )
            issues.naming_inconsistency_ratio = total_naming_issues / total_identifiers
        
        return issues
    
    def _analyze_formatting_issues(self, lines: List[str], code: str) -> FormattingIssues:
        """Phân tích formatting issues"""
        issues = FormattingIssues()
        
        brace_styles = []
        comment_styles = []
        
        for line_num, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            
            # Check brace style consistency
            if '{' in line:
                if stripped == '{':  # Allman style
                    brace_styles.append('allman')
                elif stripped.endswith('{'):  # K&R style
                    brace_styles.append('kr')
                else:  # Mixed or other
                    brace_styles.append('mixed')
            
            # Check line length
            if len(line) > 120:  # Very long lines
                issues.too_long_lines += 1
            
            # Check comment formatting
            if '//' in line:
                comment_part = line[line.index('//'):]
                if comment_part.startswith('//'):
                    if comment_part.startswith('// '):  # Good spacing
                        comment_styles.append('spaced')
                    elif comment_part.startswith('//'):  # No space
                        comment_styles.append('nospace')
                        issues.poor_comment_formatting += 1
        
        # Check brace style consistency
        if brace_styles:
            style_counts = Counter(brace_styles)
            if len(style_counts) > 1:  # Mixed brace styles
                issues.inconsistent_brace_style = len(style_counts) - 1
        
        # Check comment style consistency
        if comment_styles:
            comment_counts = Counter(comment_styles)
            if len(comment_counts) > 1:
                issues.inconsistent_comment_style = len(comment_counts) - 1
        
        # Calculate formatting issues ratio
        total_code_lines = len([l for l in lines if l.strip()])
        if total_code_lines > 0:
            total_format_issues = (
                issues.inconsistent_brace_style + issues.unnecessary_nested_braces +
                issues.inappropriate_line_breaks + issues.too_long_lines +
                issues.too_short_logical_blocks + issues.poor_comment_formatting +
                issues.inconsistent_comment_style
            )
            issues.formatting_issues_ratio = total_format_issues / total_code_lines
        
        return issues
    
    def _calculate_human_score(self, spacing: SpacingIssues, indentation: IndentationIssues,
                             naming: NamingInconsistency, formatting: FormattingIssues) -> float:
        """Tính overall human-likeness score"""
        
        # Weight different types of issues
        spacing_weight = 0.3
        indentation_weight = 0.3  
        naming_weight = 0.25
        formatting_weight = 0.15
        
        # Calculate weighted score (higher score = more human-like issues)
        score = (
            spacing.spacing_issues_ratio * spacing_weight +
            indentation.indentation_issues_ratio * indentation_weight +
            naming.naming_inconsistency_ratio * naming_weight +
            formatting.formatting_issues_ratio * formatting_weight
        )
        
        # Normalize to 0-1 scale and cap at 1.0
        return min(1.0, score)