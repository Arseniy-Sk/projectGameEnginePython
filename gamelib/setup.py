from setuptools import setup, find_packages
import re

with open('gamelib/data/version.py', 'r') as f:
    version = re.search(r"__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read()).group(1)

setup(
    name="gamelib",
    version=version,
    packages=find_packages(),
    description="A simple game engine library for 2D games",
    author="Zubanov A.S",
    author_email="zzz",
    python_requires='>=3.7',
    install_requires=['pillow>=8.0.0', 'pydub>=0.25.0'],
    extras_require={
        'audio': ['pydub>=0.25.0'],
        'full': ['pillow>=8.0.0', 'pydub>=0.25.0'],
    },
    entry_points={
        'console_scripts': [
            'gamelib-create=create_game:main_cli',
            'new-game=create_game:main_cli',
        ],
    },
)