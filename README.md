# MLOps_converter# ML DevOps Converter

A powerful tool that transforms Jupyter notebooks into production-ready Python projects with comprehensive DevOps features. Streamline your machine learning workflow from experimentation to deployment.

## 🚀 Features

### 🔄 Notebook Conversion
- **Smart Code Organization**: Automatically categorizes notebook cells into logical Python modules
- **Dependency Analysis**: Detects and analyzes imported packages
- **Code Quality**: Generates clean, well-structured Python code
- **Template System**: Customizable code generation templates

### 🏗️ Project Management
- **Standard ML Project Structure**: Creates organized directory layouts
- **Configuration Management**: Generates framework-specific configuration files
- **Multiple Framework Support**: TensorFlow, PyTorch, Scikit-learn, and generic ML projects

### 🔧 DevOps Integration
- **Version Control**: Automatic Git initialization with ML-optimized hooks
- **Data Versioning**: DVC setup for large datasets and models
- **CI/CD Templates**: GitHub Actions workflows for ML pipelines
- **Branch Management**: Standard branch structure for ML projects

### 📊 Project Health
- **Status Monitoring**: Check project health and configuration
- **Dependency Tracking**: Automated requirements.txt generation
- *# ML DevOps Converter

A powerful tool that transforms Jupyter notebooks into production-ready Python projects with comprehensive DevOps features. Streamline your machine learning workflow from experimentation to deployment.

## 🚀 Features

### 🔄 Notebook Conversion
- **Smart Code Organization**: Automatically categorizes notebook cells into logical Python modules
- **Dependency Analysis**: Detects and analyzes imported packages
- **Code Quality**: Generates clean, well-structured Python code
- **Template System**: Customizable code generation templates

### 🏗️ Project Management
- **Standard ML Project Structure**: Creates organized directory layouts
- **Configuration Management**: Generates framework-specific configuration files
- **Multiple Framework Support**: TensorFlow, PyTorch, Scikit-learn, and generic ML projects

### 🔧 DevOps Integration
- **Version Control**: Automatic Git initialization with ML-optimized hooks
- **Data Versioning**: DVC setup for large datasets and models
- **CI/CD Templates**: GitHub Actions workflows for ML pipelines
- **Branch Management**: Standard branch structure for ML projects

### 📊 Project Health
- **Status Monitoring**: Check project health and configuration
- **Dependency Tracking**: Automated requirements.txt generation
- **Structure Validation**: Ensure project follows ML best practices

## 📦 Installation

### From Source
```bash
git clone https://github.com/yourusername/ml_devops_converter
cd ml_devops_converter
pip install -e .
```

### Requirements
- Python 3.7+
- Dependencies: `click`, `nbformat`, `pyyaml`, `jinja2`

## 🛠️ Quick Start

### Convert a Notebook to Production Code
```bash
# Basic conversion
ml-converter convert my_notebook.ipynb --output-dir ./my_project

# Full DevOps setup
ml-converter convert my_notebook.ipynb \
    --output-dir ./production_ready \
    --create-structure \
    --analyze-deps \
    --framework pytorch \
    --setup-vcs \
    --setup-dvc \
    --setup-ci \
    --generate-config
```

### Initialize a New ML Project
```bash
ml-converter init my_ml_project \
    --framework tensorflow \
    --with-vcs \
    --with-ci
```

## 📚 Usage Examples

### Basic Conversion
```bash
ml-converter convert experiment.ipynb --output-dir ./converted
```

### With Project Structure
```bash
ml-converter convert experiment.ipynb \
    --create-structure \
    --analyze-deps \
    --output-dir ./organized_project
```

### Full ML DevOps Pipeline
```bash
ml-converter convert research.ipynb \
    --output-dir ./production_model \
    --create-structure \
    --analyze-deps \
    --framework tensorflow \
    --setup-vcs \
    --setup-dvc \
    --dvc-remote s3://my-bucket/models \
    --setup-ci \
    --generate-config
```

### Project Management Commands
```bash
# Check project health
ml-converter status ./my_project

# Setup version control for existing project
ml-converter setup-vcs ./my_project --with-dvc --with-ci

# Generate configuration files
ml-converter setup-config ./my_project --framework pytorch

# List available templates
ml-converter list-templates

# Create custom template
ml-converter create-template my_template --content "Custom code template"
```

## 🏗️ Generated Project Structure

```
project_name/
├── data/
│   ├── raw/          # Raw datasets
│   ├── processed/    # Processed data
│   └── external/     # External data sources
├── models/
│   ├── trained/      # Trained models
│   └── pretrained/   # Pre-trained models
├── src/
│   ├── main.py       # Main execution script
│   ├── functions.py  # Utility functions
│   ├── training.py   # Model training code
│   ├── config.py     # Python configuration
│   └── dependencies_analysis.json
├── notebooks/
│   ├── exploratory/  # Exploration notebooks
│   └── experimental/ # Experiment notebooks
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
├── config/
│   ├── project_config.yaml
│   ├── environment.yaml
│   └── training_config.yaml
├── reports/
│   └── figures/      # Output figures and plots
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Configuration

### Framework Support
- **TensorFlow**: Optimized for Keras and TF workflows
- **PyTorch**: Custom configurations for PyTorch projects
- **Scikit-learn**: Traditional ML pipeline setup
- **Generic**: Framework-agnostic ML project structure

### Generated Configuration Files

1. **project_config.yaml**: Project metadata and paths
2. **environment.yaml**: Conda environment specification
3. **training_config.yaml**: Training parameters and hyperparameters
4. **data_config.yaml**: Data preprocessing and validation settings

## 🔄 Version Control Features

### Git Integration
- Automatic repository initialization
- ML-optimized .gitignore
- Pre-commit hooks for code quality
- Post-commit hooks for experiment tracking

### DVC Setup
- Data and model versioning
- Remote storage configuration (S3, GCS, Azure, local)
- Pipeline management

### CI/CD Templates
- Automated testing
- Model training pipelines
- Code quality checks
- Coverage reporting

## 🎯 Cell Categorization

The converter intelligently categorizes notebook cells:

| Category | Description | Output File |
|----------|-------------|-------------|
| `imports` | Package imports | `main.py` |
| `function_definitions` | Functions and classes | `functions.py` |
| `model_training` | Training loops and model code | `training.py` |
| `data_processing` | Data cleaning and preprocessing | `main.py` |
| `visualization` | Plots and charts | `main.py` |
| `general_code` | Miscellaneous code | `main.py` |

## 📊 Dependency Analysis

Automatically detects and categorizes Python packages:

- **Core Dependencies**: Essential Python packages
- **Data Science**: NumPy, Pandas, Scikit-learn
- **ML Frameworks**: TensorFlow, PyTorch, XGBoost
- **Visualization**: Matplotlib, Seaborn, Plotly

## 🛠️ Advanced Usage

### Custom Templates
Create custom code generation templates:

```bash
ml-converter create-template custom_module --file ./my_template.j2
```

### Project Health Check
```bash
ml-converter status ./my_project
```
Output includes:
- Project structure validation
- Version control status
- Configuration file checks
- Dependency analysis

### Branch Management
```bash
ml-converter setup-vcs ./my_project --create-branches
```
Creates standard branches:
- `main` - Production code
- `develop` - Development branch
- `experiment/*` - Experimental features

## 🔧 Troubleshooting

### Common Issues

1. **Notebook parsing errors**
   ```bash
   # Check notebook validity
   python -m json.tool notebook.ipynb > /dev/null
   ```

2. **Missing dependencies**
   ```bash
   pip install nbformat pyyaml jinja2 click
   ```

3. **Permission errors**
   ```bash
   chmod +x src/cli/main.py
   ```

### Debug Mode
```bash
# Enable debug output
ml-converter convert notebook.ipynb --output-dir ./debug_output -v
```

## 📈 Example Workflow

### From Research to Production
1. **Experiment**: Develop model in Jupyter notebook
2. **Convert**: `ml-converter convert model.ipynb --create-structure --analyze-deps`
3. **Version**: `ml-converter setup-vcs ./model --with-dvc --with-ci`
4. **Configure**: `ml-converter setup-config ./model --framework tensorflow`
5. **Deploy**: Push to repository, CI/CD handles testing and deployment

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/yourusername/ml_devops_converter
cd ml_devops_converter
pip install -e ".[dev]"
pre-commit install
```

### Running Tests
```bash
pytest tests/ -v
```

## �� License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by ML industry best practices
- Built with the Python data science ecosystem
- Thanks to the open-source community for excellent tools and libraries

---

**ML DevOps Converter** - Bridge the gap between research and production with intelligent notebook conversion and comprehensive DevOps integration.*Structure Validation**: Ensure project follows ML best practices

## 📦 Installation

### From Source
```bash
git clone https://github.com/yourusername/ml_devops_converter
cd ml_devops_converter
pip install -e .
```

### Requirements
- Python 3.7+
- Dependencies: `click`, `nbformat`, `pyyaml`, `jinja2`

## 🛠️ Quick Start

### Convert a Notebook to Production Code
```bash
# Basic conversion
ml-converter convert my_notebook.ipynb --output-dir ./my_project

# Full DevOps setup
ml-converter convert my_notebook.ipynb \
    --output-dir ./production_ready \
    --create-structure \
    --analyze-deps \
    --framework pytorch \
    --setup-vcs \
    --setup-dvc \
    --setup-ci \
    --generate-config
```

### Initialize a New ML Project
```bash
ml-converter init my_ml_project \
    --framework tensorflow \
    --with-vcs \
    --with-ci
```

## 📚 Usage Examples

### Basic Conversion
```bash
ml-converter convert experiment.ipynb --output-dir ./converted
```

### With Project Structure
```bash
ml-converter convert experiment.ipynb \
    --create-structure \
    --analyze-deps \
    --output-dir ./organized_project
```

### Full ML DevOps Pipeline
```bash
ml-converter convert research.ipynb \
    --output-dir ./production_model \
    --create-structure \
    --analyze-deps \
    --framework tensorflow \
    --setup-vcs \
    --setup-dvc \
    --dvc-remote s3://my-bucket/models \
    --setup-ci \
    --generate-config
```

### Project Management Commands
```bash
# Check project health
ml-converter status ./my_project

# Setup version control for existing project
ml-converter setup-vcs ./my_project --with-dvc --with-ci

# Generate configuration files
ml-converter setup-config ./my_project --framework pytorch

# List available templates
ml-converter list-templates

# Create custom template
ml-converter create-template my_template --content "Custom code template"
```

## 🏗️ Generated Project Structure

```
project_name/
├── data/
│   ├── raw/          # Raw datasets
│   ├── processed/    # Processed data
│   └── external/     # External data sources
├── models/
│   ├── trained/      # Trained models
│   └── pretrained/   # Pre-trained models
├── src/
│   ├── main.py       # Main execution script
│   ├── functions.py  # Utility functions
│   ├── training.py   # Model training code
│   ├── config.py     # Python configuration
│   └── dependencies_analysis.json
├── notebooks/
│   ├── exploratory/  # Exploration notebooks
│   └── experimental/ # Experiment notebooks
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
├── config/
│   ├── project_config.yaml
│   ├── environment.yaml
│   └── training_config.yaml
├── reports/
│   └── figures/      # Output figures and plots
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Configuration

### Framework Support
- **TensorFlow**: Optimized for Keras and TF workflows
- **PyTorch**: Custom configurations for PyTorch projects
- **Scikit-learn**: Traditional ML pipeline setup
- **Generic**: Framework-agnostic ML project structure

### Generated Configuration Files

1. **project_config.yaml**: Project metadata and paths
2. **environment.yaml**: Conda environment specification
3. **training_config.yaml**: Training parameters and hyperparameters
4. **data_config.yaml**: Data preprocessing and validation settings

## 🔄 Version Control Features

### Git Integration
- Automatic repository initialization
- ML-optimized .gitignore
- Pre-commit hooks for code quality
- Post-commit hooks for experiment tracking

### DVC Setup
- Data and model versioning
- Remote storage configuration (S3, GCS, Azure, local)
- Pipeline management

### CI/CD Templates
- Automated testing
- Model training pipelines
- Code quality checks
- Coverage reporting

## 🎯 Cell Categorization

The converter intelligently categorizes notebook cells:

| Category | Description | Output File |
|----------|-------------|-------------|
| `imports` | Package imports | `main.py` |
| `function_definitions` | Functions and classes | `functions.py` |
| `model_training` | Training loops and model code | `training.py` |
| `data_processing` | Data cleaning and preprocessing | `main.py` |
| `visualization` | Plots and charts | `main.py` |
| `general_code` | Miscellaneous code | `main.py` |

## 📊 Dependency Analysis

Automatically detects and categorizes Python packages:

- **Core Dependencies**: Essential Python packages
- **Data Science**: NumPy, Pandas, Scikit-learn
- **ML Frameworks**: TensorFlow, PyTorch, XGBoost
- **Visualization**: Matplotlib, Seaborn, Plotly

## 🛠️ Advanced Usage

### Custom Templates
Create custom code generation templates:

```bash
ml-converter create-template custom_module --file ./my_template.j2
```

### Project Health Check
```bash
ml-converter status ./my_project
```
Output includes:
- Project structure validation
- Version control status
- Configuration file checks
- Dependency analysis

### Branch Management
```bash
ml-converter setup-vcs ./my_project --create-branches
```
Creates standard branches:
- `main` - Production code
- `develop` - Development branch
- `experiment/*` - Experimental features

## 🔧 Troubleshooting

### Common Issues

1. **Notebook parsing errors**
   ```bash
   # Check notebook validity
   python -m json.tool notebook.ipynb > /dev/null
   ```

2. **Missing dependencies**
   ```bash
   pip install nbformat pyyaml jinja2 click
   ```

3. **Permission errors**
   ```bash
   chmod +x src/cli/main.py
   ```

### Debug Mode
```bash
# Enable debug output
ml-converter convert notebook.ipynb --output-dir ./debug_output -v
```

## 📈 Example Workflow

### From Research to Production
1. **Experiment**: Develop model in Jupyter notebook
2. **Convert**: `ml-converter convert model.ipynb --create-structure --analyze-deps`
3. **Version**: `ml-converter setup-vcs ./model --with-dvc --with-ci`
4. **Configure**: `ml-converter setup-config ./model --framework tensorflow`
5. **Deploy**: Push to repository, CI/CD handles testing and deployment


### Development Setup
```bash
git clone https://github.com/yourusername/ml_devops_converter
cd ml_devops_converter
pip install -e ".[dev]"
pre-commit install
```

### Running Tests
```bash
pytest tests/ -v
```

