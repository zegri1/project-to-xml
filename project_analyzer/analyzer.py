import json
import os
import xml.etree.ElementTree as ET
from typing import Optional
from xml.dom import minidom


class ProjectAnalyzer:
    """A class to analyze project structure and generate XML documentation."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the ProjectAnalyzer with optional configuration.

        Args:
            config_path: Path to a JSON configuration file. If None, searches for 'analyzer_config.json'
                        in the working directory and uses default configuration if not found.
        """
        self.config = None
        self.default_config = {
            "excluded_folders": [
                ".git",
                "node_modules",
                "__pycache__",
                "venv",
                ".idea",
                ".venv",
                "dist",
                "build"
            ],
            "excluded_files": [
                ".DS_Store",
                ".gitignore",
                "*.pyc",
                "*.pyo",
                "*.pyd",
                "*.so",
                "*.dylib",
                "*.dll"
            ],
            "excluded_extensions": [
                ".pkl",
                ".pdf",
                ".jpg",
                ".png",
                ".exe"
            ],
            "default_output_name": "project_structure.xml",
            "project_overview": "This is a PyCharm project analysis."
        }

        # Initialize with provided config or search for default config file
        self.load_config(config_path)

    def load_config(self, config_path: Optional[str] = None) -> None:
        """
        Load configuration from file or use defaults.
        Searches for 'analyzer_config.json' in the current directory if no path provided.
        """
        config = self.default_config.copy()

        def try_load_config(path: str) -> bool:
            """Try to load config from a specific path."""
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        user_config = json.load(f)
                        config.update(user_config)
                        print(f"Loaded configuration from: {path}")
                        return True
                except Exception as e:
                    print(f"Warning: Error loading config file {path}: {e}")
            return False

        # First try the explicitly provided config path
        if config_path and try_load_config(config_path):
            self.config = config
            return

        # Then look for analyzer_config.json in current directory
        if try_load_config('analyzer_config.json'):
            self.config = config
            return

        # Use default config if no file found
        print("Using default configuration")
        self.config = config

    def update_config_for_project(self, project_path: str) -> None:
        """
        Update configuration by looking for analyzer_config.json in the project directory.
        """
        config_path = os.path.join(project_path, 'analyzer_config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    project_config = json.load(f)
                    self.config.update(project_config)
                    print(f"Updated configuration from project: {config_path}")
            except Exception as e:
                print(f"Warning: Error loading project config file: {e}")

    def should_exclude(self, path: str) -> bool:
        """Check if the path should be excluded based on configured patterns."""
        name = os.path.basename(path)
        ext = os.path.splitext(name)[1]

        if os.path.isdir(path):
            return name in self.config["excluded_folders"]

        if ext in self.config["excluded_extensions"]:
            return True

        for pattern in self.config["excluded_files"]:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
        return False

    def create_project_xml(self, folder_path: str, output_file: Optional[str] = None) -> str:
        """
        Generate XML structure for the project.

        Args:
            folder_path: Path to the project folder to analyze
            output_file: Optional output file path. If None, uses default name.

        Returns:
            str: Path to the generated XML file
        """
        folder_path = os.path.abspath(folder_path)

        # Look for project-specific config
        self.update_config_for_project(folder_path)

        if output_file is None:
            output_file = os.path.join(folder_path, self.config["default_output_name"])

        def process_directory_structure(path: str, parent_element: ET.Element) -> None:
            try:
                items = sorted(os.listdir(path))
            except PermissionError:
                return

            for item in items:
                full_path = os.path.join(path, item)
                if self.should_exclude(full_path):
                    continue

                if os.path.isdir(full_path):
                    dir_element = ET.SubElement(parent_element, 'dir')
                    dir_element.set('name', item)
                    process_directory_structure(full_path, dir_element)
                else:
                    file_element = ET.SubElement(parent_element, 'file')
                    file_element.set('name', item)
                    file_element.set('path', os.path.relpath(full_path, folder_path))

        def process_files_content(path: str, parent_element: ET.Element) -> None:
            try:
                items = sorted(os.listdir(path))
            except PermissionError:
                return

            for item in items:
                full_path = os.path.join(path, item)
                if self.should_exclude(full_path):
                    continue

                if os.path.isfile(full_path):
                    file_element = ET.SubElement(parent_element, 'file')
                    file_element.set('name', item)
                    file_element.set('path', os.path.relpath(full_path, folder_path))

                    content_element = ET.SubElement(file_element, 'content')
                    content_element.text = ''

                elif os.path.isdir(full_path):
                    process_files_content(full_path, parent_element)

        # Create root element
        root = ET.Element('project')
        root.set('path', folder_path)

        # Add project overview
        overview = ET.SubElement(root, 'overview')
        overview.text = self.config["project_overview"].strip()

        # Add clean project structure
        structure = ET.SubElement(root, 'structure')
        process_directory_structure(folder_path, structure)

        # Add file contents
        contents = ET.SubElement(root, 'contents')
        process_files_content(folder_path, contents)

        # Convert to string and parse with minidom
        xml_str = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_str)

        # Add CDATA sections for file contents
        for content_elem in dom.getElementsByTagName('content'):
            while content_elem.firstChild:
                content_elem.removeChild(content_elem.firstChild)

            if content_elem.parentNode.hasAttribute('path'):
                file_path = content_elem.parentNode.getAttribute('path')
                try:
                    with open(os.path.join(folder_path, file_path), 'r', encoding='utf-8') as f:
                        cdata = dom.createCDATASection(f.read())
                        content_elem.appendChild(cdata)
                except Exception as e:
                    cdata = dom.createCDATASection(f"Error reading file: {str(e)}")
                    content_elem.appendChild(cdata)

        # Create pretty XML string
        xml_str = dom.toprettyxml(indent="  ")

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_str)

        return output_file