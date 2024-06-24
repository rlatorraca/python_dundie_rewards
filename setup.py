from setuptools import setup, find_packages

setup(
    name="dundie",
    version="0.1.0",  # x(major), y(minor), z(patch/bugs)
    description="Main reward points system at Dunder Mifflin Inc.",
    author="RLSP",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dundie = dundie.__main__:main"
        ]
    },
)

# pyproject

# external build tools (ex.: poetry, flit)
