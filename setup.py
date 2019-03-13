#! /usr/bin/env python3

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    return open(os.path.join(here, fname)).read()


setup(
    name="passwd-aas",
    packages=find_packages(exclude=("tests", "tests.*")),
    python_requires=">=3.7",
    install_requires=["flask"],
    version="1.0.0",
    description="Passwd as a service coding challenge.",
    long_description=read("README.md"),
    author="Tyler Roberts",
    entry_points={"console_scripts": ["passwd-aas=passwd.__main__:main"]},
)
