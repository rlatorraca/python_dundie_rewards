# setup tools [vem com o python]
from setuptools import setup, find_packages

setup(
    name="dundie",
    version="0.1.0",  # x(major), y(minor), z(patch/bugs)
    description="Main reward points system at Dunder Mifflin Inc.",
    author="RLSP",
    packages=find_packages(),
)

# pyproject

# external build tools (ex.: poetry, flit)
