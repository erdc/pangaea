# -*- coding: utf-8 -*-
#
#  conftest.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

import os

import pytest
from shutil import rmtree

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


class TestDirectories(object):
    input = os.path.join(SCRIPT_DIR, 'input')
    compare = os.path.join(SCRIPT_DIR, 'compare')
    write = os.path.join(SCRIPT_DIR, 'output')

    def clean(self):
        """
        Clean out test directory
        """
        os.chdir(self.write)

        # Clear out directory
        file_list = os.listdir(self.write)

        for afile in file_list:
            if not afile.endswith('.gitignore'):
                path = os.path.join(self.write, afile)
                if os.path.isdir(path):
                    rmtree(path)
                else:
                    os.remove(path)


@pytest.fixture(scope="module")
def tgrid(request):
    _td = TestDirectories()
    _td.clean()

    yield _td

    _td.clean()
