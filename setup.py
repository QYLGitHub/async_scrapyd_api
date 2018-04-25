#!/usr/bin/env python
# -*- coding: utf-8 -*-
from async_scrapy_api import __version__
from setuptools import setup

readme = open('README.md', encoding='utf-8').read()

setup(
    name='async_scrapy_api',
    version=__version__,
    description='一个更方便管理scrapyd api的封装, 基于scrapyd_api上',
    keywords='python-scrapyd-api scrapyd scrapy api wrapper async_scrapy_api',
    long_description=readme,
    author='perror',
    url='https://github.com/QYLGitHub/async_scrapyd_api',
    packages=[
        'async_scrapy_api',
    ],
    package_dir={
        'async_scrapy_api': 'async_scrapy_api'
    },
    include_package_data=True,
    setup_requires=['setuptools>=38.6.0'],
    license="BSD",
    zip_safe=False,
)
