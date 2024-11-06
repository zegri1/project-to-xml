# Project to XML

A Python tool that converts project directories into structured XML documentation. It creates a comprehensive XML representation containing:
- Project overview
- Clean directory structure
- File contents with CDATA sections

While designed with AI code analysis in mind (particularly optimized for Claude 3.5), it can be useful for any scenario requiring XML representation of project structures.

## Features

- 📁 Hierarchical directory structure representation
- 📝 File contents preserved in CDATA sections
- ⚙️ Smart exclusion system (structure-only vs. complete exclusion)
- 🔧 Both API and CLI interfaces
- 🚫 Default exclusions for common patterns (.git, __pycache__, etc.)

## Installation

```bash
# From source
git clone https://github.com/zegri1/project-to-xml.git
cd project_to_xml
pip install -e .
```

## Usage

### Command Line

```bash
# Basic usage (analyzes current directory)
project-to-xml

# Specify project directory
project-to-xml /path/to/project

# Custom output file
project-to-xml /path/to/project -o output.xml

# Use specific configuration file
project-to-xml /path/to/project -c config.json
```

### Python API

```python
from project_to_xml import ProjectAnalyzer

# Basic usage - will look for analyzer_config.json in current and target directories
analyzer = ProjectAnalyzer()
analyzer.create_project_xml('/path/to/project')

# With explicit configuration file
analyzer = ProjectAnalyzer('/path/to/custom_config.json')
analyzer.create_project_xml('/path/to/project', 'output.xml')
```

## Configuration

The analyzer looks for configuration in the following order:
1. Explicitly provided configuration file path
2. `analyzer_config.json` in the current working directory
3. `analyzer_config.json` in the project directory being analyzed
4. Default configuration if no files found

Create an `analyzer_config.json` file to customize the analyzer's behavior:

```json
{
    "full_excludes": {
        "folders": [
            ".git",
            "node_modules",
            "__pycache__",
            "venv",
            ".idea"
        ],
        "files": [
            ".DS_Store",
            "*.pyc",
            "*.pyo",
            ".gitignore"
        ]
    },
    "content_excludes": {
        "folders": [
            "migrations",
            "static",
            "media"
        ],
        "files": [
            "__init__.py",
            "*.log",
            "*.pkl",
            "*.pdf",
            "*.sqlite3",
            "*.json"
        ]
    },
    "project_overview": "Custom project description"
}
```

### Exclusion Types

The tool supports two types of exclusions:
- **Full Excludes**: Items that are completely excluded from both the structure overview and content parsing
- **Content Excludes**: Items that appear in the structure overview but whose content is not parsed

This allows you to:
1. Completely hide irrelevant files/folders (like `.git`)
2. Show important structural elements while skipping their content (like database files or `__init__.py`)

### Project-Specific Configuration

You can place an `analyzer_config.json` file in your project root to provide project-specific settings:

```
your-project/
├── analyzer_config.json    # Project-specific configuration
├── src/
│   └── main.py
└── tests/
    └── test_main.py
```

## Output Format

The tool generates an XML file with the following structure:

```xml
<project path="/absolute/path/to/project">
    <overview>
        Project description...
    </overview>
    <structure>
        <dir name="src">
            <file name="main.py" path="src/main.py"/>
        </dir>
    </structure>
    <contents>
        <file name="main.py" path="src/main.py">
            <content><![CDATA[
                File contents here...
            ]]></content>
        </file>
    </contents>
</project>
```

## Development

```bash
# Clone the repository
git clone https://github.com/zegri1/project-to-xml.git

# Install in development mode
cd project_to_xml
pip install -e .
```

## Default Configuration

If no configuration file is found, the following defaults are used:

```json
{
    "full_excludes": {
        "folders": [
            ".git",
            "node_modules",
            "__pycache__",
            ".venv",
            "venv",
            "env",
            ".idea",
            ".vscode",
            "dist",
            "build",
            "eggs",
            ".eggs",
            ".pytest_cache",
            ".mypy_cache",
            ".coverage",
            ".tox"
        ],
        "files": [
            ".DS_Store",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.so",
            "*.dylib",
            "*.dll",
            ".gitignore",
            ".coverage",
            ".python-version",
            ".env"
        ]
    },
    "content_excludes": {
        "folders": [
            "migrations",
            "static",
            "media"
        ],
        "files": [
            "__init__.py",
            "*.log",
            "*.pkl",
            "*.pdf",
            "*.jpg",
            "*.png",
            "*.svg",
            "*.sqlite3",
            "*.db",
            "*.csv",
            "*.json",
            "*.xml",
            "*.yaml",
            "*.yml",
            "*.lock",
            "requirements.txt"
        ]
    },
    "project_overview": "This is a Python project analysis."
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.