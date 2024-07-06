import os
from setuptools import setup, find_packages


def read(*paths):
    """Read the contents of a text file safely.
    >>> read("dundie", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """
    rootpath = os.path.dirname(__file__)
    filepath = os.path.join(rootpath, *paths)
    with open(filepath, 'r') as file_:
        return file_.read().strip()


def read_requirements(path):
    """Return a list of requirements from a text file"""
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(("#", "git+", '"', '-'))
    ]


setup(
    name="rlsp-dundie",
    version="0.1.1",  # x(major), y(minor), z(patch/bugs)
    description="Main reward points system at Dunder Mifflin Inc.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="RLSP",
    python_requires=">=3.9",
    packages=find_packages(exclude=["integration"]) ,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dundie = dundie.__main__:main"
        ]
    },
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "test": read_requirements("requirements.test.txt"),
        "dev": read_requirements("requirements.dev.txt"),
    }

)

# pyproject

# external build tools (ex.: poetry, flit)
