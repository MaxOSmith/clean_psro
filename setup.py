"""Install script for setuptools."""
from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup

setup(
    name="clean_psro",
    version="0.0.1",
    description="Clean Poliy-Space Response Oracles (PSRO).",
    author="Max Smith",
    packages=find_packages(),
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
