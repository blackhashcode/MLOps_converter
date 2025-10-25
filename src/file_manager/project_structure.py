# src/file_manager/project_structure.py
from pathlib import Path
import shutil
from typing import Dict, List

class ProjectStructureManager:
    def __init__(self):
        self.standard_structure = {
            'data': ['raw', 'processed', 'external'],
            'models': ['trained', 'pretrained'],
            'src': ['data', 'models', 'utils', 'config'],
            'notebooks': ['exploratory', 'experimental'],
            'tests': ['unit', 'integration'],
            'docs': [],
            'reports': ['figures']
        }
    
    def create_ml_project_structure(self, base_path: str, project_name: str) -> Dict[str, str]:
        """Create standard ML project structure"""
        project_path = Path(base_path) / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        created_paths = {}
        
        # Create directory structure
        for dir_name, subdirs in self.standard_structure.items():
            dir_path = project_path / dir_name
            dir_path.mkdir(exist_ok=True)
            created_paths[dir_name] = str(dir_path)
            
            for subdir in subdirs:
                subdir_path = dir_path / subdir
                subdir_path.mkdir(exist_ok=True)
        
        # Create standard files
        self._create_standard_files(project_path, created_paths)
        
        return created_paths
    
    def _create_standard_files(self, project_path: Path, created_paths: Dict):
        """Create standard configuration files"""
        # requirements.txt
        requirements_content = """# Core dependencies
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=1.0.0

# ML/DL frameworks (uncomment as needed)
# tensorflow>=2.8.0
# torch>=1.9.0
# xgboost>=1.5.0
# lightgbm>=3.3.0

# Utilities
jupyter>=1.0.0
ipykernel>=6.0.0
"""
        (project_path / "requirements.txt").write_text(requirements_content)
        
        # .gitignore
        gitignore_content = """# Data
data/raw/
data/processed/
data/external/

# Models
models/trained/
models/pretrained/

# Environment
.env
.venv
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints
"""
        (project_path / ".gitignore").write_text(gitignore_content)
        
        # config.py
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
        (project_path / "config.py").write_text(config_content)