import argparse

from .analyzer import ProjectAnalyzer
from project_to_xml.analyzer import ProjectAnalyzer  # Updated import


def main():
    parser = argparse.ArgumentParser(description='Analyze project structure and generate XML documentation.')
    parser.add_argument('path', nargs='?', default='.',
                        help='Path to the project directory (default: current directory)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-c', '--config', help='Path to configuration file')

    args = parser.parse_args()

    try:
        analyzer = ProjectAnalyzer(args.config)
        output_file = analyzer.create_project_xml(args.path, args.output)
        print(f"XML file created successfully: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())