# -*- coding: utf-8 -*-
#
#  setup.py
#  pangaea
#
#  Created by Alan D Snow, 2017.
#  BSD 3-Clause

from setuptools import setup, find_packages

requires = [
    'gazar',
    'wrf-python',
]

setup(name='pangaea',
      version='0.0.4',
      description='An xarray extension for gridded land surface & weather model output.',
      # long_description='',
      author='Alan D. Snow',
      author_email='alansnow21@gmail.com',
      url='https://github.com/snowman2/pangaea',
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
          'Programming Language :: Python :: 3.6',
      ],
      install_requires=requires,
      extras_require={
          'tests': [
              'coveralls',
              'flake8',
              'pytest',
              'pytest-cov',
              'pylint',
          ],
          'docs': [
              'mock',
              'sphinx',
              'sphinx_rtd_theme',
              'sphinxcontrib-napoleon',
          ]
      },
      )
