#!/usr/bin/env python3
"""
SynapseWatcher - Setup Script

Installation:
    pip install -e .

Usage after installation:
    synapsewatcher --help
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="synapsewatcher",
    version="1.1.0",
    author="Atlas (Team Brain)",
    author_email="logan@metaphy.com",
    description="Real-time Synapse message notifications for Team Brain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/SynapseWatcher",
    py_modules=["synapsewatcher"],
    python_requires=">=3.7",
    install_requires=[],  # Zero dependencies - pure stdlib!
    entry_points={
        "console_scripts": [
            "synapsewatcher=synapsewatcher:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="synapse, notifications, real-time, team-brain, agents",
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/SynapseWatcher/issues",
        "Source": "https://github.com/DonkRonk17/SynapseWatcher",
    },
)
