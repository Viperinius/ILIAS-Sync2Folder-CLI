#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='sync2folder',
    version='0.1.0',
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
            'sync2folder = sync2folder.app:main'
        ],
        'sync2folder.cli': [
            'set-connection = sync2folder.commands:SetConnection',
            'show-connection = sync2folder.commands:ShowConnection',
            'set-dir-config = sync2folder.commands:SetDirectorySettings',
            'show-dir-config = sync2folder.commands:ShowDirectorySettings',
            'list-courses = sync2folder.commands:ListCourses',
            'edit-courses = sync2folder.commands:EditCourses',
            'sync = sync2folder.commands:Sync',
            'login = sync2folder.commands:Login',
            'logout = sync2folder.commands:Logout',
        ],
    },
)