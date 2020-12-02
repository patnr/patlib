#!/usr/bin/env python3

import os
import re

import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
long_description = ("Misc tools for python.")

def find_version(*file_paths):
    """Get version by regex'ing a file."""
    # Source: packaging.python.org/guides/single-sourcing-package-version

    def read(*parts):
        here = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(here, *parts), 'r') as fp:
            return fp.read()

    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(

    # Basic meta
    name="patlib",
    version=find_version("patlib", "__init__.py"),
    author="Patrick N. Raanes",
    author_email="patrick.n.raanes@gmail.com",
    description=long_description,

    python_requires='>=3.7',

    # TODO: this has not been checked at all
    install_requires=[
        'scipy>=1.1',
        'ipython>=5.1',
        'matplotlib~=3.1',
    ],

    # Detailed meta
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',

        'Programming Language :: Python :: 3',

        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
