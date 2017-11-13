# -*- coding: utf-8 -*-

"""
    simple asynchrone web-server with flask, mongodb and gevent frameworks
    @author Lukashov_ai
"""

from setuptools import setup, find_packages
import os

DIR_LOG = '/var/log/mongo_flask'

if not os.path.isdir(DIR_LOG):
    os.mkdir(DIR_LOG)
    os.chmod(DIR_LOG, 0777)

setup(
    name='mongo_flask',
    version="0.26",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'flask',
        'gevent',
        'pymongo',
        'bson'
    ],
)

