#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='euterpe',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'euterpe = euterpe:main',
        ],
    },

    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    description='Music playlist syncing',
    license='',
    url='',
)
