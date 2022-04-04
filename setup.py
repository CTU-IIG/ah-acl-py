#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup.py
"""Install script for this package."""

import os
from setuptools import setup, find_packages
from aversio import Version, get_git_version, maintain_version

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

VERSION = maintain_version(str(Version(get_git_version()[1:])), "VERSION")


setup(
    name = "aclpy",
    version = VERSION,
    author = "Jaroslav Klapálek",
    author_email = "klapajar@fel.cvut.cz",
    description = ("Lightweight Arrowhead Client Library for Python."),
    license = "GPLv3",
    keywords = "Arrowhead Arrowhead-Tools Client Python",
    #url = "http://packages.python.org/an_example_pypi_project",
    packages=find_packages(),
    #long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=[
        "requests_pkcs12"
    ],
    python_requires=">3",
)
