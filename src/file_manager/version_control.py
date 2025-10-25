# src/file_manager/version_control.py
import subprocess
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

class VersionControlManager:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.logger = logging.getLogger(__name__)
    
    def initialize_git_repo(self, initial_commit_message: str = "Initial ML project commit") -> bool:
        """Initialize Git repository for the project"""
        try:
            # Check if already a git repository
            if (self.project_path / '.git').exists():
                self.logger.info("Git repository already exists")
                return True
            
            # Initialize git repository
            self._run_git_command(['init'])
            
            # Create .gitignore if it doesn't exist
            self._ensure_gitignore()
            
            # Add all files
            self._run_git_command(['add', '.'])
            
            # Initial commit
            self._run_git_command(['commit', '-m', initial_commit_message])
            
            self.logger.info("Git repository initialized successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to initialize git repository: {e}")
            return False
    
    def _ensure_gitignore(self):
        """Ensure .gitignore file exists with ML project patterns"""
        gitignore_path = self.project_path / '.gitignore'
        
        if not gitignore_path.exists():
            gitignore_content = """# Data files
data/raw/
data/processed/
data/external/

# Model files
models/trained/
models/pretrained/
models/checkpoints/

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
.ipynb_checkpoints/
*.ipynb_checkpoints*

# MLFlow
mlruns/

# DVC
.dvc/

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp

# Large files
*.h5
*.hdf5
*.pickle
*.pkl
"""
            gitignore_path.write_text(gitignore_content)
    
    def setup_git_hooks(self) -> Dict[str, bool]:
        """Setup useful git hooks for ML projects"""
        hooks_dir = self.project_path / '.git' / 'hooks'
        hooks_dir.mkdir(exist_ok=True)
        
        hooks_created = {}
        
        # Pre-commit hook for code quality
        pre_commit_hook = hooks_dir / 'pre-commit'
        pre_commit_content = """#!/bin/bash
# Pre-commit hook for ML project

echo "Running pre-commit checks..."

# Check for large files
large_files=$(find . -type f -size +10M -not -path "./.git/*")
if [ -n "$large_files" ]; then
    echo "Warning: Large files detected:"
    echo "$large_files"
    echo "Consider using DVC for large files."
fi

# Check for credentials
if grep -r "password\\|secret\\|key" --include="*.py" --include="*.yaml" --include="*.yml" . | grep -v ".git"; then
    echo "Warning: Possible credentials detected in code"
    # Uncomment the line below to make it a hard check
    # exit 1
fi

# Run black formatting check
echo "Checking code formatting with black..."
python -m black --check --diff src/ tests/

# Exit if any check fails
if [ $? -ne 0 ]; then
    echo "Code formatting check failed. Run 'black src/ tests/' to format."
    exit 1
fi

echo "Pre-commit checks passed!"
"""
        pre_commit_hook.write_text(pre_commit_content)
        pre_commit_hook.chmod(0o755)
        hooks_created['pre-commit'] = True
        
        # Post-commit hook for experiment tracking
        post_commit_hook = hooks_dir / 'post-commit'
        post_commit_content = """#!/bin/bash
# Post-commit hook for ML project

echo "Post-commit actions..."

# Get current commit hash
COMMIT_HASH=$(git rev-parse HEAD)

# Update experiment tracking with commit hash if needed
if [ -f "src/tracking.py" ]; then
    echo "Updating experiment tracking with commit $COMMIT_HASH"
    # This would call your experiment tracking setup
fi

echo "Post-commit actions completed"
"""
        post_commit_hook.write_text(post_commit_content)
        post_commit_hook.chmod(0o755)
        hooks_created['post-commit'] = True
        
        return hooks_created
    
    def initialize_dvc(self, remote_storage: Optional[str] = None) -> bool:
        """Initialize DVC for data versioning"""
        try:
            # Check if DVC is installed
            subprocess.run(['dvc', '--version'], check=True, capture_output=True)
            
            # Initialize DVC
            self._run_command(['dvc', 'init'])
            
            # Setup remote storage if provided
            if remote_storage:
                if remote_storage.startswith('s3://'):
                    self._run_command(['dvc', 'remote', 'add', '-d', 'myremote', remote_storage])
                elif remote_storage.startswith('gs://'):
                    self._run_command(['dvc', 'remote', 'add', '-d', 'myremote', remote_storage])
                elif remote_storage.startswith('azure://'):
                    self._run_command(['dvc', 'remote', 'add', '-d', 'myremote', remote_storage])
                else:
                    # Local directory
                    remote_path = Path(remote_storage)
                    remote_path.mkdir(parents=True, exist_ok=True)
                    self._run_command(['dvc', 'remote', 'add', '-d', 'myremote', str(remote_path)])
            
            # Add data directories to DVC
            data_dirs = ['data/raw', 'data/processed', 'models/trained']
            for data_dir in data_dirs:
                dir_path = self.project_path / data_dir
                if dir_path.exists() and any(dir_path.iterdir()):
                    self._run_command(['dvc', 'add', data_dir])
            
            # Commit DVC files
            self._run_git_command(['add', '.dvc', '*.dvc'])
            self._run_git_command(['commit', '-m', 'Initialize DVC'])
            
            self.logger.info("DVC initialized successfully")
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.logger.warning(f"DVC initialization failed or DVC not installed: {e}")
            return False
    
    def create_branch_structure(self, branches: List[str] = None) -> Dict[str, bool]:
        """Create standard branch structure for ML project"""
        if branches is None:
            branches = ['develop', 'staging', 'experiment/data-preprocessing', 'experiment/model-tuning']
        
        branch_results = {}
        
        for branch in branches:
            try:
                self._run_git_command(['checkout', '-b', branch])
                self._run_git_command(['checkout', 'main'])  # Return to main
                branch_results[branch] = True
            except subprocess.CalledProcessError as e:
                branch_results[branch] = False
                self.logger.error(f"Failed to create branch {branch}: {e}")
        
        return branch_results
    
    def setup_ci_cd_template(self, platform: str = "github") -> Optional[Path]:
        """Setup CI/CD configuration template"""
        if platform == "github":
            workflows_dir = self.project_path / '.github' / 'workflows'
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            ci_cd_file = workflows_dir / 'ml-pipeline.yml'
            ci_cd_content = """name: ML Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9]

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov black flake8
    
    - name: Check code formatting with black
      run: |
        black --check src/ tests/
    
    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --max-line-length=88
    
    - name: Run tests with pytest
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml

  train-model:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Train model
      run: |
        python src/training.py --config config/training_config.yaml
    
    - name: Save model artifact
      uses: actions/upload-artifact@v2
      with:
        name: trained-model
        path: models/trained/
"""
            ci_cd_file.write_text(ci_cd_content)
            return ci_cd_file
        
        return None
    
    def _run_git_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run git command in project directory"""
        return subprocess.run(
            ['git'] + args,
            cwd=self.project_path,
            check=True,
            capture_output=True,
            text=True
        )
    
    def _run_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run general command in project directory"""
        return subprocess.run(
            args,
            cwd=self.project_path,
            check=True,
            capture_output=True,
            text=True
        )
    
    def get_repo_status(self) -> Dict[str, Any]:
        """Get repository status information"""
        try:
            # Get current branch
            branch_result = self._run_git_command(['branch', '--show-current'])
            current_branch = branch_result.stdout.strip()
            
            # Get status
            status_result = self._run_git_command(['status', '--porcelain'])
            changes = status_result.stdout.strip().split('\n') if status_result.stdout else []
            
            # Get commit count
            commit_result = self._run_git_command(['rev-list', '--count', 'HEAD'])
            commit_count = int(commit_result.stdout.strip()) if commit_result.stdout else 0
            
            return {
                'current_branch': current_branch,
                'changes': [c for c in changes if c],
                'commit_count': commit_count,
                'is_repository': True
            }
            
        except subprocess.CalledProcessError:
            return {
                'is_repository': False,
                'current_branch': None,
                'changes': [],
                'commit_count': 0
            }