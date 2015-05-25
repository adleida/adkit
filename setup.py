#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
adkit
-----

adkit is an test tool for adexchange.

"""

import ast
import os
import os.path
import re
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
data_dir = 'adkit/res'
data = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]

with open('adkit/__init__.py', 'rb') as f:
        version = str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))
        setup(
            name='adkit',
            version=version,
            url='http://git.adleida.com/paxp/',
            author='adleida',
            author_email='noreply@adleida.com',
            description='adkit is an test tool for adexchange.',
            long_description=__doc__,
            packages=['adkit'],
            package_data={'adkit': data},
            include_package_data=True,
            zip_safe=False,
            platforms='any',
            entry_points='''
                [console_scripts]
                adkit=adkit.kit:main
            ''',
            install_requires=[
                'jsonschema==2.4.0',
                'PyYAML==3.11',
                'requests',
                'termcolor==1.1.0',
                'tabulate'
            ],
        )
