#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setuptools is a fully-featured, actively-maintained, and stable
# library designed to facilitate packaging Python projects.
# setup.py is the build script for setuptools.
# It tells setuptools about your package (such as the name and version)
# as well as which code files to include.
# https://packaging.python.org/tutorials/packaging-projects/
# https://setuptools.readthedocs.io/en/latest/

import io
import os
from setuptools import find_packages, setup

CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name="pythonloc",
    version="0.1.2.2",
    author="Chad Smith",
    author_email="chadsmith.software@gmail.com",
    description="Run Python using packages from local directory __pypackages__",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cs01/pythonloc",
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    keywords=[],
    scripts=[],
    entry_points={
        "console_scripts": [
            "pythonloc = pythonloc.pythonloc:pythonloc",
            "piploc = pythonloc.pythonloc:piploc",
            "pipfreezeloc = pythonloc.pythonloc:pipfreezeloc",
        ]
    },
    zip_safe=False,
    install_requires=['pipx>=0.12.2.0;python_version>="3.6"'],
    python_requires=">=2.7",
    # license and classifier list:
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
