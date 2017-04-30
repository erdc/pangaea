# -*- coding: utf-8 -*-
#
#  setup.py
#  sloot
#
#  Created by Alan D Snow, 2017.
#  BSD 3-Clause

from setuptools import setup, find_packages

requires = [
    'affine',
    'appdirs',
    'gdal',
    'mapkit',
    'pyproj',
    'timezonefinder',
    'utm',
    'wrf-python',
]

setup(name='sloot',
      version='0.0.1',
      description='An xarray extension for land surface models'
                  ' and a collection of GDAL based functions.',
      #long_description='',
      author='Alan D. Snow',
      author_email='alansnow21@gmail.com',
      url='https://github.com/snowman2/sloot',
      license='BSD 3-Clause',
      keywords='land surface model, xarray, gdal',
      packages=find_packages(),
      classifiers=[
                'Intended Audience :: Developers',
                'Intended Audience :: Science/Research',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.5',
                ],
      install_requires=requires,
      extras_require={
        'tests': [
            'pytest',
            'pytest-cov',
        ],
        'docs': [
            'mock',
            'sphinx',
            'sphinx_rtd_theme',
            'sphinxcontrib-napoleon',
        ]
      },
)
