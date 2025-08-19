#!/usr/bin/env python3
"""
Ortho4XPDark Setup Configuration

Enhanced orthoscenery generation for X-Plane with professional dark theme,
intelligent automation, and specialized Ireland/UK region support.
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
requirements_path = this_directory / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    # Fallback requirements if file doesn't exist
    requirements = [
        'pillow>=9.0.0',
        'requests>=2.25.0',
        'numpy>=1.20.0',
        'psutil>=5.8.0',
        'aiofiles>=0.8.0',
        'websockets>=10.0',
        'xxhash>=2.0.0',
        'lz4>=3.1.0',
        'pybloom_live>=4.0.0',
        'bsdiff4>=1.2.0',
        'bitarray>=2.5.0',
    ]

# Optional dependencies for enhanced functionality
extras_require = {
    'gdal': ['gdal>=3.0.0'],  # For advanced geospatial processing
    'pyproj': ['pyproj>=3.0.0'],  # For coordinate transformations
    'dev': [
        'pytest>=6.0.0',
        'pytest-asyncio>=0.18.0',
        'mypy>=0.900',
        'black>=21.0.0',
        'flake8>=3.9.0',
        'isort>=5.0.0',
    ],
    'docs': [
        'sphinx>=4.0.0',
        'sphinx-rtd-theme>=1.0.0',
        'sphinx-autodoc-typehints>=1.12.0',
    ],
    'performance': [
        'numba>=0.55.0',  # For numerical acceleration
        'cython>=0.29.0',  # For compiled extensions
    ],
    'networking': [
        'asyncio-mqtt>=0.11.0',  # For advanced P2P features
        'cryptography>=36.0.0',  # For secure communications
    ]
}

# All optional dependencies combined
extras_require['all'] = list(set(
    dep for deps in extras_require.values() for dep in deps
    if isinstance(deps, list)
))

setup(
    # Package metadata
    name="ortho4xp-dark",
    version="1.0.0",
    author="Ortho4XPDark Development Team",
    author_email="contact@ortho4xpdark.example",
    description="Enhanced orthoscenery generation for X-Plane with professional dark theme and intelligent automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/c42meitheal-collab/Ortho4XPDark",
    project_urls={
        "Development Repository": "https://github.com/c42meitheal-collab/Ortho4XPDark",
        "Bug Reports": "https://github.com/c42meitheal-collab/Ortho4XPDark/issues",
        "Source": "https://github.com/c42meitheal-collab/Ortho4XPDark",
        "Documentation": "https://github.com/c42meitheal-collab/Ortho4XPDark/docs",
        "Changelog": "https://github.com/c42meitheal-collab/Ortho4XPDark/blob/main/CHANGELOG.md",
        "Developer Guide": "https://github.com/c42meitheal-collab/Ortho4XPDark/blob/main/DEVELOPER_INTEGRATION_GUIDE.md",
        "Original Ortho4XP": "https://github.com/shred86/Ortho4XP",
        "X-Plane.org Forum": "https://forums.x-plane.org/index.php?/forums/forum/322-ortho4xp/",
    },
    
    # Package discovery and structure
    packages=find_packages(where=".", exclude=["tests", "tests.*", "docs", "docs.*"]),
    package_dir={"": "."},
    
    # Include non-Python files
    include_package_data=True,
    package_data={
        "": [
            "*.md", "*.txt", "*.cfg", "*.json", "*.png", "*.svg", "*.gif",
            "*.sh", "*.bat", "*.c", "*.exe", "*.dll", "*.so",
            "demfiles/*", "assets/*", "enhanced_scenery_objects/*",
            "Licence/*", "docs/*", "tools/*", "src/*", "Utils/*",
            "Extents/*", "Filters/*", "Patches/*", "Previews/*", "Providers/*",
        ],
    },
    
    # Dependencies
    install_requires=requirements,
    extras_require=extras_require,
    python_requires=">=3.8",
    
    # Entry points for command-line tools
    entry_points={
        "console_scripts": [
            "ortho4xp-dark=Ortho4XPDark:main",
            "ortho4xp-dark-launcher=enhanced_launcher:main",
            "ortho4xp-dark-simple=simple_launcher:main",
            "ortho4xp-dark-verify=system_verification:main",
            "ortho4xp-treelines=treelines_manager:main",
        ],
    },
    
    # Classification
    classifiers=[
        # Development Status
        "Development Status :: 5 - Production/Stable",
        
        # Intended Audience
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        
        # Topic
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        
        # License
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        
        # Operating Systems
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        
        # Programming Language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        
        # Environment
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Environment :: Console",
        
        # Natural Language
        "Natural Language :: English",
        
        # Framework
        "Framework :: AsyncIO",
    ],
    
    # Keywords for search
    keywords=[
        "x-plane", "flight-simulation", "orthoscenery", "photorealistic-scenery",
        "digital-elevation-model", "aviation", "scenery-generation", "geospatial",
        "ireland", "uk", "united-kingdom", "transparent-roads", "forest-management",
        "dark-theme", "multiplayer", "p2p-networking", "xroads", "treelines",
        "gdal", "satellite-imagery", "dem", "srtm", "automation", "gui"
    ],
    
    # Platform compatibility
    platforms=["Windows", "macOS", "Linux"],
    
    # Archive options
    zip_safe=False,  # Package contains data files that need to be extracted
    
    # Additional metadata for PyPI
    license="GPL-3.0-or-later",
    license_files=["LICENSE", "Licence/gpl.txt"],
    
    # Project maturity and stability
    # This is a stable, production-ready release
    # Built on the mature foundation of the original Ortho4XP project
)
