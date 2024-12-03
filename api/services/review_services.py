# services/review_service.py
import re
import ast
import difflib
import radon.metrics
import radon.complexity
from typing import Dict, List, Any, Optional

class CodeReviewService:
    def generate_code_review(self, pr_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive code review for a pull request
        
        Args:
            pr_details (dict): Details of the pull request including patch and files
        
        Returns:
            dict: Structured code review results
        """
        files = self._parse_patch_files(pr_details.get('patch', ''))
        issues = []
        
        for file_path in files:
            file_issues = self._analyze_file(file_path, pr_details.get('patch', ''))
            issues.extend(file_issues)
        
        return self._structure_review_results(files, issues)
    
    def _parse_patch_files(self, patch_content: str) -> List[str]:
        """
        Extract unique filenames from GitHub patch
        
        Args:
            patch_content (str): Raw patch content
        
        Returns:
            List of modified file paths
        """
        file_pattern = re.compile(r'^\+\+\+ b/(.+)', re.MULTILINE)
        return list(set(file_pattern.findall(patch_content)))
    
    def _analyze_file(self, file_path: str, patch_content: str) -> List[Dict[str, Any]]:
        """
        Perform comprehensive analysis on a single file
        
        Args:
            file_path (str): Path of the file to analyze
            patch_content (str): Entire patch content
        
        Returns:
            List of identified issues
        """
        file_issues = []
        
        # Extract file content changes from patch
        file_changes = self._extract_file_changes(file_path, patch_content)
        
        # Style and Formatting Analysis
        style_issues = self._check_code_style(file_changes)
        file_issues.extend(style_issues)
        
        # Complexity Analysis
        complexity_issues = self._analyze_code_complexity(file_changes)
        file_issues.extend(complexity_issues)
        
        # Security and Best Practices
        security_issues = self._detect_security_concerns(file_changes)
        file_issues.extend(security_issues)
        
        # Performance Analysis
        performance_issues = self._check_performance_patterns(file_changes)
        file_issues.extend(performance_issues)
        
        return file_issues
    
    def _extract_file_changes(self, file_path: str, patch_content: str) -> str:
        """
        Extract the modified content for a specific file from patch
        
        Args:
            file_path (str): Path of the file
            patch_content (str): Full patch content
        
        Returns:
            str: Modified file content
        """
        # Use difflib to extract changed lines
        file_lines = [line for line in patch_content.split('\n') if line.startswith('+') and not line.startswith('+++')]
        return '\n'.join(file_lines)
    
    def _check_code_style(self, file_content: str) -> List[Dict[str, Any]]:
        """
        Check code style and formatting issues
        
        Args:
            file_content (str): File content to analyze
        
        Returns:
            List of style-related issues
        """
        issues = []
        
        # Line length check
        for i, line in enumerate(file_content.split('\n'), 1):
            if len(line) > 120:
                issues.append({
                    "type": "style",
                    "line": i,
                    "description": f"Line exceeds recommended length of 120 characters (current: {len(line)})",
                    "suggestion": "Break the line into multiple lines or refactor"
                })
        
        return issues
    
    def _analyze_code_complexity(self, file_content: str) -> List[Dict[str, Any]]:
        """
        Analyze code complexity using cyclomatic complexity
        
        Args:
            file_content (str): File content to analyze
        
        Returns:
            List of complexity-related issues
        """
        issues = []
        
        try:
            # Use Radon to calculate cyclomatic complexity
            complexity = radon.complexity.cc_visit(file_content)
            
            for block in complexity:
                if block.complexity > 10:
                    issues.append({
                        "type": "best_practice",
                        "line": block.lineno,
                        "description": f"High cyclomatic complexity ({block.complexity}) in {block.name}",
                        "suggestion": "Consider refactoring into smaller, more focused functions"
                    })
        except Exception:
            # Fallback if parsing fails
            pass
        
        return issues
    
    def _detect_security_concerns(self, file_content: str) -> List[Dict[str, Any]]:
        """
        Detect potential security vulnerabilities
        
        Args:
            file_content (str): File content to analyze
        
        Returns:
            List of security-related issues
        """
        issues = []
        
        # Regex patterns for potential security risks
        security_patterns = [
            (r'eval\(', 'Avoid using eval() as it can execute arbitrary code'),
            (r'subprocess\..*shell\s*=\s*True', 'Shell=True in subprocess can be a security risk'),
            (r'pickle\..*load', 'Avoid unpickling from untrusted sources'),
        ]
        
        for pattern, description in security_patterns:
            matches = re.finditer(pattern, file_content)
            for match in matches:
                issues.append({
                    "type": "security",
                    "line": file_content[:match.start()].count('\n') + 1,
                    "description": description,
                    "suggestion": "Use safer alternatives or add strict input validation"
                })
        
        return issues
    
    def _check_performance_patterns(self, file_content: str) -> List[Dict[str, Any]]:
        """
        Check for potential performance anti-patterns
        
        Args:
            file_content (str): File content to analyze
        
        Returns:
            List of performance-related issues
        """
        issues = []
        
        # Performance anti-patterns
        if 'for ' in file_content and '.append(' in file_content:
            issues.append({
                "type": "performance",
                "line": file_content.index('.append(') + 1,
                "description": "Potential inefficient list building",
                "suggestion": "Consider list comprehensions or generator expressions"
            })
        
        return issues
    
    def _structure_review_results(self, files: List[str], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Structure the review results in the required format
        
        Args:
            files (List[str]): List of files analyzed
            issues (List[Dict]): List of all detected issues
        
        Returns:
            Structured review results
        """
        return {
            "files": [
                {
                    "name": file,
                    "issues": [issue for issue in issues if issue.get('file') == file]
                } for file in files
            ],
            "summary": {
                "total_files": len(files),
                "total_issues": len(issues),
                "critical_issues": len([i for i in issues if i.get('type') in ['security', 'bug']])
            }
        }

# Example usage
def generate_code_review(pr_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Public interface for generating a code review
    
    Args:
        pr_details (dict): Pull Request details
    
    Returns:
        Structured code review results
    """
    review_service = CodeReviewService()
    return review_service.generate_code_review(pr_details)