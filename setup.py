# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

setup(
    name='mm',  # 包名
    version='1.1.0',  # 版本号
    description='My common constants and functions',  # 描述
    author='Shifa Yang',  # 作者
    author_email='ysf504703038@163.com',  # 作者邮箱
    url='null',  # 包的网址
    license='',
    install_requires=['requests', 'selenium', 'bs4'],  # 安装依赖
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='',
    packages=find_packages('src'),  # 必填
    package_dir={'': 'src'},  # 必填
    include_package_data=True,
)
