#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='sync2folder',
    version='0.1',
    description='Download your ILIAS course files to your local disk automatically',
    author='Viperinius',
    author_email='viperinius@gmx.de',
    url='https://github.com/Viperinius/ILIAS-Sync2Folder-CLI',
    download_url='https://github.com/Viperinius/ILIAS-Sync2Folder-CLI/tarball/master',
    install_requires=[
        'cliff',
        'zeep',
        'pyyaml',
        'xmltodict',
        ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'sync2folder = app:main'
        ],
    },
)