from setuptools import setup, find_packages

setup(
    name="ml_devops_converter",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "nbformat>=5.1.0",
        "pyyaml>=5.4.0",
        "jinja2>=3.0.0",
        "black>=21.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ml-converter=cli.main:cli",
        ],
    },
    author="Your Name",
    description="A DevOps tool for converting Jupyter notebooks to production-ready Python projects",
    python_requires=">=3.7",
)