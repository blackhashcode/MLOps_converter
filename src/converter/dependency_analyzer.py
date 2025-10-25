# src/converter/dependency_analyzer.py
import ast
import re
from typing import Set, Dict, List

class DependencyAnalyzer:
    def __init__(self):
        self.import_patterns = {
            'standard_lib': self._is_standard_lib,
            'data_science': self._is_data_science_lib,
            'ml_frameworks': self._is_ml_framework,
            'visualization': self._is_visualization_lib
        }
    
    def analyze_dependencies(self, notebook_cells: List[Dict]) -> Dict[str, Set[str]]:
        """Analyze dependencies from notebook cells"""
        all_imports = set()
        lib_categories = {}
        
        for cell in notebook_cells:
            if cell['cell_type'] == 'code':
                imports = self._extract_imports(cell['source'])
                all_imports.update(imports)
        
        # Categorize imports
        for category, check_func in self.import_patterns.items():
            lib_categories[category] = {lib for lib in all_imports if check_func(lib)}
        
        return {
            'all_dependencies': all_imports,
            'categorized': lib_categories,
            'requirements': self._generate_requirements(all_imports)
        }
    
    def _extract_imports(self, code: str) -> Set[str]:
        """Extract import statements from code"""
        imports = set()
        
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except SyntaxError:
            # Fallback to regex for problematic code
            imports.update(self._extract_imports_regex(code))
        
        return imports
    
    def _extract_imports_regex(self, code: str) -> Set[str]:
        """Fallback import extraction using regex"""
        imports = set()
        
        # Match import statements
        import_matches = re.findall(r'^\s*import\s+([^\n#]+)', code, re.MULTILINE)
        for match in import_matches:
            for lib in match.split(','):
                imports.add(lib.strip().split('.')[0])
        
        # Match from ... import statements
        from_matches = re.findall(r'^\s*from\s+([^\s\n#]+)\s+import', code, re.MULTILINE)
        imports.update([lib.split('.')[0] for lib in from_matches])
        
        return imports