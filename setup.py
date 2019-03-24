#!/usr/bin/env python
import os

from setuptools import setup

os.environ['PBR_VERSION'] = '1.0'
setup(
    description='SQLi small lab on the university moodle',
    setup_requires=['pbr'],
    python_requires='~=2.7',
    include_package_data=True,
    pbr=True,
    zip_safe=False
)