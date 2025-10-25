# src/converter/code_generator.py
import os
from typing import Dict, List
from pathlib import Path

class CodeGenerator:
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load templates - for now return empty dict, will be enhanced later"""
        return {}
    
    def generate_python_files(self, parsed_notebook: Dict, output_dir: str) -> Dict[str, str]:
        """Generate organized Python files from parsed notebook"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        generated_files = {}
        
        # Group cells by category
        categorized_cells = self._categorize_cells(parsed_notebook['cells'])
        
        # Generate main script
        main_script = self._generate_main_script(categorized_cells)
        main_file = output_path / "main.py"
        main_file.write_text(main_script)
        generated_files['main.py'] = str(main_file)
        
        # Generate modules for different categories
        if 'function_definitions' in categorized_cells:
            functions_module = self._generate_functions_module(categorized_cells['function_definitions'])
            functions_file = output_path / "functions.py"
            functions_file.write_text(functions_module)
            generated_files['functions.py'] = str(functions_file)
        
        if 'model_training' in categorized_cells:
            training_module = self._generate_training_module(categorized_cells['model_training'])
            training_file = output_path / "training.py"
            training_file.write_text(training_module)
            generated_files['training.py'] = str(training_file)
        
        # Generate configuration files
        self._generate_config_files(parsed_notebook, output_path, generated_files)
        
        return generated_files    
        
    def _categorize_cells(self, cells: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize cells by their type and content"""
        categorized = {}
        
        for cell in cells:
            category = cell.get('category', 'other')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(cell)
        
        return categorized
    
    def _generate_main_script(self, categorized_cells: Dict[str, List]) -> str:
        """Generate the main execution script"""
        lines = [
            "#!/usr/bin/env python3",
            '"""',
            "Main execution script generated from Jupyter notebook",
            '"""',
            "\n"
        ]
        
        # Add imports
        if 'imports' in categorized_cells:
            for cell in categorized_cells['imports']:
                lines.append(cell['source'])
            lines.append("\n")
        
        # Add main function
        lines.extend([
            "def main():",
            "    \"\"\"Main execution function\"\"\""
        ])
        
        # Add execution code
        execution_categories = ['data_processing', 'model_training', 'visualization', 'general_code']
        for category in execution_categories:
            if category in categorized_cells:
                lines.append(f"    # {category.replace('_', ' ').title()}")
                for cell in categorized_cells[category]:
                    # Indent code for main function
                    indented_code = '\n'.join(f"    {line}" for line in cell['source'].split('\n'))
                    lines.append(indented_code)
                lines.append("")
        
        lines.extend([
            "\nif __name__ == \"__main__\":",
            "    main()"
        ])
        
        return '\n'.join(lines)
    
    def _generate_functions_module(self, function_cells: List[Dict]) -> str:
        """Generate functions module"""
        lines = [
            '"""',
            "Utility functions generated from Jupyter notebook",
            '"""',
            "\n"
        ]
        
        for cell in function_cells:
            lines.append(cell['source'])
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_training_module(self, training_cells: List[Dict]) -> str:
        """Generate training module"""
        lines = [
            '"""',
            "Training module for machine learning models",
            '"""',
            "\n"
        ]
        
        for cell in training_cells:
            lines.append(cell['source'])
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_config_files(self, parsed_notebook: Dict, output_path: Path, generated_files: Dict):
        """Generate basic configuration files"""
        # Generate a simple config.py
        config_content = '''"""Configuration file for ML project"""

import os
from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
MODELS_DIR = PROJECT_ROOT / 'models'
REPORTS_DIR = PROJECT_ROOT / 'reports'

# Data configuration
class DataConfig:
    RAW_DATA_PATH = DATA_DIR / 'raw'
    PROCESSED_DATA_PATH = DATA_DIR / 'processed'
    
class ModelConfig:
    SAVE_PATH = MODELS_DIR / 'trained'
    HYPERPARAMETERS = {
        'random_state': 42,
        'test_size': 0.2
    }
'''
        config_file = output_path / "config.py"
        config_file.write_text(config_content)
        generated_files['config.py'] = str(config_file)