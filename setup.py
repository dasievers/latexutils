#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='latexutils-dasievers',
    version='0.1.0',
    description='Python tools for working with LaTeX document scripts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dasievers/latexutils',
    author='David Sievers',
    packages=['latexutils'],
    install_requires=[
                      'pandas',
                      ],

    classifiers=[
                'Development Status :: 4 - Beta',
                'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                'Intended Audience :: Science/Research',
                'Topic :: Text Processing :: Markup :: LaTeX',
                'Programming Language :: Python :: 3',
                ],
    python_requires=">=3.6",
)
