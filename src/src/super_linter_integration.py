#!/usr/bin/env python3
"""
Super Linter Integration
Tích hợp các công cụ linting để phân tích chất lượng code
"""

import subprocess
import tempfile
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LintResult:
    """Kết quả linting"""
    file_path: str
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    style_issues: int = 0
    complexity_score: float = 0.0
    maintainability_index: float = 0.0
    raw_output: str = ""
    tool_used: str = ""

class SuperLinterIntegration:
    """Tích hợp các công cụ linting"""
    
    def __init__(self):
        self.available_tools = self._check_available_tools()
        logger.info(f"Available linting tools: {list(self.available_tools.keys())}")
    
    def _check_available_tools(self) -> Dict[str, bool]:
        """Kiểm tra các công cụ linting có sẵn"""
        tools = {}
        
        # Check for cppcheck
        try:
            subprocess.run(['cppcheck', '--version'], 
                         capture_output=True, check=True, timeout=5)
            tools['cppcheck'] = True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            tools['cppcheck'] = False
        
        # Check for clang-tidy
        try:
            subprocess.run(['clang-tidy', '--version'], 
                         capture_output=True, check=True, timeout=5)
            tools['clang-tidy'] = True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            tools['clang-tidy'] = False
        
        # Check for lizard (complexity analyzer)
        try:
            subprocess.run(['lizard', '--version'], 
                         capture_output=True, check=True, timeout=5)
            tools['lizard'] = True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            tools['lizard'] = False
        
        # Check for gcc/g++
        try:
            subprocess.run(['gcc', '--version'], 
                         capture_output=True, check=True, timeout=5)
            tools['gcc'] = True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            tools['gcc'] = False
        
        return tools
    
    def lint_code_with_cppcheck(self, code: str, filename: str = "temp.c") -> LintResult:
        """Sử dụng cppcheck để phân tích code"""
        result = LintResult(file_path=filename, tool_used="cppcheck")
        
        if not self.available_tools.get('cppcheck', False):
            logger.warning("cppcheck not available")
            return result
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                temp_path = f.name
            
            # Run cppcheck
            cmd = [
                'cppcheck',
                '--enable=all',
                '--xml',
                '--xml-version=2',
                temp_path
            ]
            
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            result.raw_output = proc.stderr  # cppcheck outputs to stderr
            
            # Parse XML output (simplified)
            import xml.etree.ElementTree as ET
            try:
                root = ET.fromstring(result.raw_output)
                errors = root.findall('.//error')
                
                for error in errors:
                    severity = error.get('severity', '')
                    if severity in ['error']:
                        result.errors += 1
                    elif severity in ['warning']:
                        result.warnings += 1
                    elif severity in ['style', 'performance', 'portability']:
                        result.style_issues += 1
                
                result.total_issues = result.errors + result.warnings + result.style_issues
                
            except ET.ParseError:
                # If XML parsing fails, count lines with issues
                lines = result.raw_output.split('\n')
                result.total_issues = len([l for l in lines if 'error:' in l or 'warning:' in l])
            
            # Cleanup
            Path(temp_path).unlink(missing_ok=True)
            
        except subprocess.TimeoutExpired:
            logger.warning("cppcheck timeout")
        except Exception as e:
            logger.error(f"cppcheck error: {e}")
        
        return result
    
    def lint_code_with_lizard(self, code: str, filename: str = "temp.c") -> LintResult:
        """Sử dụng lizard để phân tích complexity"""
        result = LintResult(file_path=filename, tool_used="lizard")
        
        if not self.available_tools.get('lizard', False):
            logger.warning("lizard not available")
            return result
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                temp_path = f.name
            
            # Run lizard
            cmd = ['lizard', temp_path]
            
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            result.raw_output = proc.stdout
            
            # Parse lizard output
            lines = result.raw_output.split('\n')
            complexity_scores = []
            
            for line in lines:
                if temp_path in line and line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            complexity = int(parts[0])
                            complexity_scores.append(complexity)
                        except ValueError:
                            continue
            
            if complexity_scores:
                result.complexity_score = sum(complexity_scores) / len(complexity_scores)
            
            # Cleanup
            Path(temp_path).unlink(missing_ok=True)
            
        except subprocess.TimeoutExpired:
            logger.warning("lizard timeout")
        except Exception as e:
            logger.error(f"lizard error: {e}")
        
        return result
    
    def lint_code_with_gcc(self, code: str, filename: str = "temp.c") -> LintResult:
        """Sử dụng gcc để check syntax và warnings"""
        result = LintResult(file_path=filename, tool_used="gcc")
        
        if not self.available_tools.get('gcc', False):
            logger.warning("gcc not available")
            return result
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                temp_path = f.name
            
            # Run gcc with warnings
            cmd = [
                'gcc',
                '-Wall',
                '-Wextra',
                '-fsyntax-only',
                temp_path
            ]
            
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            result.raw_output = proc.stderr
            
            # Count warnings and errors
            lines = result.raw_output.split('\n')
            for line in lines:
                if 'error:' in line.lower():
                    result.errors += 1
                elif 'warning:' in line.lower():
                    result.warnings += 1
            
            result.total_issues = result.errors + result.warnings
            
            # Cleanup
            Path(temp_path).unlink(missing_ok=True)
            
        except subprocess.TimeoutExpired:
            logger.warning("gcc timeout")
        except Exception as e:
            logger.error(f"gcc error: {e}")
        
        return result
    
    def comprehensive_lint(self, code: str, filename: str = "temp.c") -> Dict[str, Any]:
        """Chạy tất cả các linting tools có sẵn"""
        results = {}
        
        # Run available tools
        if self.available_tools.get('cppcheck', False):
            results['cppcheck'] = self.lint_code_with_cppcheck(code, filename)
        
        if self.available_tools.get('lizard', False):
            results['lizard'] = self.lint_code_with_lizard(code, filename)
        
        if self.available_tools.get('gcc', False):
            results['gcc'] = self.lint_code_with_gcc(code, filename)
        
        # Aggregate results
        aggregate = {
            'total_tools_used': len(results),
            'total_issues': sum(r.total_issues for r in results.values()),
            'total_errors': sum(r.errors for r in results.values()),
            'total_warnings': sum(r.warnings for r in results.values()),
            'total_style_issues': sum(r.style_issues for r in results.values()),
            'avg_complexity': sum(r.complexity_score for r in results.values()) / len(results) if results else 0,
            'tools_results': results
        }
        
        return aggregate
    
    def install_tools_guide(self) -> str:
        """Hướng dẫn cài đặt các công cụ linting"""
        guide = """
HƯỚNG DẪN CÀI ĐẶT LINTING TOOLS
===============================

Ubuntu/Debian:
--------------
sudo apt update
sudo apt install cppcheck clang-tidy gcc g++
pip install lizard

CentOS/RHEL:
------------
sudo yum install cppcheck clang-tools-extra gcc gcc-c++
pip install lizard

MacOS (với Homebrew):
--------------------
brew install cppcheck llvm gcc
pip install lizard

Windows:
--------
- Cài đặt MSYS2 hoặc Visual Studio Build Tools
- pip install lizard
"""
        return guide

def main():
    """Test chức năng linting"""
    linter = SuperLinterIntegration()
    
    # Test code
    test_code = '''
#include <stdio.h>

int main() {
    int a, b;
    printf("Enter two numbers: ");
    scanf("%d %d", &a, &b);
    printf("Sum: %d\\n", a + b);
    return 0;
}
'''
    
    print("🔍 Testing linting tools...")
    print(f"Available tools: {linter.available_tools}")
    
    if any(linter.available_tools.values()):
        results = linter.comprehensive_lint(test_code, "test.c")
        print(f"\n📊 Lint Results:")
        print(f"Total issues: {results['total_issues']}")
        print(f"Errors: {results['total_errors']}")
        print(f"Warnings: {results['total_warnings']}")
        print(f"Style issues: {results['total_style_issues']}")
        print(f"Average complexity: {results['avg_complexity']:.2f}")
    else:
        print("\n❌ No linting tools available.")
        print(linter.install_tools_guide())

if __name__ == "__main__":
    main()
