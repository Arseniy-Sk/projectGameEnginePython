# setup.py
from setuptools import setup, find_packages
import re

# Read version from gamelib/data/version.py
with open('gamelib/data/version.py', 'r') as f:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read()).group(1)

setup(
    name="gamelib",
    version=version,
    packages=find_packages(),
    description="A simple game engine library",
    author="Zubanov A.S",
    author_email="zzz",
)