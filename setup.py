from setuptools import setup, find_packages

# Read README with explicit UTF-8 encoding
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="project-to-xml",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'project-to-xml=project_to_xml.cli:main',
        ],
    },
    author="zegri1",
    author_email="andrei@zegrean.ro",
    description="A tool that converts project directories into structured XML documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zegri1/project-to-xml",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)