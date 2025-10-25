# src/cli/main.py
import click
from pathlib import Path
import json
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from converter.notebook_parser import NotebookParser
from converter.code_generator import CodeGenerator
from converter.dependency_analyzer import DependencyAnalyzer
from converter.template_manager import TemplateManager
from file_manager.project_structure import ProjectStructureManager
from file_manager.config_manager import ConfigManager
from file_manager.version_control import VersionControlManager

@click.group()
def cli():
    """ML DevOps Converter - Transform Jupyter notebooks into production-ready Python projects"""
    pass

@cli.command()
@click.argument('notebook_path')
@click.option('--output-dir', '-o', default='./converted_project', 
              help='Output directory for converted project')
@click.option('--create-structure', '-s', is_flag=True, 
              help='Create standard ML project structure')
@click.option('--analyze-deps', '-d', is_flag=True, 
              help='Analyze and generate requirements.txt')
@click.option('--framework', '-f', default='generic',
              type=click.Choice(['generic', 'tensorflow', 'pytorch', 'sklearn']),
              help='ML framework for configuration')
@click.option('--setup-vcs', '-v', is_flag=True,
              help='Setup version control (Git)')
@click.option('--setup-dvc', is_flag=True,
              help='Setup DVC for data versioning')
@click.option('--dvc-remote', help='DVC remote storage path')
@click.option('--setup-ci', is_flag=True,
              help='Add CI/CD templates')
@click.option('--generate-config', '-c', is_flag=True,
              help='Generate configuration files')
def convert(notebook_path, output_dir, create_structure, analyze_deps, framework,
           setup_vcs, setup_dvc, dvc_remote, setup_ci, generate_config):
    """Convert Jupyter notebook to organized Python files with DevOps features"""
    
    try:
        # Validate notebook path
        notebook_path = Path(notebook_path)
        if not notebook_path.exists():
            click.echo(f"❌ Notebook file not found: {notebook_path}")
            return
        
        click.echo(f"📓 Processing notebook: {notebook_path}")
        
        # Parse notebook
        parser = NotebookParser()
        parsed_notebook = parser.parse_notebook(str(notebook_path))
        click.echo("✅ Notebook parsed successfully")
        
        # Create project structure if requested
        project_root = output_dir
        if create_structure:
            project_manager = ProjectStructureManager()
            project_paths = project_manager.create_ml_project_structure(
                output_dir, 
                notebook_path.stem
            )
            output_dir = project_paths['src']
            project_root = Path(output_dir).parent
            click.echo("✅ Project structure created")
        
        # Generate Python files
        generator = CodeGenerator()
        generated_files = generator.generate_python_files(parsed_notebook, output_dir)
        click.echo("✅ Python files generated")
        
        # Analyze dependencies
        dependencies_info = {}
        if analyze_deps:
            analyzer = DependencyAnalyzer()
            dependencies = analyzer.analyze_dependencies(parsed_notebook['cells'])
            dependencies_info = dependencies
            
            # Save dependency analysis
            deps_file = Path(output_dir) / "dependencies_analysis.json"
            with open(deps_file, 'w') as f:
                json.dump(dependencies, f, indent=2)
            
            # Generate requirements.txt
            reqs_file = Path(output_dir).parent / "requirements.txt"
            if 'requirements' in dependencies:
                reqs_file.write_text('\n'.join(dependencies['requirements']))
            click.echo("✅ Dependencies analyzed and requirements.txt generated")
        
        # Generate configuration files
        if generate_config:
            config_manager = ConfigManager(Path(project_root) / 'config')
            config_files = config_manager.create_ml_config(
                notebook_path.stem,
                dependencies_info.get('categorized', {}),
                framework
            )
            click.echo("✅ Configuration files generated")
        
        # Setup version control
        if setup_vcs or setup_dvc or setup_ci:
            vcs_manager = VersionControlManager(project_root)
            
            if setup_vcs:
                if vcs_manager.initialize_git_repo():
                    click.echo("✅ Git repository initialized")
                
                hooks = vcs_manager.setup_git_hooks()
                click.echo(f"✅ Git hooks setup: {list(hooks.keys())}")
            
            if setup_dvc:
                if vcs_manager.initialize_dvc(dvc_remote):
                    click.echo("✅ DVC initialized")
                else:
                    click.echo("⚠️  DVC initialization skipped or failed")
            
            if setup_ci:
                ci_file = vcs_manager.setup_ci_cd_template()
                if ci_file:
                    click.echo(f"✅ CI/CD template created: {ci_file}")
            
            # Show repo status
            status = vcs_manager.get_repo_status()
            if status['is_repository']:
                click.echo(f"📊 Repository status: {status['current_branch']} branch, {status['commit_count']} commits")
        
        # Summary
        click.echo(f"\n🎉 Successfully converted {notebook_path}")
        click.echo(f"📁 Project location: {project_root}")
        click.echo(f"📄 Generated files: {list(generated_files.keys())}")
        
        if analyze_deps and dependencies_info.get('all_dependencies'):
            click.echo(f"📦 Dependencies detected: {len(dependencies_info['all_dependencies'])} packages")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        import traceback
        click.echo(f"🔍 Debug: {traceback.format_exc()}", err=True)

@cli.command()
@click.argument('project_name')
@click.option('--base-path', '-b', default='.', help='Base path for project creation')
@click.option('--framework', '-f', default='generic',
              type=click.Choice(['generic', 'tensorflow', 'pytorch', 'sklearn']),
              help='ML framework for configuration')
@click.option('--with-vcs', is_flag=True, help='Initialize version control')
@click.option('--with-dvc', is_flag=True, help='Initialize DVC')
@click.option('--with-ci', is_flag=True, help='Add CI/CD templates')
def init(project_name, base_path, framework, with_vcs, with_dvc, with_ci):
    """Initialize a new ML project structure"""
    try:
        click.echo(f"🚀 Creating ML project: {project_name}")
        
        project_manager = ProjectStructureManager()
        paths = project_manager.create_ml_project_structure(base_path, project_name)
        
        # Generate basic configuration
        config_manager = ConfigManager(Path(paths['src']).parent / 'config')
        config_files = config_manager.create_ml_config(project_name, {}, framework)
        
        click.echo(f"✅ Created ML project: {project_name}")
        click.echo("📁 Project structure:")
        for dir_name, dir_path in paths.items():
            click.echo(f"  📁 {dir_name}: {dir_path}")
        
        # Setup version control if requested
        if with_vcs or with_dvc or with_ci:
            project_root = Path(paths['src']).parent
            vcs_manager = VersionControlManager(str(project_root))
            
            if with_vcs:
                if vcs_manager.initialize_git_repo():
                    click.echo("✅ Git repository initialized")
                
                hooks = vcs_manager.setup_git_hooks()
                click.echo(f"✅ Git hooks setup: {list(hooks.keys())}")
            
            if with_dvc:
                if vcs_manager.initialize_dvc():
                    click.echo("✅ DVC initialized")
                else:
                    click.echo("⚠️  DVC initialization skipped or failed")
            
            if with_ci:
                ci_file = vcs_manager.setup_ci_cd_template()
                if ci_file:
                    click.echo(f"✅ CI/CD template created: {ci_file}")
        
        click.echo(f"\n🎉 Project ready! Next steps:")
        click.echo(f"  cd {Path(paths['src']).parent}")
        if with_vcs:
            click.echo("  # Start developing with version control enabled")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

@cli.command()
@click.argument('project_path')
@click.option('--with-dvc', is_flag=True, help='Initialize DVC for data versioning')
@click.option('--dvc-remote', help='DVC remote storage path')
@click.option('--with-ci', is_flag=True, help='Add CI/CD templates')
@click.option('--create-branches', is_flag=True, help='Create standard branch structure')
def setup_vcs(project_path, with_dvc, dvc_remote, with_ci, create_branches):
    """Setup version control for existing ML project"""
    try:
        vcs_manager = VersionControlManager(project_path)
        
        # Initialize Git
        if vcs_manager.initialize_git_repo():
            click.echo("✅ Git repository initialized")
        
        # Setup git hooks
        hooks = vcs_manager.setup_git_hooks()
        click.echo(f"✅ Git hooks setup: {list(hooks.keys())}")
        
        # Initialize DVC if requested
        if with_dvc:
            if vcs_manager.initialize_dvc(dvc_remote):
                click.echo("✅ DVC initialized")
            else:
                click.echo("⚠️  DVC initialization skipped or failed")
        
        # Setup CI/CD if requested
        if with_ci:
            ci_file = vcs_manager.setup_ci_cd_template()
            if ci_file:
                click.echo(f"✅ CI/CD template created: {ci_file}")
        
        # Create branch structure if requested
        if create_branches:
            branches = vcs_manager.create_branch_structure()
            click.echo(f"✅ Branch structure created: {list(branches.keys())}")
        
        # Show repo status
        status = vcs_manager.get_repo_status()
        click.echo(f"📊 Repository status: {status['current_branch']} branch, {status['commit_count']} commits")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

@cli.command()
@click.argument('project_path')
@click.option('--framework', default='generic', 
              type=click.Choice(['generic', 'tensorflow', 'pytorch', 'sklearn']),
              help='ML framework for configuration')
def setup_config(project_path, framework):
    """Generate configuration files for ML project"""
    try:
        config_manager = ConfigManager(Path(project_path) / 'config')
        
        # Load dependencies if available
        dependencies = {}
        deps_file = Path(project_path) / 'src' / 'dependencies_analysis.json'
        if deps_file.exists():
            with open(deps_file, 'r') as f:
                deps_data = json.load(f)
                dependencies = deps_data.get('categorized', {})
        
        # Create configurations
        config_files = config_manager.create_ml_config(
            Path(project_path).name,
            dependencies,
            framework
        )
        
        click.echo("✅ Configuration files created:")
        for config_type, config_path in config_files.items():
            click.echo(f"   📄 {config_type}: {config_path}")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

@cli.command()
@click.argument('template_name')
@click.option('--content', '-c', help='Template content string')
@click.option('--file', '-f', type=click.File('r'), help='Template content file')
def create_template(template_name, content, file):
    """Create a custom template for code generation"""
    try:
        template_manager = TemplateManager()
        
        if content:
            template_content = content
        elif file:
            template_content = file.read()
        else:
            click.echo("❌ Please provide template content via --content or --file")
            return
        
        template_manager.create_custom_template(template_name, template_content)
        click.echo(f"✅ Custom template '{template_name}' created successfully")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

@cli.command()
def list_templates():
    """List all available templates"""
    try:
        template_manager = TemplateManager()
        templates = template_manager.get_available_templates()
        
        click.echo("📋 Available templates:")
        for template in templates:
            click.echo(f"  • {template}")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

@cli.command()
@click.argument('project_path')
def status(project_path):
    """Check project status and configuration"""
    try:
        project_path = Path(project_path)
        
        click.echo(f"📊 Project Status: {project_path.name}")
        click.echo("=" * 50)
        
        # Check project structure
        click.echo("\n📁 Project Structure:")
        expected_dirs = ['data', 'models', 'src', 'notebooks', 'tests', 'config']
        for dir_name in expected_dirs:
            dir_path = project_path / dir_name
            status = "✅" if dir_path.exists() else "❌"
            click.echo(f"  {status} {dir_name}/")
        
        # Check version control
        click.echo("\n🔧 Version Control:")
        vcs_manager = VersionControlManager(str(project_path))
        repo_status = vcs_manager.get_repo_status()
        if repo_status['is_repository']:
            click.echo(f"  ✅ Git: {repo_status['current_branch']} ({repo_status['commit_count']} commits)")
            if repo_status['changes']:
                click.echo(f"  ⚠️  Uncommitted changes: {len(repo_status['changes'])}")
        else:
            click.echo("  ❌ Git: Not initialized")
        
        # Check configuration
        click.echo("\n⚙️  Configuration:")
        config_files = ['project_config.yaml', 'environment.yaml', 'training_config.yaml']
        for config_file in config_files:
            config_path = project_path / 'config' / config_file
            status = "✅" if config_path.exists() else "❌"
            click.echo(f"  {status} {config_file}")
        
        # Check requirements
        reqs_path = project_path / 'requirements.txt'
        if reqs_path.exists():
            with open(reqs_path, 'r') as f:
                num_deps = len([line for line in f.readlines() if line.strip() and not line.startswith('#')])
            click.echo(f"  ✅ requirements.txt: {num_deps} dependencies")
        else:
            click.echo("  ❌ requirements.txt: Not found")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli()