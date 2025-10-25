# src/converter/notebook_parser.py
import json
import nbformat
from typing import Dict, List, Any
import ast

class NotebookParser:
    def __init__(self):
        self.supported_versions = [4, 5]
    
    def parse_notebook(self, notebook_path: str) -> Dict[str, Any]:
        """Parse Jupyter notebook and extract structured information"""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook_content = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to read notebook file: {e}")
        
        nb_version = notebook_content.get('nbformat', 4)
        if nb_version not in self.supported_versions:
            raise ValueError(f"Unsupported notebook version: {nb_version}")
        
        return {
            'metadata': notebook_content.get('metadata', {}),
            'cells': self._extract_cells(notebook_content.get('cells', [])),
            'kernel_info': self._extract_kernel_info(notebook_content.get('metadata', {}))
        }
    
    def _extract_cells(self, cells: List[Dict]) -> List[Dict]:
        """Extract and categorize notebook cells"""
        parsed_cells = []
        
        for cell in cells:
            cell_type = cell.get('cell_type', 'code')
            
            # Handle different source formats (string vs list)
            source_parts = cell.get('source', [])
            if isinstance(source_parts, list):
                source = ''.join(source_parts)
            else:
                source = str(source_parts)
            
            parsed_cell = {
                'cell_type': cell_type,
                'source': source,
                'metadata': cell.get('metadata', {}),
                'outputs': cell.get('outputs', []) if cell_type == 'code' else []
            }
            
            # Add cell categorization
            if cell_type == 'code':
                parsed_cell['category'] = self._categorize_code_cell(source)
            elif cell_type == 'markdown':
                parsed_cell['category'] = self._categorize_markdown_cell(source)
            else:
                parsed_cell['category'] = 'other'
            
            parsed_cells.append(parsed_cell)
        
        return parsed_cells
    
    def _categorize_code_cell(self, source: str) -> str:
        """Categorize code cells for better organization"""
        if not source.strip():
            return 'empty'
            
        source_lower = source.lower()
        
        if any(imp in source_lower for imp in ['import', 'from ']):
            return 'imports'
        elif any(pattern in source_lower for pattern in ['def ', 'class ', 'function']):
            return 'function_definitions'
        elif any(pattern in source_lower for pattern in ['model', 'train', 'fit', 'compile']):
            return 'model_training'
        elif any(pattern in source_lower for pattern in ['plot', 'visualize', 'plt.', 'seaborn']):
            return 'visualization'
        elif any(pattern in source_lower for pattern in ['preprocess', 'clean', 'transform']):
            return 'data_processing'
        elif any(pattern in source_lower for pattern in ['test', 'assert', 'check']):
            return 'testing'
        else:
            return 'general_code'
    
    def _categorize_markdown_cell(self, source: str) -> str:
        """Categorize markdown cells for better organization"""
        if not source.strip():
            return 'empty'
            
        source_lower = source.lower()
        
        if any(pattern in source_lower for pattern in ['# introduction', '# overview', '# abstract']):
            return 'introduction'
        elif any(pattern in source_lower for pattern in ['# setup', '# installation', '# requirements']):
            return 'setup'
        elif any(pattern in source_lower for pattern in ['# data', '# dataset', '# loading']):
            return 'data_description'
        elif any(pattern in source_lower for pattern in ['# method', '# approach', '# methodology']):
            return 'methodology'
        elif any(pattern in source_lower for pattern in ['# result', '# output', '# finding']):
            return 'results'
        elif any(pattern in source_lower for pattern in ['# conclusion', '# summary', '# discussion']):
            return 'conclusion'
        elif source_lower.startswith('#') or '##' in source_lower:
            return 'section_header'
        else:
            return 'documentation'
    
    def _extract_kernel_info(self, metadata: Dict) -> Dict[str, str]:
        """Extract kernel information from notebook metadata"""
        kernel_info = {}
        
        # Try to get kernel info from different possible locations
        if 'kernelspec' in metadata:
            kernelspec = metadata['kernelspec']
            kernel_info['name'] = kernelspec.get('name', 'unknown')
            kernel_info['display_name'] = kernelspec.get('display_name', 'unknown')
            kernel_info['language'] = kernelspec.get('language', 'python')
        
        elif 'language_info' in metadata:
            language_info = metadata['language_info']
            kernel_info['name'] = language_info.get('name', 'python')
            kernel_info['version'] = language_info.get('version', 'unknown')
        
        return kernel_info