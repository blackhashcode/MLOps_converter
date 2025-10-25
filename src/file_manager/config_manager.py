# src/file_manager/config_manager.py
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def create_ml_config(self, project_name: str, dependencies: Dict, 
                        framework: str = "generic") -> Dict[str, Path]:
        """Create comprehensive ML project configuration"""
        config_files = {}
        
        # Main configuration file
        main_config = {
            'project': {
                'name': project_name,
                'version': '1.0.0',
                'description': f'ML project generated from Jupyter notebook'
            },
            'paths': {
                'data': {
                    'raw': 'data/raw',
                    'processed': 'data/processed',
                    'external': 'data/external'
                },
                'models': 'models/trained',
                'notebooks': 'notebooks',
                'reports': 'reports'
            },
            'framework': framework,
            'dependencies': {
                'core': list(dependencies.get('standard_lib', [])),
                'data_science': list(dependencies.get('data_science', [])),
                'ml_frameworks': list(dependencies.get('ml_frameworks', [])),
                'visualization': list(dependencies.get('visualization', []))
            },
            'training': {
                'default_parameters': {
                    'random_state': 42,
                    'test_size': 0.2,
                    'validation_size': 0.1
                }
            }
        }
        
        config_path = self.config_dir / "project_config.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(main_config, f, default_flow_style=False)
        config_files['main'] = config_path
        
        # Create environment configuration
        env_config = self._create_environment_config(dependencies)
        env_config_path = self.config_dir / "environment.yaml"
        with open(env_config_path, 'w') as f:
            yaml.dump(env_config, f, default_flow_style=False)
        config_files['environment'] = env_config_path
        
        # Create training configuration template
        training_config = self._create_training_config_template(framework)
        training_config_path = self.config_dir / "training_config.yaml"
        with open(training_config_path, 'w') as f:
            yaml.dump(training_config, f, default_flow_style=False)
        config_files['training'] = training_config_path
        
        # Create data configuration
        data_config = self._create_data_config()
        data_config_path = self.config_dir / "data_config.yaml"
        with open(data_config_path, 'w') as f:
            yaml.dump(data_config, f, default_flow_style=False)
        config_files['data'] = data_config_path
        
        self.logger.info(f"Created configuration files: {list(config_files.keys())}")
        return config_files
    
    def _create_environment_config(self, dependencies: Dict) -> Dict[str, Any]:
        """Create environment configuration for conda/pip"""
        channels = ['conda-forge', 'defaults']
        
        # Map dependencies to conda packages
        conda_dependencies = []
        pip_dependencies = []
        
        # Categorize dependencies for conda vs pip
        for category, libs in dependencies.items():
            for lib in libs:
                # Some packages are better installed via conda
                if lib in ['tensorflow', 'pytorch', 'cudatoolkit']:
                    conda_dependencies.append(lib)
                else:
                    pip_dependencies.append(lib)
        
        return {
            'name': 'ml-project-env',
            'channels': channels,
            'dependencies': conda_dependencies + [{'pip': pip_dependencies}]
        }
    
    def _create_training_config_template(self, framework: str) -> Dict[str, Any]:
        """Create training configuration template based on framework"""
        base_config = {
            'experiment': {
                'name': 'default_experiment',
                'tracking_uri': './mlruns',
                'run_name': 'run_001'
            },
            'data': {
                'train_path': 'data/processed/train.csv',
                'test_path': 'data/processed/test.csv',
                'target_column': 'target'
            },
            'training': {
                'random_state': 42,
                'test_size': 0.2,
                'validation_size': 0.1
            }
        }
        
        # Framework-specific configurations
        if framework.lower() == 'tensorflow':
            base_config['training'].update({
                'batch_size': 32,
                'epochs': 10,
                'learning_rate': 0.001,
                'early_stopping_patience': 5
            })
        elif framework.lower() == 'pytorch':
            base_config['training'].update({
                'batch_size': 32,
                'epochs': 10,
                'learning_rate': 0.001,
                'optimizer': 'Adam',
                'scheduler': 'StepLR'
            })
        elif framework.lower() == 'sklearn':
            base_config['training'].update({
                'cv_folds': 5,
                'scoring': 'accuracy',
                'n_jobs': -1
            })
        
        return base_config
    
    def _create_data_config(self) -> Dict[str, Any]:
        """Create data configuration template"""
        return {
            'data_sources': {
                'raw': {
                    'path': 'data/raw',
                    'file_patterns': ['*.csv', '*.parquet', '*.json']
                },
                'processed': {
                    'path': 'data/processed',
                    'formats': ['csv', 'parquet', 'h5']
                }
            },
            'preprocessing': {
                'missing_values': {
                    'strategy': 'mean',  # or 'median', 'most_frequent', 'drop'
                    'fill_value': None
                },
                'scaling': {
                    'method': 'standard',  # or 'minmax', 'robust'
                    'feature_range': [0, 1]
                },
                'categorical_encoding': {
                    'method': 'onehot'  # or 'label', 'target'
                }
            },
            'validation': {
                'split_strategy': 'train_test_split',  # or 'cross_validation', 'time_series_split'
                'test_size': 0.2,
                'random_state': 42
            }
        }
    
    def load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from file"""
        with open(config_path, 'r') as f:
            if config_path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif config_path.suffix == '.json':
                return json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {config_path.suffix}")
    
    def update_config(self, config_path: Path, updates: Dict[str, Any]):
        """Update configuration file with new values"""
        config = self.load_config(config_path)
        
        # Deep update
        def deep_update(source, update):
            for key, value in update.items():
                if isinstance(value, dict) and key in source and isinstance(source[key], dict):
                    deep_update(source[key], value)
                else:
                    source[key] = value
        
        deep_update(config, updates)
        
        # Save updated config
        with open(config_path, 'w') as f:
            if config_path.suffix in ['.yaml', '.yml']:
                yaml.dump(config, f, default_flow_style=False)
            elif config_path.suffix == '.json':
                json.dump(config, f, indent=2)
    
    def generate_config_py(self, config_dict: Dict) -> str:
        """Generate Python configuration file from dict"""
        lines = ['"""Configuration file generated automatically"""', '']
        
        def dict_to_python(obj, indent=0):
            spaces = ' ' * indent
            if isinstance(obj, dict):
                lines.append(f'{spaces}# Configuration')
                for key, value in obj.items():
                    if isinstance(value, dict):
                        lines.append(f'{spaces}class {key.upper()}:')
                        dict_to_python(value, indent + 4)
                    else:
                        if isinstance(value, str):
                            value_str = f"'{value}'"
                        else:
                            value_str = str(value)
                        lines.append(f'{spaces}{key.upper()} = {value_str}')
                lines.append('')
        
        dict_to_python(config_dict)
        return '\n'.join(lines)